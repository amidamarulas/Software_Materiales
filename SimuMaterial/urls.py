from django.contrib import admin
from django.urls import include
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Bienvenido a CoreLab 👋</h1><p>Simulación interactiva de materiales y ensayos.</p>")


urlpatterns = [
    path('', include('core_lab.urls')),
    path("", home),
    path("admin/", admin.site.urls),
    path("api/lab/", include("core_lab.urls")),  # ✅ Única app activa
]
