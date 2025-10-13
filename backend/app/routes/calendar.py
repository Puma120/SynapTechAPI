from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.task import Task
from app.services.calendar_service import GoogleCalendarService

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')
calendar_service = GoogleCalendarService()

@calendar_bp.route('/auth-url', methods=['GET'])
@jwt_required()
def get_auth_url():
    """Obtener URL de autorizacion de Google"""
    try:
        redirect_uri = request.args.get('redirect_uri', 'http://localhost:5173/calendar/callback')
        
        auth_url = calendar_service.get_auth_url(redirect_uri)
        
        if not auth_url:
            return jsonify({'error': 'Error al generar URL de autorizacion'}), 500
        
        return jsonify({
            'auth_url': auth_url
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@calendar_bp.route('/callback', methods=['POST'])
@jwt_required()
def handle_callback():
    """Manejar callback de autorizacion"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        code = data.get('code')
        redirect_uri = data.get('redirect_uri', 'http://localhost:5173/calendar/callback')
        
        if not code:
            return jsonify({'error': 'Codigo de autorizacion requerido'}), 400
        
        credentials = calendar_service.exchange_code_for_token(code, redirect_uri)
        
        if not credentials:
            return jsonify({'error': 'Error al obtener credenciales'}), 500
        
        # En produccion, guardar credenciales en base de datos asociadas al usuario
        # Por ahora, retornar para que el frontend las maneje
        
        return jsonify({
            'message': 'Autorizacion exitosa',
            'credentials': credentials
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@calendar_bp.route('/sync-task/<int:task_id>', methods=['POST'])
@jwt_required()
def sync_task_to_calendar(task_id):
    """Sincronizar tarea especifica con Google Calendar"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        credentials = data.get('credentials')
        
        if not credentials:
            return jsonify({'error': 'Credenciales requeridas'}), 400
        
        # Inicializar servicio
        if not calendar_service.initialize_service(credentials):
            return jsonify({'error': 'Error al inicializar servicio'}), 500
        
        # Obtener tarea
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        if not task.due_date:
            return jsonify({'error': 'La tarea debe tener fecha de vencimiento'}), 400
        
        # Crear o actualizar evento
        if task.google_calendar_event_id:
            success = calendar_service.update_event(
                task.google_calendar_event_id,
                task.to_dict()
            )
            if not success:
                return jsonify({'error': 'Error al actualizar evento'}), 500
        else:
            event_id = calendar_service.create_event(task.to_dict())
            if not event_id:
                return jsonify({'error': 'Error al crear evento'}), 500
            task.google_calendar_event_id = event_id
            db.session.commit()
        
        return jsonify({
            'message': 'Tarea sincronizada con calendario',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 500

@calendar_bp.route('/sync-all', methods=['POST'])
@jwt_required()
def sync_all_tasks():
    """Sincronizar todas las tareas con fechas de vencimiento"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        credentials = data.get('credentials')
        
        if not credentials:
            return jsonify({'error': 'Credenciales requeridas'}), 400
        
        # Inicializar servicio
        if not calendar_service.initialize_service(credentials):
            return jsonify({'error': 'Error al inicializar servicio'}), 500
        
        # Obtener tareas con fechas
        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.due_date.isnot(None),
            Task.status != 'completed'
        ).all()
        
        synced_count = 0
        errors = []
        
        for task in tasks:
            try:
                if task.google_calendar_event_id:
                    calendar_service.update_event(
                        task.google_calendar_event_id,
                        task.to_dict()
                    )
                else:
                    event_id = calendar_service.create_event(task.to_dict())
                    if event_id:
                        task.google_calendar_event_id = event_id
                        synced_count += 1
            except Exception as e:
                errors.append(f"Tarea {task.id}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': f'{synced_count} tareas sincronizadas',
            'synced': synced_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 500

@calendar_bp.route('/events', methods=['POST'])
@jwt_required()
def list_calendar_events():
    """Listar eventos del calendario"""
    try:
        data = request.get_json()
        
        credentials = data.get('credentials')
        
        if not credentials:
            return jsonify({'error': 'Credenciales requeridas'}), 400
        
        # Inicializar servicio
        if not calendar_service.initialize_service(credentials):
            return jsonify({'error': 'Error al inicializar servicio'}), 500
        
        events = calendar_service.list_events(max_results=50)
        
        return jsonify({
            'events': events
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500
