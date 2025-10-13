import multiprocessing

# Configuracion de Gunicorn para produccion
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
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

# SSL (para produccion)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Nombre del proceso
proc_name = "synaptech_api"

# Reload automatico en desarrollo
reload = False
