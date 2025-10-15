# 🚀 Inicio Rápido - Despliegue en Render

## ✅ Checklist Pre-Despliegue

Tu API está lista para Render con los siguientes archivos:

- ✅ `requirements.txt` - Todas las dependencias
- ✅ `build.sh` - Script de construcción automática
- ✅ `render.yaml` - Blueprint de configuración (opcional)
- ✅ `gunicorn_config.py` - Configuración del servidor
- ✅ `.env.example` - Plantilla de variables de entorno
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ `DEPLOYMENT.md` - Guía detallada de despliegue

## 🎯 Pasos Rápidos para Desplegar

### 1️⃣ Crear Base de Datos PostgreSQL

```
Dashboard → New + → PostgreSQL
Name: synaptech-db
Plan: Free
```

### 2️⃣ Crear Web Service

```
Dashboard → New + → Web Service
Repository: Tu repo de GitHub
Root Directory: backend
Build Command: ./build.sh
Start Command: gunicorn -c gunicorn_config.py run:app
```

### 3️⃣ Variables de Entorno Mínimas

```bash
DATABASE_URL=<auto-generado al vincular BD>
JWT_SECRET_KEY=<generar con comando abajo>
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

**Generar JWT_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Variables Opcionales (Recomendadas)

```bash
GEMINI_API_KEY=<tu-key-de-gemini>
GOOGLE_CLIENT_ID=<tu-client-id>
GOOGLE_CLIENT_SECRET=<tu-secret>
CORS_ORIGINS=https://tu-frontend.com,http://localhost:5173
```

### 5️⃣ Vincular Base de Datos

```
En Environment → Advanced → Link Database → synaptech-db
```

### 6️⃣ Desplegar

```
Click "Create Web Service" y espera ~5 minutos
```

## 🧪 Verificar Funcionamiento

Una vez desplegado:

```bash
# Health check
curl https://tu-app.onrender.com/health

# Respuesta esperada:
# {"status":"ok","message":"SynapTech API is running"}
```

## 📚 Documentación Completa

Lee `DEPLOYMENT.md` para instrucciones detalladas y troubleshooting.

## 🆘 Problemas Comunes

### Build falla
- Verifica que `build.sh` tenga permisos de ejecución
- En Render, los permisos se manejan automáticamente

### No conecta a BD
- Asegúrate de vincular la base de datos en Environment
- Verifica que `DATABASE_URL` esté presente

### Error 500
- Revisa logs en Render Dashboard
- Verifica todas las variables de entorno obligatorias

---

**¡Tu API está lista para producción! 🎉**

Para más detalles, consulta `DEPLOYMENT.md`
