from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Profesor
from .models import TipoDocumento
from .models import Cliente
from .models import Horario
from .models import TipoDeActividad
from .models import Actividad
from .models import Inscripcion
from gym.models import Contacto



admin.site.register(TipoDocumento)
admin.site.register(Cliente)
admin.site.register(Profesor)
admin.site.register(Horario)
admin.site.register(TipoDeActividad)
admin.site.register(Actividad)
admin.site.register(Inscripcion)
admin.site.register(Contacto)

class GymAdminSite(admin.AdminSite):
    site_header = 'Powerful Gym'
    site_title = 'Administración Powerful Gym'
    index_title = 'Administración Powerful Gym'
    empty_values_display = 'No hay registros para mostrar'

# Personalización del CRUD de Actividad
#Las inscripciones se muestran como campo ManyToMany
class InscripcionInline(admin.TabularInline):
    model = Inscripcion

class HorarioInline(admin.TabularInline):
    model = Horario


class ActividadAdmin(admin.ModelAdmin):
    inlines = [
        HorarioInline,
        InscripcionInline,
    ]

sitio_admin = GymAdminSite(name = "gymadmin")
sitio_admin.register(Actividad, ActividadAdmin)
sitio_admin.register(TipoDocumento)
sitio_admin.register(Cliente)
sitio_admin.register(Profesor)
sitio_admin.register(Horario)
sitio_admin.register(TipoDeActividad)
sitio_admin.register(Inscripcion)
sitio_admin.register(Contacto)