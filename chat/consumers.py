import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import ChatRoom, Message, UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unique identifier per connection
        self.user_id = self.channel_name
        self.room_name = None
        self.user_profile = None
        self.user_location = None
        self.is_logged_in = False

        # Try to match with an existing waiting room; otherwise create one and wait
        waiting_room = await self.get_waiting_room()
        if waiting_room is None:
            room = await self.create_waiting_room(self.user_id)
            self.room_name = str(room.room_id)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            await self.send(text_data=json.dumps({"status": "waiting", "room_id": self.room_name}))
        else:
            room = await self.assign_user2(waiting_room, self.user_id)
            self.room_name = str(room.room_id)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat_message", "message": "You are now connected!", "sender_id": None}
            )

    async def disconnect(self, close_code):
        if self.room_name:
            # Notify the room and force close the counterpart so both can requeue
            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat_message", "message": "Stranger has disconnected.", "sender_id": None}
            )
            await self.channel_layer.group_send(self.room_name, {"type": "force_close"})
            await self.deactivate_room(self.room_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # Handle location data
        if data.get("type") == "location":
            self.user_location = data.get("location")
            self.is_logged_in = data.get("isLoggedIn", False)
            # Update room with location data
            if self.room_name:
                await self.update_room_location(self.room_name, self.user_id, self.user_location)
            return
        
        msg = data.get("message", "")
        if not msg:
            return

        if self.room_name:
            # Get sender name for admin display
            sender_name = await self.get_sender_name(self.user_id, self.is_logged_in)
            await self.save_message(self.room_name, self.user_id, msg, sender_name)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message", 
                    "message": msg, 
                    "sender_id": self.user_id,
                    "sender_name": sender_name
                }
            )

    async def chat_message(self, event):
        # Only send the message to users who didn't send it
        if event.get("sender_id") != self.user_id:
            await self.send(text_data=json.dumps({
                "message": event["message"],
                "sender_name": event.get("sender_name")
            }))

    async def force_close(self, event):
        # Close this websocket connection when admin kills the session
        await self.close()

    @database_sync_to_async
    def get_waiting_room(self):
        return ChatRoom.objects.filter(active=True, user2__isnull=True).order_by("id").first()

    @database_sync_to_async
    def create_waiting_room(self, user1_id):
        return ChatRoom.objects.create(user1=user1_id, user2=None, active=True)

    @database_sync_to_async
    def assign_user2(self, room, user2_id):
        room.user2 = user2_id
        room.save(update_fields=["user2"])
        return room

    @database_sync_to_async
    def deactivate_room(self, room_id):
        ChatRoom.objects.filter(room_id=room_id).update(active=False)

    @database_sync_to_async
    def update_room_location(self, room_id, user_id, location):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            if room.user1 == user_id:
                room.user1_location = location
            elif room.user2 == user_id:
                room.user2_location = location
            room.save(update_fields=["user1_location", "user2_location"])
        except ChatRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def get_sender_name(self, user_id, is_logged_in):
        if is_logged_in:
            try:
                # Try to get username from the user_id if it's a session key
                # This is a simplified approach - in production you'd want proper user session handling
                return "User"  # Placeholder - would need proper user session management
            except:
                return "Anonymous"
        return "Anonymous"

    @database_sync_to_async
    def save_message(self, room_id, sender, content, sender_name=None):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            Message.objects.create(room=room, sender=sender, content=content)
        except ChatRoom.DoesNotExist:
            return


class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if isinstance(user, AnonymousUser) or not getattr(user, "is_staff", False):
            await self.close()
            return
        self.user = user
        self.room_name = None
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        action = data.get("action")
        if action == "subscribe_room":
            room_id = data.get("room_id")
            if room_id:
                if self.room_name:
                    await self.channel_layer.group_discard(self.room_name, self.channel_name)
                self.room_name = room_id
                await self.channel_layer.group_add(self.room_name, self.channel_name)
                await self.send(text_data=json.dumps({"status": "subscribed", "room_id": self.room_name}))
                # Optionally send history
                history = await self.get_last_messages(room_id)
                await self.send(text_data=json.dumps({"type": "history", "messages": history}))
        elif action == "message":
            content = data.get("message")
            if content and self.room_name:
                await self.save_message(self.room_name, f"admin:{self.user.username}", content)
                await self.channel_layer.group_send(
                    self.room_name,
                    {"type": "chat_message", "message": content, "sender_id": f"admin:{self.user.username}"}
                )
        elif action == "kill_room":
            room_id = data.get("room_id") or self.room_name
            if room_id:
                await self.deactivate_room(room_id)
                # Inform participants and force close their sockets
                await self.channel_layer.group_send(
                    room_id,
                    {"type": "chat_message", "message": "Session terminated by admin.", "sender_id": None}
                )
                await self.channel_layer.group_send(room_id, {"type": "force_close"})
                await self.send(text_data=json.dumps({"status": "killed", "room_id": room_id}))
        elif action == "connect_to_waiting":
            # Admin claims a waiting room so that the user is connected seamlessly
            room_id = data.get("room_id")
            if room_id:
                claimed = await self.claim_waiting_room(room_id, f"admin:{self.user.username}")
                if claimed:
                    # Join the group and notify participants like normal connect
                    if self.room_name:
                        await self.channel_layer.group_discard(self.room_name, self.channel_name)
                    self.room_name = room_id
                    await self.channel_layer.group_add(self.room_name, self.channel_name)
                    await self.channel_layer.group_send(
                        self.room_name,
                        {"type": "chat_message", "message": "You are now connected!", "sender_id": None}
                    )
                    # Send history to admin after connecting
                    history = await self.get_last_messages(room_id)
                    await self.send(text_data=json.dumps({"status": "connected", "room_id": self.room_name}))
                    await self.send(text_data=json.dumps({"type": "history", "messages": history}))
                else:
                    await self.send(text_data=json.dumps({"status": "failed", "reason": "not_waiting_or_missing"}))
        elif action == "delete_room":
            room_id = data.get("room_id") or self.room_name
            if room_id:
                # Notify, close sockets, then delete from DB
                await self.channel_layer.group_send(
                    room_id,
                    {"type": "chat_message", "message": "Room deleted by admin.", "sender_id": None}
                )
                await self.channel_layer.group_send(room_id, {"type": "force_close"})
                await self.delete_room_record(room_id)
                await self.send(text_data=json.dumps({"status": "deleted", "room_id": room_id}))
        elif action == "delete_all":
            # Notify all rooms, close sockets, then delete all
            room_ids = await self.get_all_room_ids()
            for rid in room_ids:
                rid_str = str(rid)
                await self.channel_layer.group_send(
                    rid_str,
                    {"type": "chat_message", "message": "All rooms are being deleted by admin.", "sender_id": None}
                )
                await self.channel_layer.group_send(rid_str, {"type": "force_close"})
            await self.delete_all_rooms()
            await self.send(text_data=json.dumps({"status": "deleted_all"}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event.get("message")}))

    @database_sync_to_async
    def get_last_messages(self, room_id, limit=50):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except ChatRoom.DoesNotExist:
            return []
        qs = room.messages.order_by("-timestamp").values("sender", "content", "timestamp")[:limit]
        # Return in chronological order
        items = list(qs)[::-1]
        for item in items:
            item["timestamp"] = item["timestamp"].isoformat()
        return items

    @database_sync_to_async
    def save_message(self, room_id, sender, content):
        try:
            room = ChatRoom.objects.get(room_id=room_id)
            Message.objects.create(room=room, sender=sender, content=content)
        except ChatRoom.DoesNotExist:
            return

    @database_sync_to_async
    def delete_room_record(self, room_id):
        ChatRoom.objects.filter(room_id=room_id).delete()

    @database_sync_to_async
    def get_all_room_ids(self):
        return list(ChatRoom.objects.values_list("room_id", flat=True))

    @database_sync_to_async
    def delete_all_rooms(self):
        ChatRoom.objects.all().delete()

    @database_sync_to_async
    def claim_waiting_room(self, room_id: str, admin_label: str) -> bool:
        try:
            room = ChatRoom.objects.get(room_id=room_id)
        except ChatRoom.DoesNotExist:
            return False
        if not room.active or room.user2:
            return False
        room.user2 = admin_label
        room.save(update_fields=["user2"])
        return True
