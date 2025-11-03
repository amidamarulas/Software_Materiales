from django.contrib import admin
from .models import Material, Ensayo, Simulacion

# Panel de administración de materiales
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'modulo_elasticidad', 'limite_elastico')
    search_fields = ('nombre', 'tipo')

# Panel de administración de ensayos
@admin.register(Ensayo)
class EnsayoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'descripcion')
    search_fields = ('tipo', )

# Panel de administración de simulaciones
@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'ensayo', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)
    list_filter = ('material', 'ensayo')
