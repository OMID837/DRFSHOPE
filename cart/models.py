from django.db import models
from account.models import Account
from product.models import Product


class Cart(models.Model):
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date_added)


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True,related_name='items')
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity * self.product.price
