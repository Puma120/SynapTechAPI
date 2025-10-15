import multiprocessing
import os

# Configuracion de Gunicorn para produccion
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Aumentado para operaciones de IA
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Proceso
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Nombre del proceso
proc_name = "synaptech_api"

# Reload automatico en desarrollo (deshabilitado en produccion)
reload = False
