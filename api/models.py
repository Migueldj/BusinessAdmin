from concurrent.futures import process
import email
from itertools import product
from math import prod
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.FloatField()
    bar_code = models.CharField(max_length=64)

    def __str__(self):
        return f" ID: {self.id} {self.name} ${self.price} | Description: {self.description}"

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    pieces_sold = models.IntegerField()
    total = models.FloatField(default=0, editable=False)
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return f"User: {self.user} Total: {self.total} On: {self.created_date} "

class ProductSale(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sale = models.ForeignKey(Sale, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    pieces = models.IntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return f"Product: {self.product} Pieces: {self.pieces} Subtotal: {self.subtotal}"

class ProductInventory(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    stock = models.IntegerField()

    def __str__(self):
        return f"Product: {self.product} Stock: {self.stock}"
      
class InboundInventory(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    pieces = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return f"Product: {self.product} Pieces Added: {self.pieces} Date: {self.created_date}"

    def save(self, *args, **kwargs):
        qs_product_inventory = ProductInventory.objects.filter(product = self.product)
        
        if qs_product_inventory.exists():
            product_inventory = qs_product_inventory.first()
            product_inventory.stock = product_inventory.stock + self.pieces
            product_inventory.save()
            
        else:
            ProductInventory.objects.create(
                product = self.product,
                stock = self.pieces
            )

        super(InboundInventory, self).save(*args, **kwargs)

class OutboundInventory(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    pieces = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return f"Product: {self.product} Pieces Removed: {self.pieces} Date: {self.created_date}"