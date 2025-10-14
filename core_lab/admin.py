from django.contrib import admin
from .models import Material, Ensayo, Simulacion

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

@admin.register(Ensayo)
class EnsayoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'descripcion']

@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'material', 'ensayo', 'fecha_creacion']
    readonly_fields = ['fecha_creacion']
