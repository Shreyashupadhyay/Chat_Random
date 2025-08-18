import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom

waiting_user = None  # simple matchmaking pool (can use Redis for scaling)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global waiting_user

        self.user_id = self.scope["client"][1]  # just use socket info (later use auth)
        self.room_name = None

        # Matchmaking
        if waiting_user is None:
            waiting_user = self
            await self.accept()
            await self.send(text_data=json.dumps({"status": "waiting"}))
        else:
            # Create chat room
            room = await self.create_room(waiting_user.user_id, self.user_id)
            self.room_name = str(room.room_id)
            waiting_user.room_name = self.room_name

            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.channel_layer.group_add(self.room_name, waiting_user.channel_name)

            await self.accept()

            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat_message", "message": "You are now connected!", "sender_id": None}
            )

            waiting_user = None

    async def disconnect(self, close_code):
        if self.room_name:
            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat_message", "message": "Stranger has disconnected.", "sender_id": None}
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data.get("message", "")

        if self.room_name:
            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat_message", "message": msg, "sender_id": self.user_id}
            )

    async def chat_message(self, event):
        # Only send the message to users who didn't send it
        if event.get("sender_id") != self.user_id:
            await self.send(text_data=json.dumps({"message": event["message"]}))

    @database_sync_to_async
    def create_room(self, user1, user2):
        return ChatRoom.objects.create(user1=user1, user2=user2)
