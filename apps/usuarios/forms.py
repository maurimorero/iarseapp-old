from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from models import Profile

class RegistroForm (UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
        ]
        labels = {
            'username':'CUIT',
        }
        widgets= {
            'username': forms.TextInput(attrs={'type':'number'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]
        labels = {
            'username': 'CUIT',
        }
        widgets = {
            'username': forms.TextInput(attrs={'type': 'number'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('empresa',
                  'empresaCom',
                  'actividadPrincipal',
                  'actividadSecundaria',
                  'cp',
                  'comentarios',
                  'nombre',
                  'email',
                  'puesto',
                  'provincia',
                  'localidad',
                  'direccion',
                  'telefono',
                  )
        labels = {
            'empresa': 'Empresa',
            'empresaCom':'Empresa (Nombre comercial)',
            'actividadPrincipal':'Actividad Principal',
            'actividadSecundaria':'Actividad Secundario',
            'cp':'Codigo Postal',
            'comentarios':'Comentarios Adicionales',
            'nombre':'Nombre completo',
            'email':'E-mail',
            'puesto':'Puesto',
            'provincia':'Provincia',
            'localidad':'Localidad',
            'direccion':'Direccion',
            'telefono':'Telefono',
        }
