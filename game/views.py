from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Player, Task

@require_GET
def game_data_api(request):
    players = list(Player.objects.values('name', 'position'))
    
    # Гарантируем 20 заданий
    tasks = []
    for i in range(1, 21):
        try:
            task = Task.objects.get(id=i)
            tasks.append({"description": task.description})
        except Task.DoesNotExist:
            tasks.append({"description": ""})
    
    return JsonResponse({
        "players": players,
        "tasks": tasks
    })
