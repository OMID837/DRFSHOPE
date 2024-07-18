from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from cart.models import Cart, CartItem
from cart.serializers import CartSerializers, CartItemSerializers, AddItemSerializers, UpdateCartItemSerializers


# class CartVeiw(APIView):
#
#     def get(self, request):
#         carts = Cart.objects.all()
#         serializers = CartSerializers(carts, many=True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
# class CartDetail(APIView):
#     def get(self,request,pk):
#         cart = Cart.objects.get(pk=pk)
#         serializer=CartSerializers(cart)
#         return Response(serializer.data)


class CartVeiw(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            carts = Cart.objects.all()  # Admin can see all carts
        else:
            carts = Cart.objects.filter(items__user=request.user)  # Non-admins see only their own carts
        serializers = CartSerializers(carts, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_staff:
            cart = get_object_or_404(Cart, pk=pk)  # Admin can see any cart
        else:
            cart = get_object_or_404(Cart, pk=pk, items__user=request.user)  # Non-admins see only their own carts
        serializer = CartSerializers(cart)
        return Response(serializer.data)

    def delete(self, request, pk):
        if request.user.is_staff:
            cart = get_object_or_404(Cart, pk=pk)  # Admin can delete any cart
        else:
            cart = get_object_or_404(Cart, pk=pk,
                                     items__user=request.user)  # Non-admins can delete only their own carts
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemView(APIView):
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['pk'], 'user_id': self.request.user.id}

    def get(self, request, pk):
        cart_items = CartItem.objects.filter(cart_id=pk, user_id=request.user.id)  # Filter by cart_id and user_id
        serializer = CartItemSerializers(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = AddItemSerializers(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    def get(self, request, pk, item_pk):
        cart_item = get_object_or_404(CartItem, cart_id=pk, pk=item_pk)
        serializer = CartItemSerializers(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, item_pk):
        cart_item = get_object_or_404(CartItem, cart_id=pk, pk=item_pk)
        serializer = UpdateCartItemSerializers(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, item_pk):
        cart_item = get_object_or_404(CartItem, cart_id=pk, pk=item_pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


