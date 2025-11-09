import os
import sys
import django
import pandas as pd

# ===========================================
# 🔧 CONFIGURACIÓN DEL ENTORNO DJANGO
# ===========================================
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimuMaterial.settings")
django.setup()

from materials.models import Material, Resultado

# ===========================================
# 📂 CONFIGURACIÓN DE ARCHIVOS CSV
# ===========================================
CARPETA_DATOS = os.path.join("materials", "data")

if not os.path.exists(CARPETA_DATOS):
    print(f"❌ La carpeta '{CARPETA_DATOS}' no existe. Verifica la ruta.")
    sys.exit(1)

# ===========================================
# 🚀 CARGA DE DATOS A LA BASE DE DATOS
# ===========================================
for archivo in os.listdir(CARPETA_DATOS):
    if not archivo.endswith(".csv"):
        continue

    ruta = os.path.join(CARPETA_DATOS, archivo)
    print(f"\n📥 Cargando datos desde: {archivo}")

    try:
        df = pd.read_csv(ruta)
    except Exception as e:
        print(f"⚠️ Error al leer {archivo}: {e}")
        continue

    # ==============================
    # 🧱 Crear o recuperar el material
    # ==============================
    nombre_material = archivo.replace(".csv", "").strip()
    material, creado = Material.objects.get_or_create(nombre=nombre_material)

    if creado:
        print(f"🆕 Material agregado: {material.nombre}")
    else:
        print(f"♻️ Material ya existía: {material.nombre}")

    columnas = df.columns.tolist()

    # ==============================
    # 🔍 Detección automática del tipo de ensayo
    # ==============================
    if all(col in columnas for col in ["Strain", "Stress(Pa)"]):
        tipo = "tension/compresion"
        x_col = "Strain"
        y_col = "Stress(Pa)"
    elif all(col in columnas for col in ["Curvature(1/m)", "Moment(N·m/m)"]):
        tipo = "flexion"
        x_col = "Curvature(1/m)"
        y_col = "Moment(N·m/m)"
    else:
        print(f"⚠️ Columnas no reconocidas en {archivo}: {columnas}")
        continue

    # ==============================
    # 🧾 Evitar duplicados
    # ==============================
    existentes = Resultado.objects.filter(material=material).count()
    if existentes > 0:
        print(f"⚠️ {existentes} registros existentes encontrados para {material.nombre}. Se agregarán nuevos.")
    
    # ==============================
    # 💾 Insertar registros
    # ==============================
    registros_creados = 0
    nuevos_resultados = []
    for _, fila in df.iterrows():
        nuevos_resultados.append(Resultado(
            material=material,
            deformacion=fila[x_col],
            esfuerzo=fila[y_col],
            tiempo=None,
            temperatura=None
        ))

    Resultado.objects.bulk_create(nuevos_resultados)
    registros_creados = len(nuevos_resultados)

    print(f"✅ {registros_creados} registros cargados para {nombre_material} ({tipo})")

print("\n🎉 Todos los materiales y resultados se cargaron correctamente en db.sqlite3")
