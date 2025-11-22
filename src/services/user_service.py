from src.models.user import User
from src.config.database import db
from sqlalchemy.exc import IntegrityError

class UserService:
    """
    Capa de Servicios para User.
    Contiene la lógica de negocio relacionada con usuarios.
    """
    
    @staticmethod
    def create_user(name, email):
        """
        Crea un nuevo usuario.
        
        Validación 1: Email único - No permitir usuarios con email duplicado
        
        Args:
            name (str): Nombre del usuario
            email (str): Email del usuario (debe ser único)
        
        Returns:
            User: Usuario creado
        
        Raises:
            ValueError: Si el email ya existe en la base de datos
        """
        # Validación 1: Email único
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError(f"El email '{email}' ya está registrado")
        
        try:
            # Crear nuevo usuario
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"El email '{email}' ya está registrado")
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            User: Usuario encontrado o None
        """
        return db.session.get(User, user_id)
    
    @staticmethod
    def get_all_users():
        """
        Obtiene todos los usuarios.
        
        Returns:
            list[User]: Lista de todos los usuarios
        """
        return User.query.all()
    
    @staticmethod
    def user_exists(user_id):
        """
        Verifica si un usuario existe.
        
        Validación 3: Usuario existente - Verificar que user_id exista
        
        Args:
            user_id (int): ID del usuario a verificar
        
        Returns:
            bool: True si existe, False en caso contrario
        """
        return db.session.get(User, user_id) is not None
