import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuracion base de la aplicacion"""
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Fix para Render: Render usa postgres:// pero SQLAlchemy necesita postgresql://
    database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/synaptech_db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuracion JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    
    # Configuracion CORS
    # Añade tu dominio de frontend en producción aquí
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
    CORS_ORIGINS = cors_origins.split(',')

class DevelopmentConfig(Config):
    """Configuracion para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuracion para produccion"""
    DEBUG = False
    TESTING = False
    # La URL ya se configura en la clase base Config

class TestingConfig(Config):
    """Configuracion para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/synaptech_test_db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
