from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework .response import Response
from rest_framework import status
from rest_framework .permissions import AllowAny , IsAuthenticated
from .models import *
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# Create your views here.


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }



class Admin_Signup(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_admin=True)
            token = get_refresh_token(user)

            return Response({'message':'succesfully Registered your Account','token':token, 'user': SignupSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response({'message':'failed' , 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class User_Signup(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_admin=False)
            token = get_refresh_token(user)

            return Response({'message':'succesfully Registered your Account','token':token,'user': SignupSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response({'message':'failed' ,'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Invalid fields'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        # now safe to generate token
        token = get_refresh_token(user)
        serializer = SignupSerializer(user)

        return Response({
            'message': 'Successfully logged in',
            'is_admin': user.is_admin,
            'token': token,
            'Data': serializer.data
        }, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error':'NO refresh Token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'succesfully Logout'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
