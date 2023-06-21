from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombre,apellido,documento,password):
        if not email:
            raise ValueError('El usuario debe tener una casilla de correo')
        usuario = self.model(username = username,
                             email = self.normalize_email(email),
                             nombre=nombre,
                             apellido=apellido,
                             documento=documento,
                             )
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, email,username,nombre,apellido,documento,password):
        usuario = self.create_user(
                            email,
                            username = username,
                            nombre=nombre,
                            apellido=apellido,
                            documento=documento,
                            password=password
                            )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True, max_length=20)
    email= models.EmailField('Casilla de correo', unique=True, max_length=254)
    nombre= models.CharField('Nombre', max_length=50)
    apellido= models.CharField('Apellido', max_length=50, blank=True)
    documento= models.CharField('Documento',max_length=8, unique=True,blank=True)
    # genero=models.CharField('Genero', max_length=20, blank=True)
    # telefono = models.CharField('Telefono',max_length=20,blank=True)
    # fecha_nacimiento=models.DateField('Fecha de nacimiento', blank=True)
    # cobertura_medica = models.CharField('Cobertura Medica',max_length=40, blank=True,null=True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank=True,default=None)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador= models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre', 'apellido','documento']

    def __str__(self):
        return f'Usuario{self.nombre},{self.apellido}'
    
    def has_perm(self,perm,obj =None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


