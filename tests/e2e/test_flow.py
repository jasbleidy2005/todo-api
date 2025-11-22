"""
Prueba End-to-End (E2E) - Flujo Completo
Simula un flujo de usuario real con múltiples operaciones
"""
import json


class TestE2EFlow:
    """Prueba E2E del flujo completo del sistema"""
    
    def test_complete_user_task_flow(self, client):
        """
        Prueba E2E: Flujo completo de 6 pasos
        
        1. Crear usuario
        2. Crear 2 tareas para ese usuario
        3. Listar tareas del usuario
        4. Marcar una tarea como completada
        5. Eliminar una tarea
        6. Verificar que solo queda 1 tarea
        """
        
        # ========== PASO 1: Crear usuario ==========
        user_data = {
            'name': 'Sofía Ramírez',
            'email': 'sofia@example.com'
        }
        user_response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert user_response.status_code == 201
        user_id = json.loads(user_response.data)['user']['id']
        print(f"\nPaso 1: Usuario creado con ID {user_id}")
        
        # ========== PASO 2: Crear 2 tareas para ese usuario ==========
        task1_data = {
            'title': 'Tarea 1 - Estudiar para el parcial',
            'description': 'Repasar todos los temas',
            'user_id': user_id
        }
        task1_response = client.post(
            '/api/tasks',
            data=json.dumps(task1_data),
            content_type='application/json'
        )
        assert task1_response.status_code == 201
        task1_id = json.loads(task1_response.data)['task']['id']
        print(f"Paso 2a: Tarea 1 creada con ID {task1_id}")
        
        task2_data = {
            'title': 'Tarea 2 - Hacer ejercicios de práctica',
            'description': 'Completar lista de ejercicios',
            'user_id': user_id
        }
        task2_response = client.post(
            '/api/tasks',
            data=json.dumps(task2_data),
            content_type='application/json'
        )
        assert task2_response.status_code == 201
        task2_id = json.loads(task2_response.data)['task']['id']
        print(f"Paso 2b: Tarea 2 creada con ID {task2_id}")
        
        # ========== PASO 3: Listar tareas del usuario ==========
        tasks_response = client.get(f'/api/users/{user_id}/tasks')
        assert tasks_response.status_code == 200
        tasks_data = json.loads(tasks_response.data)
        assert tasks_data['total'] == 2
        assert len(tasks_data['tasks']) == 2
        print(f"Paso 3: Usuario tiene {tasks_data['total']} tareas")
        
        # Verificar que ambas tareas están sin completar
        for task in tasks_data['tasks']:
            assert task['is_completed'] is False
        
        # ========== PASO 4: Marcar una tarea como completada ==========
        complete_response = client.patch(f'/api/tasks/{task1_id}/complete')
        assert complete_response.status_code == 200
        completed_task = json.loads(complete_response.data)['task']
        assert completed_task['is_completed'] is True
        print(f"Paso 4: Tarea {task1_id} marcada como completada")
        
        # Verificar que se actualizó correctamente
        tasks_after_complete = client.get(f'/api/users/{user_id}/tasks')
        tasks_list = json.loads(tasks_after_complete.data)['tasks']
        completed_tasks = [t for t in tasks_list if t['is_completed']]
        assert len(completed_tasks) == 1
        
        # ========== PASO 5: Eliminar una tarea ==========
        delete_response = client.delete(f'/api/tasks/{task2_id}')
        assert delete_response.status_code == 200
        print(f"Paso 5: Tarea {task2_id} eliminada")
        
        # ========== PASO 6: Verificar que solo queda 1 tarea ==========
        final_tasks_response = client.get(f'/api/users/{user_id}/tasks')
        assert final_tasks_response.status_code == 200
        final_tasks_data = json.loads(final_tasks_response.data)
        
        # Verificaciones finales
        assert final_tasks_data['total'] == 1, "Debe quedar exactamente 1 tarea"
        assert len(final_tasks_data['tasks']) == 1
        
        # La tarea restante debe ser la primera (task1)
        remaining_task = final_tasks_data['tasks'][0]
        assert remaining_task['id'] == task1_id
        assert remaining_task['is_completed'] is True
        assert remaining_task['title'] == 'Tarea 1 - Estudiar para el parcial'
        
        print(f"Paso 6: Verificación exitosa - Solo queda 1 tarea (ID {task1_id}, completada)")
        print("\n=== FLUJO E2E COMPLETADO EXITOSAMENTE ===")
