from django.db import models
from django.contrib.auth.models import User
from app_materials.models import Material

class Simulation(models.Model):
    TIPO_PRUEBA = [
        ('traccion', 'Tracción'),
        ('compresion', 'Compresión'),
        ('dureza', 'Dureza'),
        ('fatiga', 'Fatiga'),
        ('flexion', 'Flexión'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    tipo_prueba = models.CharField(max_length=20, choices=TIPO_PRUEBA)
    fecha = models.DateTimeField(auto_now_add=True)
    resultados = models.JSONField()

    def __str__(self):
        return f"{self.tipo_prueba} - {self.material.nombre}"
