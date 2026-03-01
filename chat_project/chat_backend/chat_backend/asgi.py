import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "chat_backend.settings"
)

django.setup()  # ✅ MUST come BEFORE importing routing

import chat.routing  # ✅ Import AFTER setup

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})