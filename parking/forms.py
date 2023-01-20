from django import forms
from .models import Cliente, Abono

class CrearAbonoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=8)
    matricula = forms.CharField(max_length=7)
    tipo_suscripcion = forms.ChoiceField(choices=[(1, 'Mensual'), (2, 'Trimestral'), (3, 'Anual')])
