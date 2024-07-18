from django.contrib import admin

from order.models import Order, OrderItems


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'place_at']


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'unit_price']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
