from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    p_id = models.IntegerField()
    p_name = models.CharField(max_length=50)
    p_description = models.TextField(max_length=200)
    p_image = models.ImageField(upload_to='images/')
    p_stock = models.IntegerField(default=0)
    p_cost = models.IntegerField(default=0)
    p_discount = models.IntegerField(default=0)
    p_category = models.CharField(max_length=30, default='General')

class CartNew(models.Model):
    c_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    orderedby = models.ForeignKey(User,on_delete=models.CASCADE)


class Wish(models.Model):
    w_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    cost = models.IntegerField(default=0)
    orderedby = models.ForeignKey(User,on_delete=models.CASCADE)
