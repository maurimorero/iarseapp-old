from django.shortcuts import render
from models import Evaluacion,Indicador,Nota,TipoIndicador,Provincia
from ..survey.models import ResponseMgr,Response,AnswerRadio,Dimension,Survey,Encuesta, Category, AnswerText
from ..usuarios.models import Profile
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import base64
import random

# Create your views here.

def Resultados(request, id):
    evaluacion= Evaluacion.objects.get(id=id)
    perfiles = Profile.objects.all()

    for p in perfiles:
        if (p.user==evaluacion.usuario):
            perfil=p

    # Cargo los indicadores de la encuesta para saber cuantos son para el calculo de estadio que no se identifiquen
    dimensiones = Dimension.objects.filter(encuesta=evaluacion.rspMgr.encuesta)
    temas=[]
    indicadores=[]

    for dim in dimensiones:
        temDim = Survey.objects.filter(dimension=dim)
        for t in temDim:
            temas.append(t)

    for tem in temas:
        indica = Category.objects.filter(survey=tem)
        for ind in indica:
            indicadores.append(ind)

    cantInd= len(indicadores)

    notas= Nota.objects.filter(evaluacion=evaluacion).order_by("orden")

    estadio1 = 0
    estadio2 = 0
    estadio3 = 0
    estadio4 = 0
    totalEst = 0
    for nota in notas:
        if (nota.indicador.id==77):
            estadio1=nota
            totalEst = totalEst+ nota.nota
           # print estadio1
        if (nota.indicador.id == 78):
            estadio2 = nota
            totalEst = totalEst + nota.nota
            #print estadio2
        if (nota.indicador.id==79):
            estadio3=nota
            totalEst = totalEst + nota.nota
            #print estadio3
        if (nota.indicador.id==80):
            estadio4=nota
            totalEst = totalEst + nota.nota
            #print estadio4
    estadioNo= cantInd-totalEst

    sitio=get_current_site(request)
    print sitio

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'])
    driver.set_window_size(1024, 768)   
    #urlcaptura='http://www.lavoz.com.ar'
    #urlcaptura='http://indicagro.bccba.com.ar/indicadores/graficos/'+str(evaluacion.id)
    #urlcaptura='https://192.168.100.217/indicadores/graficos/'+str(evaluacion.id)
    urlcaptura= str(sitio)+'/indicadores/graficos/'+str(evaluacion.id)
    driver.get(urlcaptura)
    time.sleep(2)
    driver.execute_script('document.body.style.background = "white"')
    driver.save_screenshot('./static/graficos/'+str(evaluacion.id)+'.png')
    driver.quit()

    with open('./static/graficos/'+str(evaluacion.id)+'.png', "rb") as imageFile:
        imagen = base64.b64encode(imageFile.read())
        #print cadena

    with open('./static/img/logobolsa.png', "rb") as imageFile:
        imagen1 = base64.b64encode(imageFile.read())

    with open('./static/img/indicadores2.png', "rb") as imageFile:
        imagen2 = base64.b64encode(imageFile.read())

    with open('./static/img/logoiarse.png', "rb") as imageFile:
        imagen3 = base64.b64encode(imageFile.read())

    contexto = {
                'evaluacion':evaluacion,
                'notas':notas,
                'estadio1':estadio1,
                'estadio2': estadio2,
                'estadio3': estadio3,
                'estadio4': estadio4,
                'imagen':imagen,
                'imagen1':imagen1,
                'imagen2': imagen2,
                'imagen3': imagen3,
                'perfil':perfil,
                'estadioNo':str("%0.2f" % estadioNo)
                }
    return render(request, 'resultados1.html', contexto)

def Respuestas(request, id):
    rspMgr=ResponseMgr.objects.get(id=id)
    encuesta= Encuesta.objects.get(id=rspMgr.encuesta.id)
    profile= Profile.objects.get(user=rspMgr.user)
    indicadores = []
    # Levanto los responses (uno para cada subtema)
    responses = Response.objects.filter(respMgr=rspMgr)

    # Aca se van a almacenar todas las respuestas (para no tene que levantarlas para cada indicador
    todasRespuestas = []

    # Levanto las respuestas de la evaluacion
    for indx, res in enumerate(responses):
        resps = AnswerRadio.objects.filter(response=res)
        respsTxt = AnswerText.objects.filter(response=res)
        for r in resps:
            todasRespuestas.append(r)
        for r in respsTxt:
            todasRespuestas.append(r)
        indi = Category.objects.filter(survey=res.survey)
        for ind in indi:
            indicadores.append(ind)
    todasRespuestas.sort(key=lambda todasRespuestas:todasRespuestas.question.text)
    indicadores.sort(key=lambda indicadores:indicadores.orden)
    contexto = {
                'rspMgr':rspMgr,
                'profile':profile,
                'encuesta':encuesta,
                'responses':responses,
                'indicadores':indicadores,
                'todasRespuestas':todasRespuestas
                }
    return render(request, 'respuestas.html', contexto)

def ResultadosComp(request, id):
    user= User.objects.get(id=id)
    perfiles = Profile.objects.all()

    for p in perfiles:
        if (p.user==user):
            perfil=p
    evaluaciones= Evaluacion.objects.filter(usuario=user).order_by('-fecha')

    if (len(evaluaciones) <= 1):
        messages.error(request, 'Para hacer la consulta comparativa debe haber realizado al menos, dos auto-evaluaciones')
        return redirect('usuarios:usuarios_home')



    for indx, ev in enumerate(evaluaciones):
        if(indx==0):
            evaluacion = ev

            # Cargo los indicadores de la encuesta para saber cuantos son para el calculo de estadio que no se identifiquen
            dimensiones = Dimension.objects.filter(encuesta=ev.rspMgr.encuesta)
            temas = []
            indicadores = []

            for dim in dimensiones:
                temDim = Survey.objects.filter(dimension=dim)
                for t in temDim:
                    temas.append(t)

            for tem in temas:
                indica = Category.objects.filter(survey=tem)
                for ind in indica:
                    indicadores.append(ind)

            cantInd = len(indicadores)

            notas = Nota.objects.filter(evaluacion=ev).order_by("orden")
            estadio1 = 0
            estadio2 = 0
            estadio3 = 0
            estadio4 = 0
            suma1=0
            for nota in notas:
                if (nota.indicador.id==77):
                    estadio1=nota
                    suma1=suma1+nota.nota
                if (nota.indicador.id == 78):
                    estadio2 = nota
                    suma1 = suma1 + nota.nota
                if (nota.indicador.id==79):
                    estadio3=nota
                    suma1 = suma1 + nota.nota
                if (nota.indicador.id==80):
                    estadio4=nota
                    suma1 = suma1 + nota.nota
            estadioNo1 = cantInd - suma1

        if (indx == 1):
            evaluacion1 = ev

            # Cargo los indicadores de la encuesta para saber cuantos son para el calculo de estadio que no se identifiquen
            dimensiones = Dimension.objects.filter(encuesta=ev.rspMgr.encuesta)
            temas = []
            indicadores = []

            for dim in dimensiones:
                temDim = Survey.objects.filter(dimension=dim)
                for t in temDim:
                    temas.append(t)

            for tem in temas:
                indica = Category.objects.filter(survey=tem)
                for ind in indica:
                    indicadores.append(ind)

            cantInd = len(indicadores)

            notas1 = Nota.objects.filter(evaluacion=ev).order_by("orden")
            estadio11 = 0
            estadio21 = 0
            estadio31 = 0
            estadio41 = 0
            suma2 = 0

            for nota in notas1:
                if (nota.indicador.id == 77):
                    estadio11 = nota
                    suma2 = suma2 + nota.nota
                if (nota.indicador.id == 78):
                    estadio21 = nota
                    suma2 = suma2 + nota.nota
                if (nota.indicador.id == 79):
                    estadio31 = nota
                    suma2 = suma2 + nota.nota
                if (nota.indicador.id == 80):
                    estadio41 = nota
                    suma2 = suma2 + nota.nota
            estadioNo2 = cantInd - suma1

    tipoIndicador= TipoIndicador.objects.get(id=2)
    dimensiones= Indicador.objects.filter(tipo=tipoIndicador)
    notasDim= []
    notasDim1 = []

    for dim in dimensiones:
        band=False
        for nota in notas:
            if(dim.id ==nota.indicador.id):
                notasDim.append(nota)
                band=True
        if(band==False):
            notaVacia = Nota()
            notaVacia.indicador = dim
            notaVacia.nota = 0
            notasDim.append(notaVacia)
        band = False
        for nota in notas1:
            if (dim.id == nota.indicador.id):
                notasDim1.append(nota)
                band = True
        if (band == False):
            notaVacia = Nota()
            notaVacia.indicador = tem
            notaVacia.nota = 0
            notasDim1.append(notaVacia)

    tipoIndicador= TipoIndicador.objects.get(id=4)
    temas= Indicador.objects.filter(tipo=tipoIndicador)
    notasTem= []
    notasTem1 = []

    for tem in temas:
        band=False
        for nota in notas:
            if(tem.id ==nota.indicador.id):
                notasTem.append(nota)
                band=True
        if(band==False):
            notaVacia = Nota()
            notaVacia.indicador = tem
            notaVacia.nota = 0
            notasTem.append(notaVacia)
        band = False
        for nota in notas1:
            if (tem.id == nota.indicador.id):
                notasTem1.append(nota)
                band = True
        if (band == False):
            notaVacia= Nota()
            notaVacia.indicador=tem
            notaVacia.nota=0
            notasTem1.append(notaVacia)

    sitio=get_current_site(request)
    #print sitio

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")

    driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--web-security=false'])
    driver.set_window_size(1024, 768)
    #print str(sitio) + '/indicadores/graficos/' + str(evaluacion.id)
    nombreImagen= str(id)+'-'+str(random.randrange(1, 999999999999999))+'.png'
    try:
        driver.get(str(sitio)+'/indicadores/graficoscomp/'+str(id))
        time.sleep(2)
        driver.execute_script('document.getElementsByClassName("mp")[0].style.background = "white"')
        # driver.execute_script('document.body.style.background = "black"')
    except Exception, e:
        driver.save_screenshot('./static/graficos/'+nombreImagen)
        driver.quit()

    with open('./static/graficos/'+nombreImagen, "rb") as imageFile:
        imagen = base64.b64encode(imageFile.read())
        #print cadena

    with open('./static/img/logobolsa.png', "rb") as imageFile:
        imagen1 = base64.b64encode(imageFile.read())

    with open('./static/img/indicadores2.png', "rb") as imageFile:
        imagen2 = base64.b64encode(imageFile.read())

    with open('./static/img/logoiarse.png', "rb") as imageFile:
        imagen3 = base64.b64encode(imageFile.read())

    contexto = {
                'evaluacion':evaluacion,
                'notas':notas,
                'estadio1':estadio1,
                'estadio2': estadio2,
                'estadio3': estadio3,
                'estadio4': estadio4,
                'evaluacion1': evaluacion1,
                'notas1': notas1,
                'estadio11': estadio11,
                'estadio21': estadio21,
                'estadio31': estadio31,
                'estadio41': estadio41,
                'dimensiones':dimensiones,
                'notasDim':notasDim,
                'notasDim1':notasDim1,
                'temas': temas,
                'notasTem': notasTem,
                'notasTem1': notasTem1,
                'imagen':imagen,
                'imagen1': imagen1,
                'imagen2': imagen2,
                'imagen3': imagen3,
                'perfil':perfil,
                'estadioNo1':str("%0.2f" % estadioNo1),
                'estadioNo2':str("%0.2f" % estadioNo2)
                }
    return render(request, 'resultadoscomp1.html', contexto)

def ConsultaConsolidada(request):
    empresas = Profile.objects.exclude(id=1).order_by('empresa')
    provincias = Provincia.objects.order_by('name')
    grupos = Group.objects.order_by('name')
    if request.method == 'POST':
        band=False
        empresasConsult = []
        ubicacionesConsult = []
        gruposConsult = []
        banderaEncuesta=0

        if(request.POST.get("tipoencuesta", "")=='2'):
            banderaEncuesta = 2
        if (request.POST.get("tipoencuesta", "")=='3'):
            banderaEncuesta = 3
        if (request.POST.get("tipoencuesta", "")=='1'):
            banderaEncuesta = 1

        for empresa in empresas:
            etiqueta="e"+str(empresa.id)
            if request.POST.get(etiqueta, ""):
                empresasConsult.append(Profile.objects.get(id=request.POST.get(etiqueta, "")))
                band = True
        for provincia in provincias:
            etiqueta="p"+str(provincia.id)
            if request.POST.get(etiqueta, ""):
                ubicacionesConsult.append(Provincia.objects.get(id=request.POST.get(etiqueta, "")))
                band = True

        for grupo in grupos:
            etiqueta="g"+str(grupo.id)
            if request.POST.get(etiqueta, ""):
                gruposConsult.append(Group.objects.get(id=request.POST.get(etiqueta, "")))
                band = True

        if (request.POST.get("filtro", "")=='3'):
            bandGroup=False
            for grupo in gruposConsult:
                usuarios = User.objects.filter(groups__name= grupo.name)
                if(len(usuarios)>=1):
                    bandGroup=True
        else:
            bandGroup = True
        if(band==False):
            messages.error(request, 'Debe seleccionar al menos una Empresa/Ubicacion/Grupo')
            return redirect('indicadores:consultaconsolidada')

        if (bandGroup == False):
            messages.error(request, 'El/Los grupos seleccionados no tienen miembros')
            return redirect('indicadores:consultaconsolidada')

        return ResultadosConsolidados(request,empresasConsult,ubicacionesConsult,gruposConsult,banderaEncuesta)

    contexto = { 'empresas':empresas,
                 'provincias':provincias,
                 'grupos':grupos
                }
    return render(request, 'consultaconsolidada.html', contexto)

def ResultadosConsolidados(request,empresasConsult,ubicacionesConsult,gruposConsult,banderaEncuestas):

    evaluaciones = []
    listadoFiltros= []
    #print str(banderaEncuestas)

    #Levanta encuestas segun filtros aplicados
    if (banderaEncuestas==2):
        for empresa in empresasConsult:
            user=User.objects.get(id=empresa.user.id)
            evaEmpresa = Evaluacion.objects.filter(usuario=user).order_by('-fecha')
            banderita=False
            if(len(evaEmpresa)>0):
                for evalu in evaEmpresa:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if(rsp.encuesta.id==2)and (banderita==False):
                        evaluaciones.append(evalu)
                        banderita==True
            listadoFiltros.append(empresa.empresa)

        for provincia in ubicacionesConsult:
            evaProv = Evaluacion.objects.filter(ubicacion=provincia)
            banderita = False
            if (len(evaProv) > 0):
                for evalu in evaProv:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if (rsp.encuesta.id == 2) and (banderita == False):
                        evaluaciones.append(evalu)
                        banderita == True
            listadoFiltros.append(provincia.name)

        for grupo in gruposConsult:
            usuarios= User.objects.filter(groups__name= grupo.name)
            for usu in usuarios:
                evaEmpresa = Evaluacion.objects.filter(usuario=usu).order_by('-fecha')
                banderita = False
                if (len(evaEmpresa) > 0):
                    for evalu in evaEmpresa:
                        rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                        if (rsp.encuesta.id == 2) and (banderita == False):
                            evaluaciones.append(evalu)
                            banderita == True
            listadoFiltros.append(grupo.name)

    if (banderaEncuestas==1):
        for empresa in empresasConsult:
            user=User.objects.get(id=empresa.user.id)
            evaEmpresa = Evaluacion.objects.filter(usuario=user).order_by('-fecha')
            banderita=False
            if(len(evaEmpresa)>0):
                for evalu in evaEmpresa:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if(rsp.encuesta.id==1)and (banderita==False):
                        evaluaciones.append(evalu)
                        banderita==True
            listadoFiltros.append(empresa.empresa)

        for provincia in ubicacionesConsult:
            evaProv = Evaluacion.objects.filter(ubicacion=provincia)
            banderita = False
            if (len(evaProv) > 0):
                for evalu in evaProv:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if (rsp.encuesta.id == 1) and (banderita == False):
                        evaluaciones.append(evalu)
                        banderita == True
            listadoFiltros.append(provincia.name)

        for grupo in gruposConsult:
            usuarios= User.objects.filter(groups__name= grupo.name)
            for usu in usuarios:
                evaEmpresa = Evaluacion.objects.filter(usuario=usu).order_by('-fecha')
                banderita = False
                if (len(evaEmpresa) > 0):
                    for evalu in evaEmpresa:
                        rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                        if (rsp.encuesta.id == 1) and (banderita == False):
                            evaluaciones.append(evalu)
                            banderita == True
            listadoFiltros.append(grupo.name)

    if (banderaEncuestas==3):
        for empresa in empresasConsult:
            user=User.objects.get(id=empresa.user.id)
            evaEmpresa = Evaluacion.objects.filter(usuario=user).order_by('-fecha')
            banderita=False
            if(len(evaEmpresa)>0):
                for evalu in evaEmpresa:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if(rsp.encuesta.id==3)and (banderita==False):
                        evaluaciones.append(evalu)
                        banderita==True
            listadoFiltros.append(empresa.empresa)

        for provincia in ubicacionesConsult:
            evaProv = Evaluacion.objects.filter(ubicacion=provincia)
            banderita = False
            if (len(evaProv) > 0):
                for evalu in evaProv:
                    rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                    if (rsp.encuesta.id == 3) and (banderita == False):
                        evaluaciones.append(evalu)
                        banderita == True
            listadoFiltros.append(provincia.name)

        for grupo in gruposConsult:
            usuarios= User.objects.filter(groups__name= grupo.name)
            for usu in usuarios:
                evaEmpresa = Evaluacion.objects.filter(usuario=usu).order_by('-fecha')
                banderita = False
                if (len(evaEmpresa) > 0):
                    for evalu in evaEmpresa:
                        rsp = ResponseMgr.objects.get(id=evalu.rspMgr.id)
                        if (rsp.encuesta.id == 3) and (banderita == False):
                            evaluaciones.append(evalu)
                            banderita == True
            listadoFiltros.append(grupo.name)

    if (len(evaluaciones) < 1):
        messages.error(request, 'No existen autoevaluaciones con los filtros aplicados')
        return redirect('indicadores:consultaconsolidada')

    #Calcula indicadores
    indicadores = Indicador.objects.filter().order_by("orden")
    evaluacionConsolidada= Evaluacion()
    notas=[]
    notasMin = []
    notasMax = []
    nose =True


    for indi in indicadores:
        cuenta=0
        suma=0
        banderaInit = True
        for eva in evaluaciones:
            nota= Nota.objects.filter(evaluacion=eva,indicador=indi)
            if(nota):
                suma=suma+nota[0].nota
                cuenta=cuenta+1
                if (banderaInit == True):
                    notaMin=nota[0]
                    notaMax=nota[0]
                    banderaInit = False
                if(nota[0].nota > notaMax.nota):
                    notaMax = nota[0]
                if (nota[0].nota < notaMin.nota):
                    notaMin = nota[0]
        if (suma==0 and cuenta==0):
                nose = False #Esto no hace nada
        else:
            nota = Nota()
            nota.evaluacion = evaluacionConsolidada
            nota.nota= (suma/cuenta)
            nota.indicador=indi
            nota.orden=indi.orden
            notas.append(nota)
            notasMin.append(notaMin)
            notasMax.append(notaMax)

    #estadio1=0
    #estadio2=0
    #estadio3=0
    #estadio4=0
    #estadio1Min=0
    #estadio2Min=0
    #estadio3Min=0
    #estadio4Min=0
    #estadio1Max=0
    #estadio2Max=0
    #estadio3Max=0
    #estadio4Max=0

    for nota in notas:
        if (nota.indicador.id==77):
            estadio1=nota
        if (nota.indicador.id == 78):
            estadio2 = nota
        if (nota.indicador.id==79):
            estadio3=nota
        if (nota.indicador.id==80):
            estadio4=nota

    for nota in notasMin:
        if (nota.indicador.id==77):
            estadio1Min=nota
        if (nota.indicador.id == 78):
            estadio2Min = nota
        if (nota.indicador.id==79):
            estadio3Min=nota
        if (nota.indicador.id==80):
            estadio4Min=nota

    for nota in notasMax:
        if (nota.indicador.id==77):
            estadio1Max=nota
        if (nota.indicador.id == 78):
            estadio2Max = nota
        if (nota.indicador.id==79):
            estadio3Max=nota
        if (nota.indicador.id==80):
            estadio4Max=nota

    contexto = {
                'evaluaciones':evaluaciones,
                'notas':notas,
                'estadio1':estadio1,
                'estadio2': estadio2,
                'estadio3': estadio3,
                'estadio4': estadio4,
                'estadio1Min': estadio1Min,
                'estadio2Min': estadio2Min,
                'estadio3Min': estadio3Min,
                'estadio4Min': estadio4Min,
                'estadio1Max': estadio1Max,
                'estadio2Max': estadio2Max,
                'estadio3Max': estadio3Max,
                'estadio4Max': estadio4Max,
                'notasMin':notasMin,
                'notasMax':notasMax,
                'listadoFiltros':listadoFiltros
                }
    return render(request, 'resultadosconsolidados1.html', contexto)

def Graficos(request, id):
    evaluacion= Evaluacion.objects.get(id=id)
    notas= Nota.objects.filter(evaluacion=evaluacion)

    estadio1 = 0
    estadio2 = 0
    estadio3 = 0
    estadio4 = 0
    for nota in notas:
        if (nota.indicador.id==77):
            estadio1=nota
            #print estadio1
        if (nota.indicador.id == 78):
            estadio2 = nota
            #print estadio2
        if (nota.indicador.id==79):
            estadio3=nota
            #print estadio3
        if (nota.indicador.id==80):
            estadio4=nota
            #print estadio4

    contexto = {
                'evaluacion':evaluacion,
                'notas':notas,
                'estadio1':estadio1,
                'estadio2': estadio2,
                'estadio3': estadio3,
                'estadio4': estadio4
                }
    return render(request, 'graficos.html', contexto)

def GraficosComp(request, id):
    user= User.objects.get(id=id)
    evaluaciones= Evaluacion.objects.filter(usuario=user).order_by('-fecha')

    if (len(evaluaciones) <= 1):
        messages.error(request, 'Para hacer la consulta comparativa debe haber realizado al menos, dos auto-evaluaciones')
        return redirect('usuarios:usuarios_home')

    for indx, ev in enumerate(evaluaciones):
        if(indx==0):
            evaluacion = ev
            notas = Nota.objects.filter(evaluacion=ev)
            estadio1 = 0
            estadio2 = 0
            estadio3 = 0
            estadio4 = 0
            for nota in notas:
                if (nota.indicador.id==77):
                    estadio1=nota
                if (nota.indicador.id == 78):
                    estadio2 = nota
                if (nota.indicador.id==79):
                    estadio3=nota
                if (nota.indicador.id==80):
                    estadio4=nota
        if (indx == 1):
            evaluacion1 = ev
            notas1 = Nota.objects.filter(evaluacion=ev)
            estadio11 = 0
            estadio21 = 0
            estadio31 = 0
            estadio41 = 0
            for nota in notas1:
                if (nota.indicador.id == 77):
                    estadio11 = nota
                if (nota.indicador.id == 78):
                    estadio21 = nota
                if (nota.indicador.id == 79):
                    estadio31 = nota
                if (nota.indicador.id == 80):
                    estadio41 = nota

    tipoIndicador= TipoIndicador.objects.get(id=2)
    dimensiones= Indicador.objects.filter(tipo=tipoIndicador)
    notasDim= []
    notasDim1 = []

    for dim in dimensiones:
        band=False
        for nota in notas:
            if(dim.id ==nota.indicador.id):
                notasDim.append(nota)
                band=True
        if(band==False):
            notaVacia = Nota()
            notaVacia.indicador = dim
            notaVacia.nota = 0
            notasDim.append(notaVacia)
        band = False
        for nota in notas1:
            if (dim.id == nota.indicador.id):
                notasDim1.append(nota)
                band = True
        if (band == False):
            notaVacia = Nota()
            notaVacia.indicador = tem
            notaVacia.nota = 0
            notasDim1.append(notaVacia)

    tipoIndicador= TipoIndicador.objects.get(id=4)
    temas= Indicador.objects.filter(tipo=tipoIndicador)
    notasTem= []
    notasTem1 = []

    for tem in temas:
        band=False
        for nota in notas:
            if(tem.id ==nota.indicador.id):
                notasTem.append(nota)
                band=True
        if(band==False):
            notaVacia = Nota()
            notaVacia.indicador = tem
            notaVacia.nota = 0
            notasTem.append(notaVacia)
        band = False
        for nota in notas1:
            if (tem.id == nota.indicador.id):
                notasTem1.append(nota)
                band = True
        if (band == False):
            notaVacia= Nota()
            notaVacia.indicador=tem
            notaVacia.nota=0
            notasTem1.append(notaVacia)

    contexto = {
                'evaluacion':evaluacion,
                'notas':notas,
                'estadio1':estadio1,
                'estadio2': estadio2,
                'estadio3': estadio3,
                'estadio4': estadio4,
                'evaluacion1': evaluacion1,
                'notas1': notas1,
                'estadio11': estadio11,
                'estadio21': estadio21,
                'estadio31': estadio31,
                'estadio41': estadio41,
                'dimensiones':dimensiones,
                'notasDim':notasDim,
                'notasDim1':notasDim1,
                'temas': temas,
                'notasTem': notasTem,
                'notasTem1': notasTem1
                }
    return render(request, 'graficoscomp.html', contexto)

def Indicadores (request, id):
    encuesta= Encuesta.objects.get(id=id)
    dimensiones = Dimension.objects.filter(encuesta=encuesta)
    temas=[]
    indicadores=[]

    for dim in dimensiones:
        temDim = Survey.objects.filter(dimension=dim).order_by("orden")
        for t in temDim:
            temas.append(t)

    for tem in temas:
        indica = Category.objects.filter(survey=tem).order_by("orden")
        for ind in indica:
            indicadores.append(ind)

    contexto = {
        'indicadores':indicadores,
        'encuesta':encuesta
    }
    return render(request,'indicadores.html',contexto)
