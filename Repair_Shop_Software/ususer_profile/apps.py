from django.apps import AppConfig


class UsuserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ususer_profile'


    def ready(self) -> None:
        from . signals import sync_profile
        return super().ready()