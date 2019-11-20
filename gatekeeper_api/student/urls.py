from django.urls import path
from . import views

urlpatterns = [
    path('addstudents', views.AddStudents, name="addstudents"),
]
