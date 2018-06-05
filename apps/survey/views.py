# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
from django.conf import settings
from models import ResponseMgr, Response
from forms import ResponseMgrForm
from django.urls import reverse_lazy
from models import Question, Survey, Category,Dimension,Encuesta, AnswerRadio,AnswerBase
from forms import ResponseForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from ..indicadores.models import Evaluacion,Nota,Indicador, TipoIndicador
from ..usuarios.models import Provincia,Profile


def GetNextSlide(subtema):
	if (subtema.dimension.encuesta.name == 'Nivel Comprensivo'):
		if (subtema.name == 'Visión y estrategia'):
			return 1
		elif (subtema.name == 'Autoregulación de la conducta'):
			return 1
		elif (subtema.name == 'Relaciones transparentes con la sociedad'):
			return 1
		elif (subtema.name == 'Integración de la RS&S a la estrategia del negocio'):
			return 1
		elif (subtema.name == 'Sistema de gestión de la responsabilidad social y sustentabilidad'):
			return 2
		elif (subtema.name == 'Trabajo decente'):
			return 2
		elif (subtema.name == 'Salud y seguridad en el trabajo y calidad de vida'):
			return 2
		elif (subtema.name == 'Derechos humanos y respeto al individuo'):
			return 3
		elif (subtema.name == 'Buenas prácticas agropecuarias orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Buenas prácticas ganaderas orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Gerenciamiento del impacto ambiental (1/2)'):
			return 3
		elif (subtema.name == 'Gerenciamiento del impacto ambiental (2/2)'):
			return 4
		elif (subtema.name == 'Selección, evaluación y alianza con proveedores'):
			return 4
		elif (subtema.name == 'Desarrollo de las economías locales'):
			return 5
		elif (subtema.name == 'Trato justo y transparencia'):
			return 5
		elif (subtema.name == 'Salud y seguridad del consumidor'):
			return 6
		elif (subtema.name == 'Impacto económico indirecto'):
			return 6
		elif (subtema.name == 'Relaciones con la comunidad local'):
			return 7
		elif (subtema.name == 'Construcción de ciudadanía'):
			return 7
		elif (subtema.name == 'Relaciones éticas con la sociedad'):
			return 7

	elif (subtema.dimension.encuesta.name == 'Nivel Amplio'):
		if (subtema.name == 'Visión y estrategia'):
			return 1
		elif (subtema.name == 'Autoregulación de la conducta'):
			return 1
		elif (subtema.name == 'Relaciones transparentes con la sociedad'):
			return 1
		elif (subtema.name == 'Integración de la RS&S a la estrategia del negocio'):
			return 1
		elif (subtema.name == 'Sistema de gestión de la responsabilidad social y sustentabilidad'):
			return 2
		elif (subtema.name == 'Trabajo decente'):
			return 2
		elif (subtema.name == 'Salud y seguridad en el trabajo y calidad de vida'):
			return 2
		elif (subtema.name == 'Derechos humanos y respeto al individuo'):
			return 3
		elif (subtema.name == 'Buenas prácticas agropecuarias orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Buenas prácticas ganaderas orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Gerenciamiento del impacto ambiental (1/2)'):
			return 3
		elif (subtema.name == 'Gerenciamiento del impacto ambiental (2/2)'):
			return 4
		elif (subtema.name == 'Salud y seguridad del consumidor'):
			return 5
		elif (subtema.name == 'Relaciones con la comunidad local'):
			return 6
		elif (subtema.name == 'Relaciones éticas con la sociedad'):
			return 6
	elif (subtema.dimension.encuesta.name == 'Nivel Básico'):
		if (subtema.name == 'Visión y estrategia'):
			return 1
		elif (subtema.name == 'Relaciones transparentes con la sociedad'):
			return 1
		elif (subtema.name == 'Integración de la RS&S a la estrategia del negocio'):
			return 2
		elif (subtema.name == 'Trabajo decente'):
			return 2
		elif (subtema.name == 'Salud y seguridad en el trabajo y calidad de vida'):
			return 2
		elif (subtema.name == 'Derechos humanos y respeto al individuo'):
			return 3
		elif (subtema.name == 'Buenas prácticas agropecuarias orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Buenas prácticas ganaderas orientadas a la sustentabilidad'):
			return 3
		elif (subtema.name == 'Gerenciamiento del impacto ambiental'):
			return 4
		elif (subtema.name == 'Salud y seguridad del consumidor'):
			return 4

	return 1

def Index(request):
	return render(request, 'index.html')

def SurveyDetail(request, idr, ids):
	##import ipdb;ipdb.set_trace()
	survey = Survey.objects.get(id=ids)
	responseMgr = ResponseMgr.objects.get(id=idr)
	category_items = Category.objects.filter(survey=survey)
	categories = [c for c in category_items]
	usuario=request.user
	#print 'categories for this survey:'
	#print categories
	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey,user=usuario,responseMgr=responseMgr)
		if form.is_valid():
			response = form.save()
			return redirect('surveys:encuesta_view',id=idr,errorMsg=0,slide=GetNextSlide(survey))
	else:
		form = ResponseForm(survey=survey,user=usuario, responseMgr=responseMgr	)

		#Calculo de porcentaje
		#responseMgr= ResponseMgr.objects.get(id=id)

		responAux= Response.objects.filter(respMgr=responseMgr) #Levanto las respuestas asociadas al RspMgr

		subtemasCompletados=[]

		for res in responAux:
			subtemasCompletados.append(res.survey)

		encuesta= Encuesta.objects.get(id=responseMgr.encuesta.id)

		subtemas=[]

		dimensiones= Dimension.objects.filter(encuesta=encuesta)

		for indx, dim in enumerate(dimensiones):
			sub = Survey.objects.filter(dimension=dim).order_by('orden')
			for s in sub:
				subtemas.append(s)

		for s in subtemas:
			for sc in subtemasCompletados:
				if s==sc:
					s.completada=True

		#calcula cuanto se ha completado y la imagen que corresponde
		porcentaje=((float(len(subtemasCompletados))) / (float(len(subtemas))))*100
		imagen=0

		if(porcentaje > 0 and porcentaje < 10):
			imagen=1
		if (porcentaje >= 10 and porcentaje < 20):
			imagen = 1
		if (porcentaje >= 20 and porcentaje < 30):
			imagen = 2
		if (porcentaje >= 30 and porcentaje < 40):
			imagen = 3
		if (porcentaje >= 40 and porcentaje < 50):
			imagen = 4
		if (porcentaje >= 50 and porcentaje < 60):
			imagen = 5
		if (porcentaje >= 60 and porcentaje < 70):
			imagen = 6
		if (porcentaje >= 70 and porcentaje < 80):
			imagen = 7
		if (porcentaje >= 80 and porcentaje < 90):
			imagen = 8
		if (porcentaje >= 90 and porcentaje < 100):
			imagen = 9
		if (porcentaje >= 100):
			imagen = 10
		# TODO sort by category

		#carga los temas de la dimension
		subtemasDimension = Survey.objects.filter(dimension=survey.dimension)
		tabs=(len(categories)-1)

	return render(request, 'survey.html', {'response_form': form,
										   'survey': survey,
										   'categories': categories,
										   'id_resp_mgr':idr,
										   'porcentaje':porcentaje,
										   'imagen':imagen,
										   'subtemasDimension':subtemasDimension,
										   'encuesta':encuesta,
										   'tabs':tabs})

def Confirm(request, uuid):
	email = "iarse.it.dep@gmail.com"
	return render(request, 'confirm.html', {'uuid':uuid, "email": email})

def privacy(request):
	return render(request, 'privacy.html')

def EncuestaIndexView(request, id, errorMsg,slide):
	# chequea si el usuario esta habilitado
	perfil = Profile.objects.get(user=request.user)
	if (perfil.habilitado == False):
		return redirect('usuarios:usuarios_home_err', 3)
	# Chequea si hay alguna encuesta en los ultimos 6 meses
	rsMgrCheckList = ResponseMgr.objects.filter(user=request.user, completada=True).order_by('-id')
	if (rsMgrCheckList):
		rsMgrCheck = rsMgrCheckList[0]
		now = timezone.now()
		diferencia = ((now - rsMgrCheck.created).days)
		if (diferencia <= 180):
			return redirect('usuarios:usuarios_home_err', 1)
	responseMgr= ResponseMgr.objects.get(id=id)
	#import ipdb;ipdb.set_trace()
	responseMgr.user=request.user
	responAux= Response.objects.filter(respMgr=responseMgr) #Levanto las respuestas asociadas al RspMgr

	subtemasCompletados=[]

	for res in responAux:
		subtemasCompletados.append(res.survey)

	encuesta= Encuesta.objects.get(id=responseMgr.encuesta.id)

	subtemas=[]

	dimensiones= Dimension.objects.filter(encuesta=encuesta)

	for indx, dim in enumerate(dimensiones):
		sub = Survey.objects.filter(dimension=dim).order_by('orden')
		for s in sub:
			subtemas.append(s)

	for s in subtemas:
		for sc in subtemasCompletados:
			if s==sc:
				s.completada=True

	#calcula cuanto se ha completado y la imagen que corresponde
	porcentaje=((float(len(subtemasCompletados))) / (float(len(subtemas))))*100
	imagen=0

	if(porcentaje > 0 and porcentaje < 10):
		imagen=1
	if (porcentaje >= 10 and porcentaje < 20):
		imagen = 1
	if (porcentaje >= 20 and porcentaje < 30):
		imagen = 2
	if (porcentaje >= 30 and porcentaje < 40):
		imagen = 3
	if (porcentaje >= 40 and porcentaje < 50):
		imagen = 4
	if (porcentaje >= 50 and porcentaje < 60):
		imagen = 5
	if (porcentaje >= 60 and porcentaje < 70):
		imagen = 6
	if (porcentaje >= 70 and porcentaje < 80):
		imagen = 7
	if (porcentaje >= 80 and porcentaje < 90):
		imagen = 8
	if (porcentaje >= 90 and porcentaje < 100):
		imagen = 9
	if (porcentaje >= 100):
		imagen = 10
	#print(porcentaje)
	#print(imagen)

	#responseMgrForm = ResponseMgrForm()
	if request.method == 'POST':
		responseMgrForm = ResponseMgrForm(request.POST, instance=responseMgr)
		if responseMgrForm.is_valid():
			responseMgr = responseMgrForm.save()
			return redirect('surveys:encuesta_view', id=responseMgr.id, errorMsg=0,slide=1)
	else:
		responseMgrForm = ResponseMgrForm(instance=responseMgr)

	contexto={
		'dimensiones':dimensiones,
		'subtemas':subtemas,
		'encuesta':encuesta.name,
		'responseMgrForm':responseMgrForm,
		'responseMgr':responseMgr,
		'errorMsg':errorMsg,
		'porcentaje':porcentaje,
		'imagen':imagen,
		'slide':slide
		}
	return render(request, 'encuestaIndex.html', contexto)

def EncuestaIndex(request, id):
	#chequea si el usuario esta habilitado
	perfil= Profile.objects.get(user=request.user)
	if(perfil.habilitado==False):
		return redirect('usuarios:usuarios_home_err', 3)
	#Chequea si hay alguna ecuensta en los ultimos 6 meses
	rsMgrCheckList= ResponseMgr.objects.filter(user=request.user,completada=True).order_by('-id')
	if(rsMgrCheckList):
		rsMgrCheck=rsMgrCheckList[0]
		now = timezone.now()
		diferencia= ((now - rsMgrCheck.created).days)
		if (diferencia <= 180):
			return redirect('usuarios:usuarios_home_err',1)
	# Chequea si hay alguna ecuensta pendiente
	rsMgrCheckListPen = ResponseMgr.objects.filter(user=request.user, completada=False)
	if (rsMgrCheckListPen):
		return redirect('usuarios:usuarios_home_err', 2)
	encuesta= Encuesta.objects.get(id=id)

	subtemas = []

	dimensiones = Dimension.objects.filter(encuesta=encuesta)

	for indx, dim in enumerate(dimensiones):
		sub = Survey.objects.filter(dimension=dim).order_by('orden')
		for s in sub:
			subtemas.append(s)

	#responseMgrForm = ResponseMgrForm()
	if request.method == 'POST':
		responseMgrForm = ResponseMgrForm(request.POST)
		if responseMgrForm.is_valid():
			responseMgr = responseMgrForm.save()
			responseMgr.encuesta=encuesta
			responseMgr.user=request.user
			responseMgr.save()
			return redirect('surveys:encuesta_view',id=responseMgr.id,errorMsg=0,slide=1)
	else:
		responseMgrForm = ResponseMgrForm()
		responseMgr= ResponseMgr()
		responseMgr.id=0

	contexto={
		'dimensiones':dimensiones,
		'subtemas':subtemas,
		'encuesta':encuesta.name,
		'responseMgrForm':responseMgrForm,
		'responseMgr':responseMgr,
		'porcentaje':0,
		'imagen':0
		}
	return render(request, 'encuestaIndex.html', contexto)

def SubtemaView(request,idr,ids):
	return redirect('surveys:survey_detail', idr,ids)

def ResponseDelete(request,id):
    responseMrg= ResponseMgr.objects.get(id=id)
    responseMrg.delete()
    return redirect('usuarios:usuarios_home')

def EncuestaTerminar(request, id):
  responseMgr = ResponseMgr.objects.get(id=id)
  responAux = Response.objects.filter(respMgr=responseMgr)  # Levanto las respuestas asociadas al RspMgr

  cantOk = len(responAux)

  encuesta = Encuesta.objects.get(id=responseMgr.encuesta.id)

  subtemas = []
  dimensiones = Dimension.objects.filter(encuesta=encuesta)
  for indx, dim in enumerate(dimensiones):
     sub = Survey.objects.filter(dimension=dim)
     for s in sub:
        subtemas.append(s)
  cantTot = len(subtemas)
  print "Cantidad Total=" + str(cantTot)
  print "Cantidad Completados=" + str(cantOk)

  if (cantTot <= cantOk):
     responseMgr.completada = True
     responseMgr.save()
     # return redirect('usuarios:usuarios_home')
     return GeneraIndicadores(request, responseMgr)
  else:
     return EncuestaIndexView(request, responseMgr.id, 1,1)

def GeneraIndicadores(request, responseMgr ):
	if	(responseMgr.encuesta.id==1):
		return IndicadoresComp(request,responseMgr)
	if (responseMgr.encuesta.id == 2):
		return IndicadoresBasica(request,responseMgr)
	if (responseMgr.encuesta.id == 3):
		return IndicadoresAmplia (request,responseMgr)


def IndicadoresComp(request,responseMgr):
	#creo la evaluacion
	evaluacion= Evaluacion()
	evaluacion.rspMgr=responseMgr
	evaluacion.usuario=responseMgr.user
	profile= Profile.objects.get(user=responseMgr.user)
	evaluacion.ubicacion=profile.provincia
	evaluacion.save()
	
	estadio1 = 0
	estadio2 = 0
	estadio3 = 0
	estadio4 = 0
	#Levanto los responses (uno para cada subtema)
	responses = Response.objects.filter(respMgr=responseMgr)

	#Aca se van a almacenar todas las respuestas (para no tene que levantarlas para cada indicador
	todasRespuestas = []

	#Indicador 1
	#Levanto las respuestas del indicador
	respuestas = []
	categoria = Category.objects.get(id=1)
	indicador= Indicador.objects.get(id=1)
	for indx, res in enumerate(responses):
		resps = AnswerRadio.objects.filter(response=res)
		for r in resps:
			#print r.question.category
			#print r.body
			todasRespuestas.append(r)
			if(r.question.category==categoria):
				respuestas.append(r)
				if(r.question.id==168):
					if(r.body=='Si'):
						aplica = True
					if (r.body == 'No'):
						aplica = False
				if (r.question.id == 167):
					estadio=r.body[8]
	cuentaSi=0
	if(aplica): #si selecciono que el indicador aplica
		for r in respuestas:
			if(r.body=='Si'):
				cuentaSi=cuentaSi+1
		cuentaSi=cuentaSi-1 #Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total=len(respuestas)-2 #Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0/total) * cuentaSi) #Calcula la parte de la nota que corresponde a las binarias
		notaInd=notaBinarias

		#Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota=Nota()
		nota.evaluacion=evaluacion
		nota.indicador=indicador
		nota.orden=indicador.orden
		nota.nota=notaInd
		nota.save()


		#Indicador 2
	respuestas = []
	categoria = Category.objects.get(id=7)
	indicador = Indicador.objects.get(id=2)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 27):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 26):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias

		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 3
	respuestas = []
	categoria = Category.objects.get(id=8)
	indicador = Indicador.objects.get(id=3)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 29):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 17):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
			# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 4 (Practicas de buen gobierno)
	respuestas = []
	categoria = Category.objects.get(id=9)
	indicador = Indicador.objects.get(id=4)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 53):
					if (r.body == 'Si'):
						aplica = True
					if (r.body == 'No'):
						aplica = False
			if (r.question.id == 52):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 5 (Dialogo y partici ..)
	respuestas = []
	categoria = Category.objects.get(id=10)
	indicador = Indicador.objects.get(id=5)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 69):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 68):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
		(6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 6 (Relaciones con invesoers y ..)
	respuestas = []
	categoria = Category.objects.get(id=11)
	indicador = Indicador.objects.get(id=6)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 84):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 83):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
	# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 7 (Memoria de resp social ..)
	respuestas = []
	categoria = Category.objects.get(id=12)
	indicador = Indicador.objects.get(id=7)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 100):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 99):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 8 (Relaciones con la competencia ..)
	respuestas = []
	categoria = Category.objects.get(id=13)
	indicador = Indicador.objects.get(id=8)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 119):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 118):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = ((6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 9 (Practicas anti corrup y anti coima ..)
	respuestas = []
	categoria = Category.objects.get(id=14)
	indicador = Indicador.objects.get(id=9)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 138):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 137):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 10 (Contribuciones para campa ..)
	respuestas = []
	categoria = Category.objects.get(id=15)
	indicador = Indicador.objects.get(id=10)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 152):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 151):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 11 (Compromisos voluntarios y..)
	respuestas = []
	categoria = Category.objects.get(id=16)
	indicador = Indicador.objects.get(id=11)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 181):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 180):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
					(
					6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 12 (Sistema de gestion de la re..)
	respuestas = []
	categoria = Category.objects.get(id=17)
	indicador = Indicador.objects.get(id=12)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 196):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 195):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 13 (Relaciones con trb pr..)
	respuestas = []
	categoria = Category.objects.get(id=18)
	indicador = Indicador.objects.get(id=13)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 212):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 211):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 14 (Relaciones con trb terce..)
		respuestas = []
		categoria = Category.objects.get(id=19)
		indicador = Indicador.objects.get(id=14)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 228):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 227):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 15 (politica de remun..)
	respuestas = []
	categoria = Category.objects.get(id=20)
	indicador = Indicador.objects.get(id=15)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 246):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 245):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 16 (Compromiso con el desarrollo p..)
	respuestas = []
	categoria = Category.objects.get(id=21)
	indicador = Indicador.objects.get(id=16)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 264):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 263):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 17 (Conducta frente a desvinculaciones..)
	respuestas = []
	categoria = Category.objects.get(id=22)
	indicador = Indicador.objects.get(id=17)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 281):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 280):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 18 (Cuidados de salud, seg..)
	respuestas = []
	categoria = Category.objects.get(id=23)
	indicador = Indicador.objects.get(id=18)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 303):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 302):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 19 (Seguridad en el uso y opera..)
	respuestas = []
	categoria = Category.objects.get(id=24)
	indicador = Indicador.objects.get(id=19)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 318):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 317):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()
	# Indicador 20 (Condiciones de trabajo, calidad..)
	respuestas = []
	categoria = Category.objects.get(id=25)
	indicador = Indicador.objects.get(id=20)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 339):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 338):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

		# Indicador 21 (Relaciones con sindicatos..)
		respuestas = []
		categoria = Category.objects.get(id=26)
		indicador = Indicador.objects.get(id=21)
		for r in todasRespuestas:
			# print r.question.category
			# print r.body
			if (r.question.category == categoria):
				respuestas.append(r)
				if (r.question.id == 353):
					if (r.body == 'Si'):
						aplica = True
					if (r.body == 'No'):
						aplica = False
				if (r.question.id == 352):
					estadio = r.body[8]
		cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 22 (Compromiso con el futuro de los ni..)
	respuestas = []
	categoria = Category.objects.get(id=27)
	indicador = Indicador.objects.get(id=22)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 371):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 370):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 23 (Compromiso con el desarrollo infantil..)
	respuestas = []
	categoria = Category.objects.get(id=28)
	indicador = Indicador.objects.get(id=23)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 385):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 384):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 24 (Valoracion de la diversidad y ..)
	respuestas = []
	categoria = Category.objects.get(id=29)
	indicador = Indicador.objects.get(id=24)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 411):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 410):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 25 (Compromiso con la equidad ..)
	respuestas = []
	categoria = Category.objects.get(id=30)
	indicador = Indicador.objects.get(id=25)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 426):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 425):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 26 (Compromiso con la promocion de la equidad ..)
	respuestas = []
	categoria = Category.objects.get(id=31)
	indicador = Indicador.objects.get(id=26)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 442):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 441):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 27 (Uso sustentable de los recursos: suelo ..)
	respuestas = []
	categoria = Category.objects.get(id=32)
	indicador = Indicador.objects.get(id=27)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 461):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 460):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 28 (Uso sustentable de instumos: semillas ..)
	respuestas = []
	categoria = Category.objects.get(id=33)
	indicador = Indicador.objects.get(id=28)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 478):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 477):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 29 (Uso sustentable y seguro de instumos..)
	respuestas = []
	categoria = Category.objects.get(id=34)
	indicador = Indicador.objects.get(id=29)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 506):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 505):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 30 (Bienestar animal..)
	respuestas = []
	categoria = Category.objects.get(id=102)
	indicador = Indicador.objects.get(id=30)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1687):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1686):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 31 (Acciones relacionadas al cambio climatico..)
	respuestas = []
	categoria = Category.objects.get(id=36)
	indicador = Indicador.objects.get(id=31)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 542):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 541):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 32 (Adapctacion al cambio climatico..)
	respuestas = []
	categoria = Category.objects.get(id=37)
	indicador = Indicador.objects.get(id=32)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 559):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 558):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 33 (Sistema de gestion ambiental..)
	respuestas = []
	categoria = Category.objects.get(id=38)
	indicador = Indicador.objects.get(id=33)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 580):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 579):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 34 (Sustentabilidad de materiales e insumos..)
	respuestas = []
	categoria = Category.objects.get(id=39)
	indicador = Indicador.objects.get(id=34)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 593):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 592):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 35 (Uso sustentable del agua..)
	respuestas = []
	categoria = Category.objects.get(id=40)
	indicador = Indicador.objects.get(id=35)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 612):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 611):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 36 (Uso sustentable de la enegia..)
	respuestas = []
	categoria = Category.objects.get(id=41)
	indicador = Indicador.objects.get(id=36)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 631):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 630):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
			for r in respuestas:
				if (r.body == 'Si'):
					cuentaSi = cuentaSi + 1
			cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
			total = len(
				respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
			notaBinarias = (
				(
					6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
			notaInd = notaBinarias
			# Le sumo la parte correspondiente al estadio
			if (estadio == '1'):
				notaInd= notaInd + 1
				estadio1=estadio1+1
			if (estadio == '2'):
				notaInd = notaInd + 2
				estadio2 = estadio2 + 1
			if (estadio == '3'):
				notaInd = notaInd + 3
				estadio3 = estadio3 + 1
			if (estadio == '4'):
				notaInd = notaInd + 4
				estadio4 = estadio4 + 1
			nota = Nota()
			nota.evaluacion = evaluacion
			nota.indicador = indicador
			nota.orden = indicador.orden
			nota.nota = notaInd
			nota.save()

	# Indicador 37 (Prevension de la contaminacion..)
	respuestas = []
	categoria = Category.objects.get(id=42)
	indicador = Indicador.objects.get(id=37)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 650):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 649):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 38 (Uso sustentable de la bio..)
	respuestas = []
	categoria = Category.objects.get(id=43)
	indicador = Indicador.objects.get(id=38)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 667):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 666):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 39 (Uso sustentable de la bio..)
	respuestas = []
	categoria = Category.objects.get(id=44)
	indicador = Indicador.objects.get(id=39)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 682):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 681):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 40 (Impacto del transporte, logistica..)
	respuestas = []
	categoria = Category.objects.get(id=45)
	indicador = Indicador.objects.get(id=40)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 704):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 703):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 41 (Criterio de seleccion y evaluacion..)
	respuestas = []
	categoria = Category.objects.get(id=46)
	indicador = Indicador.objects.get(id=41)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 722):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 721):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 42 (Lucha contra el trabajo infantil..)
	respuestas = []
	categoria = Category.objects.get(id=47)
	indicador = Indicador.objects.get(id=42)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 736):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 735):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 43 (Apoyo al desarrollo de proveedores..)
	respuestas = []
	categoria = Category.objects.get(id=48)
	indicador = Indicador.objects.get(id=43)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 750):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 749):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 44 (Calidad de las relaciones con clientes..)
	respuestas = []
	categoria = Category.objects.get(id=49)
	indicador = Indicador.objects.get(id=44)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 767):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 766):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 45 (Cuidado de la inocuidad...)
	respuestas = []
	categoria = Category.objects.get(id=50)
	indicador = Indicador.objects.get(id=45)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 784):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 783):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 46 (Gerenciamiento del impacto de la empresa..)
	respuestas = []
	categoria = Category.objects.get(id=51)
	indicador = Indicador.objects.get(id=46)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 804):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 803):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 47 (Compromiso con el desarrollo de la comunicdad..)
	respuestas = []
	categoria = Category.objects.get(id=52)
	indicador = Indicador.objects.get(id=47)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 825):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 824):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 48 (Liderazgo e influencia social..)
	respuestas = []
	categoria = Category.objects.get(id=53)
	indicador = Indicador.objects.get(id=48)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 839):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 838):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 49 (Participacion en el desarrollo de politicas..)
	respuestas = []
	categoria = Category.objects.get(id=54)
	indicador = Indicador.objects.get(id=49)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 855):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 854):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 30 (Salud y Seguridad Animal:Practicas Responsables y Sustentables de Produccion Animal...)
	respuestas = []
	categoria = Category.objects.get(id=35)
	indicador = Indicador.objects.get(id=81)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1673):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1672):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd= notaInd + 1
			estadio1=estadio1+1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	#Calculo de los estadios
	indicador = Indicador.objects.get(id=77)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio1
	nota.save()

	indicador = Indicador.objects.get(id=78)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio2
	nota.save()

	indicador = Indicador.objects.get(id=79)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio3
	nota.save()

	indicador = Indicador.objects.get(id=80)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio4
	nota.save()

	# CALCULO DE INDICADORES DE SUBTEMAS
	# Vision y estrategia
	indicador = Indicador.objects.get(id=50)
	indicadoresRegulares = Nota.objects.filter(evaluacion=evaluacion)
	notaSubtema = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 2):
			notaSubtema = ind.nota
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = notaSubtema
		nota.save()

	# AUTORREGULACION DE LA CONDUCTA
	indicador = Indicador.objects.get(id=51)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 3):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 4):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES TRANSPARENTES CON LA SOCIEDAD
	indicador = Indicador.objects.get(id=52)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 5):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 6):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 7):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 8):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 9):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 10):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# INTEGRACION DE LA RS & SUSTENTABILIDAD A LA ESTRATEGIA DEL NEGOCIO
	indicador = Indicador.objects.get(id=53)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 1):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 11):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SISTEMA INTEGRADO DE GESTION DE LA RS & SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=54)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 12):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# Trabajo decente
	indicador = Indicador.objects.get(id=55)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 13):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 14):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 15):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 16):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 17):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD EN EL TRABAJO Y CALIDAD DE VIDA
	indicador = Indicador.objects.get(id=56)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 18):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 19):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 20):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# DERECHOS HUMANOS Y RESPETO AL INDIVIDUO
	indicador = Indicador.objects.get(id=57)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 21):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 22):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 23):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 24):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 25):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 26):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# BUENAS PRACTICAS AGROPECUARIAS ORIENTADAS A LA SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=58)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 27):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 28):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 29):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# BUENAS PRACTICAS GANADERAS ORIENTADAS A LA SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=59)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 30):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 81):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# GERENCIAMIENTO DEL IMPACTO AMBIENTAL
	indicador = Indicador.objects.get(id=60)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 31):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 32):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 33):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 34):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 35):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 36):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 37):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 38):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 39):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 40):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SELECCION, EVALUACION Y ALIANZA CON PROVEEDORES
	indicador = Indicador.objects.get(id=61)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 41):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 42):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# DESARROLLO DE LAS ECONOMIAS LOCALES
	indicador = Indicador.objects.get(id=62)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 43):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# TRATO JUSTO Y TRANSPARENCIA
	indicador = Indicador.objects.get(id=63)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 44):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD DEL CONSUMIDOR
	indicador = Indicador.objects.get(id=64)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 45):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# IMPACTO ECONOMICO INDIRECTO
	indicador = Indicador.objects.get(id=65)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 46):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES CON LA COMUNIDAD LOCAL
	indicador = Indicador.objects.get(id=66)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 47):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# CONSTRUCCION DE CIUDADANIA
	indicador = Indicador.objects.get(id=67)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 48):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES ETICAS CON LA SOCIEDAD
	indicador = Indicador.objects.get(id=68)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 49):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	#Indicadore de DIMENSIONES
	#tipoIndSubtema= TipoIndicador.objects.get(id=4)
	notas= Nota.objects.filter(evaluacion=evaluacion)

	#DIMENSION VALORES - TRANSPARENCIA Y GESTION
	indicador = Indicador.objects.get(id=69)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 50):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 51):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 52):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 53):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 54):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION PRACTICAS DE EMPLEO Y TRABAJO DIGNO
	indicador = Indicador.objects.get(id=70)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 55):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 56):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 57):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION SUSTENTABILIDAD DE LAS PRACTICAS AGRICOLAS - GANADERAS
	indicador = Indicador.objects.get(id=71)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 58):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 59):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 60):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACION CON PROVEEDORES
	indicador = Indicador.objects.get(id=72)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 61):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 62):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON CLIENTES Y OTROS PRODUCTORES
	indicador = Indicador.objects.get(id=73)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 63):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 64):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON LAS COMUNIDADES LOCALES
	indicador = Indicador.objects.get(id=74)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 65):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 66):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON GOBIERNO Y SOCIEDAD
	indicador = Indicador.objects.get(id=75)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 67):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 68):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#Calcula la nota general
	notas= Nota.objects.filter(evaluacion=evaluacion)
	indicador = Indicador.objects.get(id=76)
	notaGral = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 69):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 70):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 71):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 72):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 73):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 74):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 75):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaGral / cuenta)
		nota.save()

	return redirect('indicadores:resultados',evaluacion.id)


def IndicadoresAmplia(request,responseMgr):
	# creo la evaluacion
	evaluacion = Evaluacion()
	evaluacion.rspMgr = responseMgr
	evaluacion.usuario = responseMgr.user
	profile = Profile.objects.get(user=responseMgr.user)
	evaluacion.ubicacion = profile.provincia
	evaluacion.save()
	estadio1 = 0
	estadio2 = 0
	estadio3 = 0
	estadio4 = 0

	# Levanto los responses (uno para cada subtema)
	responses = Response.objects.filter(respMgr=responseMgr)

	#Aca se van a almacenar todas las respuestas (para no tene que levantarlas para cada indicador
	todasRespuestas = []

	#Levanto las respuestas de la evaluacion
	for indx, res in enumerate(responses):
		resps = AnswerRadio.objects.filter(response=res)
		for r in resps:
			todasRespuestas.append(r)
	# Indicador 1 (Vision - Mision ...)
	respuestas = []
	categoria = Category.objects.get(id=55)
	indicador = Indicador.objects.get(id=2)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 871):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 870):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 2 (Practicas de buen gobierno...)
	respuestas = []
	categoria = Category.objects.get(id=56)
	indicador = Indicador.objects.get(id=4)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 895):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 894):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 3 (Dialogo y participacion de los grupos...)
	respuestas = []
	categoria = Category.objects.get(id=57)
	indicador = Indicador.objects.get(id=5)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 911):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 910):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 4 (Practicas anti corrucion...)
	respuestas = []
	categoria = Category.objects.get(id=58)
	indicador = Indicador.objects.get(id=9)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 930):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 929):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 5 (Mapeo de los impactos...)
	respuestas = []
	categoria = Category.objects.get(id=59)
	indicador = Indicador.objects.get(id=1)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 948):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 947):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 6 (Relaciones con trabajadores propios...)
	respuestas = []
	categoria = Category.objects.get(id=60)
	indicador = Indicador.objects.get(id=13)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 964):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 963):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 7 (Relaciones con trabajadores tecerizados / contratados...)
	respuestas = []
	categoria = Category.objects.get(id=61)
	indicador = Indicador.objects.get(id=14)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 980):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 979):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 8 (Politica de remuneracion...)
	respuestas = []
	categoria = Category.objects.get(id=62)
	indicador = Indicador.objects.get(id=15)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 998):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 997):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 9 (Conducta frente a desvinculaciones...)
	respuestas = []
	categoria = Category.objects.get(id=63)
	indicador = Indicador.objects.get(id=17)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1015):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1014):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 10 (Cuidados de salud, seguridad...)
	respuestas = []
	categoria = Category.objects.get(id=64)
	indicador = Indicador.objects.get(id=18)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1037):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1036):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 11 (Seguridad en el uso y operacion...)
	respuestas = []
	categoria = Category.objects.get(id=65)
	indicador = Indicador.objects.get(id=19)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1052):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1051):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 12 (Condiciones de trabajo, calidad de vida...)
	respuestas = []
	categoria = Category.objects.get(id=66)
	indicador = Indicador.objects.get(id=20)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1073):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1072):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 13 (Compromiso con el futuro de los ni...)
	respuestas = []
	categoria = Category.objects.get(id=67)
	indicador = Indicador.objects.get(id=22)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1091):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1090):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 14 (Compromiso con el desarrollo infantil...)
	respuestas = []
	categoria = Category.objects.get(id=68)
	indicador = Indicador.objects.get(id=23)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1105):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1104):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 15 (Compromiso con equidad y la no disciminacion...)
	respuestas = []
	categoria = Category.objects.get(id=69)
	indicador = Indicador.objects.get(id=25)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1120):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1119):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 16 (Uso sustentable de los recursos:suelo..)
	respuestas = []
	categoria = Category.objects.get(id=70)
	indicador = Indicador.objects.get(id=27)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1139):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1138):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 17 (Uso sustentable de insumos :semillas..)
	respuestas = []
	categoria = Category.objects.get(id=71)
	indicador = Indicador.objects.get(id=28)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1156):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1155):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 18 (Uso sustentable y seguro de insumos..)
	respuestas = []
	categoria = Category.objects.get(id=72)
	indicador = Indicador.objects.get(id=29)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1184):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1183):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 19 (Bienestar animal..)
	respuestas = []
	categoria = Category.objects.get(id=100)
	indicador = Indicador.objects.get(id=30)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1655):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1654):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 20 (Acciones relacionadas al cambio climatico.)
	respuestas = []
	categoria = Category.objects.get(id=74)
	indicador = Indicador.objects.get(id=31)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1220):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1219):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 21 (Sustent de mat e ins.)
	respuestas = []
	categoria = Category.objects.get(id=75)
	indicador = Indicador.objects.get(id=34)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1233):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1232):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 22 (Uso sustentable del agua.)
	respuestas = []
	categoria = Category.objects.get(id=77)
	indicador = Indicador.objects.get(id=33)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1252):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1251):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 23 (Prevencion de la contaminacion)
	respuestas = []
	categoria = Category.objects.get(id=78)
	indicador = Indicador.objects.get(id=37)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1271):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1270):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 24 (Uso sustentable de la bio)
	respuestas = []
	categoria = Category.objects.get(id=79)
	indicador = Indicador.objects.get(id=38)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1288):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1287):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 25 (Uso sustentable de la bio)
	respuestas = []
	categoria = Category.objects.get(id=80)
	indicador = Indicador.objects.get(id=39)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1303):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1302):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 26 (Cuidado de la inocuidad)
	respuestas = []
	categoria = Category.objects.get(id=81)
	indicador = Indicador.objects.get(id=45)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1320):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1319):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 27 (Compromiso con el desarrollo de la comunidad)
	respuestas = []
	categoria = Category.objects.get(id=82)
	indicador = Indicador.objects.get(id=47)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1341):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1340):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 28 (Participacion en el desarrollo de politicas)
	respuestas = []
	categoria = Category.objects.get(id=83)
	indicador = Indicador.objects.get(id=49)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1357):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1356):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 29 (Salud y Seguridad Animal: Practicas Responsables y Sustentables de Produccion Animal.)
	respuestas = []
	categoria = Category.objects.get(id=73)
	indicador = Indicador.objects.get(id=81)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1648):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1647):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 30 (Sistema de Gestion de la RS & Sustentabilidad)
	respuestas = []
	categoria = Category.objects.get(id=101)
	indicador = Indicador.objects.get(id=12)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1670):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1669):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Calculo de los estadios
	indicador = Indicador.objects.get(id=77)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio1
	nota.save()

	indicador = Indicador.objects.get(id=78)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio2
	nota.save()

	indicador = Indicador.objects.get(id=79)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio3
	nota.save()

	indicador = Indicador.objects.get(id=80)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio4
	nota.save()

	# CALCULO DE INDICADORES DE SUBTEMAS
	# Vision y estrategia
	indicador = Indicador.objects.get(id=50)
	indicadoresRegulares = Nota.objects.filter(evaluacion=evaluacion)
	notaSubtema = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 2):
			notaSubtema = ind.nota
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = notaSubtema
		nota.save()

	# AUTORREGULACION DE LA CONDUCTA
	indicador = Indicador.objects.get(id=51)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 4):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES TRANSPARENTES CON LA SOCIEDAD
	indicador = Indicador.objects.get(id=52)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 5):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 9):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SISTEMA INTEGRADO DE GESTION DE LA RS & SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=54)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 12):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# INTEGRACION DE LA RS & SUSTENTABILIDAD A LA ESTRATEGIA DEL NEGOCIO
	indicador = Indicador.objects.get(id=53)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 1):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# Trabajo decente
	indicador = Indicador.objects.get(id=55)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 13):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 14):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 15):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 17):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD EN EL TRABAJO Y CALIDAD DE VIDA
	indicador = Indicador.objects.get(id=56)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 18):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 19):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 20):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# DERECHOS HUMANOS Y RESPETO AL INDIVIDUO
	indicador = Indicador.objects.get(id=57)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 22):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 23):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 25):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# BUENAS PRACTICAS AGROPECUARIAS ORIENTADAS A LA SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=58)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 27):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 28):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 29):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# BUENAS PRACTICAS GANADERAS ORIENTADAS A LA SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=59)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 30):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 81):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# GERENCIAMIENTO DEL IMPACTO AMBIENTAL
	indicador = Indicador.objects.get(id=60)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 31):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 34):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 35):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 37):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 38):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 39):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD DEL CONSUMIDOR
	indicador = Indicador.objects.get(id=64)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 45):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES CON LA COMUNIDAD LOCAL
	indicador = Indicador.objects.get(id=66)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 47):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# RELACIONES ETICAS CON LA SOCIEDAD
	indicador = Indicador.objects.get(id=68)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 49):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	#Indicadores de DIMENSIONES
	#tipoIndSubtema= TipoIndicador.objects.get(id=4)
	notas= Nota.objects.filter(evaluacion=evaluacion)

	#DIMENSION VALORES - TRANSPARENCIA Y GESTION
	indicador = Indicador.objects.get(id=69)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 50):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 51):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 52):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 53):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 54):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION PRACTICAS DE EMPLEO Y TRABAJO DIGNO
	indicador = Indicador.objects.get(id=70)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 55):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 56):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 57):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION SUSTENTABILIDAD DE LAS PRACTICAS AGRICOLAS - GANADERAS
	indicador = Indicador.objects.get(id=71)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 58):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 59):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 60):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON CLIENTES Y OTROS PRODUCTORES
	indicador = Indicador.objects.get(id=73)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 64):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON LAS COMUNIDADES LOCALES
	indicador = Indicador.objects.get(id=74)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 66):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON GOBIERNO Y SOCIEDAD
	indicador = Indicador.objects.get(id=75)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 68):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()


	#Calcula la nota general
	notas= Nota.objects.filter(evaluacion=evaluacion)
	indicador = Indicador.objects.get(id=76)
	notaGral = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 69):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 70):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 71):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 73):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 74):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 75):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaGral / cuenta)
		nota.save()

	return redirect('indicadores:resultados',evaluacion.id)

def IndicadoresBasica(request,responseMgr):

	# creo la evaluacion
	evaluacion = Evaluacion()
	evaluacion.rspMgr = responseMgr
	evaluacion.usuario = responseMgr.user
	profile = Profile.objects.get(user=responseMgr.user)
	evaluacion.ubicacion = profile.provincia
	evaluacion.save()
	estadio1 = 0
	estadio2 = 0
	estadio3 = 0
	estadio4 = 0

	# Levanto los responses (uno para cada subtema)
	responses = Response.objects.filter(respMgr=responseMgr)

	# Aca se van a almacenar todas las respuestas (para no tener que levantarlas para cada indicador
	todasRespuestas = []

	# Levanto las respuestas de la evaluacion
	for indx, res in enumerate(responses):
		resps = AnswerRadio.objects.filter(response=res)
		for r in resps:
			todasRespuestas.append(r)
	# Indicador 1 (Vision - Mision ...)
	respuestas = []
	categoria = Category.objects.get(id=84)
	indicador = Indicador.objects.get(id=2)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1373):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1372):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 2 (Practicas anticorrupcion anticoima...)
	respuestas = []
	categoria = Category.objects.get(id=85)
	indicador = Indicador.objects.get(id=9)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1392):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1391):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 3 (Mapeo de los impactos...)
	respuestas = []
	categoria = Category.objects.get(id=86)
	indicador = Indicador.objects.get(id=1)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1410):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1409):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 4 (Relaciones con trabajadores propios...)
	respuestas = []
	categoria = Category.objects.get(id=87)
	indicador = Indicador.objects.get(id=13)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1426):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1425):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 5 (Relaciones con trabajadores tercerizados...)
	respuestas = []
	categoria = Category.objects.get(id=88)
	indicador = Indicador.objects.get(id=14)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1442):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1441):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 6 (Politica de remuneraciones...)
	respuestas = []
	categoria = Category.objects.get(id=89)
	indicador = Indicador.objects.get(id=15)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1460):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1459):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 7 (Cuidados de salud, seguridad...)
	respuestas = []
	categoria = Category.objects.get(id=90)
	indicador = Indicador.objects.get(id=18)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1481):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1480):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 8 (Condi de tabajo...)
	respuestas = []
	categoria = Category.objects.get(id=91)
	indicador = Indicador.objects.get(id=20)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1502):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1501):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 9 (Compromiso con el futuro de los ni...)
	respuestas = []
	categoria = Category.objects.get(id=92)
	indicador = Indicador.objects.get(id=22)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1520):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1519):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 10 (Compromiso con la equidad y la no discriminacion...)
	respuestas = []
	categoria = Category.objects.get(id=93)
	indicador = Indicador.objects.get(id=25)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1535):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1534):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 11 (Uso sustentable de los recursos: suelo...)
	respuestas = []
	categoria = Category.objects.get(id=94)
	indicador = Indicador.objects.get(id=27)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1554):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1553):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 12 (Uso sustentable y seguro de insumos...)
	respuestas = []
	categoria = Category.objects.get(id=95)
	indicador = Indicador.objects.get(id=29)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1582):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1581):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 13 (Uso sustentable de la biodiversidad : Bosques nativos..)
	respuestas = []
	categoria = Category.objects.get(id=97)
	indicador = Indicador.objects.get(id=39)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1597):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1596):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 14 (Cuidado de la inocuidad de los alimentos..)
	respuestas = []
	categoria = Category.objects.get(id=98)
	indicador = Indicador.objects.get(id=45)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1614):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1613):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	# Indicador 15 (Salud y Seguridad Animal:Practicas Responsables y Sustentables de Produccion Animal...)
	respuestas = []
	categoria = Category.objects.get(id=99)
	indicador = Indicador.objects.get(id=81)
	for r in todasRespuestas:
		# print r.question.category
		# print r.body
		if (r.question.category == categoria):
			respuestas.append(r)
			if (r.question.id == 1632):
				if (r.body == 'Si'):
					aplica = True
				if (r.body == 'No'):
					aplica = False
			if (r.question.id == 1631):
				estadio = r.body[8]
	cuentaSi = 0
	if (aplica):  # si selecciono que el indicador aplica
		for r in respuestas:
			if (r.body == 'Si'):
				cuentaSi = cuentaSi + 1
		cuentaSi = cuentaSi - 1  # Le resto uno porque se sumo la pregunta de que si el indicador aplica
		total = len(
			respuestas) - 2  # Le resto 2 al total asi saco la de si aplica y la de los estadios
		notaBinarias = (
			(
				6.0 / total) * cuentaSi)  # Calcula la parte de la nota que corresponde a las binarias
		notaInd = notaBinarias
		# Le sumo la parte correspondiente al estadio
		if (estadio == '1'):
			notaInd = notaInd + 1
			estadio1 = estadio1 + 1
		if (estadio == '2'):
			notaInd = notaInd + 2
			estadio2 = estadio2 + 1
		if (estadio == '3'):
			notaInd = notaInd + 3
			estadio3 = estadio3 + 1
		if (estadio == '4'):
			notaInd = notaInd + 4
			estadio4 = estadio4 + 1
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.orden = indicador.orden
		nota.nota = notaInd
		nota.save()

	#Calculo de los estadios
	indicador = Indicador.objects.get(id=77)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio1
	nota.save()

	indicador = Indicador.objects.get(id=78)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio2
	nota.save()

	indicador = Indicador.objects.get(id=79)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio3
	nota.save()

	indicador = Indicador.objects.get(id=80)
	nota = Nota()
	nota.evaluacion = evaluacion
	nota.indicador = indicador
	nota.nota = estadio4
	nota.save()

	# CALCULO DE INDICADORES DE SUBTEMAS
	# Vision y estrategia
	indicador = Indicador.objects.get(id=50)
	indicadoresRegulares = Nota.objects.filter(evaluacion=evaluacion)
	notaSubtema = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 2):
			notaSubtema = ind.nota
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = notaSubtema
		nota.save()

	# RELACIONES TRANSPARENTES CON LA SOCIEDAD
	indicador = Indicador.objects.get(id=52)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 9):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# INTEGRACION DE LA RS & SUSTENTABILIDAD A LA ESTRATEGIA DEL NEGOCIO
	indicador = Indicador.objects.get(id=53)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 1):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# Trabajo decente
	indicador = Indicador.objects.get(id=55)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 13):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 14):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 15):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD EN EL TRABAJO Y CALIDAD DE VIDA
	indicador = Indicador.objects.get(id=56)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 18):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 20):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# DERECHOS HUMANOS Y RESPETO AL INDIVIDUO
	indicador = Indicador.objects.get(id=57)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 22):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 25):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# BUENAS PRACTICAS AGROPECUARIAS ORIENTADAS A LA SUSTENTABILIDAD
	indicador = Indicador.objects.get(id=58)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 27):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 29):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# GERENCIAMIENTO DEL IMPACTO AMBIENTAL
	indicador = Indicador.objects.get(id=60)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 39):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# SALUD Y SEGURIDAD DEL CONSUMIDOR
	indicador = Indicador.objects.get(id=64)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 45):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	# Buenas practicas ganaderas orientadas a la sustentabilidad
	indicador = Indicador.objects.get(id=59)
	notaSubtema = 0
	cuenta = 0
	bandera = False
	for ind in indicadoresRegulares:
		if (ind.indicador.id == 81):
			notaSubtema = notaSubtema + ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaSubtema / cuenta)
		nota.save()

	#Indicadores de DIMENSIONES
	notas= Nota.objects.filter(evaluacion=evaluacion)

	#DIMENSION VALORES - TRANSPARENCIA Y GESTION
	indicador = Indicador.objects.get(id=69)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 50):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 51):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 52):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 53):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION PRACTICAS DE EMPLEO Y TRABAJO DIGNO
	indicador = Indicador.objects.get(id=70)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 55):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 56):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 57):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION SUSTENTABILIDAD DE LAS PRACTICAS AGRICOLAS - GANADERAS
	indicador = Indicador.objects.get(id=71)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 58):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 59):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 60):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 81):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON CLIENTES Y OTROS PRODUCTORES
	indicador = Indicador.objects.get(id=73)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 64):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON LAS COMUNIDADES LOCALES
	indicador = Indicador.objects.get(id=74)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 66):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	#DIMENSION RELACIONES CON GOBIERNO Y SOCIEDAD
	indicador = Indicador.objects.get(id=75)
	notaDim = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 68):
			notaDim = notaDim+ ind.nota
			cuenta = cuenta + 1
			bandera = True
	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaDim / cuenta)
		nota.save()

	# Calcula la nota general
	notas = Nota.objects.filter(evaluacion=evaluacion)
	indicador = Indicador.objects.get(id=76)
	notaGral = 0
	cuenta = 0
	bandera = False
	for ind in notas:
		if (ind.indicador.id == 69):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 70):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 71):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 73):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 74):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True
		if (ind.indicador.id == 75):
			notaGral = notaGral + ind.nota
			cuenta = cuenta + 1
			bandera = True

	if (bandera == True):
		nota = Nota()
		nota.evaluacion = evaluacion
		nota.indicador = indicador
		nota.nota = (notaGral / cuenta)
		nota.save()

	return redirect('indicadores:resultados',evaluacion.id)
