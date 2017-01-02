"""
WSGI config for roomfinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application


sys.path.append("/home/ubuntu/FrawtBeta/Frawt/django/frawt")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roomfinder.settings")

application = get_wsgi_application()
