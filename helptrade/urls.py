"""helptrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
    path('', views.start, name='start'),
    path('home/', views.home, name='home'),
    path('create/', views.signUpView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('signout/', views.signoutView, name='signout'),
    path('reverse/', views.reverse, name="reverse"),
    path('change/', views.change, name="change"),
    path('changed/', views.changed, name="changed"),
    path('transaction/', views.transaction, name="transaction"),
    path('transaction_result/', views.transaction_result, name="transaction_result"),
    path('sms_settings/', views.sms_settings, name="sms_settings"),
    path('sms_set_res/', views.sms_set_res, name="sms_set_res"),
    path('json_page/', views.json_page, name="json_page"),
    path('purchase/', views.purchase, name="purchase"),
    path('acc/', views.one_ac, name="acc"),

    #path('set_prices/', views.set_prices, name="set_prices"),
    #path('set_prices_res1/', views.set_prices_res1, name="set_prices_res1"),
    #path('set_prices_save/', views.set_prices_save, name="set_prices_save"),

]
