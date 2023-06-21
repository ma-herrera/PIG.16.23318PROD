from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    asunto = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre
