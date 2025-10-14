#!/bin/bash
# ==============================================
# Script: fix_home_route.sh
# Autor: Kevin Andrés Cruz Velandia
# Descripción: Añade una vista raíz "home" en Django
# para evitar error 404 en http://127.0.0.1:8001/
# ==============================================

PROJECT_DIR="SimuMaterial"
APP_DIR="app_materials"

echo "==> Corrigiendo URLs en $PROJECT_DIR/urls.py ..."

# 1️⃣ Añadimos una vista base "home" si no existe
grep -q "def home(request)" "$PROJECT_DIR/urls.py" || cat >> "$PROJECT_DIR/urls.py" << 'EOF'

from django.http import HttpResponse

def home(request):
    return HttpResponse("<h2>Servidor de simulación de materiales funcionando correctamente 🚀</h2>")
EOF

# 2️⃣ Reescribimos el bloque de urlpatterns
sed -i '/urlpatterns = \[/,/\]/c\urlpatterns = [\
    path("", home),\
    path("admin/", admin.site.urls),\
    path("api/", include("app_materials.urls")),\
]' "$PROJECT_DIR/urls.py"

echo "✅ URLs corregidas exitosamente."
echo "==> Iniciando servidor en http://127.0.0.1:8001/"
python3 manage.py runserver 8001
