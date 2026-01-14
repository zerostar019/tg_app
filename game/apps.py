from django.apps import AppConfig
from django.db.models.signals import post_migrate

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'
    verbose_name = "Игра"

    def ready(self):
        post_migrate.connect(self.create_initial_tasks, sender=self)

    def create_initial_tasks(self, **kwargs):
        """Создаём 20 пустых заданий при первой миграции"""
        from .models import Task
        if not Task.objects.exists():
            for i in range(1, 21):
                Task.objects.get_or_create(
                    id=i,
                    defaults={'description': ''}
                )