from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="pass_register"),
    path('validate/', views.validate, name='pass_validate'),
]
