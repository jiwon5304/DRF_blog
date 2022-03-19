from dataclasses import field
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = '__all__' 
    
    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=30, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('LOGIN_EMAIL_WRONG')
        
        if not user.check_password(password):
            raise serializers.ValidationError('LOGIN_PASSWORD_WRONG')
        
        user.last_login = timezone.now()
        user.save()
        
        return user

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'last_login',
            'created_at',
            'updated_at'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'name',
        )