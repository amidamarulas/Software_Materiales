#!/bin/bash
# Script para crear proyecto Django SimuMaterial
# Kevin Andrés Cruz Velandia

# Crear proyecto Django
django-admin startproject SimuMaterial
cd SimuMaterial

# Crear apps
python3 manage.py startapp materials
python3 manage.py startapp simulations
python3 manage.py startapp users

# Crear directorios adicionales
mkdir -p templates/static templates/simulations plots

# Crear requirements.txt
cat <<EOT > requirements.txt
Django>=5.0
psycopg2-binary
plotly
matplotlib
pandas
reportlab
EOT

# Crear LICENSE (MIT)
cat <<EOT > LICENSE
MIT License

Copyright (c) 2025 Kevin Andrés Cruz Velandia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
EOT

# Crear README.md
cat <<EOT > README.md
# SimuMaterial

Software en Django para simulación de pruebas mecánicas de materiales.

## Instrucciones

1. Clonar este repositorio
2. Instalar dependencias:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. Configurar base de datos PostgreSQL en \`SimuMaterial/settings.py\`
4. Ejecutar migraciones:
   \`\`\`bash
   python manage.py migrate
   \`\`\`
5. Crear superusuario:
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`
6. Ejecutar servidor:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

## Apps
- materials: CRUD de materiales
- simulations: gestión de simulaciones y generación de resultados
- users: autenticación y roles (admin, investigador, estudiante)
EOT

# Crear models.py en materials
cat <<EOT > materials/models.py
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
EOT

# Crear models.py en simulations
cat <<EOT > simulations/models.py
from django.db import models
from django.contrib.auth.models import User
from materials.models import Material

class Simulacion(models.Model):
    TIPO_PRUEBA = [
        ("traccion", "Tracción"),
        ("compresion", "Compresión"),
        ("dureza", "Dureza"),
        ("fatiga", "Fatiga"),
        ("flexion", "Flexión"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    tipo_prueba = models.CharField(max_length=20, choices=TIPO_PRUEBA)
    fecha = models.DateTimeField(auto_now_add=True)
    resultados = models.JSONField()

    def __str__(self):
        return f"{self.tipo_prueba} - {self.material.nombre} - {self.fecha}"
EOT

# Crear models.py en users
cat <<EOT > users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = [
        ("admin", "Administrador"),
        ("investigador", "Investigador"),
        ("estudiante", "Estudiante"),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default="estudiante")
EOT

# Crear simulación ejemplo (tracción)
mkdir -p simulations/sims
cat <<EOT > simulations/sims/traction.py
import numpy as np
import plotly.graph_objects as go

def simulate_tension(material):
    strain = np.linspace(0, 0.2, 200)
    stress = np.minimum(material.modulo_elasticidad * strain, material.resistencia_traccion)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strain, y=stress, mode="lines", name="Esfuerzo-Deformación"))
    fig.update_layout(title=f"Curva Tracción - {material.nombre}",
                      xaxis_title="Deformación",
                      yaxis_title="Esfuerzo (MPa)")
    return fig.to_html(), {
        "modulo_elasticidad": material.modulo_elasticidad,
        "limite_elastico": material.limite_elastico,
        "resistencia_traccion": material.resistencia_traccion,
    }
EOT

# Crear fixtures iniciales (3 materiales de ejemplo)
mkdir -p materials/fixtures
cat <<EOT > materials/fixtures/materiales.json
[
    {
        "model": "materials.material",
        "pk": 1,
        "fields": {
            "nombre": "Acero A36",
            "densidad": 7850,
            "modulo_elasticidad": 200000,
            "limite_elastico": 250,
            "resistencia_traccion": 400,
            "dureza": 120
        }
    },
    {
        "model": "materials.material",
        "pk": 2,
        "fields": {
            "nombre": "Aluminio 6061",
            "densidad": 2700,
            "modulo_elasticidad": 69000,
            "limite_elastico": 275,
            "resistencia_traccion": 310,
            "dureza": 95
        }
    },
    {
        "model": "materials.material",
        "pk": 3,
        "fields": {
            "nombre": "Titanio Ti-6Al-4V",
            "densidad": 4430,
            "modulo_elasticidad": 113000,
            "limite_elastico": 880,
            "resistencia_traccion": 950,
            "dureza": 349
        }
    }
]
EOT

echo "✅ Proyecto SimuMaterial creado con éxito."

