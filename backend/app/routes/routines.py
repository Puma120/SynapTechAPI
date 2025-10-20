from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.services.gemini_service import GeminiService

routines_bp = Blueprint("routines", __name__, url_prefix="/api/routines")
gemini_service = GeminiService()

@routines_bp.route("", methods=["GET"])
@jwt_required()
def get_routines():
    try:
        current_user_id = get_jwt_identity()
        
        user_tasks = Task.query.filter_by(user_id=current_user_id, status="pending").all()
        
        tasks_data = [task.to_dict() for task in user_tasks]
        
        routine_suggestions = gemini_service.generate_routine_suggestions(tasks_data)
        
        return jsonify({
            "message": "Rutinas generadas exitosamente",
            "routines": routine_suggestions
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al generar rutinas: {str(e)}"}), 500
