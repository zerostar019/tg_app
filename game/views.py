from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Player, Task

@require_GET
def game_data_api(request):
    """
    Возвращает данные в формате:
    {
      "players": [{"name": "...", "position": 1}, ...],
      "tasks": [{"description": "..."}, ...]
    }
    """
    players = list(Player.objects.values('name', 'position').order_by('position'))
    tasks = [{"description": t.description} for t in Task.objects.all().order_by('id')]
    
    return JsonResponse({
        "players": players,
        "tasks": tasks
    })