from django.contrib import admin

from .models import Category, Product, ProductViewModel


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ['category_name']
    list_filter = ['category_name']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['product_name', 'price', 'stuck', 'create_date']
    list_filter = ['product_name']

class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'ip_address', 'created_at')  # نمایش اطلاعات بازدید
    list_filter = ('product', 'created_at')  # فیلتر کردن بر اساس محصول و تاریخ بازدید
    search_fields = ('ip_address',)  # امکان جستجو بر اساس IP


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductViewModel, ProductViewAdmin)
# admin.site.register(product.product_name)




