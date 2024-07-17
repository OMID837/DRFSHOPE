from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ['category_name']
    list_filter = ['category_name']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['product_name', 'price', 'stuck', 'create_date']
    list_filter = ['product_name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
