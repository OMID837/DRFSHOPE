from django.utils import timezone
from rest_framework import serializers

from account.models import Account
from cart.models import Cart, CartItem
from order.models import OrderItems, Order
from product.serializers import SimpleProductSerializers


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializers()

    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'place_at', 'items']


class CreateOrderSerializers(serializers.Serializer):
    id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.validated_data['id']
        user_id = self.context['user_id']

        # (customer, created) = Account.objects.get_or_create(id=user_id)
        # Order.objects.create(customer=customer)
        order = Order.objects.create(customer_id=user_id)
        cart_items = CartItem.objects.filter(cart_id=cart_id, user_id=user_id)
        for item in cart_items:
            order_items = OrderItems.objects.create(
                product=item.product,
                # user_id=user_id,
                order=order,
                quantity=item.count,
                unit_price=item.product.price,
            )
            order_items.save()
            Cart.objects.filter(pk=cart_id).delete()
