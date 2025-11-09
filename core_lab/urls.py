# core_lab/urls.py
from django.urls import path
from . import views

app_name = "core_lab"

urlpatterns = [
    # Página principal: simulación
    path('', views.simulacion, name='home'),

    # Páginas del sistema
    path('simulacion/', views.simulacion, name='simulacion'),
    path('materiales/', views.materiales, name='materiales'),

    # Gráfico y descarga (placeholders)
    path('plot.png', views.plot_png, name='plot_png'),
    path('download/data.csv', views.download_csv, name='download_csv'),

    # 🔹 Endpoint para obtener datos reales desde la base de datos
    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
]

