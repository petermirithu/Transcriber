from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url("^$",views.home,name="home"),
    url("^file_upload$",views.file_upload,name="file_upload"),
    url('^convert$',views.converter,name="converter"),        
]
