#!/bin/bash
echo "🔬 Configurando app central 'lab_core' para SimuMaterial..."
echo "📁 Directorio actual: $(pwd)"

# 1️⃣ Crear app central
python manage.py startapp lab_core

# 2️⃣ Instalar dependencias necesarias
echo "📦 Instalando dependencias..."
pip install djangorestframework --quiet

# 3️⃣ Agregar app al settings.py
echo "⚙️  Modificando SimuMaterial/settings.py..."
SETTINGS_FILE="SimuMaterial/settings.py"
if grep -q "lab_core" "$SETTINGS_FILE"; then
    echo "✅ 'lab_core' ya está en INSTALLED_APPS"
else
    sed -i "/'django.contrib.staticfiles',/a\    'rest_framework',\n    'lab_core'," "$SETTINGS_FILE"
fi

# 4️⃣ Crear modelos
echo "🧱 Creando models.py..."
cat > lab_core/models.py << 'EOF'
from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    densidad = models.FloatField()
    elasticidad = models.FloatField()
    resistencia = models.FloatField()

    def __str__(self):
        return self.nombre


class Simulacion(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="simulaciones")
    tipo_prueba = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.JSONField()

    def __str__(self):
        return f"{self.tipo_prueba} - {self.material.nombre}"
EOF

# 5️⃣ Crear serializers
echo "📜 Creando serializers.py..."
cat > lab_core/serializers.py << 'EOF'
from rest_framework import serializers
from .models import Material, Simulacion

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class SimulacionSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    class Meta:
        model = Simulacion
        fields = '__all__'
EOF

# 6️⃣ Crear views
echo "👁️  Creando views.py..."
cat > lab_core/views.py << 'EOF'
from rest_framework import viewsets
from .models import Material, Simulacion
from .serializers import MaterialSerializer, SimulacionSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class SimulacionViewSet(viewsets.ModelViewSet):
    queryset = Simulacion.objects.all()
    serializer_class = SimulacionSerializer
EOF

# 7️⃣ Crear urls
echo "🌐 Creando urls.py..."
cat > lab_core/urls.py << 'EOF'
from rest_framework import routers
from .views import MaterialViewSet, SimulacionViewSet

router = routers.DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'simulations', SimulacionViewSet)

urlpatterns = router.urls
EOF

# 8️⃣ Conectar rutas globales
echo "🔗 Agregando rutas al proyecto principal..."
sed -i "/from django.urls import path/a\from django.urls import include" SimuMaterial/urls.py
if ! grep -q "lab_core.urls" SimuMaterial/urls.py; then
    sed -i "/urlpatterns = \[/a\    path('api/lab/', include('lab_core.urls'))," SimuMaterial/urls.py
fi

# 9️⃣ Migrar base de datos
echo "🧩 Ejecutando migraciones..."
python manage.py makemigrations lab_core
python manage.py migrate

echo "✅ Configuración completada con éxito."
echo "🚀 Ejecuta: python manage.py runserver"
echo "🌍 Luego abre:"
echo "   👉 http://127.0.0.1:8000/api/lab/materials/"
echo "   👉 http://127.0.0.1:8000/api/lab/simulations/"
