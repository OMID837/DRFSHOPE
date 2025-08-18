from django.db import models

from account.models import Account
from product.models import Product


class Order(models.Model):
    place_at=models.DateTimeField(auto_now_add=True)
    customer=models.ForeignKey(Account,on_delete=models.CASCADE)

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    unit_price=models.IntegerField()
