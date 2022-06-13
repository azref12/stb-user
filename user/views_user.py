from django.shortcuts import render
import datetime 
from codecs import ignore_errors
from functools import partial
from inspect import isfunction
from re import X

from django.db import DatabaseError, transaction
from django.db.models.aggregates import Max
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import *
from .serializers import *
# from backendapi.page import PageNumberPagination, StandardResultsSetPagination
import os
from pathlib import Path
from decouple import Config ,RepositoryEnv, Csv

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import random
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_FILE = './config/.env'
getenv = Config(RepositoryEnv(DOTENV_FILE))
APP_ID=getenv('APP_ID')

t = datetime.datetime.now()
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

@csrf_exempt
@api_view(["GET", "POST", "PUT"])
@permission_classes([AllowAny])
def UserActive(request, *args, **kwargs):

    if request.method == 'GET':
        try :
            ModelUser = Users.objects.all()
            UsersSerializer = UserSerializer(ModelUser, many=True)
            formater = {
                            "User": UsersSerializer.data,
            }
            
            return JsonResponse({'message' : 'successfully' , 'status' : True , 'count' : 1 , 'results' : formater})
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:          
            localrequest = JSONParser().parse(request)   
            zemail=localrequest['email']
            zphone=localrequest["phone_number"]
            zuser=localrequest['username']
            zpass=localrequest['password']
            if(re.fullmatch(regex, zemail)):
                print('oke')
            else:
                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Format Email Salah"},
                                    status=404)

            if len(zpass)<8:
                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Password Minimum 8 Karakter"},
                                    status=404)
            if User.objects.filter(username=zuser).count()!=0:

                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Nama User Telah Terdaftar"},
                                    status=404)  

            if User.objects.filter(email=zemail).count()!=0:

                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Email Telah Terdaftar"},
                                    status=404)

            if Users.objects.filter(phone_number=zphone).count()!=0:

                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "No Telphone Telah Terdaftar"},
                                    status=404)  
            else:
                                         
                        user = User(
                                username=zuser,
                                email=zemail,
                                first_name=localrequest['first_name'],
                                last_name=localrequest['last_name'],
                                is_active=False
                                )
                        user.set_password(zpass)
                        user.save()                                      
                        UserSave = Users ( 
                                                                id = user.id,
                                                                reward=0,
                                                                point=0,
                                                                coin=0,
                                                                phone_number = zphone,
                                                                app_id = APP_ID,
                                                                pin=localrequest["pin"],
                                                                code=randomDigits(4)
                                                        )
                        UserSave.save()
                        Modeluser = Users.objects.filter(id=user.id)
                        UsersSerializer = UserSerializer(Modeluser, many=True)
                                
                        formater = {
                                        "master": UsersSerializer.data
                                }
                            
                        return JsonResponse({'message' : 'successfully' , 'status' : True , 'count' : 1 , 'results' : formater},
                                    status=201)  

        except Exception as e:
            return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Data Not Valid"},
                                    status=500)  

