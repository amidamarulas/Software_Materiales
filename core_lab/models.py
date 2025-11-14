# Es importante importar TestCase para usar la base de datos de prueba
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

# Importa los modelos que vas a probar
# El '.' asume que tests.py y models.py están en la misma app
from .models import Material, Ensayo, Simulacion

class ModelTests(TestCase):
    """
    Suite de pruebas para los modelos Material, Ensayo y Simulacion.
    """

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Es ideal para crear objetos que se usarán en múltiples tests.
        """
        self.material_acero = Material.objects.create(
            nombre="Acero AISI 1045",
            descripcion="Acero al carbono de alta resistencia."
        )
        self.ensayo_tension = Ensayo.objects.create(
            tipo="Tensión",
            descripcion="Ensayo para medir la resistencia de un material a una fuerza de estiramiento."
        )

    def test_material_model(self):
        """Prueba la creación y representación de un objeto Material."""
        material = self.material_acero
        
        # Verificar que el objeto fue creado y los campos son correctos
        self.assertEqual(material.nombre, "Acero AISI 1045")
        self.assertEqual(material.descripcion, "Acero al carbono de alta resistencia.")
        
        # Verificar que el método __str__ funciona como se espera
        self.assertEqual(str(material), "Acero AISI 1045")
        print(f"OK - test_material_model: {str(material)}")

    def test_ensayo_model(self):
        """Prueba la creación y representación de un objeto Ensayo."""
        ensayo = self.ensayo_tension
        
        # Verificar que el objeto fue creado y los campos son correctos
        self.assertEqual(ensayo.tipo, "Tensión")
        self.assertEqual(ensayo.descripcion, "Ensayo para medir la resistencia de un material a una fuerza de estiramiento.")
        
        # Verificar que el método __str__ funciona como se espera
        self.assertEqual(str(ensayo), "Tensión")
        print(f"OK - test_ensayo_model: {str(ensayo)}")

    def test_simulacion_model(self):
        """Prueba la creación y los valores por defecto de un objeto Simulacion."""
        # Datos de ejemplo para el campo JSON
        resultados_data = {
            "fuerza_maxima": 550,
            "unidad_fuerza": "MPa",
            "deformacion_unitaria": 0.15
        }

        simulacion = Simulacion.objects.create(
            material=self.material_acero,
            ensayo=self.ensayo_tension,
            resultados=resultados_data
        )

        # 1. Verificar las relaciones (ForeignKey)
        self.assertEqual(simulacion.material, self.material_acero)
        self.assertEqual(simulacion.material.nombre, "Acero AISI 1045")
        self.assertEqual(simulacion.ensayo, self.ensayo_tension)
        self.assertEqual(simulacion.ensayo.tipo, "Tensión")

        # 2. Verificar el campo JSONField
        self.assertEqual(simulacion.resultados["fuerza_maxima"], 550)
        self.assertEqual(simulacion.resultados["unidad_fuerza"], "MPa")

        # 3. Verificar el valor por defecto de la fecha de creación
        # Comprobamos que la fecha está dentro de un rango razonable (ej. último minuto)
        # para evitar fallos por milisegundos de diferencia.
        ahora = timezone.now()
        self.assertTrue(ahora - timedelta(minutes=1) < simulacion.fecha_creacion < ahora + timedelta(minutes=1))

        # 4. Verificar el método __str__
        self.assertEqual(str(simulacion), f"Simulación {simulacion.id} - Acero AISI 1045")
        print(f"OK - test_simulacion_model: {str(simulacion)}")

    def test_simulacion_resultados_default(self):
        """
        Prueba que el valor por defecto del campo 'resultados' es un diccionario vacío.
        """
        simulacion_sin_resultados = Simulacion.objects.create(
            material=self.material_acero,
            ensayo=self.ensayo_tension
        )
        
        # Verificar que el campo 'resultados' es un diccionario vacío por defecto
        self.assertEqual(simulacion_sin_resultados.resultados, {})
        print(f"OK - test_simulacion_resultados_default: {simulacion_sin_resultados.resultados}")