from django.utils import timezone
from rest_framework import serializers

from account.models import Account
from product.models import Product


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'short_description', 'description', 'price', 'category']
