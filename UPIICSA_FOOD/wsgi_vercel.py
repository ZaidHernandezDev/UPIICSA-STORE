"""
WSGI config for UPIICSA_FOOD project - Vercel configuration.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UPIICSA_FOOD.settings')

application = get_wsgi_application()

# Vercel serverless function handler
app = application
