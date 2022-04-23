from django.urls import path
from .consumers import NotificationConsumer , ChatConsumer

websocket_urlpatterns = [
    path('ws/notification/' , NotificationConsumer.as_asgi() , name='notification'),
    path('ws/chat/<str:targetUser>/' , ChatConsumer.as_asgi() , name='chat'),
]