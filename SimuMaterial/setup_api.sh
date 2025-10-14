#!/bin/bash
# =====================================
# Script automático para crear la API REST
# Compatible con ejecución desde cualquier ruta
# =====================================

# Determinar la ruta raíz del proyecto (un nivel arriba del script)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT" || exit

echo "📁 Ruta del proyecto: $PROJECT_ROOT"
echo "🔧 Creando archivos de serializers, views y urls para las apps..."

# --- app_materials ---
cat > app_materials/serializers.py << 'PYCODE'
from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
PYCODE

cat > app_materials/views.py << 'PYCODE'
from rest_framework import viewsets
from .models import Material
from .serializers import MaterialSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
PYCODE

cat > app_materials/urls.py << 'PYCODE'
from rest_framework import routers
from .views import MaterialViewSet

router = routers.DefaultRouter()
router.register(r'materials', MaterialViewSet)

urlpatterns = router.urls
PYCODE


# --- app_simulations ---
cat > app_simulations/serializers.py << 'PYCODE'
from rest_framework import serializers
from .models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'
PYCODE

cat > app_simulations/views.py << 'PYCODE'
from rest_framework import viewsets
from .models import Simulation
from .serializers import SimulationSerializer

class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
PYCODE

cat > app_simulations/urls.py << 'PYCODE'
from rest_framework import routers
from .views import SimulationViewSet

router = routers.DefaultRouter()
router.register(r'simulations', SimulationViewSet)

urlpatterns = router.urls
PYCODE


# --- urls.py global ---
cat > SimuMaterial/urls.py << 'PYCODE'
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_materials.urls')),
    path('api/', include('app_simulations.urls')),
]
PYCODE


echo "✅ Archivos creados correctamente."
echo "⚙️  Ejecutando migraciones..."

python manage.py makemigrations
python manage.py migrate

echo "🚀 API configurada correctamente. Ejecuta:"
echo "python manage.py runserver"
echo "Luego abre: http://127.0.0.1:8000/api/materials/ o /api/simulations/"
