#!/bin/bash
echo "🧬 Configurando app central 'core_lab' para SimuMaterial..."

PROJECT_DIR=$(pwd)
APP_NAME="core_lab"
PROJECT_NAME="SimuMaterial"

cd "$PROJECT_DIR" || exit

# 1️⃣ Crear app si no existe
if [ ! -d "$APP_NAME" ]; then
  echo "📦 Creando app '$APP_NAME'..."
  python manage.py startapp "$APP_NAME"
else
  echo "ℹ️  App '$APP_NAME' ya existe."
fi

# 2️⃣ Asegurar que la app esté en settings.py
SETTINGS_FILE="$PROJECT_NAME/settings.py"
if ! grep -q "'$APP_NAME'," "$SETTINGS_FILE"; then
  echo "📦 Agregando '$APP_NAME' a INSTALLED_APPS..."
  sed -i "/'rest_framework',/a\ \ \ \ '$APP_NAME'," "$SETTINGS_FILE"
else
  echo "✅ '$APP_NAME' ya está en INSTALLED_APPS."
fi

# 3️⃣ Crear estructura básica de urls, serializers y views
echo "🧩 Generando archivos básicos..."

cat > "$APP_NAME/urls.py" << 'EOF'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet, SimulationViewSet

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='materials')
router.register(r'simulations', SimulationViewSet, basename='simulations')

urlpatterns = [
    path('', include(router.urls)),
]
EOF

cat > "$APP_NAME/views.py" << 'EOF'
from rest_framework import viewsets
from app_materials.models import Material
from app_simulations.models import Simulation
from .serializers import MaterialSerializer, SimulationSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
EOF

cat > "$APP_NAME/serializers.py" << 'EOF'
from rest_framework import serializers
from app_materials.models import Material
from app_simulations.models import Simulation

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'
EOF

# 4️⃣ Registrar rutas en SimuMaterial/urls.py
URLS_FILE="$PROJECT_NAME/urls.py"
if grep -q "include('lab_core.urls')" "$URLS_FILE"; then
  echo "🩹 Corrigiendo import incorrecto (lab_core → core_lab)..."
  sed -i "s/include('lab_core.urls')/include('core_lab.urls')/g" "$URLS_FILE"
fi

if ! grep -q "include('core_lab.urls')" "$URLS_FILE"; then
  echo "🧭 Registrando rutas en SimuMaterial/urls.py..."
  sed -i "/urlpatterns = \[/a\ \ \ \ path('api/lab/', include('core_lab.urls'))," "$URLS_FILE"
else
  echo "✅ Las rutas ya estaban registradas."
fi

# 5️⃣ Ejecutar migraciones
echo "⚙️  Ejecutando migraciones..."
python manage.py makemigrations "$APP_NAME"
python manage.py migrate

echo "✅ Configuración completada con éxito."
echo "🚀 Ejecuta: python manage.py runserver"
echo "🌍 Luego abre:"
echo "   👉 http://127.0.0.1:8000/api/lab/materials/"
echo "   👉 http://127.0.0.1:8000/api/lab/simulations/"
