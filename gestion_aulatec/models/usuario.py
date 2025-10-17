from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin #importar para Autenticación

#Personalizamos la creación de usuarios.
class CustomUserManager(BaseUserManager):
    def create_user(self, NumId, password=None, **extra_fields):
        if not NumId:
            raise ValueError('El número de identificación debe ser proporcionado.')
        user = self.model(NumId=NumId , **extra_fields) # Crea el usuario con NumId
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, NumId, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('Rol', 'Administrador')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Llama a create_user con 'num_id' como el primer argumento posicional
        # y luego pasa el resto de los extra_fields.
        # 'createsuperuser' de Django lo espera así cuando USERNAME_FIELD es el primer argumento.
        return self.create_user(NumId, password, **extra_fields)
    
#Modelo tabla usuarios.
class Usuario(AbstractBaseUser, PermissionsMixin): # Hereda de AbstractBaseUser y PermissionsMixin
    IdUsuario = models.AutoField(primary_key=True)
    TipoId = models.CharField(max_length=20)
    NumId = models.CharField(max_length=10, unique=True)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    # Contrasena ya no se define aquí directamente, AbstractBaseUser la maneja
    Rol = models.CharField(max_length=50)
    Celular = models.CharField(max_length=20, blank=True, null=True)

    # Campos requeridos por AbstractBaseUser (para el admin de Django, etc.)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager() # Asigna tu CustomUserManager

    USERNAME_FIELD = 'NumId' # Campo que se usará para el login (nombre de usuario)
    REQUIRED_FIELDS = ['TipoId', 'Nombres', 'Apellidos', 'Rol'] # Campos requeridos al crear superusuario

    def __str__(self):
        return f"{self.Nombres} {self.Apellidos} ({self.Rol})"

    # Métodos necesarios para PermissionsMixin si no usas los grupos y permisos de Django directamente
    # (aunque PermissionsMixin los provee, si solo usas el campo Rol, puedes ignorar estos para el login)
    
    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser # O implementa lógica de rol más compleja

    def has_module_perms(self, app_label):
        return self.is_active and self.is_superuser # O implementa lógica de rol más compleja

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'