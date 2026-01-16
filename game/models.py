from django.db import models
from django.core.exceptions import ValidationError
from core.settings import MAX_TASKS_COUNT, MIN_PLAYER_POSITION, MAX_PLAYER_POSITION


class Player(models.Model):
    """Модель игрока с ограничениями"""
    name = models.CharField(
        max_length=100,
        verbose_name="Имя игрока"
    )
    position = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Позиция",
        help_text=f"Число от {MIN_PLAYER_POSITION} до {MAX_PLAYER_POSITION}"
    )
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['position']
    
    def clean(self):
        """Валидация данных при сохранении"""
        # Проверка диапазона позиции
        if not (MIN_PLAYER_POSITION <= self.position <= MAX_PLAYER_POSITION):
            raise ValidationError({
                'position': f"Позиция должна быть от {MIN_PLAYER_POSITION} до {MAX_PLAYER_POSITION}"
            })
        
        # Проверка максимального количества игроков
        existing_count = Player.objects.exclude(pk=self.pk).count()
        if existing_count >= 6:
            raise ValidationError(f"Максимальное количество игроков — {MAX_PLAYER_POSITION}")
    
    def save(self, *args, **kwargs):
        """Автоматический вызов валидации перед сохранением"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (Позиция: {self.position})"

class Task(models.Model):
    """Модель задания (ровно 20 штук)"""
    id = models.PositiveSmallIntegerField(
        primary_key=True,
        verbose_name="ID задания",
        help_text=f"Фиксированный ID от 1 до {MAX_TASKS_COUNT}"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание задания"
    )
    
    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ['id']
    
    def clean(self):
        """Валидация ID задания"""
        if not (1 <= self.id <= MAX_TASKS_COUNT):
            raise ValidationError({
                'id': f"ID задания должен быть от 1 до {MAX_TASKS_COUNT}"
            })
    
    def save(self, *args, **kwargs):
        """Автоматический вызов валидации"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Задание #{self.id}: {self.description[:30]}..." if self.description else f"Задание #{self.id} (пусто)"


class Rules(models.Model):
    text = models.TextField(verbose_name='Текст правил')
    
    class Meta:
        verbose_name = "Правила"
        verbose_name_plural = "Правила"

    def clean(self):
        if Rules.objects.exists():
            raise ValidationError('Уже есть правила')

    def save(self, *args, **kwargs):
        """Автоматический вызов валидации перед сохранением"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text