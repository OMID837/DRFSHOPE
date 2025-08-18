from django.utils import timezone
from rest_framework import serializers

from account.models import Account
from cart.models import Cart, CartItem
from product.models import Product
from product.serializers import SimpleProductSerializers


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['user', 'product', 'quantity']

    product = SimpleProductSerializers()


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items']

    id = serializers.IntegerField(read_only=True)
    items = CartItemSerializers(many=True, read_only=True)


class AddItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        product_id = self.validated_data.get('product_id')
        count = self.validated_data.get('count')
        cart_id = self.context.get('cart_id')
        user_id = self.context.get('user_id')

        if not cart_id:
            raise serializers.ValidationError('cart_id is required in the context.')

        cart_items = CartItem.objects.filter(cart_id=cart_id, product_id=product_id, user_id=user_id)

        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.count += count
            cart_item.save()
            self.instance = cart_item
        else:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, count=count,
                                                    user_id=user_id)

        return self.instance


class UpdateCartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
