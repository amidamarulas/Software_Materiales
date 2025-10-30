from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    modulo_elasticidad = models.FloatField(help_text="Módulo de Young en Pa")
    limite_elastico = models.FloatField(help_text="Límite elástico en Pa")
    resistencia_maxima = models.FloatField(help_text="Resistencia máxima en Pa")
    deformacion_maxima = models.FloatField(help_text="Deformación máxima en %")
    densidad = models.FloatField(help_text="Densidad en kg/m³", blank=True, null=True)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("metal", "Metal"),
            ("polimero", "Polímero"),
            ("ceramico", "Cerámico"),
            ("compuesto", "Compuesto"),
        ],
        default="metal"
    )

    def __str__(self):
        return self.nombre
