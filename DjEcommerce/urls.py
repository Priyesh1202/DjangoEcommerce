"""DjEcommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import products.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',products.views.homepage, name='home'),
    path('addtocart/<int:product_id>/', products.views.addtocart, name='addtocart'),
    path('addtowish/<int:product_id>/', products.views.addtowish, name='addtowish'),
    path('removewish/<int:product_id>/', products.views.removewish, name='deletefromwish'),
    path('wishlist/', products.views.wishes, name='wishlist'),
    path('emptywish/', products.views.deleteallw, name='delete'),
    path('<int:product_id>/',products.views.detail,name='detail'),
    path('cart/<int:product_id>/',products.views.editcart,name='editcart'),
    path('cart/',products.views.showcart,name='showcart'),
    path('accounts/', include('accounts.urls')),
    path('checkout/',products.views.checkout,name='checkout'),
    path('page/<int:page_id>/',products.views.page,name='page'),
    path('placeorder/',products.views.placeorder,name='placeorder'),
    path('about/', products.views.about, name='about'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
