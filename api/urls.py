from django.urls import path, include

from . import views

urlpatterns=[
   #Test
   path('test/', views.test),
   #Products
   path('get-products/', views.getProducts),
   path('create-product/', views.createProduct),
   path('update-product/', views.updateProduct),
   path('upload-products/', views.uploadProductsCSV),
   #Sales
   path('create-sale/', views.createSale),
   #Inventory
   path('get-inventory/', views.getInventory),
   path('add-inventory/', views.addInventory),
   path('remove-inventory/', views.removeInventory),
]