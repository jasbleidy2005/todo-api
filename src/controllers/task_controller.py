from flask import jsonify, request
from src.services.task_service import TaskService
from src.services.user_service import UserService

class TaskController:
    """
    Capa de Controladores para Task.
    Maneja las peticiones HTTP y respuestas para operaciones de tareas.
    """
    
    @staticmethod
    def create_task():
        """
        POST /api/tasks - Crear tarea asociada a usuario
        
        Body esperado:
        {
            "title": "Comprar leche",
            "description": "Ir al supermercado",
            "user_id": 1
        }
        
        Returns:
            Response: JSON con tarea creada (201) o error (400/500)
        """
        try:
            # Obtener datos del body
            data = request.get_json()
            
            # Validar datos requeridos
            if not data:
                return jsonify({
                    'error': 'No se proporcionaron datos'
                }), 400
            
            title = data.get('title')
            user_id = data.get('user_id')
            description = data.get('description')
            
            if not title or not user_id:
                return jsonify({
                    'error': 'Los campos title y user_id son obligatorios'
                }), 400
            
            # Crear tarea usando el servicio
            task = TaskService.create_task(title, user_id, description)
            
            return jsonify({
                'message': 'Tarea creada exitosamente',
                'task': task.to_dict()
            }), 201
            
        except ValueError as e:
            # Error de validación de negocio
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # Error interno del servidor
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    @staticmethod
    def get_user_tasks(user_id):
        """
        GET /api/users/:id/tasks - Listar todas las tareas de un usuario
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            Response: JSON con lista de tareas (200) o error (404/500)
        """
        try:
            # Verificar que el usuario existe
            user = UserService.get_user_by_id(user_id)
            if not user:
                return jsonify({
                    'error': f'Usuario con ID {user_id} no encontrado'
                }), 404
            
            # Obtener tareas del usuario
            tasks = TaskService.get_tasks_by_user(user_id)
            
            return jsonify({
                'user_id': user_id,
                'tasks': [task.to_dict() for task in tasks],
                'total': len(tasks)
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    @staticmethod
    def update_task(task_id):
        """
        PUT /api/tasks/:id - Actualizar estado de tarea
        
        Body esperado:
        {
            "is_completed": true
        }
        
        Args:
            task_id (int): ID de la tarea
        
        Returns:
            Response: JSON con tarea actualizada (200) o error (400/404/500)
        """
        try:
            # Obtener datos del body
            data = request.get_json()
            
            if not data or 'is_completed' not in data:
                return jsonify({
                    'error': 'El campo is_completed es obligatorio'
                }), 400
            
            is_completed = data.get('is_completed')
            
            # Validar tipo de dato
            if not isinstance(is_completed, bool):
                return jsonify({
                    'error': 'El campo is_completed debe ser un booleano'
                }), 400
            
            # Actualizar tarea usando el servicio
            task = TaskService.update_task_completion(task_id, is_completed)
            
            return jsonify({
                'message': 'Tarea actualizada exitosamente',
                'task': task.to_dict()
            }), 200
            
        except ValueError as e:
            # Tarea no encontrada
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    @staticmethod
    def mark_task_completed(task_id):
        """
        PATCH /api/tasks/:id/complete - Marcar tarea como completada
        
        Args:
            task_id (int): ID de la tarea
        
        Returns:
            Response: JSON con tarea completada (200) o error (404/500)
        """
        try:
            # Marcar como completada usando el servicio
            task = TaskService.mark_task_as_completed(task_id)
            
            return jsonify({
                'message': 'Tarea marcada como completada',
                'task': task.to_dict()
            }), 200
            
        except ValueError as e:
            # Tarea no encontrada
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    @staticmethod
    def delete_task(task_id):
        """
        DELETE /api/tasks/:id - Eliminar tarea
        
        Args:
            task_id (int): ID de la tarea
        
        Returns:
            Response: JSON con confirmación (200) o error (404/500)
        """
        try:
            # Eliminar tarea usando el servicio
            TaskService.delete_task(task_id)
            
            return jsonify({
                'message': f'Tarea con ID {task_id} eliminada exitosamente'
            }), 200
            
        except ValueError as e:
            # Tarea no encontrada
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
