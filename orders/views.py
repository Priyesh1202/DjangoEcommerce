from django.shortcuts import render,redirect
from products.models import CartNew,Product
from .models import Orders


def showorders(request):
    cart = CartNew.objects.filter(orderedby=request.user)
    for c in cart:

        neworder = Orders()

    return redirect('home')
