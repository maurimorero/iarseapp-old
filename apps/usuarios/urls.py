"""iarseapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from views import RegistroUsuario,UserHome, UserHomeErr, update_profile, Creditos, Creditos1, Simulador1,Simulador2,Simulador3,Simulador4,Simulador5,Simulador6,Simulador7, Metodologia,Metodologia1,Condiciones
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^registrar/', RegistroUsuario.as_view(), name="registrar"),
    url(r'^registrar/', RegistroUsuario, name="registrar"),
    url(r'^creditos/', Creditos, name="creditos"),
    url(r'^creditos1/', Creditos1, name="creditos1"),
    url(r'^$', login_required(UserHome), name="usuarios_home"),
    url(r'^(?P<errorMsg>\d+)/$', login_required(UserHomeErr), name="usuarios_home_err"),
    url(r'^misdatos/', login_required(update_profile), name="usuarios_datos"),
    url(r'^simulador/1/', Simulador1, name="simulador1"),
    url(r'^simulador/2/', Simulador2, name="simulador2"),
    url(r'^simulador/3/', Simulador3, name="simulador3"),
    url(r'^simulador/4/', Simulador4, name="simulador4"),
    url(r'^simulador/5/', Simulador5, name="simulador5"),
    url(r'^simulador/6/', Simulador6, name="simulador6"),
    url(r'^simulador/7/', Simulador7, name="simulador7"),
    url(r'^metodologia/', Metodologia, name="metodologia"),
    url(r'^metodologia1/', login_required(Metodologia1), name="metodologia1"),
    url(r'^condiciones/', Condiciones, name="condiciones"),
    ]
