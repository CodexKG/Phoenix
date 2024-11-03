from django.apps import AppConfig
from django.db import ProgrammingError, OperationalError
from django.db.models.signals import post_migrate

def register_permissions(sender, **kwargs):
    try:
        from apps.queenbee.permissions import register_permissions as register_perms
        register_perms()
    except (ProgrammingError, OperationalError):
        pass  # Пропускаем, если база данных не готова

class QueenbeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.queenbee'

    def ready(self):
        # Привязываем функцию register_permissions к сигналу post_migrate
        post_migrate.connect(register_permissions, sender=self)