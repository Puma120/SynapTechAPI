# SynapTech API - Backend Simplificado con IA# SynapTech Backend API



API REST minimalista para gestión de tareas con procesamiento de IA usando Google Gemini.API REST para la aplicacion SynapTech - Sistema de gestion de tareas y rutinas para personas con ADHD.



## 🚀 Características## 🚀 Inicio Rápido



- **Procesamiento IA**: Tareas procesadas automáticamente por Gemini (extrae título, prioridad, fecha de vencimiento)### Despliegue en Render (Producción)

- **Autenticación JWT**: Login seguro con tokens- 📖 **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida de despliegue

- **Rutinas Dinámicas**: Generadas en tiempo real por IA basadas en tareas pendientes- 📚 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Documentación completa de despliegue

- **Base de Datos**: PostgreSQL en Render- 📡 **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - Referencia de endpoints

- **Despliegue**: Render.com con auto-deploy desde GitHub

### Desarrollo Local

## 📋 Endpoints DisponiblesVer sección [Instalación](#instalacion) abajo



### Autenticación## Caracteristicas



#### 1. Registro de Usuario- Autenticacion JWT

```http- Gestion de tareas y rutinas

POST /api/auth/register- Integracion con Google Gemini AI

```- Sincronizacion con dispositivo collar

- Integracion con Google Calendar

**Body:**- Generacion de reportes PDF/CSV

```json- Metricas de productividad

{

  "email": "usuario@example.com",## Requisitos

  "password": "Password123!",

  "name": "Juan Pérez"- Python 3.8+

}- PostgreSQL 12+

```- Google Gemini API Key

- Google Calendar API credentials (opcional)

**Respuesta (201):**

```json## Instalacion

{

  "message": "Usuario registrado exitosamente",1. Crear entorno virtual:

  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",```bash

  "user": {python -m venv venv

    "id": 1,source venv/bin/activate  # En Windows: venv\Scripts\activate

    "email": "usuario@example.com",```

    "name": "Juan Pérez"

  }2. Instalar dependencias:

}```bash

```pip install -r requirements.txt

```

---

3. Configurar variables de entorno:

#### 2. Login```bash

```httpcp .env.example .env

POST /api/auth/login# Editar .env con tus credenciales

``````



**Body:**4. Inicializar base de datos:

```json```bash

{# Crear base de datos PostgreSQL

  "email": "usuario@example.com",createdb synaptech_db

  "password": "Password123!"

}# Inicializar tablas

```flask init-db

```

**Respuesta (200):**

```json## Ejecucion

{

  "message": "Login exitoso",### Desarrollo

  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",```bash

  "user": {python wsgi.py

    "id": 1,```

    "email": "usuario@example.com",

    "name": "Juan Pérez"### Produccion con Gunicorn

  }```bash

}gunicorn -c gunicorn_config.py wsgi:app

``````



---## Endpoints Principales



#### 3. Obtener Usuario Actual### Autenticacion

```http- `POST /api/auth/register` - Registrar usuario

GET /api/auth/me- `POST /api/auth/login` - Iniciar sesion

Authorization: Bearer {token}- `GET /api/auth/me` - Obtener usuario actual

```

### Tareas

**Respuesta (200):**- `GET /api/tasks` - Listar tareas

```json- `POST /api/tasks` - Crear tarea

{- `PUT /api/tasks/:id` - Actualizar tarea

  "id": 1,- `DELETE /api/tasks/:id` - Eliminar tarea

  "email": "usuario@example.com",

  "name": "Juan Pérez",### Rutinas

  "created_at": "2024-01-15T10:30:00"- `GET /api/routines` - Listar rutinas

}- `POST /api/routines` - Crear rutina

```- `PUT /api/routines/:id` - Actualizar rutina



---### IA

- `POST /api/ai/transcribe-task` - Transcribir voz a tarea

### Tareas- `POST /api/ai/prioritize-tasks` - Priorizar tareas con IA

- `POST /api/ai/chat` - Chat con asistente IA

#### 4. Crear Tarea (con IA)

```http### Reportes

POST /api/tasks- `GET /api/reports/metrics` - Obtener metricas

Authorization: Bearer {token}- `POST /api/reports/pdf` - Generar reporte PDF

```- `GET /api/reports/dashboard` - Datos de dashboard



**Body:**## Estructura del Proyecto

```json

{```

  "cuerpo": "Tengo que terminar el informe urgente para mañana",backend/

  "fecha": "2024-01-20"├── app/

}│   ├── models/          # Modelos de base de datos

```│   ├── routes/          # Endpoints de la API

│   ├── services/        # Servicios (IA, Calendar, Reports)

**Respuesta (201):**│   ├── utils/           # Utilidades y validadores

```json│   └── create_app.py    # Factory de la aplicacion

{├── config.py            # Configuracion

  "title": "Terminar informe urgente",├── run.py              # Punto de entrada

  "priority": "urgent",└── requirements.txt    # Dependencias

  "due_date": "2024-01-20T23:59:59",```

  "id_tarea": 42

}## Seguridad

```

- Las contrasenas se hashean con Werkzeug

> **Nota**: El agente de IA extrae automáticamente el título, prioridad y fecha de vencimiento del texto ingresado.- Autenticacion mediante JWT

- CORS configurado para origenes permitidos

---- Validacion de datos en todos los endpoints



#### 5. Actualizar Estado de Tarea## Base de Datos

```http

PUT /api/tasks/{task_id}El sistema utiliza PostgreSQL con los siguientes modelos principales:

Authorization: Bearer {token}

```- **User**: Usuarios del sistema

- **Task**: Tareas individuales

**Body:**- **Routine**: Rutinas diarias/semanales

```json- **DeviceSync**: Sincronizacion con dispositivo

{- **ProductivityMetric**: Metricas de productividad

  "status": "completed"- **ReminderLog**: Registro de recordatorios

}

```## Integraciones



**Respuesta (200):**### Google Gemini AI

```json- Transcripcion de voz a tareas

{- Priorizacion inteligente

  "message": "Tarea actualizada exitosamente",- Sugerencias de rutinas

  "task": {- Analisis de patrones

    "id": 42,

    "title": "Terminar informe urgente",### Google Calendar

    "status": "completed",- Sincronizacion de tareas

    "completed_at": "2024-01-16T15:30:00"- Creacion automatica de eventos

  }- Actualizacion bidireccional

}

```## Licencia



**Estados válidos**: `pending`, `in_progress`, `completed`Copyright 2025 SynapTech


---

### Rutinas

#### 6. Obtener Rutinas Generadas por IA
```http
GET /api/routines
Authorization: Bearer {token}
```

**Respuesta (200):**
```json
{
  "message": "Rutinas generadas exitosamente",
  "routines": [
    {
      "id_tarea": 42,
      "cuerpo": "Mañana (8:00-10:00) - 2h estimadas\nPasos:\n1. Reunir datos\n2. Redactar borrador\n3. Revisar\nConsejo: Hazlo en la mañana cuando tienes más energía"
    },
    {
      "id_tarea": 43,
      "cuerpo": "Hoy (14:00-14:30) - 30min estimados\nPasos:\n1. Hacer lista de compras\n2. Ir al supermercado\nConsejo: Agrupa esta tarea con otras salidas"
    }
  ]
}
```

> **Nota**: Las rutinas se generan dinámicamente cada vez que accedes a esta ruta, basándose en tus tareas pendientes.

---

## 🛠️ Instalación Local

### 1. Clonar Repositorio
```bash
git clone https://github.com/Puma120/SynapTechAPI.git
cd SynapTechAPI/backend
```

### 2. Configurar Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en `backend/`:
```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=tu_secret_key_aqui
JWT_SECRET_KEY=tu_jwt_secret_key_aqui

# Database
DATABASE_URL=postgresql://user:password@localhost/synaptech

# Google APIs
GEMINI_API_KEY=tu_api_key_de_gemini
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret

# CORS
FRONTEND_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Inicializar Base de Datos
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Ejecutar Servidor
```bash
python run.py
```

API disponible en: `http://localhost:5000`

---

## 🚀 Despliegue en Render

### Variables de Entorno en Render
Configura las siguientes variables:
- `DATABASE_URL`: (Render auto-configura si usas PostgreSQL de Render)
- `SECRET_KEY`: Genera uno seguro
- `JWT_SECRET_KEY`: Genera uno diferente y seguro
- `GEMINI_API_KEY`: Tu API key de Google AI Studio
- `GOOGLE_CLIENT_ID`: De Google Cloud Console
- `GOOGLE_CLIENT_SECRET`: De Google Cloud Console
- `FRONTEND_ORIGINS`: URLs de tu frontend (separadas por coma)

### Comando de Inicio
```
gunicorn -c gunicorn_config.py wsgi:app
```

### Build Command
```
./build.sh
```

---

## 🧠 Cómo Funciona la IA

### Procesamiento de Tareas
1. Usuario envía texto como: `"Tengo que llamar al doctor mañana por la tarde"`
2. Gemini analiza el texto y extrae:
   - **Título**: "Llamar al doctor"
   - **Prioridad**: "high" (detecta urgencia implícita)
   - **Fecha**: "2024-01-17T15:00:00" (infiere "por la tarde")
   - **Descripción refinada**: "Llamar al doctor para seguimiento"

### Generación de Rutinas
1. API consulta todas las tareas pendientes del usuario
2. Gemini las analiza y crea una rutina optimizada:
   - Ordena por prioridad y fecha
   - Sugiere horarios óptimos
   - Estima tiempos
   - Agrupa tareas similares
   - Incluye consejos para ADHD

---

## 📦 Dependencias Principales

```txt
Flask==3.1.2
Flask-JWT-Extended==4.7.1
Flask-Migrate==4.1.0
Flask-CORS==5.0.0
psycopg2-binary==2.9.10
google-generativeai==0.8.3
gunicorn==23.0.0
python-dotenv==1.0.1
```

---

## 🔐 Seguridad

- **JWT Tokens**: Autenticación con expiración de 24h
- **Passwords**: Hasheados con Werkzeug
- **CORS**: Configurado solo para orígenes permitidos
- **SQL Injection**: Protegido por SQLAlchemy ORM
- **Variables sensibles**: En `.env` (no versionadas)

---

## 📝 Modelo de Datos

### User
```python
{
  "id": int,
  "email": str (unique),
  "password_hash": str,
  "name": str,
  "created_at": datetime
}
```

### Task
```python
{
  "id": int,
  "user_id": int (FK),
  "title": str,
  "body": text,
  "priority": str (low|medium|high|urgent),
  "due_date": datetime,
  "status": str (pending|in_progress|completed),
  "completed_at": datetime,
  "created_at": datetime
}
```

---

## 🧪 Testing

Usa el archivo `SynapTech_Postman_Collection.json` para importar todas las pruebas en Postman.

---

## 📞 Soporte

- GitHub: [Puma120/SynapTechAPI](https://github.com/Puma120/SynapTechAPI)
- Issues: Crear en el repositorio

---

## 📄 Licencia

Ver archivo `LICENSE` en la raíz del proyecto.
