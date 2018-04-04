from django.http import HttpResponse, JsonResponse

from stravalib.client import Client
from stravalib import model

from accounts.models import AuthUser

from pprint import pprint
from datetime import timedelta, datetime

import json

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

class JsonAthlete(object):
    pass

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
        pprint(detailed_activity.id)
        rtn_activity_list.append(_new_activity.toJson())
 
    pprint(rtn_activity_list)
    
    rtn = {
        "user_auth": True,
        "activities": rtn_activity_list
    }

    return JsonResponse(rtn)
