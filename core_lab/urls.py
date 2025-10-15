from django.urls import path
from . import views

app_name = "core_lab"

urlpatterns = [
    # ✨ Nueva ruta para la simulación como página principal ✨
    path('', views.simulacion, name='home'), # Ahora '/' renderiza la vista 'simulacion'
    
    # Si quieres que '/simulacion/' siga funcionando, puedes añadirlo de nuevo,
    # pero apuntando a la misma vista de simulación. Por ahora, lo mantenemos como la principal.
    # path('simulacion/', views.simulacion, name='simulacion'), # Opcional, si quieres la ruta /simulacion/ también

    path('materiales/', views.materiales, name='materiales'), # Tu vista de materiales
    path('plot.png', views.plot_png, name='plot_png'),
    path('download/data.csv', views.download_csv, name='download_csv'),
]