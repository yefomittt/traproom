"""Run on the host: python deploy/configure.py YOUR_HOSTNAME."""
import json
import re
import secrets
import sys
from pathlib import Path

if len(sys.argv) != 2 or not re.fullmatch(r'[a-zA-Z0-9-]+\.pythonanywhere\.com', sys.argv[1]):
    raise SystemExit('Usage: python deploy/configure.py USERNAME.pythonanywhere.com')
folder = Path.home() / '.config' / 'traproom'
folder.mkdir(parents=True, exist_ok=True, mode=0o700)
path = folder / 'production.json'
with path.open('x', encoding='utf-8') as stream:
    json.dump({'hostname': sys.argv[1], 'secret_key': secrets.token_urlsafe(64)}, stream)
path.chmod(0o600)
print(f'Configuration created: {path}. Existing configurations are never overwritten.')
