import email
from itertools import product
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
        return f"{self.name} ${self.price} | Description: {self.description}"

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    pieces_sold = models.IntegerField()
    total = models.FloatField(default=0, editable=False)
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return f"Sale on: {self.date}"

class ProductSale(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sale = models.ForeignKey(Sale, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.IntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return f"Product: {self.product} Quantity: {self.quantity} Subtotal: {self.subtotal}"

class ProductInventory(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    stock = models.IntegerField()

    def __str__(self):
        return f"Product: {self.product} Stock: {self.stock}"

class UpdateType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
        
class InventoryUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    pieces = models.IntegerField()
    update_type = models.ForeignKey(UpdateType, models.DO_NOTHING)
    comments = models.TextField()
    user = models.ForeignKey(User, models.DO_NOTHING)

    def __str__(self):
        return f"Product: {self.product} Pieces Added: {self.quantity} Date: {self.created_date}"
