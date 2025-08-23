from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .models import ChatRoom, Message

# Create your views here.

@csrf_exempt
def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({
        "status": "healthy",
        "message": "Stranger Chat Backend is running"
    })


def public_chat(request):
    """Public chat page that connects to the websocket and matches strangers."""
    return render(request, "chat/public_chat.html")


@staff_member_required
def admin_dashboard(request):
    return render(request, "chat/admin_dashboard.html")


@staff_member_required
def admin_rooms_summary(request):
    total_rooms = ChatRoom.objects.count()
    active_qs = ChatRoom.objects.filter(active=True, user2__isnull=False).order_by("-created_at")
    waiting_qs = ChatRoom.objects.filter(active=True, user2__isnull=True).order_by("-created_at")
    active_rooms = active_qs.count()
    waiting_count = waiting_qs.count()
    
    # Enhanced room data with location and user info
    recent_active = []
    for room in active_qs[:50]:
        room_data = {
            "id": room.id,
            "room_id": str(room.room_id),
            "user1": room.user1,
            "user2": room.user2,
            "user1_location": room.user1_location,
            "user2_location": room.user2_location,
            "active": room.active,
            "created_at": room.created_at.isoformat(),
            "updated_at": room.updated_at.isoformat()
        }
        recent_active.append(room_data)
    
    recent_waiting = []
    for room in waiting_qs[:50]:
        room_data = {
            "id": room.id,
            "room_id": str(room.room_id),
            "user1": room.user1,
            "user2": room.user2,
            "user1_location": room.user1_location,
            "user2_location": room.user2_location,
            "active": room.active,
            "created_at": room.created_at.isoformat(),
            "updated_at": room.updated_at.isoformat()
        }
        recent_waiting.append(room_data)
    
    return JsonResponse({
        "total_rooms": total_rooms,
        "active_rooms": active_rooms,
        "waiting_count": waiting_count,
        "recent_active": recent_active,
        "recent_waiting": recent_waiting,
    })


@staff_member_required
def admin_room_messages(request, room_uuid):
    try:
        room = ChatRoom.objects.get(room_id=room_uuid)
    except ChatRoom.DoesNotExist:
        return JsonResponse({"error": "room not found"}, status=404)
    
    qs = room.messages.order_by("-timestamp")
    paginator = Paginator(qs, 100)
    page = paginator.page(1)
    messages = [
        {
            "sender": m.sender, 
            "content": m.content, 
            "timestamp": m.timestamp.isoformat(),
            "sender_profile": m.sender_profile.is_anonymous if m.sender_profile else True
        }
        for m in page.object_list
    ][::-1]
    
    # Add room location info
    room_data = {
        "room_id": str(room.room_id),
        "user1": room.user1,
        "user2": room.user2,
        "user1_location": room.user1_location,
        "user2_location": room.user2_location,
        "messages": messages
    }
    
    return JsonResponse(room_data)
