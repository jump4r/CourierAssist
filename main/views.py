from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from stravalib.client import Client
from stravalib import model

from pprint import pprint
import datetime

from CourierAssist import config_vars
from accounts.models import AuthUser

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

        """
        before = datetime.datetime(2018, 3, 28)
        after = datetime.datetime(2018, 3, 29)
        activities = client.get_activities(limit=1)
        f_activity = list(activities)[0]
        """

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


def jresp(requrest):
    
    jsonObject = {
        "foo": "bar",
        "1": 2
    }

    return JsonResponse(jsonObject)