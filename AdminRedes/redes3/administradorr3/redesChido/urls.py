from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [

    url('', views.HomeView.as_view(), name='home'),
]
