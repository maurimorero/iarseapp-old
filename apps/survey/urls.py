from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from views import Index, SurveyDetail, Confirm, privacy,EncuestaIndex,EncuestaIndexView, SubtemaView, ResponseDelete, EncuestaTerminar
from django.views.static import serve
from django.contrib.auth.decorators import login_required

admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = [
	# Examples:
	url(r'^$', login_required(Index), name='home'),
	url(r'^(?P<idr>\d+)/(?P<ids>\d+)/$', login_required(SurveyDetail), name='survey_detail'),
	url(r'^subtema/(?P<idr>\d+)/(?P<ids>\d+)/$', login_required(SubtemaView), name='survey_subtema'),
	url(r'^encuesta/(?P<id>\d+)/$', login_required(EncuestaIndex), name='encuesta_completa'),
	url(r'^encuesta_terminar/(?P<id>\d+)/$', login_required(EncuestaTerminar), name='encuesta_terminar'),
	url(r'^encuesta_view/(?P<id>\d+)/(?P<errorMsg>\d+)/(?P<slide>\d+)/$', login_required(EncuestaIndexView), name='encuesta_view'),
	url(r'^encuesta_delete/(?P<id>\d+)/$', login_required(ResponseDelete), name='encuesta_delete'),
	url(r'^confirm/(?P<uuid>\w+)/$', login_required(Confirm), name='confirmation'),
	url(r'^privacy/$', login_required(privacy), name='privacy_statement'),


	# Uncomment the admin/doc line below to enable admin documentation:
	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	#url(r'^admin/', include(admin.site.urls)),

    url (r'^%s/(?P<path>.*)$' % media_url, login_required(serve),
     { 'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
]

