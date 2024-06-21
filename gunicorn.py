# Citation
# Date: 05/20/2024
# Adapted from the Gunicorn Official Documentation
# Source URL: https://docs.gunicorn.org/en/latest/configure.html

import os

#workers = 2
#threads = 4
ip = "0.0.0.0"
#port = "3797"
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
port = int(os.environ.get('GUNICORN_PORT', '3797'))
#ip = int(os.environ.get('GUNICORN_IP', '0.0.0.0'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
bind = os.environ.get('GUNICORN_BIND', f'{ip}:{port}')
forwarded_allow_ips = "*"
loglevel = "debug"
accesslog = "access.log"
acceslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = "error.log"
bind = f"{ip}:{port}"
