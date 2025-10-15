#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar Flask app
export FLASK_APP=wsgi.py

# Limpiar migraciones anteriores locales
if [ -d "migrations" ]; then
    echo "Limpiando migraciones anteriores..."
    rm -rf migrations
fi

# Limpiar tabla de versiones de Alembic en la base de datos
echo "Limpiando versiones de Alembic en la base de datos..."
python -c "
from wsgi import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Intentar eliminar la tabla alembic_version si existe
        db.session.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
        db.session.commit()
        print('✓ Tabla alembic_version eliminada')
    except Exception as e:
        print(f'Nota: {e}')
        db.session.rollback()
" || echo "Continuando..."

# Inicializar migraciones
echo "Inicializando migraciones..."
flask db init

# Crear migraciones
echo "Generando migraciones iniciales..."
flask db migrate -m "Initial migration"

# Aplicar migraciones
echo "Aplicando migraciones..."
flask db upgrade

echo "Build completado exitosamente!"
