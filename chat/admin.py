from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "user1", "user2", "active")
    list_filter = ("active",)
    search_fields = ("room_id", "user1", "user2")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "sender", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("sender", "content", "room__room_id")
