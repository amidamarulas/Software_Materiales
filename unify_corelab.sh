#!/bin/bash
set -e

echo "🧬 Unificando el proyecto en una sola app 'core_lab'..."

# Ruta del settings.py principal
SETTINGS_FILE="SimuMaterial/settings.py"

if [ ! -f "$SETTINGS_FILE" ]; then
  echo "❌ No se encontró SimuMaterial/settings.py. Asegúrate de estar en la raíz del proyecto."
  exit 1
fi

echo "📁 Usando archivo de configuración: $SETTINGS_FILE"

# 1️⃣ Asegurar que 'core_lab' esté en INSTALLED_APPS
if ! grep -q '"core_lab"' "$SETTINGS_FILE"; then
  sed -i '/INSTALLED_APPS = \[/a\    "core_lab",' "$SETTINGS_FILE"
  echo "✅ Agregada 'core_lab' a INSTALLED_APPS"
else
  echo "ℹ️  'core_lab' ya estaba en INSTALLED_APPS"
fi

# 2️⃣ Eliminar apps viejas
sed -i '/"app_materials"/d' "$SETTINGS_FILE"
sed -i '/"app_simulations"/d' "$SETTINGS_FILE"

# 3️⃣ Borrar carpetas antiguas si existen
for app in app_materials app_simulations; do
  if [ -d "$app" ]; then
    rm -rf "$app"
    echo "🗑️  Eliminada carpeta antigua: $app"
  fi
done

# 4️⃣ Ejecutar migraciones de core_lab
echo "⚙️  Ejecutando migraciones..."
python3 manage.py makemigrations core_lab
python3 manage.py migrate

# 5️⃣ Confirmar unificación
echo "✅ Proyecto unificado correctamente bajo 'core_lab'."
echo "🚀 Ejecuta ahora: python3 manage.py runserver 8001"
echo "🌍 Luego abre:"
echo "   👉 http://127.0.0.1:8001/api/lab/materials/"
echo "   👉 http://127.0.0.1:8001/api/lab/simulations/"
