"""Production settings. Secrets are stored outside the repository."""
import json
import os
from pathlib import Path

config_path = Path(os.environ['TRAPROOM_CONFIG'])
config = json.loads(config_path.read_text(encoding='utf-8'))
if len(config['secret_key']) < 50:
    raise RuntimeError('Production secret must contain at least 50 characters')
hostname = config['hostname']
if not hostname or any(c in hostname for c in '/*: '):
    raise RuntimeError('Expected an explicit hostname without scheme or path')
os.environ['DJANGO_DEBUG'] = '0'
os.environ['DJANGO_SECRET_KEY'] = config['secret_key']
os.environ['DJANGO_ALLOWED_HOSTS'] = hostname

from .settings import *  # noqa: E402,F403

DATABASES['default']['NAME'] = config_path.parent / 'traproom.sqlite3'
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
