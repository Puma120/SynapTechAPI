from flask import Flask
from flask_cors import CORS
from config import config
from app import db, jwt

def create_app(config_name='development'):
    """Factory para crear la aplicacion Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints - versión simplificada con IA
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.routines import routines_bp
    from app.routes.medications import medications_bp
    # Rutas antiguas comentadas - ahora todo está integrado con IA
    # from app.routes.ai import ai_bp
    # from app.routes.sync import sync_bp
    # from app.routes.calendar import calendar_bp
    # from app.routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(routines_bp)
    app.register_blueprint(medications_bp)
    # app.register_blueprint(ai_bp)
    # app.register_blueprint(sync_bp)
    # app.register_blueprint(calendar_bp)
    # app.register_blueprint(reports_bp)
    
    # Ruta de salud
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'SynapTech API is running'}, 200
    
    # Ruta raiz
    @app.route('/')
    def index():
        return {
            'message': 'SynapTech API - Asistente con IA para gestión de tareas',
            'version': '2.0.0 - Simplificado',
            'endpoints': {
                'auth': '/api/auth - Autenticación',
                'tasks': '/api/tasks - Crear y gestionar tareas (procesadas por IA)',
                'routines': '/api/routines - Rutinas generadas dinámicamente por IA'
            },
            'features': [
                'Creación de tareas por texto o voz procesadas por IA',
                'El agente extrae automáticamente: título, prioridad y fecha',
                'Rutinas dinámicas generadas en tiempo real por IA',
                'Gestión simplificada de tareas'
            ]
        }, 200
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint no encontrado'}, 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Error interno del servidor'}, 500
    
    return app
