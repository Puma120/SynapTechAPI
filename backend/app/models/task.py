from datetime import datetime
from app import db

class Task(db.Model):
    """Modelo de tarea individual"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    reminder_time = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))
    created_from_voice = db.Column(db.Boolean, default=False)
    google_calendar_event_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(datetime), onupdate=datetime.now(datetime))
    updated_at = db.Column(db.DateTime, default=datetime.now(datetime), onupdate=datetime.now(datetime))

    # Relaciones
    user = db.relationship('User', back_populates='tasks')
    
    def to_dict(self):
        """Convierte la tarea a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'reminder_time': self.reminder_time.isoformat() if self.reminder_time else None,
            'reminder_sent': self.reminder_sent,
            'category': self.category,
            'created_from_voice': self.created_from_voice,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Routine(db.Model):
    """Modelo de rutina diaria/semanal"""
    __tablename__ = 'routines'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20), nullable=False)  # daily, weekly, custom
    days_of_week = db.Column(db.JSON)  # [0,1,2,3,4,5,6] para lun-dom
    time_of_day = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', back_populates='routines')
    steps = db.relationship('RoutineStep', back_populates='routine', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte la rutina a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency,
            'days_of_week': self.days_of_week,
            'time_of_day': self.time_of_day.isoformat() if self.time_of_day else None,
            'is_active': self.is_active,
            'steps': [step.to_dict() for step in self.steps],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RoutineStep(db.Model):
    """Modelo para pasos individuales de una rutina"""
    __tablename__ = 'routine_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    estimated_duration = db.Column(db.Integer)  # en minutos
    
    # Relaciones
    routine = db.relationship('Routine', back_populates='steps')
    
    def to_dict(self):
        """Convierte el paso a diccionario"""
        return {
            'id': self.id,
            'step_order': self.step_order,
            'title': self.title,
            'description': self.description,
            'estimated_duration': self.estimated_duration
        }
