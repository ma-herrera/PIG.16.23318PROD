from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib import messages

from django.views.generic import View, CreateView, ListView,UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from .form_autenticacion import FormularioLogin, FormularioUsuario, CambiarPasswordForm, EditarPerfilUsuario, EditarUsuario
from usuario.models import Usuario
from usuario.mixin import LoginYSuperUsuarioMixin, LoginMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404


class RegistrarUsuario(CreateView):
    model = Usuario
    form_class= FormularioUsuario
    template_name = 'usuario/registrar_usuario.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        nuevo_usuario = form.save(commit=False)
        nuevo_usuario.set_password(form.cleaned_data.get('password1'))
        nuevo_usuario.save()
        messages.success(self.request, 'Usuario registrado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al registrar el usuario')
        return redirect('home')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = self.form_class(self.request.POST)
        else:
            context['form'] = self.form_class()
        return context

def cerrar_sesion(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión!, ¡Te esperamos nuevamente!')
    return redirect('home')

#login personalizado

class Login(FormView):
    template_name ='usuario/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().dispatch(request,*args,**kwargs)
    
    def form_valid(self,form):
        login(self.request, form.get_user())
        messages.success(self.request, '¡Bienvenido/a! Has iniciado sesión correctamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos')
        return redirect('home')
    
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))


class ListadoUsuario(LoginYSuperUsuarioMixin, ListView):
    model = Usuario
    template_name = 'usuario/listar_usuarios.html'
    paginate_by = 5  # Número de usuarios por página


    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.method == 'GET' and 'nombre' in self.request.GET:
            nombre = self.request.GET['nombre']
            queryset = queryset.filter(Q(nombre__icontains=nombre))
        
        queryset = queryset.filter(usuario_activo=True).order_by('id')
        
        return queryset

    # Paginador de usuarios en administracion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page',1)

        try:
            usuarios = paginator.page(page)
        except Exception:
            raise Http404

        context['entity'] = usuarios
        context['paginator'] = paginator
        context['messages'] = messages.get_messages(self.request)

        return context

def buscar_usuario(request):
    return render(request, "usuario/buscar_usuario.html")

class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar_usuario.html'
    success_url = reverse_lazy('listar_usuarios')

    #Eliminacion logica, no sale en la lista administrador, pero si en admin
    def post(self, request, pk,*args, **kwargs):
        object = Usuario.objects.get(id = pk)
        object.usuario_activo = False
        object.save()
        messages.success(request,"El usuario se ha eliminado correctamente")
        return redirect(self.success_url)
  
    
class EditarUsuario(LoginYSuperUsuarioMixin, UpdateView):
    model = Usuario
    template_name = 'usuario/editar_usuario.html'
    form_class = EditarUsuario
    success_url = reverse_lazy('listar_usuarios')   

    def form_valid(self, form):
        messages.success(self.request, 'El usuario se ha editado correctamente')
        return super().form_valid(form)
    
class PerfilUsuario(UpdateView):
    form_class= EditarPerfilUsuario
    template_name = 'usuario/perfil_usuario.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Tu perfil ha sido actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar tu perfil, verifica los errores')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('perfil_usuario', kwargs={'pk': self.object.pk})
    
    def get_object(self):
        return self.request.user
        
class CambiarPassword(View):
    template_name = 'usuario/cambiar_password.html'
    form_class = CambiarPasswordForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(id=request.user.id)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                logout(request)
                messages.success(request, "Contraseña modificada correctamente")
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})

