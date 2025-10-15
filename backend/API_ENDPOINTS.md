# 📡 SynapTech API - Endpoints

## Base URL
- **Desarrollo**: `http://localhost:5000`
- **Producción**: `https://tu-app.onrender.com`

---

## 🏥 Health & Info

### GET `/`
Información general de la API

**Response:**
```json
{
  "message": "SynapTech API",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/api/auth",
    "tasks": "/api/tasks",
    "routines": "/api/routines",
    "ai": "/api/ai",
    "sync": "/api/sync",
    "calendar": "/api/calendar",
    "reports": "/api/reports"
  }
}
```

### GET `/health`
Health check

**Response:**
```json
{
  "status": "ok",
  "message": "SynapTech API is running"
}
```

---

## 🔐 Autenticación (`/api/auth`)

### POST `/api/auth/register`
Registrar nuevo usuario

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "Password123!",
  "full_name": "Juan Pérez",
  "role": "user"
}
```

**Response:**
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "full_name": "Juan Pérez",
    "role": "user",
    "is_active": true,
    "created_at": "2025-10-15T10:30:00"
  },
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi..."
}
```

### POST `/api/auth/login`
Iniciar sesión

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "Password123!"
}
```

**Response:**
```json
{
  "message": "Inicio de sesion exitoso",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "full_name": "Juan Pérez",
    "role": "user"
  },
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi..."
}
```

### GET `/api/auth/profile`
Obtener perfil del usuario actual

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "full_name": "Juan Pérez",
    "role": "user",
    "is_active": true,
    "created_at": "2025-10-15T10:30:00"
  }
}
```

---

## ✅ Tareas (`/api/tasks`)

### GET `/api/tasks`
Listar todas las tareas del usuario

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Params:**
- `status` (opcional): `pending`, `in_progress`, `completed`
- `priority` (opcional): `low`, `medium`, `high`

### POST `/api/tasks`
Crear nueva tarea

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "title": "Hacer ejercicio",
  "description": "Salir a correr 30 minutos",
  "due_date": "2025-10-20T09:00:00",
  "priority": "high",
  "category": "health"
}
```

### GET `/api/tasks/:id`
Obtener tarea específica

### PUT `/api/tasks/:id`
Actualizar tarea

### DELETE `/api/tasks/:id`
Eliminar tarea

---

## 🔄 Rutinas (`/api/routines`)

### GET `/api/routines`
Listar todas las rutinas

### POST `/api/routines`
Crear nueva rutina

**Body:**
```json
{
  "name": "Rutina Matutina",
  "description": "Actividades de la mañana",
  "frequency": "daily",
  "tasks": [
    {
      "title": "Desayunar",
      "time": "08:00"
    },
    {
      "title": "Ejercicio",
      "time": "09:00"
    }
  ]
}
```

---

## 🤖 IA & Sugerencias (`/api/ai`)

### POST `/api/ai/suggestions`
Obtener sugerencias de IA para tareas

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "context": "Necesito ayuda con mi productividad",
  "current_tasks": [
    "Estudiar matemáticas",
    "Hacer ejercicio"
  ]
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "title": "Divide estudio en bloques de 25 min",
      "reason": "Técnica Pomodoro mejora concentración",
      "priority": "high"
    }
  ]
}
```

---

## 📅 Calendario (`/api/calendar`)

### GET `/api/calendar/events`
Obtener eventos del calendario

### POST `/api/calendar/sync`
Sincronizar con Google Calendar

---

## 📊 Reportes (`/api/reports`)

### GET `/api/reports/productivity`
Obtener reporte de productividad

**Query Params:**
- `start_date`: Fecha inicio (ISO format)
- `end_date`: Fecha fin (ISO format)

**Response:**
```json
{
  "period": {
    "start": "2025-10-01",
    "end": "2025-10-15"
  },
  "stats": {
    "total_tasks": 45,
    "completed_tasks": 38,
    "completion_rate": 84.4,
    "average_completion_time": "2.5 hours"
  }
}
```

---

## 🔄 Sincronización (`/api/sync`)

### POST `/api/sync/google`
Conectar con Google Calendar

### GET `/api/sync/status`
Ver estado de sincronización

---

## 🔒 Autenticación JWT

Todos los endpoints protegidos requieren un token JWT en el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Obtener Token
1. Haz login en `/api/auth/login`
2. Guarda el `access_token`
3. Inclúyelo en cada petición

### Token Expirado
- **Access Token**: 1 hora
- **Refresh Token**: 30 días

Si el access token expira, usa el refresh token en `/api/auth/refresh` para obtener uno nuevo.

---

## 📋 Códigos de Estado

- `200` - OK
- `201` - Creado
- `400` - Bad Request (datos inválidos)
- `401` - No autorizado (token inválido/expirado)
- `403` - Prohibido (sin permisos)
- `404` - No encontrado
- `409` - Conflicto (ej: email duplicado)
- `500` - Error del servidor

---

## 🧪 Testing con cURL

### Login
```bash
curl -X POST https://tu-app.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Crear Tarea
```bash
curl -X POST https://tu-app.onrender.com/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Nueva tarea",
    "priority": "high"
  }'
```

---

**📚 Documentación completa en el código fuente de cada ruta**
