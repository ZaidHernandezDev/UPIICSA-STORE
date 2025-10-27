# UPIICSA-STORE

Plataforma web de comercio para la comunidad UPIICSA, diseñada para facilitar la compra y venta de alimentos entre estudiantes y vendedores.

## Descripción

UPIICSA-STORE es una aplicación web desarrollada con Django que permite a los usuarios comprar y vender productos alimenticios dentro de la comunidad UPIICSA. La plataforma cuenta con un sistema de selección diaria de productos destacados y categorización por grupos de alimentos.

## Características

- **Sistema de autenticación** - Registro e inicio de sesión de usuarios
- **Integración con WhatsApp** - Contacto directo con vendedores
- **Selección diaria** - Muestra aleatoria de 8 productos destacados cada día
- **Categorías de productos**:
  - Postres
  - Comida rápida
  - Dulces
  - Ensaladas
  - Desayunos
  - Antojitos
- **Gestión de imágenes** - Carga y visualización de fotos de productos
- **Perfiles de usuario** - Gestión de información personal y productos
- **Búsqueda de productos** - Sistema de búsqueda avanzada

## Tecnologías

- **Backend**: Django 5.0
- **Base de datos**: SQLite3
- **Frontend**: HTML, CSS (SCSS), JavaScript
- **Python**: 3.x

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/ZaidHernandezDev/UPIICSA-STORE.git
cd UPIICSA-STORE
```

2. **Crear un entorno virtual y ejecutarlo (Windows)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Instalar dependencias**
```powershell
pip install django pillow
```

4. **Aplicar migraciones**
```powershell
python manage.py migrate
```

5. **Ejecutar el servidor de desarrollo**
```powershell
python manage.py runserver
```

6. **Acceder a la aplicación**
```
Abre tu navegador en: http://127.0.0.1:8000/
```

## Estructura del Proyecto

```
UPIICSA-STORE/
├── UPIICSA_FOOD/          # Configuración principal del proyecto
│   ├── settings.py        # Configuración de Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── UPIICSA_STORE/        # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y lógica
│   ├── forms.py          # Formularios
│   ├── urls.py           # URLs de la aplicación
│   ├── templates/        # Plantillas HTML
│   ├── static/           # Archivos estáticos (CSS, imágenes)
│   └── migrations/       # Migraciones de base de datos
├── manage.py             # Script de gestión de Django
└── db.sqlite3           # Base de datos SQLite
```

## Modelos de Datos

### Usuario
- Extensión del modelo User de Django
- Campo adicional: WhatsApp (10 dígitos)
- Relación uno a uno con User

### Producto
- Nombre del producto (máx. 25 caracteres)
- Descripción
- Precio (decimal)
- Disponibilidad (booleano)
- Imagen
- Vendedor (ForeignKey a Usuario)
- Grupo/Categoría

### Seleccion Diaria
- Fecha de selección (única)
- Productos seleccionados (ManyToMany)

## Uso

### Para Compradores
1. Registrarse en la plataforma
2. Navegar por los productos destacados o por categorías
3. Ver detalles del producto
4. Contactar al vendedor por WhatsApp

### Para Vendedores
1. Registrarse con número de WhatsApp
2. Añadir productos a través del formulario
3. Gestionar disponibilidad de productos
4. Recibir contactos de compradores

## Deploy en Vercel

### Configuración Inicial

1. **Instalar dependencias de producción**
```powershell
pip install -r requirements.txt
```

2. **Crear archivo .env**
Copia el archivo `.env.example` a `.env` y configura tus variables:
```powershell
copy .env.example .env
```

Edita el archivo `.env` con tus valores:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=.vercel.app,tu-dominio.com
```

3. **Instalar Vercel CLI (opcional, para deploy desde terminal)**
```powershell
npm i -g vercel
```

### Deploy Automático desde GitHub

1. Ve a [Vercel](https://vercel.com) e inicia sesión
2. Click en "Add New Project"
3. Importa tu repositorio de GitHub
4. Configura las variables de entorno en el dashboard de Vercel:
   - `SECRET_KEY`: Tu clave secreta de Django
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: .vercel.app
5. Click en "Deploy"

### Deploy Manual con Vercel CLI

```powershell
# Login en Vercel
vercel login

# Deploy
vercel --prod
```

### Notas Importantes para Vercel

**Limitaciones de Vercel con Django:**
- Vercel es serverless, por lo que SQLite no es persistente
- Se recomienda usar una base de datos externa (PostgreSQL, MySQL)
- Los archivos media subidos no son persistentes
- Considera usar servicios como:
  - **Database**: [Neon](https://neon.tech), [PlanetScale](https://planetscale.com), o [Supabase](https://supabase.com)
  - **Media Files**: [Cloudinary](https://cloudinary.com) o AWS S3

### Configurar Base de Datos Externa (Opcional)

Para usar PostgreSQL en producción, instala:
```powershell
pip install psycopg2-binary dj-database-url
```

Actualiza `requirements.txt`:
```
psycopg2-binary
dj-database-url
```

Y agrega en `settings.py`:
```python
import dj_database_url

if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

**Zaid Hernández**
- GitHub: [@ZaidHernandezDev](https://github.com/ZaidHernandezDev)

## Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en el repositorio de GitHub.

---

¡No olvides dar una estrella al proyecto si te fue útil!
