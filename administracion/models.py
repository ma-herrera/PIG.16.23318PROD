from django.db import models

# from rest_framework import serializers

# agregar baja logica en los registros que no se pueden eliminar físicamente
# si paso mas de cierto tiempo que no paguen que se desactiven automaticamente
# tener algun proceso que los elimine físicamente validando que ya estén inactivos
class TipoDeActividad(models.Model):
    """
    Clasificación de las Actividades.
    """

    # Campos
    nombre = models.CharField(max_length=40, verbose_name= "nombre", help_text="Nombre de la actividad")
    titulo = models.CharField(max_length=40, verbose_name= "título", help_text="Título para usar en páginas", null=True, default=None)
    subtitulo = models.CharField(max_length=40, verbose_name= "subtítulo", help_text="Subtítulo para usar en páginas", null=True, default=None)
    descripcion = models.CharField(max_length=200, verbose_name= "descripción", help_text="Texto descriptivo de la actividad", null=True, default=None)
    imagen_de_portada = models.ImageField(upload_to='imagenes/',null=True, verbose_name='Portada', help_text='Imagen para la portada')

    # Metadata
    class Meta:
        verbose_name = "tipo de actividad"
        verbose_name_plural = "tipos de actividad"
        ordering = ["nombre"]

    # Métodos
    # def get_absolute_url(self):
    #      """
    #      Devuelve la url para acceder a una instancia particular de MyModelName.
    #      """
    #      return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto TipoDeActividad (en el sitio de Admin, etc.)
        """
        return self.nombre
    
    def delete(self,using=None,keep_parents=False):
        self.imagen_de_portada.storage.delete(self.imagen_de_portada.name) #borrado fisico
        super().delete()
    #################################################################################

class TipoDocumento(models.Model):
    """
    Tipos de documento
    """
    tipoDocumento = models.CharField(max_length=5, primary_key=True, verbose_name="Tipo de documento", help_text="Tipo de documento")
    descripcion =  models.CharField(max_length=40, verbose_name="Descripción")

    def __str__(self):
        """
        Cadena para representar el objeto TipoDeDocumento (en el sitio de Admin, etc.)
        """
        return self.descripcion

    class Meta:
        verbose_name = "tipo de documento"
        verbose_name_plural = "tipos de documento"


class Persona (models.Model):
    """
    Datos personales
    """
    apellido = models.CharField(max_length=30, verbose_name="Apellido", help_text="apellido")
    nombre = models.CharField(max_length=40, verbose_name="Nombre", help_text="nombre")
    tipoDocumento = models.ForeignKey(TipoDocumento, on_delete=models.RESTRICT)
    numeroDocumento = models.IntegerField(verbose_name="Número de documento", help_text="Número de documento")
    telefono = models.CharField(max_length=20, verbose_name="Número de teléfono", help_text="Código de área y número de teléfono (sólo números)")
    email = models.EmailField(verbose_name="E-mail", help_text="Dirección de correo electrónico")
    coberturaMedica = models.CharField(max_length=40, verbose_name="Cobertura médica", help_text="Empresa y plan de la cobertura médica", null=True, default=None)
    numeroAfiliado = models.CharField(max_length=15, verbose_name="Número de afiliado", help_text="Número de afiliado de la cobertura médica (sólo números)", null=True, default=None)

    def __str__(self):
        """
        Cadena para representar el objeto Persona (en el sitio de Admin, etc.)
        """
        return 'nombre: {}, apellido: {}, tipo de documento: {}, email: {}'.format(self.nombre, self.apellido, self.tipoDocumento.descripcion, self.email)

    class Meta:
        abstract = True

class Profesor(Persona):
    # corregir para que sea un campo mumerico pero que acepte un cuil (el integer no alcanza)
    cuil = models.CharField(max_length=11, verbose_name="Cuil", help_text="Cuil (sin guiones)")
    fechaAlta = models.DateField(verbose_name="Fecha de contratación")
    fechaBaja = models.DateField(null=True, blank=True, verbose_name="Fecha de baja")

    def __str__(self):
        return "{}, fecha de alta: {}".format(super().__str__(), self.fechaAlta)

    class Meta:
        verbose_name = "profesor"
        verbose_name_plural = "profesores"



class Cliente(Persona):
    fechaAlta = models.DateField(verbose_name="Fecha de alta")
    fechaBaja = models.DateField(null=True, blank=True, verbose_name="Fecha de baja")
    paseLibre = models.BooleanField(verbose_name="Tiene pase libre?", help_text="Tiene pase libre? S/N")
    fechaPagoPaseLibre = models.DateField(null=True, blank=True, verbose_name="Última fecha de pago del pase libre")
    aptoFisico = models.BooleanField(verbose_name="Apto físico", help_text="Presenta apto físico? S/N")

    def __str__(self):
        return "{}, pase libre: {}, fecha de alta: {}".format(super().__str__(), self.paseLibre, self.fechaAlta)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"



# through Inscripcion detalla los campos para luego poder tener una constraint unique sobre el par Actividad, Cliente
class Actividad(models.Model):
    tipoDeActividad = models.ForeignKey(TipoDeActividad, on_delete=models.CASCADE)
    tarifa = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="tarifa", help_text="tarifa")
    fechaDeInicio = models.DateField(verbose_name="Fecha de inicio", help_text="fecha de inicio de clases")
    cupo = models.PositiveIntegerField(verbose_name="cupo", help_text="cantidad máxima de alumnos")
    fechaDeBaja = models.DateField(null=True, blank=True, verbose_name="Fecha de baja")
    profesor = models.ForeignKey(Profesor, verbose_name="id del profesor", on_delete=models.RESTRICT)
    clientes = models.ManyToManyField(
        Cliente,
        through="Inscripcion",
        through_fields=("actividad", "cliente")
        )

    def __str__(self):
        # return self.tipoDeActividad + ", tarifa: " + self.tarifa + ", fecha de inicio: " + self.fechaDeInicio + ", cupo: " + self.cupo + ", profesor: " + self.profesor
        return ("{} {}, fecha de inicio: {} cupo: {}, profesor: {}".format(self.tipoDeActividad.pk, self.tipoDeActividad, self.fechaDeInicio, self.cupo, self.profesor))

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"



class Inscripcion(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fechaDeInscripcion = models.DateField(verbose_name="fecha de inscripcion", help_text="fecha de inscripcion")
    fechaDeInscripcion = models.DateField(verbose_name="fecha de pago", help_text="última fecha de pago de la cuota")
    bonificacion = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="porcentaje de bonificación sobe la cuota mensual", help_text="porcentaje de bonificación sobe la cuota mensual")

    def __str__(self):
        return ("actividad: {}, cliente: {}, fecha de inscripcion: {}, bonificación: {}".format(self.actividad.tipoDeActividad.nombre, self.cliente, self.fechaDeInscripcion, self.bonificacion))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['actividad', 'cliente'], name='unique_actividad_cliente'
                )
        ]
        verbose_name = "inscripción"
        verbose_name_plural = "inscripciones"
           
           
class Horario(models.Model):
    DIAS_SEMANA = [
        ("lu", "lunes"),
        ("ma", "martes"),
        ("mi", "miércoles"),
        ("ju", "jueves"),
        ("vi", "viernes"),
        ("sa", "sábado"),
        ("do", "domingo"),
    ]
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    dia = models.CharField(max_length=2, choices=DIAS_SEMANA)
    horaInicio = models.TimeField(verbose_name="hora de inicio de la clase")
    horaFin = models.TimeField(verbose_name="hora de finalización de la clase")
    def __str__(self):
        return ("{}, {}, {} a {}".format(self.actividad.tipoDeActividad.nombre, self.dia, self.horaInicio,self.horaFin))

    class Meta:
        verbose_name = "horario"
        verbose_name_plural = "horarios"
