
from django.db import models
import uuid

class ChatRoom(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user1 = models.CharField(max_length=255, blank=True, null=True)
    user2 = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
