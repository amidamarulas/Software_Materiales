from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    densidad = models.FloatField()
    modulo_elasticidad = models.FloatField()
    limite_elastico = models.FloatField()
    resistencia_traccion = models.FloatField()
    dureza = models.FloatField()

    def __str__(self):
        return self.nombre

# Create your models here.
