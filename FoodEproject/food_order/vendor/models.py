from django.db import models

from dashboard.models import *


# Create your models here.


class AllResturants(models.Model):  #RESTURANT OWNER
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=11)
    image = models.ImageField(upload_to='resturant/', default=None)
    category = models.ManyToManyField(Categories)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255)
    delivery_charges = models.CharField(max_length=50)
    delivery_time = models.CharField(max_length=200)
