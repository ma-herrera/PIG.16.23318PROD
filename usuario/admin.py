from django.contrib import admin
from usuario.models import Usuario
from django.contrib.auth.models import Permission

admin.site.register(Usuario)
admin.site.register(Permission)
