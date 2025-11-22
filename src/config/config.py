import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """
    Clase de configuración para la aplicación Flask.
    Gestiona conexión a PostgreSQL y configuraciones generales.
    """
    # Configuración de la base de datos PostgreSQL
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'tasks_management_db')
    DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'admin123')
    
    # URI de conexión a PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    
    # Deshabilitar el seguimiento de modificaciones (ahorra recursos)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Flask
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    TESTING = False
