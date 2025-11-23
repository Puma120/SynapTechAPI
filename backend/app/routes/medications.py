"""Rutas para gestión de medicamentos"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models.medication import Medication
from app.models.task import Task

medications_bp = Blueprint("medications", __name__, url_prefix="/api/medications")

@medications_bp.route("", methods=["GET"])
@jwt_required()
def get_medications():
    """Obtener todos los medicamentos del usuario"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Obtener parámetro de query para filtrar por activos
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Construir query
        query = Medication.query.filter_by(user_id=current_user_id)
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        medications = query.order_by(Medication.created_at.desc()).all()
        
        return jsonify({
            "medications": [med.to_dict() for med in medications],
            "total": len(medications)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener medicamentos: {str(e)}"}), 500


@medications_bp.route("", methods=["POST"])
@jwt_required()
def create_medication():
    """
    Crear un nuevo medicamento
    
    Body:
    {
        "name": "Nombre del medicamento",
        "dosage": "10mg" (opcional),
        "frequency": "Cada 8 horas" (opcional),
        "schedules": ["08:00", "16:00", "00:00"],
        "notes": "Tomar con comida" (opcional)
    }
    """
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Validar campos requeridos
        name = data.get("name", "").strip()
        if not name:
            return jsonify({"error": "El nombre del medicamento es requerido"}), 400
        
        schedules = data.get("schedules", [])
        if not schedules or not isinstance(schedules, list):
            return jsonify({"error": "Debe proporcionar al menos un horario"}), 400
        
        # Validar formato de horarios (HH:MM)
        for schedule in schedules:
            try:
                datetime.strptime(schedule, "%H:%M")
            except ValueError:
                return jsonify({"error": f"Formato de horario inválido: {schedule}. Use HH:MM"}), 400
        
        # Crear medicamento
        medication = Medication(
            user_id=current_user_id,
            name=name,
            dosage=data.get("dosage", "").strip(),
            frequency=data.get("frequency", "").strip(),
            schedules=schedules,
            notes=data.get("notes", "").strip(),
            is_active=True
        )
        
        db.session.add(medication)
        db.session.commit()
        
        # Crear tareas para cada horario de hoy
        _create_medication_tasks(medication)
        
        return jsonify({
            "message": "Medicamento creado exitosamente",
            "medication": medication.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear medicamento: {str(e)}"}), 500


@medications_bp.route("/<int:medication_id>", methods=["GET"])
@jwt_required()
def get_medication(medication_id):
    """Obtener un medicamento específico"""
    try:
        current_user_id = int(get_jwt_identity())
        
        medication = Medication.query.filter_by(
            id=medication_id,
            user_id=current_user_id
        ).first()
        
        if not medication:
            return jsonify({"error": "Medicamento no encontrado"}), 404
        
        return jsonify(medication.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener medicamento: {str(e)}"}), 500


@medications_bp.route("/<int:medication_id>", methods=["PUT"])
@jwt_required()
def update_medication(medication_id):
    """
    Actualizar un medicamento existente
    
    Body: (todos los campos son opcionales)
    {
        "name": "Nuevo nombre",
        "dosage": "20mg",
        "frequency": "Cada 12 horas",
        "schedules": ["09:00", "21:00"],
        "notes": "Nueva nota",
        "is_active": true
    }
    """
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        medication = Medication.query.filter_by(
            id=medication_id,
            user_id=current_user_id
        ).first()
        
        if not medication:
            return jsonify({"error": "Medicamento no encontrado"}), 404
        
        # Actualizar campos si se proporcionan
        if "name" in data:
            name = data["name"].strip()
            if not name:
                return jsonify({"error": "El nombre no puede estar vacío"}), 400
            medication.name = name
        
        if "dosage" in data:
            medication.dosage = data["dosage"].strip()
        
        if "frequency" in data:
            medication.frequency = data["frequency"].strip()
        
        if "schedules" in data:
            schedules = data["schedules"]
            if not schedules or not isinstance(schedules, list):
                return jsonify({"error": "Debe proporcionar al menos un horario"}), 400
            
            # Validar formato de horarios
            for schedule in schedules:
                try:
                    datetime.strptime(schedule, "%H:%M")
                except ValueError:
                    return jsonify({"error": f"Formato de horario inválido: {schedule}"}), 400
            
            medication.schedules = schedules
        
        if "notes" in data:
            medication.notes = data["notes"].strip()
        
        if "is_active" in data:
            medication.is_active = bool(data["is_active"])
        
        medication.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Si se actualizaron los horarios y está activo, crear nuevas tareas
        if "schedules" in data and medication.is_active:
            _create_medication_tasks(medication)
        
        return jsonify({
            "message": "Medicamento actualizado exitosamente",
            "medication": medication.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar medicamento: {str(e)}"}), 500


@medications_bp.route("/<int:medication_id>", methods=["DELETE"])
@jwt_required()
def delete_medication(medication_id):
    """Eliminar un medicamento"""
    try:
        current_user_id = int(get_jwt_identity())
        
        medication = Medication.query.filter_by(
            id=medication_id,
            user_id=current_user_id
        ).first()
        
        if not medication:
            return jsonify({"error": "Medicamento no encontrado"}), 404
        
        db.session.delete(medication)
        db.session.commit()
        
        return jsonify({
            "message": "Medicamento eliminado exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar medicamento: {str(e)}"}), 500


def _create_medication_tasks(medication):
    """
    Función auxiliar para crear tareas automáticas para cada horario del medicamento
    Solo crea tareas para hoy si aún no existen
    """
    try:
        today = datetime.now().date()
        
        for schedule_time in medication.schedules:
            # Parsear horario
            hour, minute = map(int, schedule_time.split(":"))
            
            # Crear datetime para hoy con ese horario
            schedule_datetime = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Verificar si ya existe una tarea para este medicamento y horario hoy
            existing_task = Task.query.filter(
                Task.user_id == medication.user_id,
                Task.title.like(f"%{medication.name}%"),
                Task.due_date >= datetime.combine(today, datetime.min.time()),
                Task.due_date < datetime.combine(today + timedelta(days=1), datetime.min.time())
            ).first()
            
            # Solo crear si no existe
            if not existing_task:
                task = Task(
                    user_id=medication.user_id,
                    title=f"Tomar medicamento: {medication.name}",
                    body=f"Dosis: {medication.dosage or 'Ver instrucciones'}\n{medication.notes or ''}".strip(),
                    priority="high",  # Medicamentos son alta prioridad
                    due_date=schedule_datetime,
                    status="pending"
                )
                db.session.add(task)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error al crear tareas de medicamento: {str(e)}")
        db.session.rollback()
