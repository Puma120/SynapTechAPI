from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.task import Task
from app.models.user import User

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """Obtener todas las tareas del usuario"""
    try:
        user_id = get_jwt_identity()
        
        # Filtros opcionales
        status = request.args.get('status')
        priority = request.args.get('priority')
        category = request.args.get('category')
        
        query = Task.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        
        tasks = query.order_by(Task.due_date.asc()).all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener tareas: {str(e)}'}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Obtener una tarea especifica"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        return jsonify({
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener tarea: {str(e)}'}), 500

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """Crear nueva tarea"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'El titulo es requerido'}), 400
        
        task = Task(
            user_id=user_id,
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            priority=data.get('priority', 'medium'),
            category=data.get('category'),
            created_from_voice=data.get('created_from_voice', False)
        )
        
        # Fecha de vencimiento
        if data.get('due_date'):
            try:
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Formato de fecha invalido'}), 400
        
        # Recordatorio
        if data.get('reminder_time'):
            try:
                task.reminder_time = datetime.fromisoformat(data['reminder_time'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Formato de recordatorio invalido'}), 400
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea creada exitosamente',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear tarea: {str(e)}'}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Actualizar tarea existente"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'title' in data:
            task.title = data['title'].strip()
        if 'description' in data:
            task.description = data['description'].strip()
        if 'priority' in data:
            task.priority = data['priority']
        if 'status' in data:
            task.status = data['status']
            if data['status'] == 'completed' and not task.completed_at:
                task.completed_at = datetime.utcnow()
        if 'category' in data:
            task.category = data['category']
        if 'due_date' in data:
            try:
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Formato de fecha invalido'}), 400
        if 'reminder_time' in data:
            try:
                task.reminder_time = datetime.fromisoformat(data['reminder_time'].replace('Z', '+00:00'))
                task.reminder_sent = False
            except:
                return jsonify({'error': 'Formato de recordatorio invalido'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea actualizada exitosamente',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar tarea: {str(e)}'}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Eliminar tarea"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar tarea: {str(e)}'}), 500

@tasks_bp.route('/bulk-delete', methods=['POST'])
@jwt_required()
def bulk_delete_tasks():
    """Eliminar multiples tareas"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        task_ids = data.get('task_ids', [])
        
        if not task_ids:
            return jsonify({'error': 'No se especificaron tareas'}), 400
        
        tasks = Task.query.filter(Task.id.in_(task_ids), Task.user_id == user_id).all()
        
        for task in tasks:
            db.session.delete(task)
        
        db.session.commit()
        
        return jsonify({
            'message': f'{len(tasks)} tareas eliminadas exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar tareas: {str(e)}'}), 500
