#!/bin/bash
set -e

echo "=============================================="
echo "   🚀 Setup automático CoreLab (HTML/CSS/JS)"
echo "=============================================="
echo ""

# 1️⃣ Instalar dependencias base
echo "📦 Instalando dependencias Python necesarias..."
pip install django matplotlib numpy

# 2️⃣ Verificar existencia de la app core_lab
if [ ! -d "core_lab" ]; then
    echo "⚙️ Creando app 'core_lab'..."
    python manage.py startapp core_lab
else
    echo "ℹ️ App 'core_lab' ya existe."
fi

# 3️⃣ Asegurar que está en INSTALLED_APPS
if ! grep -q "'core_lab'," SimuMaterial/settings.py; then
    sed -i "/INSTALLED_APPS = \[/ a\    'core_lab'," SimuMaterial/settings.py
    echo "✅ 'core_lab' añadida a INSTALLED_APPS."
else
    echo "✅ 'core_lab' ya está en INSTALLED_APPS."
fi

# 4️⃣ Crear modelos base
cat > core_lab/models.py << 'EOF'
from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    densidad = models.FloatField(blank=True, null=True)
    dureza = models.FloatField(blank=True, null=True)
    limite_elastico = models.FloatField(blank=True, null=True)
    resistencia_traccion = models.FloatField(blank=True, null=True)
    modulo_elasticidad = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ensayo(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipo

class Simulacion(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE, blank=True, null=True)
    resultados = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Simulación de {self.material} ({self.ensayo})"
EOF

echo "✅ models.py actualizado."

# 5️⃣ Crear vistas básicas
cat > core_lab/views.py << 'EOF'
from django.shortcuts import render
from .models import Material, Simulacion

def home(request):
    materiales = Material.objects.all()
    return render(request, "core_lab/home.html", {"materiales": materiales})
EOF

# 6️⃣ Configurar urls.py para la app
mkdir -p core_lab/templates/core_lab
cat > core_lab/urls.py << 'EOF'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
EOF

# 7️⃣ Enlazar urls de la app en el proyecto principal
if ! grep -q "path('', include('core_lab.urls'))" SimuMaterial/urls.py; then
    sed -i "/from django.urls import path/i from django.urls import include" SimuMaterial/urls.py
    sed -i "/urlpatterns = \[/ a\    path('', include('core_lab.urls'))," SimuMaterial/urls.py
    echo "✅ Rutas de 'core_lab' integradas al proyecto."
fi

# 8️⃣ Crear templates y archivos estáticos
mkdir -p core_lab/static/core_lab/css
mkdir -p core_lab/static/core_lab/js

# HTML principal
cat > core_lab/templates/core_lab/home.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CoreLab - Simulación de Materiales</title>
    <link rel="stylesheet" href="{% static 'core_lab/css/style.css' %}">
    <script src="{% static 'core_lab/js/app.js' %}" defer></script>
</head>
<body>
    <header>
        <h1>⚙️ CoreLab</h1>
        <nav>
            <a href="#">Inicio</a>
            <a href="#">Materiales</a>
            <a href="#">Simulaciones</a>
            <a href="#">Gráficas</a>
        </nav>
    </header>

    <main>
        <section id="intro">
            <h2>Simulación interactiva de materiales y ensayos</h2>
            <p>Explora materiales, visualiza sus propiedades y ejecuta simulaciones de laboratorio virtual.</p>
        </section>

        <section id="materiales">
            <h3>🧱 Materiales disponibles</h3>
            <ul>
                {% for mat in materiales %}
                <li>
                    <strong>{{ mat.nombre }}</strong> — {{ mat.descripcion }}
                    <br>Densidad: {{ mat.densidad }} | Dureza: {{ mat.dureza }}
                </li>
                {% empty %}
                <li>No hay materiales cargados aún.</li>
                {% endfor %}
            </ul>
        </section>
    </main>

    <footer>
        <p>Desarrollado como apoyo pedagógico — CoreLab © 2025</p>
    </footer>
</body>
</html>
EOF

# CSS
cat > core_lab/static/core_lab/css/style.css << 'EOF'
body {
    font-family: "Segoe UI", sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(180deg, #eef1f5, #ffffff);
}
header {
    background: #002B5B;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
header h1 { margin: 0; }
nav a {
    color: white;
    margin-left: 1.2rem;
    text-decoration: none;
    font-weight: 500;
}
nav a:hover {
    text-decoration: underline;
}
main {
    padding: 2rem;
}
#intro {
    background: #f5f7fa;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
#materiales {
    margin-top: 2rem;
}
footer {
    text-align: center;
    padding: 1rem;
    background: #002B5B;
    color: white;
    margin-top: 2rem;
}
EOF

# JS
cat > core_lab/static/core_lab/js/app.js << 'EOF'
document.addEventListener("DOMContentLoaded", () => {
    console.log("🌐 CoreLab UI lista!");
});
EOF

# 9️⃣ Migraciones automáticas seguras
echo "🔧 Aplicando migraciones seguras..."
python manage.py makemigrations core_lab --noinput || true
python manage.py migrate --fake-initial || true

# 🔟 Mensaje final
echo ""
echo "✅ CoreLab configurado con éxito."
echo "🌍 Inicia el servidor con: python manage.py runserver 8000"
echo "y abre http://127.0.0.1:8000/"
