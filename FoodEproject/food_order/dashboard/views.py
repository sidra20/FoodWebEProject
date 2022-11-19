import os
import re
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from .encryption_util import encrypt
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from dashboard.encryption_util import *

from django.core.signing import Signer
import base64
import uuid



# Create your views here.

def adminhome(request):
    name = request.session.get('user_name')
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'adminhome.html')
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')


def menu(request):
    return render(request, 'Menu.html')

def roles(request):
    role = Roles.objects.all()

    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'roles.html', {'role': role})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')


def role_store(request):
    rolesObj = Roles()

    roles = request.POST.get('role')
    rolesObj.role = roles
    if not request.POST.get('role'):
        messages.error(request, "The fields are required!")
    if not re.match(r'^[A-Za-z ]{3,50}$', request.POST.get('role')):
        messages.error(request, "Incorrect format!")
    else:
        if Roles.objects.filter(role=roles):
            messages.error(request, "Already exists!")
        else:
            rolesObj.save()
            messages.success(request, "Role added!")

    # for list in role_list:
    #     if(list.role == request.POST.get('role')):
    #         messages.error(request, "Role alreday exists!")
    #     else:
    #         role.save()
    #         messages.success(request, "Role added!")

    return redirect('/dashboard/roles')

def delete_role(request,pk):
    role = Roles.objects.filter(id=pk)
    role.delete()
    messages.success(request, "Role deleted!")
    return redirect('/dashboard/roles')

# USERS
# def register(request):
#     role = Roles.objects.filter(role="Customer")
#     return render(request, 'register.html', {'role': role})

def register_store(request):
    usersObj = Users()
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    cpass = request.POST.get('cpass')
    userrole = request.POST.get('role')
    today = date.today()
    d = today.strftime("%d/%m/%Y")

    usersObj.name=name
    usersObj.email=email
    usersObj.password=make_password(password)
    usersObj.datejoin=d
    usersObj.role_id=userrole

    if not name:
        messages.error(request, "The fields are required!")
    elif not email:
        messages.error(request, "The fields are required!")
    elif not password:
        messages.error(request, "The fields are required!")
    elif not cpass:
        messages.error(request, "The fields are required!")
    elif not userrole:
        messages.error(request, "The fields are required!")

    else:
        if len(name)<3:
            messages.error(request, "Name shouldn't be less than 3 characters.")
        if len(password)<6:
            messages.error(request, "Password shouldn't be less than 6 characters.")

        else:
            if password != cpass:
                messages.error(request, "Password do not match.")
            elif not re.match(r'^[A-Za-z ]{3,150}$', name):
                messages.error(request, "Name is not correct in format!")
            elif not re.match(r'^[A-Za-z]{1,15}[0-9@#$%&*^!]{1,15}$', password):
                messages.error(request, "Password should contain numbers or special charater!")
            elif Users.objects.filter(email=email):
                messages.error(request, "Email already exists!")
            else:
                usersObj.save()
                messages.success(request,"Registered successfully!")
    return redirect('../website/register')


#categories index
def category_index(request):
    cat = Categories.objects.all()
    catObj = Categories()
    strId = str(catObj.id)
    encryptId=make_password(strId)
    #encryptId=crypt.crypt(strId)
    decryptId = check_password(strId, encryptId)
    signer = Signer()
    # encrypt_key = signer.sign_object(catObj.id)
    # decrypt_key = signer.unsign_object(encrypt_key)

    # li=[]
    # for i in cat:
    #     encrypt_key = base64.b64encode(i['id'])
    #     i['id'] = encrypt_key
    #     li.append(i)


    # li=[]
    # for i in cat:
    #     i['encrypt_key'] = encrypt(i['id'])
    #     i['id'] = i['id']
    #     li.append(i)
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'categories.html',{'cat':cat,'encryptId':encryptId,'decryptId':decryptId})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')


    # return render(request,'categories.html',{'cat':cat})

def category_store(request):
    catList = Categories.objects.all()
    error =""
    success=""
    cat = Categories()
    category = request.POST.get('category')
    img = request.FILES.get('image')

    cat.category = category
    cat.img = img

    if not category:
        error = "Fields are required!"
    if not img:
        error = "Fields are required!"
    elif len(category)<3:
        error = "Must be more than 3 characters."
    elif not re.match(r'^[A-Za-z ]{3,150}$', category):
        error = "Category name should only contain alphabets!"
    elif Categories.objects.filter(category=category):
        error = "Category already exists!"
    else:
        cat.save()
        success="Category added successfully!"
    return render(request,'categories.html',{'success':success,'error':error,'cat':catList})


def category_delete(request,pk):

    cat = Categories.objects.get(id=pk)
    if(len(cat.img)>0):
        os.remove(cat.img.path)
    cat.delete();
    messages.success(request,"Catgorry deleted successfully!")
    return redirect('/dashboard/categories')

def category_edit(request,pk):
    # signer = Signer()
    # decrypt_key = signer.unsign_object(pk)
    catObj = Categories()
    strId = str(catObj.id)
    decryptId = check_password(strId, pk)
    cat = Categories.objects.get(id=decryptId)

    return render(request,'category_edit.html',{'cat':cat})

def category_update(request):
    editerror = ""
    catList = Categories.objects.all()
    cat = Categories.objects.get(id=request.POST.get('id'))
    category = request.POST.get('category')
    img = request.FILES.get('image')

    if not category:
        editerror = "Couldn't update.Fields are required!"
    if not img:
        editerror = "Couldn't update.Fields are required!"

    elif not re.match(r'^[A-Za-z ]{3,150}$', category):
        editerror = "Couldn't update. Category nae should only contain alphabets!"

    else:

        if (len(request.FILES.get('image')) != 0):
            if (len(cat.img) > 0):
                os.remove(cat.img.path)
        cat.img = img
        cat.category = category
        cat.save(update_fields=['category','img'])
        messages.success(request, "Catgorry updated successfully!")

    return render(request,'categories.html',{'editerror':editerror,'cat':catList})

#foodtypes

def foodtype_index(request):
    types = FoodTypes.objects.all()
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'foodtypes.html',{'types':types})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')



def foodtype_store(request):
    types = FoodTypes.objects.all()
    error =""
    success=""
    ft = FoodTypes()
    foodtype = request.POST.get('foodtype')
    uid = uuid.uuid4()



    if not foodtype:
        error = "Fields are required!"

    elif len(foodtype)<3:
        error = "Must be more than 2 characters."
    elif not re.match(r'^[A-Za-z ]{2,150}$', foodtype):
        error = "Foodtype name should only contain alphabets!"
    elif FoodTypes.objects.filter(foodtype=foodtype):
        error = "Foodtype already exists!"
    else:
        ft.uuid = uid
        ft.foodtype = foodtype
        ft.save()
        success="Foodtype added successfully!"
    return render(request,'foodtypes.html',{'success':success,'error':error,'types':types})

def foodtype_delete(request,pk):

    types = FoodTypes.objects.get(id=pk)
    types.delete();
    messages.success(request,"Record deleted successfully!")
    return redirect('/dashboard/foodtypes')

def foodtype_edit(request,pk):
    types = FoodTypes.objects.get(uuid=pk)
    return render(request, 'foodtype_edit.html', {'types': types})

def foodtype_update(request):
    editerror = ""
    types = FoodTypes.objects.all()
    ft = FoodTypes.objects.get(uuid=request.POST.get('id'))
    foodtype = request.POST.get('foodtype')

    if not foodtype:
        editerror = "Couldn't update.Fields are required!"

    elif not re.match(r'^[A-Za-z ]{3,150}$', foodtype):
        editerror = "Couldn't update. Category nae should only contain alphabets!"

    else:

        ft.foodtype = foodtype
        ft.save(update_fields=['foodtype'])
        messages.success(request, "Record updated successfully!")

    return render(request, 'foodtypes.html', {'editerror': editerror, 'types': types})


#book

def books_index(request):
    books = Books.objects.all()
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'books.html',{'books':books})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')




def books_store(request):
    books = Books.objects.all()
    error =""
    success=""
    bookObj = Books()
    bookname = request.POST.get('bookname')
    authorname = request.POST.get('authorname')
    img = request.FILES.get('image')
    bookpdf = request.FILES.get('bookpdf')

    uid = uuid.uuid4()




    if not bookname:
        error = "Fields are required!"
    if not authorname:
        error = "Fields are required!"
    if not img:
        error = "Fields are required!"
    if not bookpdf:
        error = "Fields are required!"
    elif len(bookname)<3:
        error = "Must be more than 3 characters."
    elif len(authorname) < 3:
        error = "Must be more than 3 characters."
    elif not re.match(r'^[A-Za-z ]{3,150}$', bookname):
        error = "Book name should only contain alphabets!"

    elif not re.match(r'^[A-Za-z ]{3,150}$', authorname):
        error = "Author name should only contain alphabets!"
    elif Books.objects.filter(book_name=bookname):
        error = "Book already exists!"
    else:
        bookObj.book_name = bookname
        bookObj.book_author = authorname
        bookObj.book_cover = img
        bookObj.book = bookpdf
        bookObj.uuid=uid
        bookObj.save()
        success="Book added successfully!"
    return render(request,'books.html',{'success':success,'error':error,'books':books})

def book_delete(request,pk):

    books = Books.objects.get(id=pk)
    if(len(books.book_cover)>0):
        os.remove(books.book_cover.path)
    if (len(books.book) > 0):
        os.remove(books.book.path)
    books.delete();
    messages.success(request,"Record deleted successfully!")
    return redirect('/dashboard/books')

def book_edit(request,pk):
    book = Books.objects.get(uuid=pk)
    return render(request, 'book_edit.html', {'book': book})
def book_update(request):
    editerror = ""
    booklist = Books.objects.all()
    bookObj = Books.objects.get(uuid=request.POST.get('id'))
    bookname = request.POST.get('bookname')
    auhthorname = request.POST.get('auhthorname')
    img = request.FILES.get('bookcover')
    bookpdf = request.FILES.get('bookpdf')

    if not bookname:
        editerror = "Couldn't update.Fields are required!"
    elif not img:
        editerror = "Couldn't update.Fields are required!"
    elif not auhthorname:
        editerror = "Couldn't update.Fields are required!"
    elif not bookpdf:
        editerror = "Couldn't update.Fields are required!"

    elif not re.match(r'^[A-Za-z ]{3,150}$', bookname):
        editerror = "Couldn't update. Book name should only contain alphabets!"
    elif not re.match(r'^[A-Za-z ]{3,150}$', auhthorname):
        editerror = "Couldn't update. Author name should only contain alphabets!"

    else:


        if (len(request.FILES.get('bookpdf')) != 0):
            if (len(bookObj.book) > 0):
                os.remove(bookObj.book.path)

        elif (len(request.FILES.get('bookcover')) != 0):
            if (len(bookObj.book_cover) > 0):
                os.remove(bookObj.book_cover.path)
        else:
            editerror = "Couldn't update.Fields are required!"

        bookObj.book_name = bookname
        bookObj.book_author = auhthorname
        bookObj.book_cover = img
        bookObj.book = bookpdf
        bookObj.save(update_fields=['book_name', 'book_author','book_cover','book'])
        messages.success(request, "Record updated successfully!")

    return render(request, 'books.html', {'editerror': editerror, 'books': booklist})

#USERS
def user_index(request):
    users = Roles.objects.raw("SELECT * FROM dashboard_users JOIN dashboard_roles ON dashboard_users.role_id = dashboard_roles.id ORDER BY dashboard_users.id ")
    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'users.html',{'users':users})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')

def custusers_index(request):
    users = Roles.objects.raw("SELECT * FROM dashboard_users JOIN dashboard_roles ON dashboard_users.role_id = dashboard_roles.id WHERE dashboard_roles.role='Customer' ")

    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'customer_users.html',{'users':users})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')

def restusers_index(request):
    restusers = Roles.objects.raw(
        "SELECT * FROM dashboard_users JOIN dashboard_roles ON dashboard_users.role_id = dashboard_roles.id WHERE dashboard_roles.role='Resturant Owner' ")

    userid = request.session.get('user_id')

    if userid:
        user = Users.objects.get(id=userid)
        if user.role_id == 1:
            return render(request, 'restowner_users.html', {'restusers': restusers})
        elif user.role_id == 2:
            return redirect('../website/index')
        else:
            return redirect('../vendor/resturanthome')
    else:
        return redirect('../website/login')

def logout(request):
    request.session.clear()
    return redirect('../website/index')