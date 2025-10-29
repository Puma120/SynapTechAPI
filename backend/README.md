# SynapTech API - Backend con IA y Transcripción de Audio# SynapTech API - Backend Simplificado con IA# SynapTech Backend API



API REST minimalista para gestión de tareas con procesamiento de IA usando Google Gemini y transcripción de audio con Google Speech-to-Text.



## 🚀 CaracterísticasAPI REST minimalista para gestión de tareas con procesamiento de IA usando Google Gemini.API REST para la aplicacion SynapTech - Sistema de gestion de tareas y rutinas para personas con ADHD.



- **Procesamiento IA**: Tareas procesadas automáticamente por Gemini (extrae título, prioridad, fecha de vencimiento)

- **Transcripción de Audio**: Soporte para crear tareas desde archivos de audio WAV

- **Autenticación JWT**: Login seguro con tokens## 🚀 Características## 🚀 Inicio Rápido

- **Rutinas Dinámicas**: Generadas en tiempo real por IA basadas en tareas pendientes

- **Base de Datos**: PostgreSQL en Render

- **Despliegue**: Render.com con auto-deploy desde GitHub

- **Procesamiento IA**: Tareas procesadas automáticamente por Gemini (extrae título, prioridad, fecha de vencimiento)### Despliegue en Render (Producción)

## 📋 Endpoints Disponibles

- **Autenticación JWT**: Login seguro con tokens- 📖 **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida de despliegue

### Autenticación

- **Rutinas Dinámicas**: Generadas en tiempo real por IA basadas en tareas pendientes- 📚 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Documentación completa de despliegue

#### 1. Registro de Usuario

```http- **Base de Datos**: PostgreSQL en Render- 📡 **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - Referencia de endpoints

POST /api/auth/register

Content-Type: application/json- **Despliegue**: Render.com con auto-deploy desde GitHub

```

### Desarrollo Local

**Body:**

```json## 📋 Endpoints DisponiblesVer sección [Instalación](#instalacion) abajo

{

  "email": "usuario@example.com",

  "password": "Password123!",

  "name": "Juan Pérez"### Autenticación## Caracteristicas

}

```



**Respuesta (201):**#### 1. Registro de Usuario- Autenticacion JWT

```json

{```http- Gestion de tareas y rutinas

  "message": "Usuario registrado exitosamente",

  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",POST /api/auth/register- Integracion con Google Gemini AI

  "user": {

    "id": 1,```- Sincronizacion con dispositivo collar

    "email": "usuario@example.com",

    "name": "Juan Pérez"- Integracion con Google Calendar

  }

}**Body:**- Generacion de reportes PDF/CSV

```

```json- Metricas de productividad

---

{

#### 2. Login

```http  "email": "usuario@example.com",## Requisitos

POST /api/auth/login

Content-Type: application/json  "password": "Password123!",

```

  "name": "Juan Pérez"- Python 3.8+

**Body:**

```json}- PostgreSQL 12+

{

  "email": "usuario@example.com",```- Google Gemini API Key

  "password": "Password123!"

}- Google Calendar API credentials (opcional)

```

**Respuesta (201):**

**Respuesta (200):**

```json```json## Instalacion

{

  "message": "Login exitoso",{

  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",

  "user": {  "message": "Usuario registrado exitosamente",1. Crear entorno virtual:

    "id": 1,

    "email": "usuario@example.com",  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",```bash

    "name": "Juan Pérez"

  }  "user": {python -m venv venv

}

```    "id": 1,source venv/bin/activate  # En Windows: venv\Scripts\activate



---    "email": "usuario@example.com",```



#### 3. Obtener Usuario Actual    "name": "Juan Pérez"

```http

GET /api/auth/me  }2. Instalar dependencias:

Authorization: Bearer {token}

```}```bash



**Respuesta (200):**```pip install -r requirements.txt

```json

{```

  "id": 1,

  "email": "usuario@example.com",---

  "name": "Juan Pérez",

  "created_at": "2024-01-15T10:30:00"3. Configurar variables de entorno:

}

```#### 2. Login```bash



---```httpcp .env.example .env



### TareasPOST /api/auth/login# Editar .env con tus credenciales



#### 4. Crear Tarea (con IA)``````



**Opción A: Desde Texto**

```http

POST /api/tasks**Body:**4. Inicializar base de datos:

Authorization: Bearer {token}

Content-Type: application/json```json```bash

```

{# Crear base de datos PostgreSQL

**Body:**

```json  "email": "usuario@example.com",createdb synaptech_db

{

  "cuerpo": "Tengo que terminar el informe urgente para mañana",  "password": "Password123!"

  "fecha": "2024-01-20"

}}# Inicializar tablas

```

```flask init-db

**Opción B: Desde Audio (WAV)**

```http```

POST /api/tasks

Authorization: Bearer {token}**Respuesta (200):**

Content-Type: multipart/form-data

``````json## Ejecucion



**Form Data:**{

- `audio`: (archivo WAV)

- `fecha`: "2024-01-20" (opcional)  "message": "Login exitoso",### Desarrollo



**Opción C: Audio + Texto Combinado**  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",```bash

```http

POST /api/tasks  "user": {python wsgi.py

Authorization: Bearer {token}

Content-Type: multipart/form-data    "id": 1,```

```

    "email": "usuario@example.com",

**Form Data:**

- `audio`: (archivo WAV)    "name": "Juan Pérez"### Produccion con Gunicorn

- `cuerpo`: "Nota adicional"

- `fecha`: "2024-01-20" (opcional)  }```bash



**Respuesta (201):**}gunicorn -c gunicorn_config.py wsgi:app

```json

{``````

  "title": "Terminar informe urgente",

  "priority": "urgent",

  "due_date": "2024-01-20T23:59:59",

  "id_tarea": 42---## Endpoints Principales

}

```



> **Nota**: El agente de IA:#### 3. Obtener Usuario Actual### Autenticacion

> - Transcribe el audio automáticamente si se envía un archivo

> - Extrae título, prioridad y fecha del texto/audio```http- `POST /api/auth/register` - Registrar usuario

> - Combina texto + audio si se envían ambos

GET /api/auth/me- `POST /api/auth/login` - Iniciar sesion

**Formatos de audio soportados:**

- WAV (recomendado)Authorization: Bearer {token}- `GET /api/auth/me` - Obtener usuario actual

- Tasa de muestreo: cualquiera (se detecta automáticamente)

- Idioma: Español (es-MX por defecto)```



---### Tareas



#### 5. Actualizar Estado de Tarea**Respuesta (200):**- `GET /api/tasks` - Listar tareas

```http

PUT /api/tasks/{task_id}```json- `POST /api/tasks` - Crear tarea

Authorization: Bearer {token}

Content-Type: application/json{- `PUT /api/tasks/:id` - Actualizar tarea

```

  "id": 1,- `DELETE /api/tasks/:id` - Eliminar tarea

**Body:**

```json  "email": "usuario@example.com",

{

  "status": "completed"  "name": "Juan Pérez",### Rutinas

}

```  "created_at": "2024-01-15T10:30:00"- `GET /api/routines` - Listar rutinas



**Respuesta (200):**}- `POST /api/routines` - Crear rutina

```json

{```- `PUT /api/routines/:id` - Actualizar rutina

  "message": "Tarea actualizada exitosamente",

  "task": {

    "id": 42,

    "title": "Terminar informe urgente",---### IA

    "status": "completed",

    "completed_at": "2024-01-16T15:30:00"- `POST /api/ai/transcribe-task` - Transcribir voz a tarea

  }

}### Tareas- `POST /api/ai/prioritize-tasks` - Priorizar tareas con IA

```

- `POST /api/ai/chat` - Chat con asistente IA

**Estados válidos**: `pending`, `in_progress`, `completed`

#### 4. Crear Tarea (con IA)

---

```http### Reportes

### Rutinas

POST /api/tasks- `GET /api/reports/metrics` - Obtener metricas

#### 6. Obtener Rutinas Generadas por IA

```httpAuthorization: Bearer {token}- `POST /api/reports/pdf` - Generar reporte PDF

GET /api/routines

Authorization: Bearer {token}```- `GET /api/reports/dashboard` - Datos de dashboard

```



**Respuesta (200):**

```json**Body:**## Estructura del Proyecto

{

  "message": "Rutinas generadas exitosamente",```json

  "routines": [

    {{```

      "id_tarea": 42,

      "cuerpo": "Mañana (8:00-10:00) - 2h estimadas\nPasos:\n1. Reunir datos\n2. Redactar borrador\n3. Revisar\nConsejo: Hazlo en la mañana cuando tienes más energía"  "cuerpo": "Tengo que terminar el informe urgente para mañana",backend/

    }

  ]  "fecha": "2024-01-20"├── app/

}

```}│   ├── models/          # Modelos de base de datos



> **Nota**: Las rutinas se generan dinámicamente cada vez que accedes a esta ruta, basándose en tus tareas pendientes.```│   ├── routes/          # Endpoints de la API



---│   ├── services/        # Servicios (IA, Calendar, Reports)



## 🛠️ Instalación Local**Respuesta (201):**│   ├── utils/           # Utilidades y validadores



### 1. Clonar Repositorio```json│   └── create_app.py    # Factory de la aplicacion

```bash

git clone https://github.com/Puma120/SynapTechAPI.git{├── config.py            # Configuracion

cd SynapTechAPI/backend

```  "title": "Terminar informe urgente",├── run.py              # Punto de entrada



### 2. Configurar Entorno Virtual  "priority": "urgent",└── requirements.txt    # Dependencias

```bash

python -m venv venv  "due_date": "2024-01-20T23:59:59",```

.\venv\Scripts\activate  # Windows

source venv/bin/activate  # Linux/Mac  "id_tarea": 42

```

}## Seguridad

### 3. Instalar Dependencias

```bash```

pip install -r requirements.txt

```- Las contrasenas se hashean con Werkzeug



### 4. Configurar Variables de Entorno> **Nota**: El agente de IA extrae automáticamente el título, prioridad y fecha de vencimiento del texto ingresado.- Autenticacion mediante JWT

Crea un archivo `.env` en `backend/`:

```env- CORS configurado para origenes permitidos

FLASK_APP=wsgi.py

FLASK_ENV=development---- Validacion de datos en todos los endpoints

SECRET_KEY=tu_secret_key_aqui

JWT_SECRET_KEY=tu_jwt_secret_key_aqui



# Database#### 5. Actualizar Estado de Tarea## Base de Datos

DATABASE_URL=postgresql://user:password@localhost/synaptech

```http

# Google APIs

GEMINI_API_KEY=tu_api_key_de_geminiPUT /api/tasks/{task_id}El sistema utiliza PostgreSQL con los siguientes modelos principales:

SPEECH_API_KEY=tu_api_key_de_speech_to_text

GOOGLE_CLIENT_ID=tu_client_idAuthorization: Bearer {token}

GOOGLE_CLIENT_SECRET=tu_client_secret

```- **User**: Usuarios del sistema

# CORS

FRONTEND_ORIGINS=http://localhost:3000,http://localhost:5173- **Task**: Tareas individuales

```

**Body:**- **Routine**: Rutinas diarias/semanales

### 5. Inicializar Base de Datos

```bash```json- **DeviceSync**: Sincronizacion con dispositivo

flask db init

flask db migrate -m "Initial migration"{- **ProductivityMetric**: Metricas de productividad

flask db upgrade

```  "status": "completed"- **ReminderLog**: Registro de recordatorios



### 6. Ejecutar Servidor}

```bash

python run.py```## Integraciones

```



API disponible en: `http://localhost:5000`

**Respuesta (200):**### Google Gemini AI

---

```json- Transcripcion de voz a tareas

## 🚀 Despliegue en Render

{- Priorizacion inteligente

### Variables de Entorno en Render

Configura las siguientes variables:  "message": "Tarea actualizada exitosamente",- Sugerencias de rutinas

- `DATABASE_URL`: (Render auto-configura si usas PostgreSQL de Render)

- `SECRET_KEY`: Genera uno seguro  "task": {- Analisis de patrones

- `JWT_SECRET_KEY`: Genera uno diferente y seguro

- `GEMINI_API_KEY`: Tu API key de Google AI Studio    "id": 42,

- `SPEECH_API_KEY`: Tu API key de Google Cloud Speech-to-Text

- `GOOGLE_CLIENT_ID`: De Google Cloud Console    "title": "Terminar informe urgente",### Google Calendar

- `GOOGLE_CLIENT_SECRET`: De Google Cloud Console

- `FRONTEND_ORIGINS`: URLs de tu frontend (separadas por coma)    "status": "completed",- Sincronizacion de tareas



### Comando de Inicio    "completed_at": "2024-01-16T15:30:00"- Creacion automatica de eventos

```

gunicorn -c gunicorn_config.py wsgi:app  }- Actualizacion bidireccional

```

}

### Build Command

``````## Licencia

./build.sh

```



---**Estados válidos**: `pending`, `in_progress`, `completed`Copyright 2025 SynapTech



## 🧠 Cómo Funciona la IA

---

### Procesamiento de Tareas

1. Usuario envía texto o audio### Rutinas

2. Si es audio, se transcribe automáticamente con Google Speech-to-Text

3. Gemini analiza el texto y extrae:#### 6. Obtener Rutinas Generadas por IA

   - **Título**: "Llamar al doctor"```http

   - **Prioridad**: "high" (detecta urgencia implícita)GET /api/routines

   - **Fecha**: "2024-01-17T15:00:00" (infiere horarios)Authorization: Bearer {token}

   - **Descripción refinada**: Mejora la redacción```



### Generación de Rutinas**Respuesta (200):**

1. API consulta todas las tareas pendientes del usuario```json

2. Gemini las analiza y crea una rutina optimizada:{

   - Ordena por prioridad y fecha  "message": "Rutinas generadas exitosamente",

   - Sugiere horarios óptimos  "routines": [

   - Estima tiempos    {

   - Agrupa tareas similares      "id_tarea": 42,

   - Incluye consejos para ADHD      "cuerpo": "Mañana (8:00-10:00) - 2h estimadas\nPasos:\n1. Reunir datos\n2. Redactar borrador\n3. Revisar\nConsejo: Hazlo en la mañana cuando tienes más energía"

    },

### Transcripción de Audio    {

1. Usuario sube archivo WAV      "id_tarea": 43,

2. Se detecta automáticamente la tasa de muestreo      "cuerpo": "Hoy (14:00-14:30) - 30min estimados\nPasos:\n1. Hacer lista de compras\n2. Ir al supermercado\nConsejo: Agrupa esta tarea con otras salidas"

3. Google Speech-to-Text transcribe en español    }

4. El texto se procesa igual que un texto escrito  ]

}

---```



## 📦 Dependencias Principales> **Nota**: Las rutinas se generan dinámicamente cada vez que accedes a esta ruta, basándose en tus tareas pendientes.



```txt---

Flask==3.1.2

Flask-JWT-Extended==4.7.1## 🛠️ Instalación Local

Flask-Migrate==4.1.0

Flask-CORS==5.0.0### 1. Clonar Repositorio

psycopg2-binary==2.9.10```bash

google-generativeai==0.8.3git clone https://github.com/Puma120/SynapTechAPI.git

google-cloud-speech==2.27.0cd SynapTechAPI/backend

gunicorn==23.0.0```

python-dotenv==1.0.1

requests==2.32.3### 2. Configurar Entorno Virtual

``````bash

python -m venv venv

---.\venv\Scripts\activate  # Windows

source venv/bin/activate  # Linux/Mac

## 🔐 Seguridad```



- **JWT Tokens**: Autenticación con expiración de 1h### 3. Instalar Dependencias

- **Passwords**: Hasheados con Werkzeug```bash

- **CORS**: Configurado solo para orígenes permitidospip install -r requirements.txt

- **SQL Injection**: Protegido por SQLAlchemy ORM```

- **Variables sensibles**: En `.env` (no versionadas)

- **API Keys**: Nunca expuestas en el frontend### 4. Configurar Variables de Entorno

Crea un archivo `.env` en `backend/`:

---```env

FLASK_APP=wsgi.py

## 📝 Modelo de DatosFLASK_ENV=development

SECRET_KEY=tu_secret_key_aqui

### UserJWT_SECRET_KEY=tu_jwt_secret_key_aqui

```python

{# Database

  "id": int,DATABASE_URL=postgresql://user:password@localhost/synaptech

  "email": str (unique),

  "password_hash": str,# Google APIs

  "name": str,GEMINI_API_KEY=tu_api_key_de_gemini

  "created_at": datetimeGOOGLE_CLIENT_ID=tu_client_id

}GOOGLE_CLIENT_SECRET=tu_client_secret

```

# CORS

### TaskFRONTEND_ORIGINS=http://localhost:3000,http://localhost:5173

```python```

{

  "id": int,### 5. Inicializar Base de Datos

  "user_id": int (FK),```bash

  "title": str,flask db init

  "body": text,flask db migrate -m "Initial migration"

  "priority": str (low|medium|high|urgent),flask db upgrade

  "due_date": datetime,```

  "status": str (pending|in_progress|completed),

  "completed_at": datetime,### 6. Ejecutar Servidor

  "created_at": datetime```bash

}python run.py

``````



---API disponible en: `http://localhost:5000`



## 🧪 Testing---



### Pruebas Locales## 🚀 Despliegue en Render



**1. Probar transcripción de audio:**### Variables de Entorno en Render

```bashConfigura las siguientes variables:

python test_speech.py- `DATABASE_URL`: (Render auto-configura si usas PostgreSQL de Render)

```- `SECRET_KEY`: Genera uno seguro

- `JWT_SECRET_KEY`: Genera uno diferente y seguro

**2. Probar endpoint completo:**- `GEMINI_API_KEY`: Tu API key de Google AI Studio

```bash- `GOOGLE_CLIENT_ID`: De Google Cloud Console

# Iniciar servidor primero- `GOOGLE_CLIENT_SECRET`: De Google Cloud Console

python run.py- `FRONTEND_ORIGINS`: URLs de tu frontend (separadas por coma)



# En otra terminal:### Comando de Inicio

python test_audio_endpoint.py```

```gunicorn -c gunicorn_config.py wsgi:app

```

### Colección de Postman

Importa `SynapTech_Postman_Collection.json` en Postman para probar todos los endpoints.### Build Command

```

---./build.sh

```

## 📞 Soporte

---

- GitHub: [Puma120/SynapTechAPI](https://github.com/Puma120/SynapTechAPI)

- Issues: Crear en el repositorio## 🧠 Cómo Funciona la IA



---### Procesamiento de Tareas

1. Usuario envía texto como: `"Tengo que llamar al doctor mañana por la tarde"`

## 📄 Licencia2. Gemini analiza el texto y extrae:

   - **Título**: "Llamar al doctor"

Ver archivo `LICENSE` en la raíz del proyecto.   - **Prioridad**: "high" (detecta urgencia implícita)

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
