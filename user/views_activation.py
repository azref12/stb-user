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

@csrf_exempt
@api_view(["PUT"])
@permission_classes([AllowAny])
def UserActivation(request, *args, **kwargs):

    if request.method == 'PUT':
        try :
            localrequest = JSONParser().parse(request) 
            Modeluser = Users.objects.get(code=localrequest['code'])
            
            ModelUserl = User.objects.get(pk=Modeluser.id)
            if localrequest['username']==ModelUserl.username :
                ModelUserl.is_active=True
                ModelUserl.save()

                UsersSerializer = UserSerializer(Modeluser, data={"code":0}, partial=True)    
            

                return JsonResponse({'message' : 'successfully' , 'status' : True , 'count' : 1 , 'results' : 'User Is Active'})
            else:
                return JsonResponse({'message' : 'successfully' , 'status' : True , 'count' : 1 , 'results' : 'Data Not Valid'})
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "User Invalid"})