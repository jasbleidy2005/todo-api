from flask import jsonify, request
from src.services.user_service import UserService

class UserController:
    """
    Capa de Controladores para User.
    Maneja las peticiones HTTP y respuestas para operaciones de usuarios.
    """
    
    @staticmethod
    def create_user():
        """
        POST /api/users - Crear usuario
        
        Body esperado:
        {
            "name": "Juan Pérez",
            "email": "juan@example.com"
        }
        
        Returns:
            Response: JSON con usuario creado (201) o error (400/500)
        """
        try:
            # Obtener datos del body
            data = request.get_json()
            
            # Validar datos requeridos
            if not data:
                return jsonify({
                    'error': 'No se proporcionaron datos'
                }), 400
            
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return jsonify({
                    'error': 'Los campos name y email son obligatorios'
                }), 400
            
            # Crear usuario usando el servicio
            user = UserService.create_user(name, email)
            
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'user': user.to_dict()
            }), 201
            
        except ValueError as e:
            # Error de validación de negocio (email duplicado)
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # Error interno del servidor
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
    @staticmethod
    def get_user(user_id):
        """
        GET /api/users/:id - Consultar usuario por ID
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            Response: JSON con usuario (200) o error (404/500)
        """
        try:
            user = UserService.get_user_by_id(user_id)
            
            if not user:
                return jsonify({
                    'error': f'Usuario con ID {user_id} no encontrado'
                }), 404
            
            return jsonify({
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
