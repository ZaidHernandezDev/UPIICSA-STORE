# Script para generar SECRET_KEY
from django.core.management.utils import get_random_secret_key

print("Nueva SECRET_KEY generada:")
print(get_random_secret_key())
print("\nCopia esta clave y úsala en tu archivo .env o en las variables de entorno de Vercel")
