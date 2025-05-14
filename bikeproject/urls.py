"""
URL configuration for bikeproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from bikeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('customerreg/', views.customerreg),
    path('mechanicreg/', views.mechanicreg),
    path('sellerreg/', views.sellerreg),
    path('adminhome/', views.adminhome),
    path('cushome/', views.cushome),
    path('cusviewproduct/', views.cusviewproduct),
    path('cusviewproddetails/', views.cusviewproddetails),
    path('cusviewcart/', views.cusviewcart),
    path('cusremovefromcart/', views.cusremovefromcart),
    path('cusvieworders/', views.cusvieworders),
    path('cuspay/', views.cuspay),
    path('cusviewmechanics/', views.cusviewmechanics),
    path('cusbookmechanic/', views.cusbookmechanic),
    path('cusviewmechanicsbooking/', views.cusviewmechanicsbooking),
    path('customer_chat_with_mechanic/', views.customer_chat_with_mechanic),
    path('staffhome/', views.staffhome),
    path('mechanichome/', views.mechanichome),
    path('mechanicviewbookings/', views.mechanicviewbookings),
    path('mechanic_chat_with_customer/', views.mechanic_chat_with_customer),
    path('staffaddstock/', views.staffaddstock),
    path('staffupdatestock/', views.staffupdatestock),
    path('staffvieworders/', views.staffvieworders),
    path('staffdelivredorder/', views.staffdelivredorder),
    path('adminmanagestaff/', views.adminmanagestaff),
    path('admindeletestaff/', views.admindeletestaff),
    path('adminmanagemechanic/', views.adminmanagemechanic),
    path('admindeletemechanic/', views.admindeletemechanic),
    path('admindeleteuser/', views.admindeleteuser),
    path('adminmanageuser/', views.adminmanageuser),
    path('adminmanagestock/', views.adminmanagestock),
    path('admindeletestock/', views.admindeletestock),
    path('login/', views.login),
]
