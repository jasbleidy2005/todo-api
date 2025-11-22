"""
Pruebas de Integración - Endpoints HTTP
Prueban la interacción completa entre controladores, servicios y modelos
"""
import json


class TestUserEndpoints:
    """Pruebas de integración para endpoints de usuarios"""
    
    def test_post_users_returns_201(self, client):
        """
        Prueba de Integración 1: POST /api/users verifica respuesta 201
        Verifica creación exitosa de usuario con código HTTP correcto
        """
        # Datos del usuario
        user_data = {
            'name': 'Ana Torres',
            'email': 'ana@example.com'
        }
        
        # Hacer petición POST
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Verificar código de respuesta
        assert response.status_code == 201
        
        # Verificar contenido de respuesta
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['name'] == 'Ana Torres'
        assert data['user']['email'] == 'ana@example.com'
        assert 'id' in data['user']
        assert 'created_at' in data['user']


class TestTaskEndpoints:
    """Pruebas de integración para endpoints de tareas"""
    
    def test_post_tasks_verifies_user_association(self, client):
        """
        Prueba de Integración 2: POST /api/tasks verifica asociación con usuario
        Verifica que la tarea se cree correctamente asociada al usuario
        """
        # Primero crear un usuario
        user_data = {
            'name': 'Roberto Sánchez',
            'email': 'roberto@example.com'
        }
        user_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['user']['id']
        
        # Crear tarea asociada al usuario
        task_data = {
            'title': 'Completar proyecto',
            'description': 'Desarrollar API REST',
            'user_id': user_id
        }
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        # Verificar respuesta
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'task' in data
        assert data['task']['user_id'] == user_id
        assert data['task']['title'] == 'Completar proyecto'
        assert data['task']['is_completed'] is False
    
    def test_get_user_tasks_lists_tasks(self, client):
        """
        Prueba de Integración 3: GET /api/users/:id/tasks lista tareas
        Verifica que se listen todas las tareas de un usuario específico
        """
        # Crear usuario
        user_data = {
            'name': 'Laura Martínez',
            'email': 'laura@example.com'
        }
        user_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['user']['id']
        
        # Crear múltiples tareas para el usuario
        tasks = [
            {'title': 'Tarea 1', 'user_id': user_id},
            {'title': 'Tarea 2', 'user_id': user_id},
            {'title': 'Tarea 3', 'user_id': user_id}
        ]
        
        for task in tasks:
            client.post(
                '/api/tasks',
                data=json.dumps(task),
                content_type='application/json'
            )
        
        # Obtener tareas del usuario
        response = client.get(f'/api/users/{user_id}/tasks')
        
        # Verificar respuesta
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert data['total'] == 3
        assert len(data['tasks']) == 3
        
        # Verificar que todas las tareas pertenecen al usuario
        for task in data['tasks']:
            assert task['user_id'] == user_id
