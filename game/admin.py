from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Player, Task

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    list_editable = ('position',)
    fields = ('name', 'position')
    
    def has_add_permission(self, request):
        """Запрет добавления более 6 игроков"""
        count = Player.objects.count()
        if count >= 6:
            messages.warning(request, "Достигнуто максимальное количество игроков (6)")
        return count < 6
    
    def save_model(self, request, obj, form, change):
        """Дополнительная валидация при сохранении"""
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.error(request, f"Ошибка сохранения: {', '.join(e.messages)}")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'description_preview')
    fields = ('id', 'description')
    readonly_fields = ('id',)
    
    def description_preview(self, obj):
        """Короткое описание для списка"""
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = "Описание"
    
    def has_delete_permission(self, request, obj=None):
        """Запрет удаления заданий"""
        return False
    
    def save_model(self, request, obj, form, change):
        """Автоматическая установка ID при первом создании"""
        if not obj.id:
            # Находим первый свободный ID от 1 до 20
            existing_ids = set(Task.objects.values_list('id', flat=True))
            for i in range(1, 21):
                if i not in existing_ids:
                    obj.id = i
                    break
        
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.error(request, f"Ошибка сохранения: {', '.join(e.messages)}")
    
    def get_queryset(self, request):
        """Всегда показываем все 20 заданий"""
        qs = super().get_queryset(request)
        # Создаём недостающие задания
        existing_ids = set(qs.values_list('id', flat=True))
        for i in range(1, 21):
            if i not in existing_ids:
                Task.objects.create(id=i, description="")
        return Task.objects.all().order_by('id')