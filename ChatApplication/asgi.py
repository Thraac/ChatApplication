"""
ASGI config for ChatApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApplication.settings')

application = get_default_application()
