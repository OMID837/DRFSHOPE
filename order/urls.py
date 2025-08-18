from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .import views

urlpatterns = [
    path('order/',views.OrderView.as_view(),name='order'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),

]

