from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import date
from geopy.distance import geodesic

# Create your views here.

def index(request):
    # oneuser = User.objects.get(id=32)
    # oneuser.set_password("nuser@gmaiL123")
    # oneuser.save()
    return render(request,'index.html')

def customerreg(request):
    if request.method == "POST":
        fname = request.POST['uname']
        lname = request.POST['lName']
        house = request.POST['house']
        street = request.POST['street']
        district = request.POST['district']
        pin = request.POST['pin']
        phone = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username = email):
            messages.info(request,"Email already exist.")
            return redirect('/customerreg')
        data = User.objects.create_user(first_name=fname,
                                        last_name=lname,
                                     username=email,
                                     email=email,
                                     password=password,
                                     is_staff=1)
        data.save()
        var = Customer.objects.create(phone=phone,
                                     house=house,
                                     street=street,
                                     district=district,
                                     pin=pin,
                                     fk1=data)
        var.save()
        messages.info(request,"Signed Up succesfully.")
        return redirect('/login')
    return render(request,'customerreg.html')

def login(request):
    if request.method == "POST":
        email = request.POST['uname']
        password = request.POST['password']
        data = authenticate(username=email,password=password)
        if data is None:
            if User.objects.filter(username = email):
                us = User.objects.get(username = email)
                messages.info(request,"Password Mismatch.")
            else:
                messages.info(request,"No such user found")
        else:
            if data.is_superuser:
                messages.info(request,"Logged inn..")
                return redirect("/adminhome")
            elif data.last_name == "Mechanic":
                messages.info(request,f"Welcome {data.first_name}")
                request.session["mid"] = data.id
                return redirect("/mechanichome?name="+data.first_name)
            elif data.is_staff:
                request.session["cid"] = data.id
                messages.info(request,f"Hii {data.first_name}")
                return redirect("/cushome?name="+data.first_name)
            else:
                name = data.first_name
                messages.info(request,f"Welcome {data.first_name}")
                request.session["sid"] = data.id
                return redirect(f"/staffhome?name={name}")
    return render(request,"Login.html")

def adminhome(request):
    return render(request,'adminhome.html')

def adminmanagestaff(request):
    data = Staff.objects.filter(status = "live")
    alpha = Staff.objects.filter(status = "notlive")
    return render(request,'adminmanagestaff.html',{"data": data,"alpha":alpha})

def admindeletestaff(request):
    sid = request.GET.get("sid")
    dele = Staff.objects.get(fk2__id = sid)
    dele.status = "notlive"
    dele.save()
    messages.info(request,"Removed succesfully.")
    return redirect(adminmanagestaff)

def adminmanageuser(request):
    data = Customer.objects.all()
    return render(request,"adminmanageuser.html",{"data":data})

def admindeleteuser(request):
    cid = request.GET.get("sid")
    dele = Customer.objects.get(fk1__id = cid)
    dele.delete()
    messages.info(request,"Removed succesfully.")
    return redirect(adminmanageuser)

def adminmanagemechanic(request):
    data = Mechanic.objects.filter(status = "live") 
    alpha = Mechanic.objects.filter(status = "notlive")
    return render(request,'adminmanagemechanic.html',{"data": data,"alpha":alpha})

def mechanicreg(request):
    if request.method == "POST":
        name = request.POST['uname']
        district = request.POST['district']
        pin = request.POST['pin']
        phone = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        if User.objects.filter(username = email):
            messages.info(request,"Email already exist.")
            return redirect('/mechanicreg')
        data = User.objects.create_user(first_name=name,
                                        last_name="Mechanic",
                                     username=email,
                                     password=password,
                                     is_staff=0,
                                     is_active=1)
        data.save()
        var = Mechanic.objects.create(phone=phone,
                                     district=district,
                                     pin=pin,
                                     fk3=data,
                                     status = "live",
                                     lat=latitude,
                                     lon=longitude)
        var.save()
        messages.info(request,"Signed Up succesfully.")
        return redirect('/login')
    return render(request,'mechanicreg.html')

def sellerreg(request):
    if request.method == "POST":
        name = request.POST['uname']
        district = request.POST['district']
        pin = request.POST['pin']
        phone = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username = email):
            messages.info(request,"Email already exist.")
            return redirect('/sellerreg')
        data = User.objects.create_user(first_name=name,
                                     username=email,
                                     password=password,
                                     is_staff=0,
                                     is_active=1)
        data.save()
        var = Staff.objects.create(phone=phone,
                                     district=district,
                                     pin=pin,
                                     status = "live",
                                     fk2=data)
        var.save()
        messages.info(request,"Signed Up succesfully.")
        return redirect('/login')
    return render(request,'sellerreg.html')

def admindeletemechanic(request):
    sid = request.GET.get("sid")
    dele = Mechanic.objects.get(fk3__id = sid)
    dele.status = "notlive"
    dele.save()
    messages.info(request,"Removed succesfully.")
    return redirect(adminmanagemechanic)

def adminmanagestock(request):
    data = Stock.objects.all()
    return render(request,"adminmanagestock.html",{"data":data})

def admindeletestock(request):
    stkid = request.GET.get('stkid')
    data = Stock.objects.get(id = stkid)
    data.delete()
    messages.info(request,"Stock removed.")
    return redirect("/adminmanagestock")

def cushome(request):
    cid = request.session["cid"]
    data = Customer.objects.get(fk1__id = cid)
    return render(request,'cushome.html',{"data":data})

def cusviewproduct(request):
    data = Stock.objects.all()
    return render(request,'cusviewproduct.html',{"data":data})

def cusviewproddetails(request):
    c = request.session["cid"]
    stkid = request.GET.get("stkid")
    data = Stock.objects.get(id = stkid)
    if request.POST:
        qty = request.POST["qty"]
        if Order.objects.filter(Q(cusid__fk1__id = c) & Q(status = "pending")):
            alpha = Order.objects.get(Q(cusid__fk1__id = c) & Q(status = "pending"))
            amt = int(data.partprice) * int(qty)
            gama = Cart.objects.create(ordid = alpha,
                                        stkid = data,
                                        qty = qty,
                                        amt = amt)
            gama.save()
            data.partcount -= 1
            data.save() 
            messages.info(request,"Added To Cart.")
            return redirect(cusviewproduct)
        else:
            # print("inalpha")
            cusid = Customer.objects.get(fk1__id = c)
            beta = Order.objects.create(cusid = cusid,
                                        status = "pending")
            beta.save()
            amt = int(data.partprice) * int(qty)
            gama = Cart.objects.create(ordid = beta,
                                        stkid = data,
                                        qty = qty,
                                        amt = amt)
            gama.save()
            data.partcount -= 1
            data.save()
            messages.info(request,"Added To Cart.")
            return redirect(cusviewproduct)
    return render(request,'cusviewproddetails.html',{"data":data})

def cusviewcart(request):
    cid = request.session["cid"]
    data = Cart.objects.filter(Q(ordid__cusid__fk1__id = cid) & Q(ordid__status = "pending"))
    total = 0
    noofitems = 0
    for d in data:
        noofitems = noofitems + 1
        total = total + d.amt
    return render(request,'cusviewcart.html',{"data":data,"total":total,"noofitems":noofitems})

def cuspay(request):
    total = request.GET.get("total")
    noofitems = request.GET.get("noofitems")
    if request.POST:
        cid = request.session["cid"]
        data = Cart.objects.filter(Q(ordid__cusid__fk1__id = cid) & Q(ordid__status = "pending"))
        for d in data:
            order = Order.objects.get(id = d.ordid.id)
            order.status = "Ordered"
            order.save()
        messages.info(request,"Payment succesful")
        return redirect(cusviewcart)
    return render(request,'cuspay.html',{"total":total,"noofitems":noofitems}) 

def cusviewmechanics(request):
    if "lat" in request.GET:
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        lat = float(lat)
        lon = float(lon)
        data = Mechanic.objects.filter(status = "live")
        for d in data:
            d.distance = geodesic((lat,lon),(d.lat,d.lon)).kilometers
        for d in data:
            print(d.distance,"--------------------------------------")
        data = sorted(data, key=lambda x: x.distance)
        return render(request,'cusviewmechanics.html',{"data":data})
    data = Mechanic.objects.filter(status = "live")
    return render(request,'cusviewmechanics.html',{"data":data})

def cusbookmechanic(request):
    mid = request.GET.get("mid")
    cid = request.session["cid"]
    date = request.GET.get("booking_date")
    print(date,"--------------------------------------")
    if request.POST:
        cusid = Customer.objects.get(fk1__id = cid)
        data = Mechanic.objects.get(id = mid)
        print(date,"--------------------------------------")
        beta = MechanicBooking.objects.create(cusid = cusid,
                                            mid = data,
                                            date = date,
                                            status = "Paid")
        beta.save()
        messages.info(request,"Mechanic Booked.")
        return redirect(cusviewmechanics)
    return render(request,'cusbookmechanic.html')

def cusviewmechanicsbooking(request):
    cid = request.session["cid"]
    data = MechanicBooking.objects.filter(cusid__fk1__id = cid)
    return render(request,'cusviewmechanicsbooking.html',{"data":data})

def customer_chat_with_mechanic(request):
    cid = request.session["cid"]
    mid = request.GET.get("mid")
    mechanic = User.objects.get(id = mid)
    customer = User.objects.get(id = cid)
    data = Chat.objects.filter((Q(sender__id = cid) & Q(receiver__id = mid)) | (Q(sender__id = mid) & Q(receiver__id = cid))).order_by('date')
    if request.method == "POST":
        message = request.POST['message']
        beta = Chat.objects.create(sender = customer,
                                    receiver = mechanic,
                                    message = message)
        beta.save()
    return render(request,'customer_chat_with_mechanic.html',{"data":data, "mechanic":mechanic})

def cusremovefromcart(request):
    cartid = request.GET.get("cartid")
    data = Cart.objects.get(id = cartid)
    link = Stock.objects.get(id = data.stkid.id)
    link.partcount += 1
    link.save()
    data.delete()
    return redirect(cusviewcart)

def cusvieworders(request):
    cid = request.session["cid"]
    data = Cart.objects.filter(Q(ordid__cusid__fk1__id = cid) & (Q(ordid__status = "delivered") | Q(ordid__status = "Ordered")))
    return render(request,'cusvieworders.html',{"data":data})

def staffhome(request):
    name = request.GET.get("name") 
    return render(request,'staffhome.html',{"name":name})

def mechanichome(request):
    name = request.GET.get("name")
    return render(request,'mechanichome.html',{"name":name})

def mechanicviewbookings(request):
    mid = request.session["mid"]
    data = MechanicBooking.objects.filter(mid__fk3__id = mid)
    return render(request,'mechanicviewbookings.html',{"data":data})

def mechanic_chat_with_customer(request):
    mid = request.session["mid"]
    cid = request.GET.get("cid")
    customer = User.objects.get(id = cid)
    mechanic = User.objects.get(id = mid)
    data = Chat.objects.filter((Q(sender__id = mid) & Q(receiver__id = cid)) | (Q(sender__id = cid) & Q(receiver__id = mid))).order_by('date')
    if request.method == "POST":
        message = request.POST['message']
        beta = Chat.objects.create(sender = mechanic,
                                    receiver = customer,
                                    message = message)
        beta.save()
    return render(request,'mechanic_chat_with_customer.html',{"data":data, "customer":customer})

def staffaddstock(request):
    s = request.session["sid"]
    data = Stock.objects.filter(sid__fk2__id = s)
    if request.method == "POST":
        sid = Staff.objects.get(fk2__id = s)
        partname = request.POST['partname']
        partmanufactures = request.POST['partmanufactures']
        partprice = request.POST['partprice']
        partcount = request.POST['partcount']
        partwarranty = request.POST['partwarranty']
        partimage = request.FILES['partimage']
        beta = Stock.objects.create(partname = partname,
                                     partmanufactures = partmanufactures,
                                     partprice = partprice,
                                     partcount = partcount,
                                     partwarranty = partwarranty,
                                     partimage = partimage,
                                     sid = sid)
        beta.save()
    return render(request,'staffaddstock.html',{"data":data})

def staffupdatestock(request):
    s = request.GET.get("stkid")
    data = Stock.objects.get(id = s)
    if request.method == "POST":
        partname = request.POST['partname']
        partmanufactures = request.POST['partmanufactures']
        partprice = request.POST['partprice']
        partcount = request.POST['partcount']
        partwarranty = request.POST['partwarranty']
        data.partname = partname
        data.partmanufactures = partmanufactures
        data.partprice = partprice
        data.partcount = partcount
        data.partwarranty = partwarranty
        data.save()
        messages.info(request,"Updated succesfully.")
        return redirect(staffaddstock)
    return render(request,'staffupdatestock.html',{"data":data})

def staffvieworders(request):
    sid = request.session["sid"]
    data = Cart.objects.filter(Q(stkid__sid__fk2__id = sid) & Q(ordid__status = "Ordered"))
    beta = Cart.objects.filter(Q(stkid__sid__fk2__id = sid) & Q(ordid__status = "delivered"))
    return render(request,'staffvieworders.html',{"data":data,"beta":beta})

def staffdelivredorder(request):
    cartid = request.GET.get("cartid")
    data = Cart.objects.get(id = cartid)
    orid = data.ordid.id
    ord = Order.objects.get(id=orid)
    ord.status="delivered"
    ord.save()
    return redirect(staffvieworders)