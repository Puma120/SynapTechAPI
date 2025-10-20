from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.task import Task
from app.services.gemini_service import GeminiService

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")
gemini_service = GeminiService()

@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    try:
        current_user_id = int(get_jwt_identity())  # Convertir de string a int
        data = request.get_json()
        
        body_text = data.get("cuerpo", "") if data else ""
        fecha = data.get("fecha") if data else None
        
        ai_result = gemini_service.process_task_input(body_text=body_text, fecha=fecha)
        
        new_task = Task(
            user_id=current_user_id,
            title=ai_result["title"],
            body=ai_result["body"],
            priority=ai_result["priority"],
            due_date=datetime.fromisoformat(ai_result["due_date"]) if ai_result["due_date"] else None,
            status="pending"
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            "title": new_task.title,
            "priority": new_task.priority,
            "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
            "id_tarea": new_task.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear tarea: {str(e)}"}), 500


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task_status(task_id):
    try:
        current_user_id = int(get_jwt_identity())  # Convertir de string a int
        data = request.get_json()
        
        if not data or "status" not in data:
            return jsonify({"error": "El campo status es requerido"}), 400
        
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        task.status = data["status"]
        
        if data["status"] == "completed":
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
        
        db.session.commit()
        
        return jsonify({
            "message": "Tarea actualizada exitosamente",
            "task": task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar tarea: {str(e)}"}), 500
