# ==========================================================
#  core_lab/views.py - VERSIÓN FINALÍSIMA Y COMPLETA
# ==========================================================

import os, io, csv, json, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material, Ensayo, Simulacion

# ============================================================
#  VISTAS PRINCIPALES (TODAS LAS FUNCIONES RESTAURADAS)
# ============================================================

def simulacion(request):
    materiales = Material.objects.all().order_by('nombre')
    ensayos = Ensayo.objects.all().order_by('tipo')
    return render(request, 'core_lab/simulacion.html', {'materiales': materiales, 'ensayos': ensayos})

def materiales(request):
    return render(request, 'core_lab/materiales.html')

def home(request):
    materiales = Material.objects.all().order_by('nombre')
    ensayos = Ensayo.objects.all().order_by('tipo')
    return render(request, 'core_lab/index.html', {
        'materiales': materiales,
        'ensayos': ensayos
    })

def plot_png(request):
    # ¡ESTA ERA LA FUNCIÓN QUE FALTABA!
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_title("Esfuerzo - Deformación (placeholder)")
    ax.set_xlabel("Deformación")
    ax.set_ylabel("Esfuerzo (Pa)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.text(0.5, 0.5, "Sin datos aún", ha='center', va='center',
            transform=ax.transAxes, fontsize=14, color='gray')
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
    # ¡Y ESTA TAMBIÉN!
    headers = ['tiempo', 'deformacion', 'esfuerzo']
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="corelab_data_placeholder.csv"'
    return resp

# ============================================================
#  API PARA OBTENER DATOS (VERSIÓN ROBUSTA)
# ============================================================
@csrf_exempt
def obtener_datos(request):
    material_nombre = request.GET.get('material')
    tipo_ensayo = request.GET.get('tipo_ensayo')

    if not material_nombre or not tipo_ensayo:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    nombre_archivo = f"{material_nombre}_{tipo_ensayo.lower()}.csv"
    ruta_archivo = os.path.join(settings.BASE_DIR, 'materials', 'data', nombre_archivo)

    try:
        df = pd.read_csv(ruta_archivo, header=None)
        num_columnas = len(df.columns)
        
        if num_columnas == 3:
            df.columns = ['tiempo', 'deformacion', 'esfuerzo']
        elif num_columnas == 2:
            df.columns = ['deformacion', 'esfuerzo']
            df.insert(0, 'tiempo', [i * 0.1 for i in range(len(df))])
        else:
            raise ValueError(f"Formato de archivo inesperado con {num_columnas} columnas.")

        datos_grafica = [{'x': row['deformacion'], 'y': row['esfuerzo']} for _, row in df.iterrows()]
        datos_tabla = df.to_dict(orient='records')
        
        return JsonResponse({
            'success': True,
            'datos_grafica': datos_grafica,
            'datos_tabla': datos_tabla,
            'eje_x_label': 'Deformación (%)',
            'eje_y_label': 'Esfuerzo (Pa)',
        })
    except FileNotFoundError:
        mensaje_error = f'No se encontró el archivo: {nombre_archivo}'
        return JsonResponse({'error': mensaje_error, 'success': False}, status=404)
    except Exception as e:
        mensaje_error = f'Error al procesar el archivo: {str(e)}'
        return JsonResponse({'error': mensaje_error, 'success': False}, status=500)