from rest_framework import serializers
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id','username','email','password','password2','is_admin']
        extra_kwargs = {
            'password':{'write_only': True},
            'is_admin':{'read_only':True}
            }
       
    def validate(self,data):
        if data.get('password') != data.get('password2'):
            return serializers.validationError('passwords missmatch')

        if len(data.get('username')) < 3:
            return serializers.ValidationError('password must be more than 5 letters')  
        return data

    def create(self,validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


    

    
