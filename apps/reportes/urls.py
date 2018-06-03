from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from views import Prueba

urlpatterns = [
    url(r'^prueba', login_required(Prueba),name= "prueba"),
]