"""
Script para probar la API manualmente
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8888"

print("=" * 60)
print("PRUEBA MANUAL DE LA API - ToDo System")
print("=" * 60)

# 1. Probar endpoint raíz
print("\n1. GET / - Documentación de la API")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

# 2. Crear un usuario
print("\n2. POST /api/users - Crear usuario")
user_data = {
    "name": "Juan Pérez",
    "email": "juan.perez@example.com"
}
try:
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    print(f"Status: {response.status_code}")
    user_response = response.json()
    print(json.dumps(user_response, indent=2))
    user_id = user_response.get('user', {}).get('id')
except Exception as e:
    print(f"Error: {e}")
    user_id = None

if user_id:
    # 3. Consultar el usuario creado
    print(f"\n3. GET /api/users/{user_id} - Consultar usuario")
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Crear tareas para el usuario
    print(f"\n4. POST /api/tasks - Crear tareas")
    tasks_data = [
        {
            "title": "Comprar leche",
            "description": "Ir al supermercado",
            "user_id": user_id
        },
        {
            "title": "Estudiar Python",
            "description": "Repasar Flask y SQLAlchemy",
            "user_id": user_id
        },
        {
            "title": "Hacer ejercicio",
            "user_id": user_id
        }
    ]
    
    task_ids = []
    for task_data in tasks_data:
        try:
            response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
            print(f"Status: {response.status_code} - {task_data['title']}")
            task_response = response.json()
            task_ids.append(task_response.get('task', {}).get('id'))
        except Exception as e:
            print(f"Error: {e}")
    
    # 5. Listar todas las tareas del usuario
    print(f"\n5. GET /api/users/{user_id}/tasks - Listar tareas")
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # 6. Marcar una tarea como completada (PATCH)
    if task_ids and task_ids[0]:
        print(f"\n6. PATCH /api/tasks/{task_ids[0]}/complete - Marcar completada")
        try:
            response = requests.patch(f"{BASE_URL}/api/tasks/{task_ids[0]}/complete")
            print(f"Status: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {e}")
    
    # 7. Actualizar estado de tarea (PUT)
    if task_ids and task_ids[1]:
        print(f"\n7. PUT /api/tasks/{task_ids[1]} - Actualizar estado")
        try:
            response = requests.put(f"{BASE_URL}/api/tasks/{task_ids[1]}", 
                                   json={"is_completed": True})
            print(f"Status: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {e}")
    
    # 8. Eliminar una tarea
    if task_ids and task_ids[2]:
        print(f"\n8. DELETE /api/tasks/{task_ids[2]} - Eliminar tarea")
        try:
            response = requests.delete(f"{BASE_URL}/api/tasks/{task_ids[2]}")
            print(f"Status: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {e}")
    
    # 9. Verificar tareas restantes
    print(f"\n9. GET /api/users/{user_id}/tasks - Verificar tareas restantes")
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks")
        print(f"Status: {response.status_code}")
        tasks_response = response.json()
        print(json.dumps(tasks_response, indent=2))
        print(f"\nTotal de tareas restantes: {tasks_response.get('total')}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 60)
print("PRUEBA COMPLETADA")
print("=" * 60)
