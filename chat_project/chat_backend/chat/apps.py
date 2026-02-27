from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        # Reset all users to offline on every server start/restart.
        # This handles the case where the server crashed or was killed
        # and WebSocket disconnect events never fired — preventing users
        # from being stuck as "online" permanently in the database.
        try:
            from chat.models import UserProfile
            UserProfile.objects.all().update(is_online=False)
        except Exception:
            # Silently ignore errors during startup (e.g. DB not yet migrated)
            pass
