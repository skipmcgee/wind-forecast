import os

workers = 2
threads = 4
ip = '0.0.0.0'
port = '3797'
#workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
#threads = int(os.environ.get('GUNICORN_THREADS', '4'))
#port = int(os.environ.get('GUNICORN_PORT', '3797'))
#ip = int(os.environ.get('GUNICORN_IP', '0.0.0.0'))
#timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
#secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
#bind = os.environ.get('GUNICORN_BIND', f'{ip}:{port}')
forwarded_allow_ips = '*'
bind = f'{ip}:{port}'