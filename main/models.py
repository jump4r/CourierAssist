from django.db import models

from restaurants.models import Restaurant
# Create your models here.

class Delivery(models.Model):
    user_id = models.IntegerField()

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    service = models.CharField(max_length=20) # Postmates, UberEats, DoorDash, etc...

    time_accepted = models.DateTimeField()
    address = models.CharField(max_length=100, blank=True) # Not Required
    wait_time = models.FloatField()
    distance = models.FloatField()

    base_earning = models.FloatField()
    tip = models.FloatField()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)