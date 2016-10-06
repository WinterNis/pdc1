from django.conf.urls import include,url
from django.conf import settings
from . import views

urlpatterns = [
        url(r'^$', views.search),
        url(r'^search$', views.search),
        url(r'^generate$', views.generate),
    ]
