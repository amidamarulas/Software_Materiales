from django.shortcuts import render
from .models import Material, Simulacion

def home(request):
    materiales = Material.objects.all()
    return render(request, "core_lab/home.html", {"materiales": materiales})
