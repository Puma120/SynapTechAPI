from datetime import datetime
from app import db

class DeviceSync(db.Model):
    """Modelo para sincronizacion con el dispositivo collar"""
    __tablename__ = 'device_syncs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_id = db.Column(db.String(100), nullable=False)
    sync_type = db.Column(db.String(50), nullable=False)  # ble, cloud, manual
    data_payload = db.Column(db.JSON)
    status = db.Column(db.String(20), default='pending')  # pending, synced, failed
    synced_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', back_populates='device_syncs')
    
    def to_dict(self):
        """Convierte el registro a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'device_id': self.device_id,
            'sync_type': self.sync_type,
            'status': self.status,
            'synced_at': self.synced_at.isoformat() if self.synced_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ReminderLog(db.Model):
    """Modelo para registro de recordatorios enviados"""
    __tablename__ = 'reminder_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    reminder_type = db.Column(db.String(50), nullable=False)  # haptic, notification, both
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    was_acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convierte el log a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'reminder_type': self.reminder_type,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'was_acknowledged': self.was_acknowledged,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }

class ProductivityMetric(db.Model):
    """Modelo para metricas de productividad del usuario"""
    __tablename__ = 'productivity_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tasks_completed = db.Column(db.Integer, default=0)
    tasks_created = db.Column(db.Integer, default=0)
    routines_followed = db.Column(db.Integer, default=0)
    reminders_acknowledged = db.Column(db.Integer, default=0)
    total_focus_time = db.Column(db.Integer, default=0)  # en minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte la metrica a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'tasks_completed': self.tasks_completed,
            'tasks_created': self.tasks_created,
            'routines_followed': self.routines_followed,
            'reminders_acknowledged': self.reminders_acknowledged,
            'total_focus_time': self.total_focus_time
        }
