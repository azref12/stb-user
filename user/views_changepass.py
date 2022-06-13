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
def UserPass(request, *args, **kwargs):

    if request.method == 'PUT':
        try :
            localrequest = JSONParser().parse(request) 
            zpass=localrequest['password']
            if len(zpass)<8:
                return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "Password Minimum 8 Karakter"},
                                    status=404)
            else :
                ModelUserl = User.objects.get(pk=localrequest['id'])
                ModelUserl.set_password(zpass)
                ModelUserl.save()

            

            return JsonResponse({'message' : 'successfully' , 'status' : True , 'count' : 1 , 'results' : 'Change Password Success'})
        except Users.DoesNotExist:
            return JsonResponse({'message' : 'unsuccessfully' , 'status' : False , 'count' : 1 , 'results' : "User Invalid"})