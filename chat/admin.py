from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'user1', 'user2', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['room_id', 'user1', 'user2']
    readonly_fields = ['room_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Room Information', {
            'fields': ('room_id', 'active', 'created_at', 'updated_at')
        }),
        ('Users', {
            'fields': ('user1', 'user2', 'user1_profile', 'user2_profile')
        }),
        ('Location Data', {
            'fields': ('user1_location', 'user2_location'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'content', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['sender', 'content']
    readonly_fields = ['timestamp']
