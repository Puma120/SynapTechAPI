#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar Flask app
export FLASK_APP=app.py

# Inicializar migraciones si no existen
if [ ! -d "migrations" ]; then
    echo "Inicializando migraciones..."
    flask db init
fi

# Crear y aplicar migraciones
echo "Generando migraciones..."
flask db migrate -m "Initial migration" || true

echo "Aplicando migraciones..."
flask db upgrade

echo "Build completado exitosamente!"
