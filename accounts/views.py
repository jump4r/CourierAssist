from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from stravalib.client import Client
from stravalib import model

from CourierAssist import config_vars
from . import models
from pprint import pprint

# Create your views here.
def profile(request):
    _code = request.GET.get('code')

    if (request.user.is_authenticated):

        pprint("User is Logged In")
        pprint(request.user.username)
        return HttpResponse("Hello " + request.user.username)
    else:
        pprint("User is not logged in")
        return HttpResponse("User Anonymous")
    
def error(request):
    return HttpResponse("Error Creating User")

def create(request):

    if (request.method == 'GET'):
        return render(request, 'create.html')

    elif (request.method == 'POST'):

        # Create A User Account
        _username = request.POST.get('username')
        _password = request.POST.get('password')

        _new_user = User.objects.create_user(username=_username, password=_password)

        _new_user.save()

        success = loginUserAttempt(request, _username, _password)

        if success:
            return redirect("profile")

        else:
            return redirect("error")

def login(request):
    
    if (request.method == "POST"):
        _username = request.POST.get('username')
        _password = request.POST.get('password')

        success = loginUserAttempt(request, _username, _pasword)

        if (success):
            return redirect("profile")
        else:
            return redirect("error")


def loginUserAttempt(request, username, password):
    _user = authenticate(request, username=username, password=password)
    
    if (_user is not None):
        auth_login(request, _user)
        return True

    else:
        return False
