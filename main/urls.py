from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jsontest$', views.jresp, name="jresp"),
    url(r'^add$', views.add_delivery, name='add')
]