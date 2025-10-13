# SynapTech Backend API

API REST para la aplicacion SynapTech - Sistema de gestion de tareas y rutinas para personas con ADHD.

## Caracteristicas

- Autenticacion JWT
- Gestion de tareas y rutinas
- Integracion con Google Gemini AI
- Sincronizacion con dispositivo collar
- Integracion con Google Calendar
- Generacion de reportes PDF/CSV
- Metricas de productividad

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Google Gemini API Key
- Google Calendar API credentials (opcional)

## Instalacion

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Inicializar base de datos:
```bash
# Crear base de datos PostgreSQL
createdb synaptech_db

# Inicializar tablas
flask init-db
```

## Ejecucion

### Desarrollo
```bash
python run.py
```

### Produccion con Gunicorn
```bash
gunicorn -c gunicorn_config.py run:app
```

## Endpoints Principales

### Autenticacion
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesion
- `GET /api/auth/me` - Obtener usuario actual

### Tareas
- `GET /api/tasks` - Listar tareas
- `POST /api/tasks` - Crear tarea
- `PUT /api/tasks/:id` - Actualizar tarea
- `DELETE /api/tasks/:id` - Eliminar tarea

### Rutinas
- `GET /api/routines` - Listar rutinas
- `POST /api/routines` - Crear rutina
- `PUT /api/routines/:id` - Actualizar rutina

### IA
- `POST /api/ai/transcribe-task` - Transcribir voz a tarea
- `POST /api/ai/prioritize-tasks` - Priorizar tareas con IA
- `POST /api/ai/chat` - Chat con asistente IA

### Reportes
- `GET /api/reports/metrics` - Obtener metricas
- `POST /api/reports/pdf` - Generar reporte PDF
- `GET /api/reports/dashboard` - Datos de dashboard

## Estructura del Proyecto

```
backend/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Endpoints de la API
│   ├── services/        # Servicios (IA, Calendar, Reports)
│   ├── utils/           # Utilidades y validadores
│   └── create_app.py    # Factory de la aplicacion
├── config.py            # Configuracion
├── run.py              # Punto de entrada
└── requirements.txt    # Dependencias
```

## Seguridad

- Las contrasenas se hashean con Werkzeug
- Autenticacion mediante JWT
- CORS configurado para origenes permitidos
- Validacion de datos en todos los endpoints

## Base de Datos

El sistema utiliza PostgreSQL con los siguientes modelos principales:

- **User**: Usuarios del sistema
- **Task**: Tareas individuales
- **Routine**: Rutinas diarias/semanales
- **DeviceSync**: Sincronizacion con dispositivo
- **ProductivityMetric**: Metricas de productividad
- **ReminderLog**: Registro de recordatorios

## Integraciones

### Google Gemini AI
- Transcripcion de voz a tareas
- Priorizacion inteligente
- Sugerencias de rutinas
- Analisis de patrones

### Google Calendar
- Sincronizacion de tareas
- Creacion automatica de eventos
- Actualizacion bidireccional

## Licencia

Copyright 2025 SynapTech
