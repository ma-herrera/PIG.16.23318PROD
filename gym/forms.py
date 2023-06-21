from django import forms
from django.forms import ValidationError
import re


def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre  %(valor)s no debe contener números.',
                            code='Invalid',
                            params={'valor':value})

def validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Ingresa un correo válido, ej.: juan@gmail.com')
    return value

class ContactoForm(forms.Form):
    nombre = forms.CharField(
            label='Nombre', 
            max_length=50,
            validators=(solo_caracteres,),
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre'})
        )
    email = forms.EmailField(
            label='Email',
            max_length=100,
            validators=(validate_email,),
            error_messages={
                    'required': 'Por favor completa el campo',
                },
            widget=forms.TextInput(attrs={'class':'form-control','type':'email','placeholder':'Ingrese su email'})
        )
    asunto = forms.CharField(
        label='Asunto',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el asunto'})
    )
    mensaje = forms.CharField(
        label='Mensaje',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5,'class':'form-control', 'placeholder':'Escriba su mensaje...'})
    )
 
    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError("Debes especificar mejor el mensaje que nos envias")
        return data

