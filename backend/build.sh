#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

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
