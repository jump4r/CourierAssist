from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    total_deliveries = models.IntegerField(default=1)
    total_earnings = models.FloatField()
    total_tips = models.IntegerField(default=0)
    total_tip_amount = models.FloatField()

    def __str__(self):
        return self.name