from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url("^$",views.home,name="home"),
]