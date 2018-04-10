from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from stravalib.client import Client
from stravalib import model

from pprint import pprint
import datetime

from CourierAssist import config_vars
from accounts.models import AuthUser
from restaurants.models import Restaurant
from .models import Delivery

# Create your views here.

def index(request):

    user = None 

    if (request.user.is_authenticated):
        user = AuthUser.objects.get(user_id=request.user.id)

    client = Client()
    authorize_url = client.authorization_url(client_id=24429, redirect_uri="http://localhost:8000/main")

    #get code from get
    #Get Code from webapp response
    code = request.GET.get('code') if (request.GET.get('code') != None) else ''

    start_pos, end_pos, a_polyline = '', '', ''
    if (code != '' and request.user.is_authenticated):

        access_token = client.exchange_code_for_token(client_id=24429, client_secret=config_vars.STRAVA_CLIENT_SECRET, code=code)

        user_model = AuthUser.objects.get(user_id=request.user.id)
        
        # Store User Access Token in DB
        if (user_model is not None):
            user_model.auth_code = access_token
            user_model.save()

    # Set Access Token On Client
    if (request.user.is_authenticated and user.auth_code != ''):
        
        pprint("User Logged in and has an auth code")
        client.access_token = user.auth_code
        athlete = client.get_athlete()

        full_activity = client.get_activity(1486441471, True)
        
        a_polyline = full_activity.map.polyline
        start_pos = full_activity.start_latlng
        end_pos = full_activity.end_latlng


    return render(request, "index.html", {
        "auth_url": authorize_url, 
        "start_pos": start_pos,
        "end_pos": end_pos,
        "polyline": a_polyline,
        "user_is_authenticated": request.user.is_authenticated 
    })

def add_delivery(request):
    pprint("Are we getting here?")
    message = ""
     
    if (request.user.is_authenticated and request.method == "POST"):
        # Get POST Vars, hopefully we can get Postamtes to open their API
        # So I can get access to this shit.
        # That's not gonna happen though.
        _name = request.POST.get('name')
        _address = request.POST.get('address')
        _time = request.POST.get('time')
        _wait = request.POST.get('wait')
        _distance = request.POST.get('distance')
        _base = float(request.POST.get('base'))
        _tip = float(request.POST.get('tip'))
        
        # Update Our Restaurant Table
        try:
            r = Restaurant.objects.get(name=_name)
            message = "Delivery Already Added, updating"

            _total_tips = 0 if _tip <= 0 else 1
            r.total_tips += _total_tips
            r.total_tip_amount += _tip

            r.total_earnings += _base
            r.total_deliveries += 1
            r.save()


        except Restaurant.DoesNotExist:
            _total_tips = 0 if _tip <= 0 else 1
            r = Restaurant(name=_name, total_earnings=_base, total_tips=_total_tips, total_tip_amount=_tip)
            r.save()

        pprint(r)
        message = "Delivery Added To Database"

        # Update Our Delivery Table
        d = Delivery(
            user_id=request.user.id,
            restaurant=r,
            service="POSTMATES",
            address=_address,
            time_accepted=_time,
            wait_time=_wait,
            distance=_distance,
            base_earning=_base,
            tip=_tip
        )

        d.save()
        
    return render(request, "add.html", {"message": message})

def jresp(requrest):
    
    jsonObject = {
        "foo": "bar",
        "1": 2
    }

    return JsonResponse(jsonObject)