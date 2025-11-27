from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework .response import Response
from rest_framework .permissions import AllowAny , IsAuthenticated
from rest_framework import status
from Admin.models import *
from Admin.serializer import *

# Create your views here.


class Get_products(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response({'message':'succefully fetched All products'}, status=status.HTTP_200_OK)


class Search_products(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query = request.query_params.get('q')

            # Validate query
            if not query or len(query.strip()) == 0:
                return Response(
                    {'error': 'Invalid fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Search
            products = Product.objects.filter(product_name__icontains=query)
            serializer = ProductSerializer(products, many=True)

            # Check if result is empty
            if not products.exists():
                return Response(
                    {'error': 'The product is not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    'message': 'Successfully fetched product',
                    'Data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
