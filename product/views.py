from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.permissions import IsAuthenticatedForPutRequests
from product.serializers import ProductSerializers


class ProductView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializers=ProductSerializers(products,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


    def post(self,request):
        ...


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedForPutRequests]
    def get(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        serializer=ProductSerializers(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializers(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


