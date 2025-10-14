from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('simulacion/', views.simulacion, name='simulacion'),
    path('materiales/', views.materiales, name='materiales'),
]

app_name = "core_lab"

urlpatterns = [
    path('', views.home, name='home'),
    path('plot.png', views.plot_png, name='plot_png'),
    path('download/data.csv', views.download_csv, name='download_csv'),
]
