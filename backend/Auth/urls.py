from .views import *
from django.urls import path

urlpatterns = [
    path('get_refresh_token/',get_refresh_token ,name='tokens'),
    path('admin-signup/',Admin_Signup.as_view(),name='adminsignup'),
    path('user-signup/',User_Signup.as_view(),name='usersignup'),
    path('login/',Login.as_view(),name='Login'),
    path('logout/',Logout.as_view(),name='logout'),
]
