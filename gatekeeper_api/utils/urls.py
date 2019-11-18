from django.urls import path
from . import views

urlpatterns = [
    path('',views.registerdate,name="addevent"),
]
