from django.conf import settings
import os


WSGI_RESTART_CODE_CMDS = getattr(settings, 'WSGI_RESTART_CODE', (
    'touch %s' % os.path.join(getattr(settings, 'PROJECT_DIR', ''), 'wsgi.py'),
))
