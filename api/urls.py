from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rides', views.rides, name='rides'),
    url(r'^get_monthly_deliveries/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.monthly_deliveries, name='monthly_deliveries')
]