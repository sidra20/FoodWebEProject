import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

import sys, os

from dashboard.models import *

sys.path.append(os.path.abspath('../dashboard/models.py'))

from django.contrib.auth.hashers import make_password, check_password



# Create your views here.

def about(request):
    return render(request, 'about.html')


def gallery(request):
    return render(request, 'gallery.html')

def index(request):
    name = request.session.get('user_name')
    return render(request,'index.html',{'name':name})

def shop(request):
    return render(request,'shop.html')

def foodItem(request):
    return render(request,'fooditem.html')

def cart(request):
    userid = request.session.get('user_id')
    if userid:
        return render(request, 'cart.html')
    else:
        return render(request, 'user_login.html')


def checkout(request):
    return render(request,'checkout.html')

def userRegister(request):
    role = Roles.objects.filter(role= 'Customer')
    role1 = Roles.objects.filter(role= 'Resturant Owner')

    return render(request,'user_register.html',{'role':role,'role1':role1})

def userLogin(request):
    return render(request,'user_login.html')

def getUser(email):
    try:
        return Users.objects.get(email=email)
    except:
        return False
def login_store(request):


    email = request.POST.get('email')
    password = request.POST.get('pass')

    if not email:
        messages.error(request, "The fields are required!")
    elif not password:
        messages.error(request, "The fields are required!")

    else:
        user = getUser(email)
        if user:
            decrypt = check_password(password, user.password)
            if decrypt:
                request.session['user_id']=user.id
                request.session['user_name']=user.name
                request.session['user_email']=user.email

                #return redirect('../dashboard/categories')

                #SELECT Users.role_id, Roles.role FROM Users INNER JOIN Roles ON Users.role_id = Roles.id;
                #select * from Users join Roles on user.role_id = role.id where roles.role='Admin
                if(user.role_id==1):
                    return redirect('../dashboard/adminhome')

                elif user.role_id==2:
                    return redirect('/website/index')

                else:
                    return redirect('../vendor/resturanthome')

            else:
                messages.error(request, "Wrong password")
        else:
            messages.error(request, "Invalid email or password!")



    return redirect('/website/login')

def logout(request):
    request.session.clear()
    return redirect('/website/index')