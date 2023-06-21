from django.urls import path
from . import views
from gym.views import ListadoMensajes, EliminarMensaje, buscar_mensaje

urlpatterns = [
    path ('', views.home_administracion, name="home_administracion"),
    
    path('tipo_de_actividad/', views.TipoDeActividadIndexListView.as_view(), name="tipo_de_actividad_index_view"),
    path('tipo_de_actividad/nuevo/', views.TipoDeActividadNuevoView.as_view(), name="tipo_de_actividad_nuevo_view"),
    path('tipo_de_actividad/editar/<int:pk>', views.TipoDeActividadUpdateView.as_view(), name="tipo_de_actividad_editar_view"),
    path('tipo_de_actividad/eliminar/<int:pk>', views.TipoDeActividadDeleteView.as_view(), name="tipo_de_actividad_eliminar_view"),
    path('tipo_de_actividad/buscar/', views.tipo_de_actividad_buscar,name='tipo_de_actividad_buscar'),

    path('profesor/', views.ProfesorIndexListView.as_view(), name="profesor_index_view"),
    path('profesor/nuevo/', views.ProfesorNuevoView.as_view(), name="profesor_nuevo_view"),
    path('profesor/editar/<int:pk>', views.ProfesorUpdateView.as_view(), name="profesor_editar_view"),
    path('profesor/eliminar/<int:pk>', views.ProfesorDeleteView.as_view(), name="profesor_eliminar_view"),
    path('profesor/buscar/', views.profesor_buscar,name='profesor_buscar'),
    
    path('cliente/', views.ClienteIndexListView.as_view(), name="cliente_index_view"),
    path('cliente/nuevo/', views.ClienteNuevoView.as_view(), name="cliente_nuevo_view"),
    path('cliente/editar/<int:pk>', views.ClienteUpdateView.as_view(), name="cliente_editar_view"),
    path('cliente/eliminar/<int:pk>', views.ClienteDeleteView.as_view(), name="cliente_eliminar_view"),
    path('cliente/buscar/', views.cliente_buscar,name='cliente_buscar'),

    path('mensajes', ListadoMensajes.as_view(), name="listar_mensajes"),
    path('mensajes/eliminar/<int:pk>', EliminarMensaje.as_view(), name="eliminar_mensaje"),
    path('mensajes/buscar/', buscar_mensaje,name='mensajes_buscar'),
]