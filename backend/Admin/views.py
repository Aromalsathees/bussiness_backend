from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework .response import Response
from rest_framework .permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class Add_product(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'The product has Added to Database', 'Data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'Unvalid Field' ,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Get_product(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products , many=True)
        return Response({'message':'All products fetched from Database','Data':serializer.data}, status=status.HTTP_200_OK)
    

class Delete_product(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'message':'The item has deleted from Database'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error':'The product Does not exist in Database'}, status=status.HTTP_404_NOT_FOUND)


class UPdate_product(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product ,data=request.data)
            if serilaizer.is_valid():
                return Response({'message':'The product is Updated'},status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error':'The product ID Does not Exist in Database'}, status=status.HTTP_404_NOT_FOUND)

class Search_product(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,q):
        try:
            get_query = q
            if not get_query or len(get_query) == 0:
                return Response({'error':'Enter product Name'}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.filter(product_name__icontains=get_query)
            if not product.exists():
                 return Response({'error':'The product Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product,many=True)
            return Response({'message':'The product is founded','Data':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
class Get_user_Details(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'message':'Here is the user','Data':serializer.data}, status=status.HTTP_200_OK)