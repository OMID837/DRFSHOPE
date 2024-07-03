from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.register.as_view(), name='register')
]
