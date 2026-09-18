"""Copy into the WSGI file linked on PythonAnywhere's Web tab."""
import os
import sys
from pathlib import Path

project = Path.home() / 'traproom'
sys.path.insert(0, str(project))
os.environ['TRAPROOM_CONFIG'] = str(Path.home() / '.config/traproom/production.json')
os.environ['DJANGO_SETTINGS_MODULE'] = 'studio.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
