from django.contrib import admin

from account.models import Account


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'username', 'is_active']


admin.site.register(Account, UserAdmin)
