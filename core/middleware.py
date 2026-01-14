from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminAccessMiddleware:
    """
    Разрешает доступ к /admin/ только для пользователя 'admin'
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if request.user.username != 'admin':
                messages.error(request, "У вас нет доступа к админке. Обратитесь к мастер-админу.")
                return redirect(reverse('admin:login'))
        
        response = self.get_response(request)
        return response