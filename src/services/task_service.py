from src.models.task import Task
from src.services.user_service import UserService
from src.config.database import db

class TaskService:
    """
    Capa de Servicios para Task.
    Contiene la lógica de negocio relacionada con tareas.
    """
    
    @staticmethod
    def create_task(title, user_id, description=None):
        """
        Crea una nueva tarea asociada a un usuario.
        
        Validación 2: No crear tarea sin user_id válido
        Validación 3: Verificar que user_id exista antes de crear tarea
        
        Args:
            title (str): Título de la tarea
            user_id (int): ID del usuario propietario
            description (str, optional): Descripción de la tarea
        
        Returns:
            Task: Tarea creada
        
        Raises:
            ValueError: Si user_id es inválido o no existe
        """
        # Validación 2: No crear tarea sin user_id
        if not user_id:
            raise ValueError("El user_id es obligatorio para crear una tarea")
        
        # Validación 3: Usuario existente
        if not UserService.user_exists(user_id):
            raise ValueError(f"El usuario con ID {user_id} no existe")
        
        # Crear nueva tarea
        new_task = Task(
            title=title,
            description=description,
            user_id=user_id,
            is_completed=False
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id (int): ID de la tarea
        
        Returns:
            Task: Tarea encontrada o None
        """
        return db.session.get(Task, task_id)
    
    @staticmethod
    def get_tasks_by_user(user_id):
        """
        Obtiene todas las tareas de un usuario específico.
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            list[Task]: Lista de tareas del usuario
        """
        return Task.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_task_completion(task_id, is_completed):
        """
        Actualiza el estado de completado de una tarea.
        
        Validación 4: Actualización controlada - Solo permitir actualizar is_completed
        
        Args:
            task_id (int): ID de la tarea
            is_completed (bool): Nuevo estado de completado
        
        Returns:
            Task: Tarea actualizada
        
        Raises:
            ValueError: Si la tarea no existe
        """
        task = db.session.get(Task, task_id)
        if not task:
            raise ValueError(f"La tarea con ID {task_id} no existe")
        
        # Validación 4: Actualización controlada
        task.is_completed = is_completed
        db.session.commit()
        return task
    
    @staticmethod
    def mark_task_as_completed(task_id):
        """
        Marca una tarea como completada.
        
        Args:
            task_id (int): ID de la tarea
        
        Returns:
            Task: Tarea actualizada
        
        Raises:
            ValueError: Si la tarea no existe
        """
        return TaskService.update_task_completion(task_id, True)
    
    @staticmethod
    def delete_task(task_id):
        """
        Elimina una tarea.
        
        Args:
            task_id (int): ID de la tarea a eliminar
        
        Returns:
            bool: True si se eliminó correctamente
        
        Raises:
            ValueError: Si la tarea no existe
        """
        task = db.session.get(Task, task_id)
        if not task:
            raise ValueError(f"La tarea con ID {task_id} no existe")
        
        db.session.delete(task)
        db.session.commit()
        return True
