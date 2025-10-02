# SimuMaterial

Software en Django para simulación de pruebas mecánicas de materiales.

## Instrucciones

1. Clonar este repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar base de datos PostgreSQL en `SimuMaterial/settings.py`
4. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```
5. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

## Apps
- materials: CRUD de materiales
- simulations: gestión de simulaciones y generación de resultados
- users: autenticación y roles (admin, investigador, estudiante)
