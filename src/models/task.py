from datetime import datetime, timezone
from src.config.database import db

class Task(db.Model):
    """
    Modelo Task - Representa una tarea asociada a un usuario.
    Tabla: tasks
    """
    __tablename__ = 'tasks'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title} (User: {self.user_id})>'
    
    def to_dict(self):
        """
        Convierte el objeto Task a diccionario para serialización JSON.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
