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

        # Проверка максимального количества игроков (максимум 6)
        existing_count = Player.objects.exclude(pk=self.pk).count()
        if existing_count >= 6:
            raise ValidationError("Максимальное количество игроков — 6")

    def save(self, *args, **kwargs):
        """Автоматический вызов валидации перед сохранением"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Позиция: {self.position})"


class Task(models.Model):
    id = models.PositiveSmallIntegerField(
        primary_key=True,
        verbose_name="ID задания",
        help_text="Фиксированный ID от 1 до 20"
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
        if not (1 <= self.id <= 20):
            raise ValidationError("ID задания должен быть от 1 до 20")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Rules(models.Model):
    """Модель правил (только одна запись разрешена)"""
    text = models.TextField(verbose_name='Текст правил')

    class Meta:
        verbose_name = "Правила"
        verbose_name_plural = "Правила"

    def clean(self):
        if Rules.objects.exists() and not self.pk:
            raise ValidationError('Уже есть правила. Разрешена только одна запись.')

    def save(self, *args, **kwargs):
        """Автоматический вызов валидации перед сохранением"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text
