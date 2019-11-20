from django.urls import path
from . import views

urlpatterns = [
    path('addevent', views.registerdate, name="addevent"),
]
