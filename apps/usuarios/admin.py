from django.contrib import admin
from models import Profile,Provincia

admin.site.register(Profile)
admin.site.register(Provincia)

admin.autodiscover()

# Register your models here.
