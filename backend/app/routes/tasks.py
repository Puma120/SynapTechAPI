from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.task import Task
from app.services.gemini_service import GeminiService
from app.services.speech_service import SpeechService

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")
gemini_service = GeminiService()
speech_service = SpeechService()

@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Obtener todas las tareas del usuario autenticado
    
    Query params opcionales:
    - status: filtrar por estado (pending, in_progress, completed)
    - limit: limitar número de resultados
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Obtener parámetros de query
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        
        # Construir query
        query = Task.query.filter_by(user_id=current_user_id)
        
        # Filtrar por estado si se proporciona
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(Task.created_at.desc())
        
        # Limitar resultados si se especifica
        if limit:
            query = query.limit(limit)
        
        tasks = query.all()
        
        return jsonify({
            "tasks": [task.to_dict() for task in tasks],
            "total": len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener tareas: {str(e)}"}), 500

@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    """
    Crear tarea desde texto o audio
    
    Acepta:
    - JSON con campo 'cuerpo' (texto)
    - Multipart/form-data con archivo 'audio' (WAV)
    - Multipart/form-data con 'cuerpo' y/o 'audio' (combina ambos)
    """
    try:
        current_user_id = int(get_jwt_identity())
        body_text = ""
        fecha = None
        
        # Verificar si es multipart/form-data (con posible archivo de audio)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Obtener datos del formulario
            body_text = request.form.get("cuerpo", "").strip()
            fecha = request.form.get("fecha")
            audio_file = request.files.get("audio")
            
            # Si hay audio, transcribirlo
            if audio_file:
                try:
                    audio_content = audio_file.read()
                    transcribed_text = speech_service.transcribe_audio(audio_content)
                    
                    # Si no hay texto en cuerpo, usar solo el audio transcrito
                    # Si hay texto, combinarlos
                    if transcribed_text:
                        if body_text:
                            body_text = f"{body_text} {transcribed_text}".strip()
                        else:
                            body_text = transcribed_text.strip()
                except Exception as e:
                    return jsonify({
                        "error": f"Error al transcribir audio: {str(e)}"
                    }), 400
            
            # Si no hay audio ni texto, error
            if not body_text:
                return jsonify({
                    "error": "Debe proporcionar 'cuerpo' (texto) o 'audio' (archivo WAV)"
                }), 400
        else:
            # JSON normal
            data = request.get_json()
            if not data:
                return jsonify({"error": "No se recibieron datos"}), 400
            
            body_text = data.get("cuerpo", "").strip()
            fecha = data.get("fecha")
            
            # Validar que haya texto
            if not body_text:
                return jsonify({
                    "error": "El campo 'cuerpo' es requerido"
                }), 400
        
        # Procesar con IA
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
