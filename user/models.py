from django.db import models

# Create your models here.
class Users (models.Model) :
    id = models.IntegerField(primary_key=True) 
    reward = models.IntegerField(blank=False,default=0)
    point = models.IntegerField(blank=False,default=0)
    coin = models.IntegerField(blank=False,default=0)
    phone_number = models.CharField(max_length=50)
    app_id = models.IntegerField(blank=False,default=0)
    pin=models.IntegerField(blank=False,default=0)
    code=models.IntegerField(blank=True,default=0)
    status=models.IntegerField(blank=False,default=0)
 