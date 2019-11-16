from django.urls import path
from .views import home

urlpatterns = [
    path('register/', home),
]
