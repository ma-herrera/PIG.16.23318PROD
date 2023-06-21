from django.urls import path
from .views import  cerrar_sesion, Login, ListadoUsuario, RegistrarUsuario, EliminarUsuario,EditarUsuario, logoutUsuario, CambiarPassword, PerfilUsuario, buscar_usuario

urlpatterns = [
   # path ('', Registro.as_view(), name="usuario"),
   
    path ('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path ('loguear', Login.as_view(), name="loguear"),
    path ('perfil/<int:pk>/', PerfilUsuario.as_view(), name='perfil_usuario'),
    path ('listado_usuarios/', ListadoUsuario.as_view(), name='listar_usuarios'),
    path ('registrar_usuarios/', RegistrarUsuario.as_view(), name='registrar_usuarios'),
    path ('editar/<int:pk>',EditarUsuario.as_view(),name='editar_usuario'),
    path ('eliminar/<int:pk>',EliminarUsuario.as_view(),name='eliminar_usuario'),
    path ('cambiar_password/',CambiarPassword.as_view(),name='cambiar_password'),
    path ('buscar/', buscar_usuario,name='buscar_usuario'),
]