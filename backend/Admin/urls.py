from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('add-products/',Add_product.as_view(),name ='add_products'),
    path('get-products/',Get_product.as_view(),name='get products'),
    path('get-user/',Get_user_Details.as_view(),name='Get_user_Details'),
    path('delete-products/<int:pk>/',Delete_product.as_view(),name='delete_products'),
    path('update-products/<int:id>/',UPdate_product.as_view(),name='updatae_view'),
    path('search-products/<str:q>/',Search_product.as_view(),name='search_products'),
    
]
