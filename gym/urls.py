from django.urls import path
from . import views

urlpatterns = [
    path ('', views.home, name="home"),
    path ('contacto/', views.contacto, name="contacto"),
    path ('actividades/', views.actividades, name="actividades"),
    path ('serializar/', views.get_actividades_json, name="get_actividades_json"),
]