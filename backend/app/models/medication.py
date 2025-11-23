"""Modelo de Medicamentos para seguimiento de tratamientos"""
from datetime import datetime
from app import db

class Medication(db.Model):
    """Modelo de medicamento con horarios programados"""
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100))  # Ej: "10mg", "1 tableta"
    frequency = db.Column(db.String(100))  # Ej: "Cada 8 horas", "3 veces al día"
    schedules = db.Column(db.JSON)  # Array de horarios: ["08:00", "14:00", "20:00"]
    notes = db.Column(db.Text)  # Notas adicionales o instrucciones
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    user = db.relationship('User', back_populates='medications')
    
    def to_dict(self):
        """Convierte el medicamento a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'schedules': self.schedules or [],
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
