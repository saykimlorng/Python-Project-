from django.urls import path

from .views import dashboard


urlpatterns = [
    path('', dashboard, name='index'),
    # The template currently uses these names for its sidebar links.
    path('tasks/', dashboard, name='morning'),
    path('users/', dashboard, name='evening'),
]
