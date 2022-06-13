from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta

from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from .serializers import *

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):


    def validate(self, attrs):

        data = super().validate(attrs)

        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(days=10))
        data['token'] = str(access_token)

        data['username'] = self.user.username
        data['is_superuser'] = self.user.is_superuser
        data['is_staff'] = self.user.is_staff
        data['id'] = self.user.id
        data['firstName'] = self.user.first_name
        data['lastName'] = self.user.last_name
        data['email'] = self.user.email
        data['password'] = self.user.password
        Modeluser = Users.objects.filter(id=self.user.id)
        UsersSerializer = UserSerializer(Modeluser, many=True)

        data['details'] = UsersSerializer.data
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
