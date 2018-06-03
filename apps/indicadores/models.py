from __future__ import unicode_literals
from django.db import models
from ..usuarios.models import Provincia
from ..survey.models import ResponseMgr
from django.contrib.auth.models import User

class TipoIndicador(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True,default=None)

	def __str__(self):
		return (self.name)

class Evaluacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    ubicacion = models.ForeignKey(Provincia)
    rspMgr = models.ForeignKey(ResponseMgr)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return (str(self.fecha))

class Indicador(models.Model):
    name = models.CharField(max_length=400)
    orden = models.IntegerField(null=True, default=1)
    tipo = models.ForeignKey(TipoIndicador)

    def __str__(self):
        return (self.name)

class Nota (models.Model):
    nota = models.FloatField()
    orden = models.IntegerField(null=True, default=1)
    indicador = models.ForeignKey(Indicador)
    evaluacion = models.ForeignKey(Evaluacion)

    def __str__(self):
        #return (str(self.nota)+" - "+self.indicador.name)
        return (str("%0.2f" % self.nota))
