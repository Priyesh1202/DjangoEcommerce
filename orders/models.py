from django.db import models
from django.contrib.auth.models import User


class Orders(models.Model):
    o_name = models.CharField(max_length=30)
    o_quantity = models.IntegerField(default=1)
    o_cost = models.IntegerField(default=0)
    o_orderedby = models.ForeignKey(User, on_delete=models.CASCADE)


class PrevOrders(models.Model):
    po_name = models.CharField(max_length=30)
    po_quantity = models.IntegerField(default=1)
    po_cost = models.IntegerField(default=0)
    po_orderedby = models.ForeignKey(User, on_delete=models.CASCADE)
