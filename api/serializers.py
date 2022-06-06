from itertools import product
from math import prod
from re import I
from turtle import update
from django.forms import CharField
from pkg_resources import require
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from .models import Product, ProductInventory, Sale

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, value):
        if self.context["request"].method == 'POST':
            product = Product.objects.filter(bar_code = value['bar_code'])
            if product.exists():
                raise ValidationError(f"This bar code is already associated to an existing product: {product.first().name}")
        return value

class CreateSaleSerializer(Serializer):
    products = serializers.CharField()
    pieces = serializers.CharField()

    def validate(self, value):
        products_list = value['products'].split(',')
        pieces_list = [int(item) for item in value["pieces"].split(',')]

        #Validating all products have number of pieces
        if len(products_list) != len(pieces_list):
            raise ValidationError("Not all pieces for all products are provided")

        #Creating a list with all the product instances
        #Also validating those products exist
        sale_products_list = []
        total_amount = 0
        pieces_amount = 0
        product_instances = []
        for idx, product_id in enumerate(products_list):
            qs_product = Product.objects.filter(id = product_id)
            if qs_product.exists():
                product_id_instance = qs_product.first()
                product_instances.append(product_id_instance)

                #Validating stock available
                qs_inventory = ProductInventory.objects.filter(product = product_id_instance)
                if qs_inventory.exists():
                    if not qs_inventory.first().stock >= pieces_list[idx]:
                        raise ValidationError(f"Not enough stock for {product_id_instance.name} asking for {pieces_list[idx]} available {qs_inventory.first().stock}")
                else:
                    raise ValidationError(f"There is no stock for {product_id_instance.name}")
                
                subtotal = product_id_instance.price * pieces_list[idx]
                total_amount += subtotal
                pieces_amount += pieces_list[idx]
                sale_products_list.append({"product": product_id_instance, "pieces": pieces_list[idx], "subtotal": subtotal})

            else:
                raise ValidationError(f"Product with id {product_id} is not in the database")

            #Once validated the products existance and stock, the validated data is updated with the information of the product and pieces in a list of dictionaries
            value['total'] = total_amount
            value['pieces'] = pieces_amount
            value['products'] = sale_products_list

        return value

class InventorySerializer(ModelSerializer):
    name = serializers.CharField(source="product.name")
    description = serializers.CharField(source="product.description")
    class Meta:
        model = ProductInventory
        fields = '__all__'

class UpdateInventorySerializer(Serializer):
    products = serializers.CharField()
    pieces = serializers.CharField()
    update_type = serializers.IntegerField() # 0 Remove 1 Add

    def validate(self, attrs):
        try:
            products_list = attrs['products'].split(',')
            pieces_list = [int(item) for item in attrs["pieces"].split(',')]
        except:
            raise ValidationError("There's been an error trying to create products/pieces lists")
        
        #Validating all products have number of pieces
        if len(products_list) != len(pieces_list):
            raise ValidationError("Not all pieces for all products are provided")
        
        inventory_products_pieces=[]
        if attrs['update_type'] == 1:
            for idx, product_id in enumerate(products_list):
                qs_product = Product.objects.filter(id = product_id)
                if not qs_product.exists():
                    raise ValidationError("Product not registered in our database")
        
                product_id_instance = qs_product.first()
                inventory_products_pieces.append({"product": product_id_instance, "pieces": pieces_list[idx]})

        elif attrs['update_type'] == 0:
            for idx, product_id in enumerate(products_list):

                qs_product = Product.objects.filter(id = product_id)
                if not qs_product.exists():
                    raise ValidationError("Product not registered in our database")

                qs_inventory = ProductInventory.objects.filter(product = qs_product.first())
                if not qs_inventory.exists():
                    raise ValidationError("Can't remove inventory from a product without stock")

                if qs_inventory.first().stock < pieces_list[idx]:
                    raise ValidationError("Pieces to remove can't be greater than the current stock")
        
                product_id_instance = qs_product.first()
                inventory_products_pieces.append({"product": product_id_instance, "pieces": pieces_list[idx]})
        else:
            raise ValidationError("Select a valid update type")

        attrs["products_pieces"] = inventory_products_pieces
        
        return attrs