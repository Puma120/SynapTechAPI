import os
from app.create_app import create_app
from app import db
from flask_migrate import Migrate

# Crear aplicacion
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

@app.cli.command()
def init_db():
    """Inicializar la base de datos"""
    db.create_all()
    print('Base de datos inicializada')

@app.cli.command()
def reset_db():
    """Resetear la base de datos"""
    db.drop_all()
    db.create_all()
    print('Base de datos reseteada')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
