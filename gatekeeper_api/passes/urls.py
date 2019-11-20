from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="pass_register"),
    path('validate/', views.validate, name='pass_validate'),
    path('validate/check', views.get_guest_info, name="guest-info"),
    path('home/', views.home, name="home")
]
