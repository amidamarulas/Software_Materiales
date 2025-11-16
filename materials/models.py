# en materials/models.py
from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Módulo de Young en Pascales (Pa)
    young_modulus_e = models.FloatField()
    # Límite elástico en Pascales (Pa)
    yield_strength_sy = models.FloatField()
    # Coeficiente de Poisson (adimensional)
    poisson_ratio_v = models.FloatField()
    # ... otros campos que necesites ...

    def __str__(self):
        return self.name
