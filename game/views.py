from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Player, Task, Rules


@require_GET
def game_data_api(request):
    players = list(Player.objects.values('name', 'position'))
    tasks = list(Task.objects.all().values('description'))
    
    return JsonResponse({
        "players": players,
        "tasks": tasks,
        "rules": Rules.objects.values_list('text', flat=True).first()
    })
