from django.contrib import admin
from .models import Usuario, Producto, SeleccionDiaria
# Register your models here.

admin.site.register(Usuario)
# Registra el modelo Usuario en el panel de administración.

admin.site.register(Producto)
# Registra el modelo Producto en el panel de administración.

admin.site.register(SeleccionDiaria)
# Registra el modelo SeleccionDiaria en el panel de administración.