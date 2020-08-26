from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,CartNew,Wish
from .forms import CartForm,Filter

def homepage(request):
    if request.method == 'POST':
        print(request.POST)
        if 'search' in request.POST:
            form = CartForm()
            formfilter = Filter()
            searchstring = request.POST['search']
            products = Product.objects.filter(p_name__icontains = searchstring)
            return render(request, 'products/home.html', {'products': products,'form':form,'filter':formfilter})
        elif request.POST['max_price'] and request.POST['min_price']:
            form = CartForm()
            formfilter = Filter(request.POST)
            minp = request.POST['min_price']
            maxp = request.POST['max_price']
            if int(minp)>int(maxp):
                formfilter1 = Filter()
                products = Product.objects.raw('SELECT * FROM products_product;')
                return render(request,'products/home.html',{'products':products,'form':form,'filter':formfilter1,'filtererror':'Please enter valid parameter values'})
            else:
                products = Product.objects.raw('''SELECT * FROM products_product WHERE p_cost BETWEEN %s AND %s ''',[minp,maxp])
                return render(request,'products/home.html',{'products':products,'form':form,'filter':formfilter})

    else:
        form = CartForm()
        formfilter = Filter()
        # deals = Product.objects.raw('SELECT * FROM products_product WHERE p_discount>10;')
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


def about(request):
    return render(request, 'products/about.html')


def detail(request,product_id,error=''):
    getproduct = get_object_or_404(Product,p_id=product_id)
    form = CartForm()
    return render(request,'products/detail.html',{'product':getproduct,'form':form,'error':error})


def page(request,page_id):
    form = CartForm()
    formfilter = Filter()
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
    return render(request, 'products/home.html',{'products': products[start:end], 'pages': l,'page_no':page_id, 'form': form, 'filter': formfilter})

@login_required
def addtocart(request,product_id):
    print(request)
    if request.method == 'POST':
        form = CartForm()
        getproduct = get_object_or_404(Product,p_id=product_id)
        cart = CartNew.objects.filter(orderedby=request.user)
        c = CartNew()
        c.c_id = getproduct.p_id
        c.name = getproduct.p_name
        if request.POST['quantity'] == '':
            c.quantity = 1
        else:
            c.quantity = request.POST['quantity']
        total = getproduct.p_stock
        t = int(c.quantity)
        print(t)
        print(total)
        if total<t:
            error='Invalid quantity. Please order lower amount'
            return detail(request,getproduct.p_id,error)
        c.cost = getproduct.p_cost
        c.orderedby = request.user
        getproduct.p_stock = getproduct.p_stock - t
        getproduct.save()
        flag = 0
        for t in cart:
            if t.c_id==c.c_id:
                flag=1
        if flag==1:
            getcart = get_object_or_404(CartNew, c_id=product_id)
            getcart.quantity = int(getcart.quantity) + int(c.quantity)
            getcart.save()
        else:
            c.save()
        return redirect('home')
    else:
        form = CartForm
        formfilter = Filter()
        products = Product.objects
        return render(request, 'products/home.html', {'products': products, 'form':form,'filter':formfilter})


@login_required
def addtowish(request,product_id):
    if request.method == 'POST':
        getcart = get_object_or_404(Product,p_id=product_id)
        c = Wish()
        c.w_id = getcart.p_id
        c.name = getcart.p_name
        c.cost = getcart.p_cost
        c.image = getcart.p_image
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
    # for i in range(len(allproducts)):
    #     while allproducts[i] in allproducts[i:]:
    #         allproducts[i].quantity++
    t = len(allproducts)
    return render(request, 'products/cart.html', {'products': allproducts,'len':t})


@login_required
def wishes(request):
    form = CartForm()
    allproducts = Wish.objects.filter(orderedby=request.user)
    return render(request, 'products/wishlist.html', {'products': allproducts,'form':form})

@login_required
def removewish(request,product_id):
    if request.method == 'POST':
        Wish.objects.filter(w_id=product_id).delete()
    return wishes(request)

@login_required
def editcart(request,product_id):
    if request.method == 'POST':
        getproduct = get_object_or_404(Product, p_id=product_id)
        getcart = get_object_or_404(CartNew, c_id=product_id)
        getproduct.p_stock = getproduct.p_stock + getcart.quantity
        getproduct.save()
        CartNew.objects.filter(c_id=product_id).delete()
    return showcart(request)

@login_required
def deleteallw(request):
    if request.method == 'POST':
        Wish.objects.filter(orderedy=request.user).delete()
    return redirect('home')

@login_required
def checkout(request):
    orders = CartNew.objects.all()
    l = len(orders)
    total=0
    print(orders[0].name)
    for o in orders:
        total = total+(o.cost*o.quantity)
    return render(request,'products/checkout.html',{'orders':orders,'l':l,'total':total})

@login_required
def placeorder(request):
    if request.method == 'POST':
        CartNew.objects.filter(orderedby=request.user).delete()
    return redirect('home')

