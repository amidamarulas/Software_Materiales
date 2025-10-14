#!/usr/bin/env bash
set -euo pipefail

APP="core_lab"
TEMPLATES_DIR="$APP/templates/$APP"
STATIC_CSS_DIR="$APP/static/$APP/css"
STATIC_JS_DIR="$APP/static/$APP/js"

echo "🔧 Creando placeholders de UI para CoreLab..."

# Crear directorios
mkdir -p "$TEMPLATES_DIR"
mkdir -p "$STATIC_CSS_DIR"
mkdir -p "$STATIC_JS_DIR"

# 1) Template principal (inicio) - index.html
cat > "$TEMPLATES_DIR/index.html" <<'HTML'
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>CoreLab - Simulador de Materiales</title>
  <link rel="stylesheet" href="{% static 'core_lab/css/style.css' %}">
</head>
<body>
  <nav class="topbar">
    <div class="brand">CoreLab</div>
    <div class="menu">
      <a href="{% url 'core_lab:home' %}">Inicio</a>
      <a href="#materials">Materiales</a>
      <a href="#simulation">Simulación</a>
      <a href="#graficas">Gráficas</a>
      <a href="/admin/">Admin</a>
    </div>
  </nav>

  <header class="hero">
    <h1>Bienvenido a CoreLab 👋</h1>
    <p class="lead">
      CoreLab es una herramienta pedagógica para aprender cómo las propiedades de los materiales
      afectan el comportamiento en ensayos (tracción, compresión, torsión, fatiga...). Comprender
      estas propiedades es clave para diseñar piezas seguras y eficientes.
    </p>
    <p class="muted">En este entorno podrás seleccionar materiales, ejecutar simulaciones y visualizar resultados.</p>
  </header>

  <main class="container">
    <!-- MATERIALS -->
    <section id="materials" class="card">
      <h2>Materiales</h2>
      <p>Tabla de materiales (vacía ahora; se llenará desde la base de datos):</p>
      <table id="materials-table" class="table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Densidad (kg/m³)</th>
            <th>Módulo E (Pa)</th>
            <th>Resistencia (Pa)</th>
            <th>Descripción</th>
          </tr>
        </thead>
        <tbody>
          <!-- placeholder vacío -->
        </tbody>
      </table>
      <div class="hint">(Los materiales se cargarán aquí desde la BD)</div>
    </section>

    <!-- SIMULATION -->
    <section id="simulation" class="card">
      <h2>Máquina universal de ensayos — 2D (placeholder)</h2>
      <p>Selecciona material y tipo de ensayo. La zona de la probeta es interactiva (placeholder para futuras físicas).</p>

      <div class="sim-row">
        <div class="sim-canvas" id="sim-canvas">
          <!-- Aquí se dibujará la máquina/probeta 2D con JS (placeholder) -->
          <svg id="machine-svg" width="480" height="260" style="background:#f7f9fc;border-radius:8px">
            <!-- Ejemplo visual simple -->
            <rect x="10" y="10" width="460" height="240" fill="transparent" stroke="#e6eefc"></rect>
            <text x="240" y="40" font-size="14" text-anchor="middle" fill="#333">Máquina Universal (2D) - placeholder</text>
            <!-- probeta placeholder -->
            <rect id="specimen" x="200" y="100" width="80" height="40" fill="#fff" stroke="#0b5ed7" rx="4" ry="4"></rect>
          </svg>
        </div>

        <div class="sim-controls">
          <label>Material:
            <select id="sim-material">
              <option value="">-- seleccionar --</option>
              {% for m in materiales %}
                <option value="{{ m.id }}">{{ m.nombre }}</option>
              {% endfor %}
            </select>
          </label>

          <label>Ensayo:
            <select id="sim-type">
              <option value="traccion">Tracción</option>
              <option value="compresion">Compresión</option>
              <option value="torsion">Torsión</option>
              <option value="fatiga">Fatiga</option>
            </select>
          </label>

          <div class="controls">
            <button id="btn-start" class="btn">Iniciar (placeholder)</button>
            <button id="btn-reset" class="btn secondary">Reset</button>
          </div>
        </div>
      </div>

      <h3>Tabla de datos (resultados) — vacío por ahora</h3>
      <table id="data-table" class="table">
        <thead>
          <tr><th>Tiempo</th><th>Deformación</th><th>Esfuerzo</th></tr>
        </thead>
        <tbody><!-- vacío --></tbody>
      </table>
    </section>

    <!-- GRAPHS -->
    <section id="graficas" class="card">
      <h2>Gráficas</h2>
      <p>La gráfica se genera con matplotlib desde el servidor (placeholder sin datos).</p>

      <div class="graph-area">
        <img id="plot-img" src="{% url 'core_lab:plot_png' %}" alt="Gráfica placeholder"/>
      </div>

      <div class="download-row">
        <a id="download-plot" class="btn" href="{% url 'core_lab:plot_png' %}?download=1">Descargar gráfica (PNG)</a>
        <a id="download-csv" class="btn secondary" href="{% url 'core_lab:download_csv' %}">Descargar datos (CSV)</a>
      </div>
    </section>
  </main>

  <footer class="footer">
    <p>© 2025 CoreLab — Laboratorio Virtual de Materiales (educativo)</p>
  </footer>

  <script src="{% static 'core_lab/js/ui_placeholders.js' %}"></script>
</body>
</html>
HTML

# 2) CSS (estilos básicos)
cat > "$STATIC_CSS_DIR/style.css" <<'CSS'
:root{
  --bg:#f5f8ff;
  --accent:#0b5ed7;
  --card:#ffffff;
  --muted:#6b7280;
}
*{box-sizing:border-box}
body{font-family:Inter, system-ui, -apple-system,"Segoe UI",Roboto,Arial;margin:0;background:var(--bg);color:#111}
.topbar{display:flex;justify-content:space-between;padding:12px 24px;background:var(--accent);color:#fff}
.topbar .brand{font-weight:700}
.topbar .menu a{color:#fff;margin-left:12px;text-decoration:none}
.hero{padding:28px;text-align:center;background:linear-gradient(90deg, rgba(11,78,215,0.95), rgba(3,37,77,0.95));color:#fff}
.container{max-width:1100px;margin:20px auto;display:grid;grid-template-columns:1fr;gap:16px;padding:0 16px}
.card{background:var(--card);padding:16px;border-radius:10px;box-shadow:0 8px 20px rgba(12,20,40,0.06)}
.table{width:100%;border-collapse:collapse;margin-top:8px}
.table th,.table td{border:1px solid #e6eefc;padding:8px;text-align:left}
.sim-row{display:flex;gap:12px;align-items:flex-start}
.sim-canvas{flex:1}
.sim-controls{width:260px;display:flex;flex-direction:column;gap:8px}
label{display:block;margin-bottom:6px}
select{width:100%;padding:8px;border-radius:6px;border:1px solid #d1d5db}
.btn{background:var(--accent);color:#fff;padding:8px 12px;border-radius:8px;text-decoration:none;border:none;cursor:pointer}
.btn.secondary{background:#eef2ff;color:#111}
.graph-area img{max-width:100%;border-radius:8px;background:#fff}
.footer{text-align:center;padding:16px;color:var(--muted);font-size:0.9rem}
.hint{margin-top:8px;color:var(--muted)}
@media(max-width:900px){ .sim-row{flex-direction:column} .sim-controls{width:100%} }
CSS

# 3) JS placeholder (interactividad mínima)
cat > "$STATIC_JS_DIR/ui_placeholders.js" <<'JS'
document.addEventListener('DOMContentLoaded', function(){
  const btnStart = document.getElementById('btn-start');
  const btnReset = document.getElementById('btn-reset');
  const specimen = document.getElementById('specimen');
  const dataTableBody = document.querySelector('#data-table tbody');

  btnStart?.addEventListener('click', ()=>{
    // Animación placeholder: estirar probeta (simple transform)
    specimen.animate([{transform:'scaleY(1)'},{transform:'scaleY(1.5)'}],{duration:600,fill:'forwards'});
    // Añadir fila placeholder a la tabla de datos
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>0.0</td><td>—</td><td>—</td>`;
    if (dataTableBody) dataTableBody.appendChild(tr);
  });

  btnReset?.addEventListener('click', ()=>{
    specimen.style.transform = 'none';
    if (dataTableBody) dataTableBody.innerHTML = '';
  });
});
JS

# 4) Views: agregar endpoints para plot PNG y CSV
VIEWS_FILE="$APP/views.py"
if [ -f "$VIEWS_FILE" ]; then
  cp "$VIEWS_FILE" "${VIEWS_FILE}.bak"
fi

cat > "$VIEWS_FILE" <<'PY'
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Material, Ensayo, Simulacion
import io
import csv
import matplotlib
matplotlib.use('Agg')  # backend sin GUI
import matplotlib.pyplot as plt

def home(request):
    materiales = Material.objects.all().order_by('nombre')
    ensayos = Ensayo.objects.all().order_by('tipo')
    return render(request, 'core_lab/index.html', {'materiales': materiales, 'ensayos': ensayos})

def plot_png(request):
    """
    Genera una imagen PNG con matplotlib (placeholder).
    Si se pasa ?download=1 se fuerza Content-Disposition para descarga.
    """
    # Placeholder: figura vacía con ejes y texto "sin datos"
    fig, ax = plt.subplots(figsize=(6,3.5))
    ax.set_title("Esfuerzo - Deformación (placeholder)")
    ax.set_xlabel("Deformación")
    ax.set_ylabel("Esfuerzo (Pa)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.text(0.5,0.5,"Sin datos aún", ha='center', va='center', transform=ax.transAxes, fontsize=14, color='gray')
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    resp = HttpResponse(buf.getvalue(), content_type='image/png')
    if request.GET.get('download') == '1':
        resp['Content-Disposition'] = 'attachment; filename="corelab_plot_placeholder.png"'
    return resp

def download_csv(request):
    """
    Genera un CSV vacío con cabeceras para descarga.
    """
    headers = ['tiempo','deformacion','esfuerzo']
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    # no rows (vacío por ahora)
    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="corelab_data_placeholder.csv"'
    return resp
PY

# 5) URLs: asegurar rutas locales
URLS_FILE="$APP/urls.py"
cat > "$URLS_FILE" <<'PY'
from django.urls import path
from . import views

app_name = "core_lab"

urlpatterns = [
    path('', views.home, name='home'),
    path('plot.png', views.plot_png, name='plot_png'),
    path('download/data.csv', views.download_csv, name='download_csv'),
]
PY

echo "✅ Archivos creados/actualizados:"
echo "  - Template: $TEMPLATES_DIR/index.html"
echo "  - CSS: $STATIC_CSS_DIR/style.css"
echo "  - JS: $STATIC_JS_DIR/ui_placeholders.js"
echo "  - Views: $VIEWS_FILE (backup saved .bak if existed)"
echo "  - URLs: $URLS_FILE"

echo
echo "Siguientes pasos:"
echo "1) Asegúrate de que 'core_lab' esté en INSTALLED_APPS."
echo "2) Reinicia el servidor Django:"
echo "   python manage.py runserver"
echo
echo "Navega a: http://127.0.0.1:8000/api/core_lab/  (si ese es el include que tengas)"
echo "o a la raíz si tu project urls apunta a core_lab como home."
echo
echo "Nota: Todo está en modo placeholder (vacío). Cuando quieras, conectamos la lógica para llenar la tabla, generar simulaciones y poblar la gráfica."
