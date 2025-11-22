from flask import Blueprint
from src.controllers.user_controller import UserController
from src.controllers.task_controller import TaskController

# Blueprint para las rutas de la API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== RUTAS DE USUARIOS ====================

@api_bp.route('/users', methods=['POST'])
def create_user():
    """POST /api/users - Crear usuario"""
    return UserController.create_user()

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /api/users/:id - Consultar usuario por ID"""
    return UserController.get_user(user_id)

# ==================== RUTAS DE TAREAS ====================

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """POST /api/tasks - Crear tarea asociada a usuario"""
    return TaskController.create_task()

@api_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    """GET /api/users/:id/tasks - Listar todas las tareas de un usuario"""
    return TaskController.get_user_tasks(user_id)

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """PUT /api/tasks/:id - Actualizar estado de tarea"""
    return TaskController.update_task(task_id)

@api_bp.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def mark_task_completed(task_id):
    """PATCH /api/tasks/:id/complete - Marcar tarea como completada"""
    return TaskController.mark_task_completed(task_id)

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """DELETE /api/tasks/:id - Eliminar tarea"""
    return TaskController.delete_task(task_id)
