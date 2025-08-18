from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartVeiw.as_view(), name='cart'),
    path('cart/<int:pk>', views.CartDetail.as_view(), name='cart-detail'),
    path('cart/<int:pk>/items/', views.CartItemView.as_view(), name='cart_item_list_view'),
    path('cart/<int:pk>/items/<int:item_pk>/', views.CartItemDetailView.as_view(), name='cart_item_detail_view'),
]
