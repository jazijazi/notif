import email
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator 
from django.contrib.auth.password_validation import validate_password
from django.db import transaction



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined']




class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    email = serializers.EmailField(required=True)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email' ,'password')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user