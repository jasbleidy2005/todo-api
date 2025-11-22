import pytest
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from src.config.database import db
from src.config.config import Config

class TestConfig(Config):
    """Configuración de pruebas con base de datos en memoria"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture(scope='function')
def app():
    """
    Fixture que crea una aplicación Flask para testing.
    Se recrea para cada función de prueba.
    """
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """
    Fixture que crea un cliente de pruebas Flask.
    """
    return app.test_client()
