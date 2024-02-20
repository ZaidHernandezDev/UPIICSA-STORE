from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Usuario(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Relación uno a uno con el modelo de usuario predeterminado de Django
    whatsapp = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=10)], unique=True, null=False)  # NOT NULL    
    # Campo para almacenar el número de WhatsApp con validadores de longitud mínima y máxima, y único.

    # Propiedades para acceder al nombre y apellido del usuario de forma más sencilla.  
    @property
    def nombre(self):
        return self.usuario.first_name

    @property
    def apellido(self):
        return self.usuario.last_name
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    # Definición del modelo Producto con sus atributos.
class Producto(models.Model):
    PRODUCTO_GRUPO_CHOISES =[
        ('postres','Postres'),
        ('comida_rapida','Comida rápida'),
        ('dulces','Dulces'),
        ('ensaladas','Ensaladas'),
        ('desayunos','Desayunos'),
        ('antojitos','Antojitos')
    ]
    # Campos del modelo Producto
    nombreProd = models.CharField(max_length=25, null=False)  # NOT NULL
    descProd = models.TextField(null=False)  # NOT NULL
    precioProd = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # NOT NULL
    disponibilidad = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="", default="default.png", null=False)  # NOT NULL
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='productos', null=False)  # NOT NULL
    grupo = models.CharField(max_length=15, choices=PRODUCTO_GRUPO_CHOISES,default="postres")

    def __str__(self):
        return f"{self.nombreProd} ({self.grupo})"

class SeleccionDiaria(models.Model):
    fecha_seleccion = models.DateField(unique=True, null=False)  # NOT NULL
    productos = models.ManyToManyField(Producto, related_name='seleccion_diaria')

