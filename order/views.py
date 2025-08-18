from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from order.models import Order
from order.serializers import OrderSerializers, CreateOrderSerializers


class OrderView(APIView):
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get(self,request):
        order=Order.objects.filter(customer_id=request.user.id)
        serializers=OrderSerializers(order,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateOrderSerializers(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get(self, request, pk):
        orders = Order.objects.get(pk=pk, customer_id=self.request.user.id)
        serializer = OrderSerializers(orders)
        return Response(serializer.data, status=status.HTTP_201_CREATED)