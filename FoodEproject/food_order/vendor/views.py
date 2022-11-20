from django.shortcuts import render
import os
import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *
from dashboard.encryption_util import *
from dashboard.models import *

from django.core.signing import Signer
import base64
import uuid

# Create your views here.
def resturant_home(request):
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, '../dashboard/adminhome')
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('/vendor/resturanthome')
    else:
        return redirect('../website/login')

def add_resturant(request):
    cat = Categories.objects.all()
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return redirect('../website/index')
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return render(request, 'add_resturant.html',{'cat':cat})
    else:
        return redirect('../website/login')

def resturant_store(request):
    cat = Categories.objects.all()
    userid = request.session.get('user_id')
    myresturant = AllResturants.objects.all()
    error =""
    success=""
    restObj = AllResturants()
    name = request.POST.get('resturant_name')
    location = request.POST.get('resturant_location')
    contact = request.POST.get('resturant_contact')
    deliverytime = request.POST.get('delivery_time')
    delivery_charges = request.POST.get('delivery_charges')
    img = request.FILES.get('image')

    uid = uuid.uuid4()
    all_cat = Categories.objects.all()
    cat_names = [x.category for x in all_cat]
    cat_ids = []
    for x in cat_names:
        if(request.POST.get(x)):
            cat_ids.append(int(request.POST.get(x)))
        else:
            pass



    if not name:
        error = "Fields are required!"
    if not location:
        error = "Fields are required!"
    if not contact:
        error = "Fields are required!"

    if not deliverytime:
        error = "Fields are required!"
    if not img:
        error = "Fields are required!"
    if not delivery_charges:
        error = "Fields are required!"
    elif not cat_ids:
        error = "Category is required!"
    elif len(name)<3:
        error = "Name must be more than 3 characters."
    elif len(location) < 5:
        error = "Location or address must be more than 5 characters."
    elif not re.match(r'^[A-Za-z ]{3,150}$', name):
        error = "Resturant name should only contain alphabets!"

    elif not re.match(r'^[A-Za-z0-9 ]{5,150}$', location):
        error = "Add proper location"

    elif not re.match(r'^[0-9]{10,11}$', contact):
        error = "Invalid Phone number!"
    elif AllResturants.objects.filter(name=name):
        error = "Choose unique resturant name, this name already exists!"
    else:
        robj = AllResturants.objects.create(
            name=name,
            image=img,
            location=location,
            delivery_time=deliverytime,
            delivery_charges=delivery_charges,
            contact=contact,
            uuid=uid,
            user_id=userid
        )

        # restObj.name = name
        # restObj.contact = contact
        # restObj.img = img
        # restObj.location = location
        # restObj.delivery_charges = delivery_charges
        # restObj.delivery_time = deliverytime
        # restObj.uuid = uid
        # restObj.user_id = userid
        for x in cat_ids:
            restcat=Categories.objects.get(id=x)
            robj.category.add(restcat)

        #restObj.save()
        success="Resturant added successfully!"
    return render(request,'add_resturant.html',{'success':success,'error':error,'resturant':myresturant,'cat':cat})


def my_resturant(request):
    userid = request.session.get('user_id')
    resturant = AllResturants.objects.filter(user_id=userid)

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 3:
            return render(request,'my_resturant.html',{'resturant':resturant})
        else:
            return redirect('../website/index')
    else:
        return redirect('../website/login')


def logout(request):
    request.session.clear()
    return redirect('../website/login')