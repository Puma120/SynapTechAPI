from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.sync import DeviceSync, ReminderLog

sync_bp = Blueprint('sync', __name__, url_prefix='/api/sync')

@sync_bp.route('/device', methods=['POST'])
@jwt_required()
def sync_device():
    """Sincronizar datos con el dispositivo collar"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        device_id = data.get('device_id', '').strip()
        sync_type = data.get('sync_type', 'ble')
        payload = data.get('data', {})
        
        if not device_id:
            return jsonify({'error': 'ID de dispositivo requerido'}), 400
        
        # Crear registro de sincronizacion
        device_sync = DeviceSync(
            user_id=user_id,
            device_id=device_id,
            sync_type=sync_type,
            data_payload=payload,
            status='synced',
            synced_at=datetime.utcnow()
        )
        
        db.session.add(device_sync)
        db.session.commit()
        
        return jsonify({
            'message': 'Sincronizacion exitosa',
            'sync': device_sync.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al sincronizar: {str(e)}'}), 500

@sync_bp.route('/device/status', methods=['GET'])
@jwt_required()
def get_sync_status():
    """Obtener estado de sincronizacion"""
    try:
        user_id = get_jwt_identity()
        
        latest_sync = DeviceSync.query.filter_by(
            user_id=user_id
        ).order_by(DeviceSync.created_at.desc()).first()
        
        if not latest_sync:
            return jsonify({
                'status': 'never_synced',
                'last_sync': None
            }), 200
        
        return jsonify({
            'status': 'synced',
            'last_sync': latest_sync.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener estado: {str(e)}'}), 500

@sync_bp.route('/reminders/send', methods=['POST'])
@jwt_required()
def send_reminder():
    """Enviar recordatorio haptico al dispositivo"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        task_id = data.get('task_id')
        reminder_type = data.get('reminder_type', 'haptic')
        
        if not task_id:
            return jsonify({'error': 'ID de tarea requerido'}), 400
        
        # Registrar recordatorio
        reminder_log = ReminderLog(
            user_id=user_id,
            task_id=task_id,
            reminder_type=reminder_type,
            sent_at=datetime.utcnow()
        )
        
        db.session.add(reminder_log)
        db.session.commit()
        
        # En produccion, aqui se enviaria el comando BLE al collar
        
        return jsonify({
            'message': 'Recordatorio enviado',
            'reminder': reminder_log.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al enviar recordatorio: {str(e)}'}), 500

@sync_bp.route('/reminders/acknowledge/<int:reminder_id>', methods=['POST'])
@jwt_required()
def acknowledge_reminder(reminder_id):
    """Marcar recordatorio como reconocido"""
    try:
        user_id = get_jwt_identity()
        
        reminder = ReminderLog.query.filter_by(
            id=reminder_id,
            user_id=user_id
        ).first()
        
        if not reminder:
            return jsonify({'error': 'Recordatorio no encontrado'}), 404
        
        reminder.was_acknowledged = True
        reminder.acknowledged_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Recordatorio reconocido',
            'reminder': reminder.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al reconocer recordatorio: {str(e)}'}), 500

@sync_bp.route('/offline-queue', methods=['POST'])
@jwt_required()
def process_offline_queue():
    """Procesar cola de sincronizacion offline"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        offline_items = data.get('items', [])
        
        if not offline_items:
            return jsonify({'error': 'No hay items para sincronizar'}), 400
        
        synced_count = 0
        errors = []
        
        for item in offline_items:
            try:
                device_sync = DeviceSync(
                    user_id=user_id,
                    device_id=item.get('device_id', 'offline'),
                    sync_type='offline',
                    data_payload=item.get('data', {}),
                    status='synced',
                    synced_at=datetime.utcnow()
                )
                db.session.add(device_sync)
                synced_count += 1
            except Exception as e:
                errors.append(str(e))
        
        db.session.commit()
        
        return jsonify({
            'message': f'{synced_count} items sincronizados',
            'synced': synced_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al procesar cola: {str(e)}'}), 500
