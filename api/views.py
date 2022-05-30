from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.permissions import AllowAny
import json

from .models import Product, ProductSale, Sale

from .serializers import ProductSerializer, SaleSerializer


"""
PRODUCTS
"""

@api_view(['GET'])
def getProducts(request):
    
    response_data = {}
    q = Q ()

    if "search" in request.data:
        search = request.data['search']
        q &= Q(name__icontains=search) | Q(description__icontains=search)
    
    products = Product.objects.filter(q)
    serializer = ProductSerializer(products, many=True)

    response_data['products'] = serializer.data

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def createProduct(request):

    response_data = {}
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    Product.objects.create(**serializer.validated_data)

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateProduct(request):

    response_data = {}
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    Product.objects.update(**serializer.validated_data)

    return Response(response_data, status=status.HTTP_200_OK)


"""
SALES
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def createSale(request):
    print("Entro a la petición")
    response_data = {}
    # serializer = SaleSerializer(data=request.data)
    
    products = request.data['products'].strip('[]')
    print(products)

    # sale = Sale.objects.create(

    # )

    # for product in products:
    #     ProductSale.objects.create(

    #     )

    return Response(response_data, status=status.HTTP_200_OK)