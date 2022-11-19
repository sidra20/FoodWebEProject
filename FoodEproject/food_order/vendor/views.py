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
