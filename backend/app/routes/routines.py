from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, time
from app import db
from app.models.task import Routine, RoutineStep

routines_bp = Blueprint('routines', __name__, url_prefix='/api/routines')

@routines_bp.route('/', methods=['GET'])
@jwt_required()
def get_routines():
    """Obtener todas las rutinas del usuario"""
    try:
        user_id = get_jwt_identity()
        
        is_active = request.args.get('is_active')
        
        query = Routine.query.filter_by(user_id=user_id)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        routines = query.order_by(Routine.created_at.desc()).all()
        
        return jsonify({
            'routines': [routine.to_dict() for routine in routines]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener rutinas: {str(e)}'}), 500

@routines_bp.route('/<int:routine_id>', methods=['GET'])
@jwt_required()
def get_routine(routine_id):
    """Obtener una rutina especifica"""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        return jsonify({
            'routine': routine.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener rutina: {str(e)}'}), 500

@routines_bp.route('/', methods=['POST'])
@jwt_required()
def create_routine():
    """Crear nueva rutina"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'El nombre es requerido'}), 400
        
        if not data.get('frequency'):
            return jsonify({'error': 'La frecuencia es requerida'}), 400
        
        routine = Routine(
            user_id=user_id,
            name=data['name'].strip(),
            description=data.get('description', '').strip(),
            frequency=data['frequency'],
            days_of_week=data.get('days_of_week'),
            is_active=data.get('is_active', True)
        )
        
        # Hora del dia
        if data.get('time_of_day'):
            try:
                time_parts = data['time_of_day'].split(':')
                routine.time_of_day = time(int(time_parts[0]), int(time_parts[1]))
            except:
                return jsonify({'error': 'Formato de hora invalido'}), 400
        
        db.session.add(routine)
        db.session.flush()
        
        # Agregar pasos
        if data.get('steps'):
            for step_data in data['steps']:
                step = RoutineStep(
                    routine_id=routine.id,
                    step_order=step_data.get('step_order', 0),
                    title=step_data['title'].strip(),
                    description=step_data.get('description', '').strip(),
                    estimated_duration=step_data.get('estimated_duration')
                )
                db.session.add(step)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Rutina creada exitosamente',
            'routine': routine.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear rutina: {str(e)}'}), 500

@routines_bp.route('/<int:routine_id>', methods=['PUT'])
@jwt_required()
def update_routine(routine_id):
    """Actualizar rutina existente"""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            routine.name = data['name'].strip()
        if 'description' in data:
            routine.description = data['description'].strip()
        if 'frequency' in data:
            routine.frequency = data['frequency']
        if 'days_of_week' in data:
            routine.days_of_week = data['days_of_week']
        if 'is_active' in data:
            routine.is_active = data['is_active']
        if 'time_of_day' in data:
            try:
                time_parts = data['time_of_day'].split(':')
                routine.time_of_day = time(int(time_parts[0]), int(time_parts[1]))
            except:
                return jsonify({'error': 'Formato de hora invalido'}), 400
        
        # Actualizar pasos si se proporcionan
        if 'steps' in data:
            # Eliminar pasos existentes
            RoutineStep.query.filter_by(routine_id=routine_id).delete()
            
            # Agregar nuevos pasos
            for step_data in data['steps']:
                step = RoutineStep(
                    routine_id=routine.id,
                    step_order=step_data.get('step_order', 0),
                    title=step_data['title'].strip(),
                    description=step_data.get('description', '').strip(),
                    estimated_duration=step_data.get('estimated_duration')
                )
                db.session.add(step)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Rutina actualizada exitosamente',
            'routine': routine.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar rutina: {str(e)}'}), 500

@routines_bp.route('/<int:routine_id>', methods=['DELETE'])
@jwt_required()
def delete_routine(routine_id):
    """Eliminar rutina"""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        db.session.delete(routine)
        db.session.commit()
        
        return jsonify({
            'message': 'Rutina eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar rutina: {str(e)}'}), 500

@routines_bp.route('/<int:routine_id>/toggle', methods=['POST'])
@jwt_required()
def toggle_routine(routine_id):
    """Activar/desactivar rutina"""
    try:
        user_id = get_jwt_identity()
        routine = Routine.query.filter_by(id=routine_id, user_id=user_id).first()
        
        if not routine:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        routine.is_active = not routine.is_active
        db.session.commit()
        
        return jsonify({
            'message': f'Rutina {"activada" if routine.is_active else "desactivada"} exitosamente',
            'routine': routine.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al cambiar estado de rutina: {str(e)}'}), 500
