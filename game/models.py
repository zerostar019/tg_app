from django.db import models
from django.core.exceptions import ValidationError

class Player(models.Model):
    """Модель игрока с ограничениями"""
    name = models.CharField(
        max_length=100,
        verbose_name="Имя игрока"
    )
    position = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Позиция",
        help_text="Число от 1 до 20"
    )
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['position']
    
    def clean(self):
        """Валидация данных при сохранении"""
        # Проверка диапазона позиции
        if not (1 <= self.position <= 20):
            raise ValidationError({
                'position': "Позиция должна быть от 1 до 20"
            })
        
        # Проверка максимального количества игроков
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
    """Модель задания (ровно 20 штук)"""
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
        """Валидация ID задания"""
        if not (1 <= self.id <= 20):
            raise ValidationError({
                'id': "ID задания должен быть от 1 до 20"
            })
    
    def save(self, *args, **kwargs):
        """Автоматический вызов валидации"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Задание #{self.id}: {self.description[:30]}..." if self.description else f"Задание #{self.id} (пусто)"