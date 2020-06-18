from django.conf.urls import url
from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    url("^$",views.home,name="home"),
    url("^convert$",views.converter,name="convert"),
    url("^file_upload$",views.file_upload,name="file_upload"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)