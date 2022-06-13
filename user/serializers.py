from pyexpat import model
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from rest_framework.response import Response
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
        class Meta:
                model = Users
                fields = [
                        'id',
                        'reward',
                        'point',
                        'coin',
                        'phone_number',
                        'pin',
                        'code']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class UserSysSerializer(serializers.ModelSerializer):
   class Meta:
                model = User
                fields = [
                        'id',
                        'password',
                        'is_superuser',
                        'username',
                        'first_name',
                        'last_name',
                        'email',
                        'is_staff',
                        'is_active',
                        'date_joined']