from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.serializers import HomeSerializers
from product.models import Product


class Home(APIView):
    def get(self, request):
        all_products = Product.objects.all()
        popular_products = all_products.order_by('-views')[:10]  # نمایش ۱۰ محصول محبوب
        all_products_serialized = HomeSerializers(all_products, many=True)
        popular_products_serialized = HomeSerializers(popular_products, many=True)
        response_data = {
            'all_products': all_products_serialized.data,
            'popular_products': popular_products_serialized.data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
