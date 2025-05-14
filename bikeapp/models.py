from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    house = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    pin = models.IntegerField()
    phone = models.IntegerField()
    fk1 = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Staff(models.Model):
    phone = models.IntegerField()
    district = models.CharField(max_length=30)
    pin = models.IntegerField()
    status = models.CharField(max_length=10,null=True)
    fk2 = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Mechanic(models.Model):
    phone = models.IntegerField()
    district = models.CharField(max_length=30)
    pin = models.IntegerField()
    status = models.CharField(max_length=10,null=True)
    fk3 = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    lat = models.CharField(max_length=100,null=True)
    lon = models.CharField(max_length=100,null=True)

class MechanicBooking(models.Model):
    cusid = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date = models.DateField()#bookingdate
    time = models.DateTimeField(auto_now=True)#added datetime
    status = models.CharField(max_length=20)
    mid = models.ForeignKey(Mechanic,on_delete=models.CASCADE)

class Chat(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    message = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

class Stock(models.Model):
    date = models.DateField(auto_now=True,null=True)
    partname = models.CharField(max_length = 100)
    partmanufactures = models.CharField(max_length = 100)
    partprice = models.IntegerField()
    partcount = models.IntegerField()
    partwarranty = models.CharField(max_length=20,null=True)
    partimage = models.FileField(null=True)
    sid = models.ForeignKey(Staff,on_delete=models.CASCADE)

class Order(models.Model):
    cusid = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    # feedback = models.CharField(max_length=200,null=True)
    
class Cart(models.Model):
    ordid = models.ForeignKey(Order,on_delete=models.CASCADE)
    stkid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)
    amt = models.IntegerField(null=True)