from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.permissions import AllowAny
import csv

from .models import InboundInventory, OutboundInventory, Product, ProductInventory, ProductSale, Sale
from config.models import User

from .serializers import ProductSerializer, CreateSaleSerializer, InventorySerializer, UpdateInventorySerializer

"""
TEST
"""

@api_view(['POST'])
def test(request):
    response_data = {}
    print(type(request.data['bool']))
    return Response(response_data, status=status.HTTP_200_OK)

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
    context = {"request": request}
    serializer = ProductSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    Product.objects.create(**serializer.validated_data)

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateProduct(request):

    response_data = {}

    context = {"request": request}
    serializer = ProductSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    Product.objects.filter(bar_code = data['bar_code']).update(**serializer.validated_data)

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def uploadProductsCSV(request):

    if not bool(request.FILES.get('products_csv')):
        return Response({ 'error' : 'File missing' }, status=status.HTTP_400_BAD_REQUEST)

    try:
        csv_file = request.FILES['products_csv']
    except Exception as e:
        print(e)
        
    return Response({}, status=status.HTTP_200_OK)


"""
SALES
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def createSale(request):
    response_data = {}
    serializer = CreateSaleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data    
    print(data)
    sale = Sale.objects.create(
        pieces_sold = data["pieces"],
        total = data['total'],
        user = User.objects.first() #For now just taking the first for testing, bc token auth is not implemented yet
    )

    products = data['products']

    for product in products:
        #Create the instances of product sale
        ProductSale.objects.create(
            sale = sale,
            product = product['product'],
            pieces = product['pieces'],
            subtotal = product['subtotal']
        )
        #Updating the stock for each of this products
        product_inventory = ProductInventory.objects.get(product = product['product'])
        product_inventory.stock = product_inventory.stock - product['pieces']
        product_inventory.save()

    return Response(response_data, status=status.HTTP_200_OK)

"""
INVENTORY
"""
@api_view(['GET'])
@permission_classes([AllowAny])
def getInventory(request):
    response_data = {}
    q = Q ()

    if "search" in request.data:
        search = request.data['search']
        q &= Q(product__name__icontains=search) | Q(product__description__icontains=search)
    
    inventory = ProductInventory.objects.filter(q)
    serializer = InventorySerializer(inventory, many=True)

    response_data['inventory'] = serializer.data

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def addInventory(request):
    response_data = {}
    
    serializer = UpdateInventorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    products_pieces = data["products_pieces"]

    for product in products_pieces:
        InboundInventory.objects.create(
            product = product["product"],
            pieces = product["pieces"],
            user = User.objects.first()
        )

    response_data['status'] = 1

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def removeInventory(request):
    response_data = {}
    
    serializer = UpdateInventorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    
    products_pieces = data["products_pieces"]

    for product in products_pieces:
        OutboundInventory.objects.create(
            product = product["product"],
            pieces = product["pieces"],
            user = User.objects.first()
        )

    response_data['status'] = 1

    return Response(response_data, status=status.HTTP_200_OK)