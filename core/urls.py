from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from game.views import game_data_api
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', game_data_api, name='game_data_api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)