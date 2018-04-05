from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile$', views.profile, name='profile'),
    url(r'^create$', views.create, name='create'),
    url(r'^login', views.login, name='login')
]