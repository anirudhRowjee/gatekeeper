from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddStudents, name="addstudents"),
]
