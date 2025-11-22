from flask import Flask, jsonify
from src.config.config import Config
from src.config.database import db
from src.routes.routes import api_bp

def create_app(config_class=Config):
    """
    Factory para crear la aplicación Flask.
    
    Args:
        config_class: Clase de configuración a usar
    
    Returns:
        Flask: Aplicación Flask configurada
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Registrar blueprints (rutas)
    app.register_blueprint(api_bp)
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            'message': 'ToDo API - Sistema de Gestión de Tareas',
            'version': '1.0.0',
            'endpoints': {
                'users': {
                    'POST /api/users': 'Crear usuario',
                    'GET /api/users/:id': 'Consultar usuario por ID'
                },
                'tasks': {
                    'POST /api/tasks': 'Crear tarea',
                    'GET /api/users/:id/tasks': 'Listar tareas de usuario',
                    'PUT /api/tasks/:id': 'Actualizar estado de tarea',
                    'PATCH /api/tasks/:id/complete': 'Marcar tarea como completada',
                    'DELETE /api/tasks/:id': 'Eliminar tarea'
                }
            }
        }), 200
    
    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8888, debug=True)
