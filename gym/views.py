from django.shortcuts import render,redirect
from django.core import serializers

from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from gym.forms import ContactoForm
from gym.models import Contacto
from administracion.models import TipoDeActividad

from django.core.paginator import Paginator
from usuario.mixin import LoginYSuperUsuarioMixin
from django.views.generic import View, ListView, DeleteView
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy

# from .forms_registro import RegistroForm


# Create your views here.
def home(request):
    template = loader.get_template("gym/home.html")
    context = {"title": "Home"}
    return HttpResponse(template.render(context, request))


# Formulario de contacto que se guarda en la base y se muestra en administracion

def contacto(request):
    if request.method == 'GET':
        contacto_form = ContactoForm()
    else:
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            nombre = contacto_form.cleaned_data['nombre']
            email = contacto_form.cleaned_data['email']
            asunto = contacto_form.cleaned_data['asunto']
            mensaje = contacto_form.cleaned_data['mensaje']
            
            nuevo_contacto = Contacto(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje)
            nuevo_contacto.save()
            
            messages.success(request, '¡Mensaje enviado con éxito, responderemos a la brevedad!')
            return redirect('home')
        else:
            messages.warning(request, 'Por favor verifica los errores marcados antes de enviar')

    return render(request, 'gym/contact.html', {
        'contacto_form': contacto_form
    })

class ListadoMensajes(LoginYSuperUsuarioMixin, ListView):
    model = Contacto
    template_name = 'administracion/mensajes_contacto/listar_mensajes.html'
    paginate_by = 5  # Número de mensajes por página
    context_object_name = 'mensajes'
  
    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')

        if self.request.method == 'GET' and any(field in self.request.GET for field in ['nombre', 'asunto', 'email', 'mensaje']):
            nombre = self.request.GET.get('nombre', '')
            asunto = self.request.GET.get('asunto', '')
            email = self.request.GET.get('email', '')
            mensaje = self.request.GET.get('mensaje', '')

            queryset = queryset.filter(
                Q(nombre__icontains=nombre) |
                Q(asunto__icontains=asunto) |
                Q(email__icontains=email) |
                Q(mensaje__icontains=mensaje)
            )

            queryset = queryset.order_by('id')

        return queryset
    # Paginador de mensajes en administracion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page',1)

        try:
            mensajes = paginator.page(page)
        except Exception:
            raise Http404
        
        context['entity'] = mensajes
        context['paginator'] = paginator
        context['messages'] = messages.get_messages(self.request)

        return context

def buscar_mensaje(request):
    return render(request, "administracion/mensajes_contacto/buscar_mensaje.html")

class EliminarMensaje(DeleteView):
    model = Contacto
    template_name = 'administracion/mensajes_contacto/eliminar_mensaje.html'
    success_url = reverse_lazy('listar_mensajes')

    def post(self, request, pk,*args, **kwargs):
        objeto = self.get_object()
        objeto.delete()
        messages.success(request,"El mensaje se ha eliminado correctamente")
        return redirect(self.success_url)


def actividades(request):
    return render(request, 'gym/actividades.html')


def get_actividades_json (request):
    lista_de_actividades = TipoDeActividad.objects.all()
    lista_json = serializers.serialize("json", lista_de_actividades)
    dict_json = '{"lista":' + lista_json + '}'
    return HttpResponse(dict_json)
