from datetime import datetime, timezone
from src.config.database import db

class User(db.Model):
    """
    Modelo User - Representa a un usuario en el sistema.
    Tabla: users
    """
    __tablename__ = 'users'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relación con Task (un usuario tiene muchas tareas)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.id}: {self.email}>'
    
    def to_dict(self):
        """
        Convierte el objeto User a diccionario para serialización JSON.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
