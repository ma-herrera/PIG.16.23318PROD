from django import forms
from .models import TipoDeActividad, Profesor, Cliente, TipoDocumento

class TipoDeActividadForm(forms.ModelForm):

    class Meta:
        model=TipoDeActividad
        fields=['nombre','titulo','subtitulo','descripcion','imagen_de_portada']

    # se pueden agregar validators
    nombre=forms.CharField(
            label='Nombre', 
            widget=forms.TextInput(attrs={'class':'form-control'})
        )

    titulo=forms.CharField(
            label='Título', 
            widget=forms.TextInput(attrs={'class':'form-control'})
        )

    subtitulo=forms.CharField(
            label='Subtítulo', 
            widget=forms.TextInput(attrs={'class':'form-control'})
        )

    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 5,'class':'form-control'})
        )

    imagen_de_portada = forms.ImageField(
        widget=forms.FileInput(attrs={'class':'form-control'})
        )
    
############################## PROFESOR ########################################

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfesorForm(forms.ModelForm):

    class Meta:
        model=Profesor
        fields=["apellido", "nombre", "tipoDocumento", "numeroDocumento", "telefono", 'email', 'coberturaMedica', 'numeroAfiliado', 'cuil', 'fechaAlta', 'fechaBaja']

    apellido = forms.CharField(
        label = 'Apellido',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    nombre = forms.CharField(
        label = 'Nombre',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    
    tipoDocumento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    numeroDocumento = forms.IntegerField(
        label="Número de documento",
        widget= forms.TextInput(attrs={'class':'form-control'})
    )
    
    telefono = forms.CharField(
        label="telefono",
        widget= forms.TextInput(attrs={'class':'form-control'})
    )

    email = forms.EmailField(
        label = 'E-mail',
        widget = forms.EmailInput(attrs={'class':'form-control'})
    )
    
    coberturaMedica = forms.CharField(
        label = 'Cobertura médica',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    
    numeroAfiliado = forms.CharField(
        label = 'Número de afiliado',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    cuil = forms.CharField(
        label="Cuil",
        widget= forms.TextInput(attrs={'class':'form-control', 'maxlength': '11'})
    )

    fechaAlta = forms.DateField(
            label='Fecha Inicio', 
            widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
    )

    fechaBaja = forms.DateField(
            label='Fecha de Baja', 
            required=False,
            widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
    )


############################## CLIENTE ########################################

class ClienteForm(forms.ModelForm):

    class Meta:
        model= Cliente
        fields=['apellido', 'nombre', 'tipoDocumento', 'numeroDocumento', 'telefono', 'email', 'coberturaMedica', 'numeroAfiliado', 'fechaAlta', 'fechaBaja', 'paseLibre', 'fechaPagoPaseLibre', 'aptoFisico']

    apellido = forms.CharField(
        label = 'Apellido',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    nombre = forms.CharField(
        label = 'Nombre',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    
    tipoDocumento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    numeroDocumento = forms.IntegerField(
        label="Número de documento",
        widget= forms.NumberInput(attrs={'class':'form-control'})
    )
    
    telefono = forms.CharField(
        label="Teléfono",
        widget= forms.TextInput(attrs={'class':'form-control'})
    )

    email = forms.EmailField(
        label = 'E-mail',
        widget = forms.EmailInput(attrs={'class':'form-control'})
    )
    
    coberturaMedica = forms.CharField(
        label = 'Cobertura médica',
        required=False,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    
    numeroAfiliado = forms.CharField(
        label = 'Número de afiliado',
        required=False,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    fechaAlta = forms.DateField(
            label='Fecha de Inicio',
            widget=forms.DateInput(attrs={'type':'date', 'placeholder': 'Ingrese la fecha de inicio'}),
            # localize=True
    )

    fechaBaja = forms.DateField(
            label='Fecha de Baja', 
            required=False,
            widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
    )
    
    paseLibre = forms.BooleanField (
            label='Tiene pase libre?',
            required=False,
            widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'value':1})
    )

    fechaPagoPaseLibre = forms.DateField(
            label='Última fecha de pago del pase libre', 
            required=False,
            widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
    )
    
    aptoFisico = forms.BooleanField(
        label="Presenta apto físico? S/N",
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'form-check-input','value':'True'})
    )


