from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register_pass"),
    path('validate/', views.validate, name='validate'),
    path('validate/check', views.get_guest_info, name="guest-info"),
    path('', views.home, name="home"),
]
