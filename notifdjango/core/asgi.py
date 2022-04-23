import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import notification.routing

websocket_urlpatterns = []
websocket_urlpatterns += notification.routing.websocket_urlpatterns


application = ProtocolTypeRouter({
  "http": asgi_application,
  "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})