from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Player, Task, Rules
from core.settings import MAX_TASKS_COUNT


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    list_editable = ('position',)
    fields = ('name', 'position')
    
    def has_add_permission(self, request):
        return Player.objects.count() < 6
    
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"Ошибка: {e}", level='error')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'description_preview')
    fields = ('id', 'description')
    readonly_fields = ('id',)
    
    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = "Описание"
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            existing_ids = set(Task.objects.values_list('id', flat=True))
            for i in range(1, MAX_TASKS_COUNT):
                if i not in existing_ids:
                    obj.id = i
                    break
        
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"Ошибка: {e}", level='error')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        existing_ids = set(qs.values_list('id', flat=True))
        for i in range(1, MAX_TASKS_COUNT):
            if i not in existing_ids:
                Task.objects.create(id=i, description="")
        return Task.objects.all().order_by('id')


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('text_preview',)
    fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Правила"
    
    def has_add_permission(self, request):
        return not Rules.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False