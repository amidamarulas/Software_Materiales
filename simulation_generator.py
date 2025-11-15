import sqlite3
import csv
import os
import unittest
from pathlib import Path

# --- CONFIGURACIÓN ---
# Asume que la base de datos de Django está en la raíz del proyecto.
# Cámbiala si tu db.sqlite3 está en otro lugar.
DB_PATH = Path(__file__).parent / 'db.sqlite3'

# Directorio de salida para los CSV, relativo a la raíz del proyecto.
OUTPUT_DIR = Path(__file__).parent / 'materials' / 'data'

# Nombre de la tabla de materiales en la base de datos de Django.
# Usualmente es 'nombreapp_nombremodelo'. Ajusta si es diferente.
MATERIALS_TABLE = 'materials_material' 

# --- CLASE PRINCIPAL DEL SIMULADOR ---

class MaterialSimulator:
    """
    Genera datos de simulación para materiales leídos desde una base de datos SQLite.
    """
    def __init__(self, db_path, output_dir):
        """
        Inicializa el simulador con las rutas necesarias.

        Args:
            db_path (Path): Ruta al archivo de la base de datos SQLite.
            output_dir (Path): Ruta al directorio donde se guardarán los CSV.
        """
        if not isinstance(db_path, Path) or not isinstance(output_dir, Path):
            raise TypeError("db_path y output_dir deben ser objetos Path de pathlib.")
        
        self.db_path = db_path
        self.output_dir = output_dir
        self.connection = None

    def _connect_db(self):
        """Establece la conexión a la base de datos."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def _close_db(self):
        """Cierra la conexión a la base de datos si está abierta."""
        if self.connection:
            self.connection.close()

    def fetch_materials(self) -> list[dict]:
        """
        Obtiene todos los materiales y sus propiedades de la base de datos.
        
        Returns:
            Una lista de diccionarios, donde cada diccionario representa un material.
        """
        self._connect_db()
        try:
            cursor = self.connection.cursor()
            # Asumiendo los nombres de las columnas. ¡Ajusta si los tuyos son diferentes!
            query = f"SELECT name, young_modulus_e, yield_strength_sy, poisson_ratio_v FROM {MATERIALS_TABLE}"
            cursor.execute(query)
            materials = [dict(row) for row in cursor.fetchall()]
            if not materials:
                print("Advertencia: No se encontraron materiales en la base de datos.")
            return materials
        except sqlite3.Error as e:
            print(f"Error al leer la tabla de materiales: {e}")
            print(f"Asegúrate de que la tabla '{MATERIALS_TABLE}' existe y tiene las columnas correctas.")
            return []
        finally:
            self._close_db()

    @staticmethod
    def _generate_tension_data(e_modulus, yield_strength, points=200, max_strain=0.3):
        """
        Genera datos de una curva de esfuerzo-deformación por tensión.
        Modelo simplificado con región elástica y endurecimiento lineal.
        """
        if e_modulus <= 0 or yield_strength <= 0:
            return [], []
        
        strain_data = [0.0]
        stress_data = [0.0]
        
        # Región elástica
        yield_strain = yield_strength / e_modulus
        elastic_points = int(points * (yield_strain / max_strain))
        
        for i in range(1, elastic_points):
            strain = i * (yield_strain / elastic_points)
            stress = e_modulus * strain
            strain_data.append(strain)
            stress_data.append(stress)

        # Región plástica (endurecimiento lineal simplificado)
        hardening_modulus = e_modulus * 0.05 # 5% del módulo de Young
        for i in range(elastic_points, points):
            strain = i * (max_strain / points)
            stress = yield_strength + hardening_modulus * (strain - yield_strain)
            strain_data.append(strain)
            stress_data.append(stress)
            
        return strain_data, stress_data

    @staticmethod
    def _generate_compression_data(e_modulus, points=200, max_strain=0.05):
        """
        Genera datos de una curva de esfuerzo-deformación por compresión.
        Modelo elástico lineal simple como en el archivo de ejemplo.
        """
        if e_modulus <= 0:
            return [], []

        strain = [i * (max_strain / points) for i in range(points + 1)]
        # El esfuerzo en compresión es negativo
        stress = [-e_modulus * s for s in strain]
        return strain, stress

    @staticmethod
    def _generate_flexion_data(e_modulus, yield_strength, points=200, max_curvature=0.02):
        """
        Genera datos de una curva Momento-Curvatura para flexión.
        Modelo elasto-plástico perfecto simplificado.
        """
        if e_modulus <= 0 or yield_strength <= 0:
            return [], []

        # Suponemos una viga rectangular para calcular un momento plástico M_p relativo
        # Esto es una simplificación, ya que no tenemos la geometría.
        plastic_moment = 1.5 * yield_strength 
        
        # La rigidez a la flexión es E*I. Como no tenemos I, hacemos el momento proporcional a E.
        flexural_rigidity = e_modulus * 0.01 
        
        yield_curvature = plastic_moment / flexural_rigidity
        
        curvature_data = [0.0]
        moment_data = [0.0]

        # Región elástica
        if yield_curvature < max_curvature:
            elastic_points = int(points * (yield_curvature / max_curvature))
            for i in range(1, elastic_points):
                curvature = i * (yield_curvature / elastic_points)
                moment = flexural_rigidity * curvature
                curvature_data.append(curvature)
                moment_data.append(moment)

            # Región plástica (momento constante)
            for i in range(elastic_points, points + 1):
                curvature = i * (max_curvature / points)
                curvature_data.append(curvature)
                moment_data.append(plastic_moment)
        else: # Si el material es muy rígido y no fluye en el rango
             for i in range(1, points + 1):
                curvature = i * (max_curvature / points)
                moment = flexural_rigidity * curvature
                curvature_data.append(curvature)
                moment_data.append(moment)

        return curvature_data, moment_data

    def _save_to_csv(self, filename: Path, headers: list, data_rows: list):
        """Guarda los datos generados en un archivo CSV."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            filepath = self.output_dir / filename
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data_rows)
            print(f"Archivo guardado exitosamente: {filepath}")
        except IOError as e:
            print(f"Error al escribir el archivo {filename}: {e}")

    def run_all_simulations(self):
        """
        Ejecuta todas las simulaciones para todos los materiales de la DB
        y guarda los resultados en archivos CSV.
        """
        materials = self.fetch_materials()
        if not materials:
            print("No se encontraron materiales para simular.")
            return

        for material in materials:
            name = material.get('name', 'UnknownMaterial').replace(' ', '_')
            e_modulus = material.get('young_modulus_e', 0)
            yield_strength = material.get('yield_strength_sy', 0)

            if e_modulus == 0 or yield_strength == 0:
                print(f"Saltando material '{name}' por falta de propiedades (Módulo E o Límite Elástico).")
                continue

            print(f"\n--- Generando simulaciones para: {name} ---")
            
            # 1. Simulación de Tensión
            strain_t, stress_t = self._generate_tension_data(e_modulus, yield_strength)
            self._save_to_csv(
                Path(f"{name}_tension.csv"),
                ["Strain", "Stress(Pa)"],
                zip(strain_t, stress_t)
            )

            # 2. Simulación de Compresión
            strain_c, stress_c = self._generate_compression_data(e_modulus)
            self._save_to_csv(
                Path(f"{name}_compresion.csv"),
                ["Strain", "Stress(Pa)"],
                zip(strain_c, stress_c)
            )

            # 3. Simulación de Flexión
            curvature_f, moment_f = self._generate_flexion_data(e_modulus, yield_strength)
            self._save_to_csv(
                Path(f"{name}_flexion.csv"),
                ["Curvature(1/m)", "Moment(N·m/m)"],
                zip(curvature_f, moment_f)
            )

# --- SUITE DE PRUEBAS UNITARIAS ---

class TestMaterialSimulator(unittest.TestCase):
    
    def setUp(self):
        """Configura un entorno de prueba con una BD en memoria y un dir temporal."""
        self.db_conn = sqlite3.connect(":memory:")
        self.cursor = self.db_conn.cursor()
        
        # Crear tabla y datos de prueba
        self.cursor.execute(f"""
            CREATE TABLE {MATERIALS_TABLE} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                young_modulus_e REAL NOT NULL,
                yield_strength_sy REAL NOT NULL,
                poisson_ratio_v REAL NOT NULL
            )
        """)
        self.cursor.execute(
            f"INSERT INTO {MATERIALS_TABLE} (name, young_modulus_e, yield_strength_sy, poisson_ratio_v) VALUES (?, ?, ?, ?)",
            ("Test_Steel", 200e9, 250e6, 0.3)
        )
        self.db_conn.commit()

        # Usar un directorio temporal para los archivos CSV de prueba
        self.temp_dir = Path("temp_test_output")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Mock de la ruta de la base de datos para que el simulador use la de memoria
        # Esto es complejo, una forma más fácil es pasar la conexión directamente.
        # Por simplicidad, crearemos un archivo temporal de DB.
        self.test_db_path = Path("test_db.sqlite3")
        with sqlite3.connect(self.test_db_path) as temp_db_conn:
            self.db_conn.backup(temp_db_conn)

        self.simulator = MaterialSimulator(self.test_db_path, self.temp_dir)

    def tearDown(self):
        """Limpia los recursos de prueba."""
        self.db_conn.close()
        os.remove(self.test_db_path)
        for f in self.temp_dir.glob('*.csv'):
            os.remove(f)
        os.rmdir(self.temp_dir)

    def test_fetch_materials(self):
        """Verifica que los materiales se leen correctamente de la BD."""
        materials = self.simulator.fetch_materials()
        self.assertEqual(len(materials), 1)
        self.assertEqual(materials[0]['name'], 'Test_Steel')
        self.assertEqual(materials[0]['young_modulus_e'], 200e9)

    def test_run_all_simulations_creates_files(self):
        """Verifica que se crean los 3 archivos CSV para un material."""
        self.simulator.run_all_simulations()
        
        self.assertTrue((self.temp_dir / "Test_Steel_tension.csv").exists())
        self.assertTrue((self.temp_dir / "Test_Steel_compresion.csv").exists())
        self.assertTrue((self.temp_dir / "Test_Steel_flexion.csv").exists())
        
    def test_tension_csv_content(self):
        """Verifica el contenido básico del CSV de tensión."""
        self.simulator.run_all_simulations()
        
        with open(self.temp_dir / "Test_Steel_tension.csv", 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, ["Strain", "Stress(Pa)"])
            first_row = next(reader)
            # El primer punto debe ser (0.0, 0.0)
            self.assertEqual(float(first_row[0]), 0.0)
            self.assertEqual(float(first_row[1]), 0.0)


# --- PUNTO DE ENTRADA DEL SCRIPT ---

def setup_initial_database():
    """Función de ayuda para crear y poblar la base de datos si no existe."""
    if DB_PATH.exists():
        return # No hacer nada si ya existe
        
    print("Creando base de datos inicial 'db.sqlite3' con datos de ejemplo...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE {MATERIALS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            young_modulus_e REAL NOT NULL,
            yield_strength_sy REAL NOT NULL,
            poisson_ratio_v REAL NOT NULL
        )
    """)
    # Insertar algunos polímeros de ejemplo
    polymers = [
        ('HDPE', 1.0e9, 25e6, 0.4),
        ('Polycarbonate', 2.4e9, 60e6, 0.37),
        ('ABS', 2.0e9, 40e6, 0.35)
    ]
    cursor.executemany(
        f"INSERT INTO {MATERIALS_TABLE} (name, young_modulus_e, yield_strength_sy, poisson_ratio_v) VALUES (?, ?, ?, ?)",
        polymers
    )
    conn.commit()
    conn.close()
    print("Base de datos creada y poblada.")


if __name__ == "__main__":
    
    print("--- SCRIPT DE GENERACIÓN DE SIMULACIONES DE MATERIALES ---")
    
    # 1. (Opcional) Configurar la base de datos si es la primera vez que se ejecuta
    setup_initial_database()

    # 2. Ejecutar las simulaciones
    print("\n[MODO: GENERACIÓN DE SIMULACIONES]")
    simulator = MaterialSimulator(DB_PATH, OUTPUT_DIR)
    simulator.run_all_simulations()
    
    # 3. Ejecutar las pruebas unitarias
    print("\n[MODO: PRUEBAS UNITARIAS]")
    # Cargamos las pruebas de la clase y las ejecutamos
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMaterialSimulator))
    runner = unittest.TextTestRunner()
    runner.run(suite)