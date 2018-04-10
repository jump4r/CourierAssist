from django.http import HttpResponse, JsonResponse

from stravalib.client import Client
from stravalib import model

from accounts.models import AuthUser
from main.models import Delivery
from . import dates

from pprint import pprint
from datetime import timedelta, datetime

import json
from pprint import pprint

EPOCH = datetime(1970, 1, 1)

class JsonActivity(object):
    def __init__(self, id, polyline, total_distance, start_time):
        self.id = id
        self.polyline = polyline
        self.total_distance = total_distance
        self.start_time = self.timeDifference(start_time) # This makes the start time timezone naive...

        pprint(self.start_time)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def timeDifference(self, t):
        return (t.replace(tzinfo=None) - datetime(1970, 1, 1)).total_seconds()

"""
class JsonDeliviery(object):
    def __init__(self, restaurant, service, time, address, wait, distance, base, tip):
        self.restaurant = restaurant
        self.service = service
        self.time = time
        self.address = address
        self.distance = distance
        self.wait = wait
        self.base = base
        self.tip = tip

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
"""

# Create your views here.
# Requests a list of all rides from Strava API
# Returns a JSON File of the rides, or none if the user is not authenticated
def rides(request):

    if (not request.user.is_authenticated):
        return JsonResponse({"user_auth": False})

    client = Client()
    user = AuthUser.objects.get(user_id=request.user.id)
    client.access_token = user.auth_code

    _before = datetime.now()
    _after = datetime(2018, 4, 1)

    batched_activities = client.get_activities(before=_before, after=_after)
    list_activities = list(batched_activities)
    rtn_activity_list = []

    for a in list_activities:
        detailed_activity = client.get_activity(a.id)
        _new_activity = JsonActivity(detailed_activity.id, detailed_activity.map.polyline, a.distance, a.start_date)
        rtn_activity_list.append(_new_activity.toJson())
    
    rtn = {
        "user_auth": True,
        "activities": rtn_activity_list
    }

    return JsonResponse(rtn)

# Get the user activites for 
def monthly_deliveries(request, year, month):

    _year = int(year)
    _month = int(month) - 1

    pprint(_month)
    
    if (not request.user.is_authenticated):
        return JsonResponse({"user_auth": False})

    numDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    pprint(numDays[4])

    _before = datetime(_year, _month + 1, numDays[_month])
    _after = datetime(_year, _month + 1, 1)

    all_user_deliveries = Delivery.objects.all().filter(user_id=request.user.id).values()

    for d in list(all_user_deliveries):
        pprint(d["time_accepted"])

    rtn_activity_list = []

    rtn = {
        "user_auth": True,
        "deliveries": list(all_user_deliveries)
    }

    return JsonResponse(rtn)
    
    

