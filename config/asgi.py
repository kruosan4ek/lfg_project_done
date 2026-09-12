"""
ASGI config для LFG.
Поддерживает HTTP и WebSocket.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Сначала инициализируем Django (обязательно ДО импорта routing)
django_asgi_app = get_asgi_application()

# Импортируем Channels после django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from lfg.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP-запросы идут как обычно в Django
    'http': django_asgi_app,
    # WebSocket-запросы идут в Channels
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
})