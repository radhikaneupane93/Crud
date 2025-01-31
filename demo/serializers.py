from rest_framework import serializers
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id','full_name','email','password','phone_number'] 
        extra_kwargs ={
            'password': {'write_only':True}
        }
        
    def validate(self, data):
        email = data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError('Invalid email format')
        return data
        
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user 
    
class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password= serializers.CharField(write_only=True)
        
class UpdateSerializer(serializers.Serializer):  
    class Meta:
        model = User 
        fields= ['full_name','phone_number']
            
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
        
class DeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=True)
    
            
            
    
    
                
        
    
    
    