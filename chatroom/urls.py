from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('send', views.chatbot),
]