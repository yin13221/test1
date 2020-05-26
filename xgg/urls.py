"""xgg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload'),
    path('uploadphoto', views.uploadphoto, name='uploadphoto'),
    path('photo/<id>', views.photo, name='photo'),
    path('goods', views.goods, name='goods'),
    path('good/<id>', views.find_good, name='find_good'),
    path('good_class', views.good_class, name='good_class'),
    path('setCart', views.setCart, name='setCart'),
    path('confirm', views.confirm, name='confirm'),
    path('getCart', views.getCart, name='getCart'),
    path('getcheckCart', views.getcheckCart, name='getcheckCart'),
    path('changecheck', views.changecheck, name='changecheck'),
    path('checkall', views.checkall, name='checkall'),
    path('changenum', views.changenum, name='changenum'),
    path('setAddr', views.setAddr, name='setAddr'),
    path('updateAddr', views.updateAddr, name='updateAddr'),
    path('delAddr/<id>', views.delAddr, name='delAddr'),
    path('getAddr', views.getAddr, name='getAddr'),
    path('getfirstAddr', views.getfirstAddr, name='getfirstAddr'),
    path('Addr/<id>', views.Addr, name='Addr'),
    path('getdd', views.getdd, name='getdd'),
    path('comment', views.comment, name='comment'),
    path('getcomm/<id>', views.getcomm, name='getcomm'),
    path('getmoney', views.getmoney, name='getmoney')
]
