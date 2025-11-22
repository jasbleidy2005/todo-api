"""
Pruebas Unitarias - Capa de Servicios
Prueban la lógica de negocio aislada sin dependencias HTTP
"""
import pytest
from src.services.user_service import UserService
from src.services.task_service import TaskService
from src.models.user import User
from src.models.task import Task
from src.config.database import db


class TestUserService:
    """Pruebas unitarias para UserService"""
    
    def test_cannot_create_user_with_duplicate_email(self, app):
        """
        Prueba Unitaria 1: No se puede crear usuario con email duplicado
        Validación de negocio: Email único
        """
        with app.app_context():
            # Crear primer usuario
            user1 = UserService.create_user('Juan Pérez', 'juan@example.com')
            assert user1 is not None
            assert user1.email == 'juan@example.com'
            
            # Intentar crear segundo usuario con mismo email
            with pytest.raises(ValueError) as exc_info:
                UserService.create_user('Pedro López', 'juan@example.com')
            
            # Verificar mensaje de error
            assert 'ya está registrado' in str(exc_info.value).lower()


class TestTaskService:
    """Pruebas unitarias para TaskService"""
    
    def test_cannot_create_task_without_user_id(self, app):
        """
        Prueba Unitaria 2: No se puede crear tarea sin user_id
        Validación de negocio: user_id es obligatorio
        """
        with app.app_context():
            # Intentar crear tarea sin user_id (None)
            with pytest.raises(ValueError) as exc_info:
                TaskService.create_task('Tarea sin usuario', None)
            
            # Verificar mensaje de error
            assert 'obligatorio' in str(exc_info.value).lower()
            
            # Intentar crear tarea con user_id vacío (0)
            with pytest.raises(ValueError):
                TaskService.create_task('Otra tarea', 0)
    
    def test_is_completed_updates_correctly(self, app):
        """
        Prueba Unitaria 3: is_completed se actualiza correctamente
        Validación de negocio: Actualización controlada del estado
        """
        with app.app_context():
            # Crear usuario
            user = UserService.create_user('María González', 'maria@example.com')
            
            # Crear tarea
            task = TaskService.create_task('Estudiar Python', user.id, 'Repasar Flask')
            assert task.is_completed is False
            
            # Actualizar a completado
            updated_task = TaskService.update_task_completion(task.id, True)
            assert updated_task.is_completed is True
            
            # Verificar en base de datos
            db_task = TaskService.get_task_by_id(task.id)
            assert db_task.is_completed is True
            
            # Actualizar a no completado
            updated_task = TaskService.update_task_completion(task.id, False)
            assert updated_task.is_completed is False
    
    def test_can_delete_task(self, app):
        """
        Prueba Unitaria 4: Se puede eliminar una tarea
        Verificación de operación de eliminación
        """
        with app.app_context():
            # Crear usuario y tarea
            user = UserService.create_user('Carlos Ruiz', 'carlos@example.com')
            task = TaskService.create_task('Tarea a eliminar', user.id)
            task_id = task.id
            
            # Verificar que existe
            assert TaskService.get_task_by_id(task_id) is not None
            
            # Eliminar tarea
            result = TaskService.delete_task(task_id)
            assert result is True
            
            # Verificar que ya no existe
            assert TaskService.get_task_by_id(task_id) is None
            
            # Intentar eliminar tarea inexistente
            with pytest.raises(ValueError):
                TaskService.delete_task(999)
