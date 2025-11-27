from .views import *
from django.urls import path

urlpatterns = [
    path('get-products/',Get_products.as_view(),name='products'),
    path('search-products/',Search_products.as_view(),name='search'),
]
