import csv
from django.core.management.base import BaseCommand, CommandError
from materials.models import Material  # Asegúrate que tu modelo se llame 'Material'

class Command(BaseCommand):
    """
    Comando de gestión de Django para poblar la base de datos de materiales
    desde un archivo CSV.
    """
    help = 'Carga datos de materiales desde un archivo CSV a la base de datos'

    def add_arguments(self, parser):
        """
        Añade un argumento posicional al comando para especificar la ruta del archivo.
        """
        parser.add_argument('csv_file_path', type=str, help='La ruta del archivo CSV a importar.')

    def handle(self, *args, **options):
        """
        La lógica principal del comando.
        """
        file_path = options['csv_file_path']
        
        self.stdout.write(self.style.SUCCESS(f'Iniciando la importación desde el archivo: {file_path}'))

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                # Usamos DictReader para poder acceder a las columnas por su nombre de cabecera
                reader = csv.DictReader(csvfile)
                
                # Listas para llevar un registro de lo que se hace
                nuevos_materiales = []
                materiales_existentes = []

                for row in reader:
                    # 'get_or_create' es la forma más segura de añadir datos.
                    # Intenta obtener un material con el nombre dado.
                    # Si no lo encuentra, lo crea con los valores en 'defaults'.
                    # Esto evita crear duplicados si ejecutas el comando varias veces.
                    material, created = Material.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'young_modulus_e': float(row['young_modulus_e']),
                            'yield_strength_sy': float(row['yield_strength_sy']),
                            'poisson_ratio_v': float(row['poisson_ratio_v']),
                        }
                    )

                    if created:
                        nuevos_materiales.append(material.name)
                        self.stdout.write(f'  - Creado material: {material.name}')
                    else:
                        materiales_existentes.append(material.name)
                        self.stdout.write(self.style.WARNING(f'  - El material "{material.name}" ya existe. Saltando.'))

            self.stdout.write(self.style.SUCCESS(
                f'\n¡Proceso finalizado! Se añadieron {len(nuevos_materiales)} materiales nuevos.'
            ))
            if materiales_existentes:
                self.stdout.write(self.style.WARNING(
                    f'Se omitieron {len(materiales_existentes)} materiales que ya existían.'
                ))

        except FileNotFoundError:
            raise CommandError(f'Error: El archivo en la ruta "{file_path}" no fue encontrado.')
        except KeyError as e:
            raise CommandError(f'Error: El archivo CSV debe tener una columna llamada {e}. Revisa las cabeceras.')
        except ValueError as e:
            raise CommandError(f'Error de datos en el CSV: Asegúrate de que los valores numéricos son correctos. Detalle: {e}')
        except Exception as e:
            raise CommandError(f'Ocurrió un error inesperado: {e}')