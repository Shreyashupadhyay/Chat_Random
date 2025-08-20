from django.urls import re_path
from .consumers import ChatConsumer, AdminConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
    re_path(r"ws/admin/$", AdminConsumer.as_asgi()),
]
