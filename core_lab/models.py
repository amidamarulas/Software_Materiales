from django.db import models
from django.utils import timezone

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Ensayo(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipo


class Simulacion(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    resultados = models.JSONField(default=dict)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Simulación {self.id} - {self.material.nombre}"
