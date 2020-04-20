from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,CartNew
from .forms import CartForm,Filter

def homepage(request):
    if request.method == 'POST':
        print(request.POST)
        if 'search' in request.POST:
            form = CartForm()
            formfilter = Filter()
            print(request.POST['search'])
            searchstring = request.POST['search']
            products = Product.objects.filter(p_name__icontains = searchstring)
            print(products)
            return render(request, 'products/home.html', {'products': products,'form':form,'filter':formfilter})
        elif request.POST['max_price'] and request.POST['min_price']:
            form = CartForm()
            formfilter = Filter(request.POST)
            minp = request.POST['min_price']
            maxp = request.POST['max_price']
            products = Product.objects.raw('''SELECT * FROM products_product WHERE p_cost BETWEEN %s AND %s ''',[minp,maxp])
            return render(request,'products/home.html',{'products':products,'form':form,'filter':formfilter})

    else:
        form = CartForm()
        formfilter = Filter()
        deals = Product.objects.raw('SELECT * FROM products_product WHERE p_discount>10;')
        products = Product.objects.raw('SELECT * FROM products_product;')
        x = len(products)
        if x%4==0:
            x=x//4
        else:
            x=x//4
            x=x+1
        l = [i for i in range(2,int(x)+1)]
        t=1
        return render(request,'products/home.html',
                      {'products': products[:4], 'pages': l, 'page_no': t, 'form': form, 'filter': formfilter})


def detail(request,product_id):
    getproduct = get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'product':getproduct})


def page(request,page_id):
    products = Product.objects.raw('SELECT * FROM products_product;')
    x = len(products)
    if x % 4 == 0:
        x = x // 4
    else:
        x = x // 4
        x = x + 1
    l = [i for i in range(2, int(x) + 1)]
    start = (page_id-1)*4 +1
    end = page_id*4 +1
    return render(request, 'products/home.html',{'products': products[start:end], 'pages': l,'page_no':page_id})

@login_required
def addtocart(request,product_id):
    if request.method == 'POST':
        getcart = get_object_or_404(Product,pk=product_id)
        c = CartNew()
        c.name = getcart.p_name
        if request.POST['quantity'] == '':
            c.quantity = 1
        else:
            c.quantity = request.POST['quantity']
        c.cost = getcart.p_cost
        c.orderedby = request.user
        c.save()
        return redirect('home')
    else:
        form = CartForm
        formfilter = Filter()
        products = Product.objects
        return render(request, 'products/home.html', {'products': products, 'form':form,'filter':formfilter})


@login_required
def showcart(request):
    allproducts = CartNew.objects.filter(orderedby=request.user)
    return render(request, 'products/cart.html', {'products': allproducts})


@login_required
def editcart(request,product_id):
    if request.method == 'POST':
        CartNew.objects.filter(pk=product_id).delete()
    return showcart(request)

