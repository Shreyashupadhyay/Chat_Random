"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat.views import health_check, admin_dashboard, admin_rooms_summary, admin_room_messages, public_chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', public_chat, name='public_chat'),
    path('staff/chat/', admin_dashboard, name='admin_dashboard'),
    path('staff/chat/summary/', admin_rooms_summary, name='admin_rooms_summary'),
    path('staff/chat/rooms/<uuid:room_uuid>/messages/', admin_room_messages, name='admin_room_messages'),
]
