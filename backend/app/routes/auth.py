from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        role = data.get('role', 'user')
        
        # Validar campos requeridos
        if not email or not password or not full_name:
            return jsonify({'error': 'Email, contrasena y nombre completo son requeridos'}), 400
        
        # Validar email
        if not validate_email(email):
            return jsonify({'error': 'Email invalido'}), 400
        
        # Validar contrasena
        password_valid, password_error = validate_password(password)
        if not password_valid:
            return jsonify({'error': password_error}), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'El usuario ya existe'}), 409
        
        # Crear nuevo usuario
        user = User(
            email=email,
            full_name=full_name,
            role=role if role in ['user', 'caregiver', 'therapist'] else 'user'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al registrar usuario: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicio de sesion"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email y contrasena son requeridos'}), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciales invalidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuario inactivo'}), 403
        
        # Generar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Inicio de sesion exitoso',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al iniciar sesion: {str(e)}'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar token de acceso"""
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al renovar token: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtener usuario actual"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener usuario: {str(e)}'}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Actualizar perfil de usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'full_name' in data:
            user.full_name = data['full_name'].strip()
        
        if 'email' in data:
            new_email = data['email'].strip().lower()
            if new_email != user.email:
                if not validate_email(new_email):
                    return jsonify({'error': 'Email invalido'}), 400
                
                existing = User.query.filter_by(email=new_email).first()
                if existing:
                    return jsonify({'error': 'Email ya esta en uso'}), 409
                
                user.email = new_email
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar perfil: {str(e)}'}), 500

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Cambiar contrasena"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Contrasena actual y nueva son requeridas'}), 400
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Contrasena actual incorrecta'}), 401
        
        password_valid, password_error = validate_password(new_password)
        if not password_valid:
            return jsonify({'error': password_error}), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'message': 'Contrasena cambiada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al cambiar contrasena: {str(e)}'}), 500
