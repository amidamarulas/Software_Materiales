from rest_framework import serializers
from core_lab.models import Material
from core_lab.models import Simulation

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'
