from django.utils import timezone
from rest_framework import serializers

from account.models import Account
from cart.models import Cart, CartItem
from product.models import Product
from product.serializers import SimpleProductSerializers


class HomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'short_description']







