from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.task import Task
from app.models.sync import ReminderLog
from app.services.gemini_service import GeminiService

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
gemini_service = GeminiService()

@ai_bp.route('/transcribe-task', methods=['POST'])
@jwt_required()
def transcribe_task():
    """Transcribir texto de voz a tarea usando IA"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        voice_text = data.get('voice_text', '').strip()
        
        if not voice_text:
            return jsonify({'error': 'Texto de voz requerido'}), 400
        
        # Usar Gemini para extraer informacion
        task_data = gemini_service.transcribe_voice_to_task(voice_text)
        
        # Crear tarea
        task = Task(
            user_id=user_id,
            title=task_data.get('title', voice_text[:100]),
            description=task_data.get('description', voice_text),
            priority=task_data.get('priority', 'medium'),
            category=task_data.get('category'),
            created_from_voice=True
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea creada desde voz exitosamente',
            'task': task.to_dict(),
            'suggested_duration': task_data.get('suggested_time')
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al transcribir: {str(e)}'}), 500

@ai_bp.route('/prioritize-tasks', methods=['POST'])
@jwt_required()
def prioritize_tasks():
    """Obtener sugerencias de priorizacion de tareas"""
    try:
        user_id = get_jwt_identity()
        
        # Obtener tareas pendientes
        tasks = Task.query.filter_by(
            user_id=user_id,
            status='pending'
        ).order_by(Task.due_date.asc()).limit(20).all()
        
        if not tasks:
            return jsonify({
                'message': 'No hay tareas pendientes',
                'prioritization': []
            }), 200
        
        tasks_data = [task.to_dict() for task in tasks]
        
        # Obtener patrones del usuario (simplificado)
        user_patterns = {
            'most_productive_time': 'manana',
            'average_completion_rate': 0.7
        }
        
        # Usar IA para priorizar
        prioritization = gemini_service.prioritize_tasks(tasks_data, user_patterns)
        
        return jsonify({
            'prioritization': prioritization
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al priorizar: {str(e)}'}), 500

@ai_bp.route('/suggest-routines', methods=['POST'])
@jwt_required()
def suggest_routines():
    """Generar sugerencias de rutinas basadas en tareas"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        time_of_day = data.get('time_of_day', 'manana')
        
        # Obtener tareas del usuario
        tasks = Task.query.filter_by(user_id=user_id).limit(20).all()
        tasks_data = [task.to_dict() for task in tasks]
        
        # Generar sugerencias
        suggestions = gemini_service.generate_routine_suggestions(tasks_data, time_of_day)
        
        return jsonify({
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al generar sugerencias: {str(e)}'}), 500

@ai_bp.route('/generate-reminder/<int:task_id>', methods=['POST'])
@jwt_required()
def generate_reminder(task_id):
    """Generar mensaje de recordatorio personalizado"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        # Generar mensaje
        message = gemini_service.generate_reminder_message(task.to_dict())
        
        # Registrar recordatorio
        reminder_log = ReminderLog(
            user_id=user_id,
            task_id=task_id,
            reminder_type='notification',
            sent_at=datetime.utcnow()
        )
        
        db.session.add(reminder_log)
        task.reminder_sent = True
        db.session.commit()
        
        return jsonify({
            'message': message,
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al generar recordatorio: {str(e)}'}), 500

@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    """Chat general con asistente IA"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        if not gemini_service.model:
            return jsonify({'error': 'Servicio de IA no disponible'}), 503
        
        # Contexto para el chat
        prompt = f"""
        Eres un asistente personal para personas con ADHD. Tu objetivo es ayudar con:
        - Organizacion de tareas
        - Gestion del tiempo
        - Creacion de rutinas
        - Motivacion y apoyo
        
        Responde de manera clara, concisa y sin emojis.
        
        Usuario: {message}
        
        Asistente:
        """
        
        response = gemini_service.model.generate_content(prompt)
        
        return jsonify({
            'response': response.text.strip()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en chat: {str(e)}'}), 500
