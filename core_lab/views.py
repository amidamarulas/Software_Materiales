from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Material, Ensayo, Simulacion
import io
import csv
import matplotlib
matplotlib.use('Agg')  # backend sin GUI
import matplotlib.pyplot as plt
from django.shortcuts import render

def simulacion(request):
    return render(request, 'core_lab/simulacion.html')

def materiales(request):
    return render(request, 'core_lab/materiales.html')

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
