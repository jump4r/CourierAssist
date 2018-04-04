from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rides', views.rides, name='rides')
]