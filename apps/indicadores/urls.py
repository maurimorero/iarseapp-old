from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from views import Resultados, Respuestas, ResultadosComp,ConsultaConsolidada,ResultadosConsolidados, Graficos, GraficosComp, Indicadores

urlpatterns = [
    url(r'^resultados/(?P<id>\d+)/$', login_required(Resultados), name='resultados'),
    url(r'^resultadoscomp/(?P<id>\d+)/$', login_required(ResultadosComp), name='resultadoscomp'),
    url(r'^respuestas/(?P<id>\d+)/$', login_required(Respuestas), name='respuestas'),
    url(r'^consultaconsolidada/$', login_required(ConsultaConsolidada), name='consultaconsolidada'),
    url(r'^resultadosconsolidados/$', login_required(ResultadosConsolidados), name='resultadosconsolidados'),
    url(r'^graficos/(?P<id>\d+)/$', Graficos, name='graficos'),
    url(r'^graficoscomp/(?P<id>\d+)/$', GraficosComp, name='graficoscomp'),
    url(r'^indicadores/(?P<id>\d+)/$', login_required(Indicadores), name='indicadores'),
]