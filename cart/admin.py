from django.contrib import admin

from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['date_added']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart']



admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)