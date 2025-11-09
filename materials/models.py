from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Resultado(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    deformacion = models.FloatField()
    esfuerzo = models.FloatField()
    tiempo = models.FloatField(null=True, blank=True)
    temperatura = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.material.nombre} - ε={self.deformacion}, σ={self.esfuerzo}"
