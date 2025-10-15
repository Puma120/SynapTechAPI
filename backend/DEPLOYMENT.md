# 🚀 SynapTech API - Despliegue en Render

API Backend para SynapTech - Sistema de gestión de tareas y rutinas con IA.

## 📋 Configuración en Render

### 1. Crear la Base de Datos PostgreSQL

1. Ve a tu dashboard de Render
2. Click en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `synaptech-db`
   - **Database**: `synaptech_db`
   - **User**: `synaptech_user`
   - **Region**: Selecciona la más cercana
   - **Plan**: Free (para pruebas) o Starter
4. Click en **"Create Database"**
5. Guarda la **Internal Database URL** que se genera

### 2. Crear el Web Service

1. Ve a tu dashboard de Render
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `synaptech-api`
   - **Region**: La misma que la base de datos
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn -c gunicorn_config.py wsgi:app`

### 3. Variables de Entorno

En la sección **Environment** del Web Service, añade:

#### ✅ **Obligatorias**:

```bash
# Base de datos (se conecta automáticamente si vinculas la BD)
DATABASE_URL=<Se configura automáticamente al vincular la BD>

# Seguridad
JWT_SECRET_KEY=<genera una clave segura única>
FLASK_ENV=production

# Python version
PYTHON_VERSION=3.11.0
```

#### 🔧 **Opcionales** (pero recomendadas):

```bash
# IA - Google Gemini
GEMINI_API_KEY=<tu-api-key-de-gemini>

# OAuth - Google Calendar
GOOGLE_CLIENT_ID=<tu-client-id>
GOOGLE_CLIENT_SECRET=<tu-client-secret>

# CORS (si tienes frontend desplegado)
CORS_ORIGINS=https://tu-frontend.com,http://localhost:5173
```

### 4. Vincular la Base de Datos

1. En la configuración del Web Service, ve a la sección **Environment**
2. Click en **"Advanced"**
3. En **"Databases"**, selecciona `synaptech-db`
4. Esto configurará automáticamente la variable `DATABASE_URL`

### 5. Desplegar

1. Click en **"Create Web Service"**
2. Render automáticamente:
   - Ejecutará el `build.sh`
   - Instalará dependencias
   - Ejecutará migraciones de base de datos
   - Iniciará el servidor con Gunicorn

## 🔑 Generar JWT_SECRET_KEY

En tu terminal local, ejecuta:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado y úsalo como valor de `JWT_SECRET_KEY`.

## 🌐 URLs de API

Una vez desplegado, tu API estará disponible en:
```
https://synaptech-api.onrender.com
```

### Endpoints principales:

- `GET /` - Información de la API
- `GET /health` - Health check
- `POST /api/auth/register` - Registro de usuarios
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Perfil (requiere JWT)
- `GET /api/tasks` - Listar tareas
- `POST /api/tasks` - Crear tarea
- `GET /api/ai/suggestions` - Obtener sugerencias de IA

## 📦 Archivos Importantes

- **`requirements.txt`**: Dependencias de Python
- **`build.sh`**: Script de construcción (migraciones, etc.)
- **`render.yaml`**: Configuración de Render (Blueprint)
- **`gunicorn_config.py`**: Configuración del servidor Gunicorn
- **`.env.example`**: Plantilla de variables de entorno

## 🔍 Verificar Despliegue

### Health Check
```bash
curl https://synaptech-api.onrender.com/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "message": "SynapTech API is running"
}
```

### Test de Login
```bash
curl -X POST https://synaptech-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"tu-password"}'
```

## 🐛 Troubleshooting

### Error: "pg_config not found"
- ✅ Ya resuelto con `psycopg2-binary` en requirements.txt

### Error: "relation does not exist"
- Las migraciones no se ejecutaron correctamente
- Verifica los logs de build en Render
- Intenta hacer un **Manual Deploy**

### Error: "Internal Server Error"
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en Render Dashboard
- Verifica que `DATABASE_URL` esté correctamente vinculada

### La app se duerme (Free tier)
- En el plan Free, Render duerme la app después de 15 minutos de inactividad
- La primera petición después del "sleep" tardará ~30-60 segundos
- Considera el plan Starter ($7/mes) para mantenerla activa

## 📝 Notas Importantes

1. **Render Free Tier**: 
   - La BD tiene límite de 90 días (luego se elimina)
   - El servicio web se duerme tras 15 min de inactividad
   - 750 horas de compute gratis/mes

2. **Migraciones**:
   - Se ejecutan automáticamente en cada deploy
   - Si necesitas reset: conéctate a la BD desde Render Shell

3. **Logs**:
   - Disponibles en tiempo real en el dashboard de Render
   - Gunicorn registra todas las peticiones

4. **CORS**:
   - Actualiza `CORS_ORIGINS` con tu URL de frontend cuando la tengas

## 🔗 Recursos

- [Documentación de Render](https://render.com/docs)
- [Guía de Flask en Render](https://render.com/docs/deploy-flask)
- [PostgreSQL en Render](https://render.com/docs/databases)

## 📧 Soporte

Si tienes problemas, revisa:
1. Logs en Render Dashboard
2. Variables de entorno configuradas correctamente
3. Base de datos vinculada correctamente
4. Build script ejecutándose sin errores

---

**¡Listo para producción! 🎉**
