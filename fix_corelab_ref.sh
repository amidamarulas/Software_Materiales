#!/bin/bash
echo "🔧 Corrigiendo 'app_corelab' -> 'core_lab' en settings.py y urls.py..."

sed -i 's/app_corelab/core_lab/g' SimuMaterial/settings.py
sed -i 's/app_corelab/core_lab/g' SimuMaterial/urls.py

echo "✅ Corrección aplicada. Ahora ejecuta:"
echo "python manage.py runserver 8001"
