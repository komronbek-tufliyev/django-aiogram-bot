from .views import index, set_language
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('set_language/<str:language>/', set_language, name='set-language'),
]
