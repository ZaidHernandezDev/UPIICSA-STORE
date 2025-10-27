from django import forms
from django.shortcuts import render, redirect
from .models import Producto, SeleccionDiaria, Usuario
import random
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .forms import SignUpForm, ProductForm
from django.contrib.auth.decorators import login_required
import os

# Datos simulados para Vercel (sin base de datos)
MOCK_PRODUCTOS = [
    {
        'nombre': 'Tacos al Pastor',
        'descripcion': 'Deliciosos tacos al pastor con piña',
        'precio': 45.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Taquería El Buen Sabor',
        'whatsapp': '5512345678',
        'grupo': 'comida',
    },
    {
        'nombre': 'Torta de Jamón',
        'descripcion': 'Torta tradicional con jamón, queso y aguacate',
        'precio': 35.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Don Tortas',
        'whatsapp': '5523456789',
        'grupo': 'comida',
    },
    {
        'nombre': 'Quesadillas',
        'descripcion': 'Quesadillas de queso con champiñones',
        'precio': 25.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Quesadillas Mary',
        'whatsapp': '5534567890',
        'grupo': 'comida',
    },
    {
        'nombre': 'Agua de Jamaica',
        'descripcion': 'Agua fresca natural de jamaica',
        'precio': 15.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Aguas Frescas Lupita',
        'whatsapp': '5545678901',
        'grupo': 'bebidas',
    },
    {
        'nombre': 'Jugo de Naranja',
        'descripcion': 'Jugo natural de naranja recién exprimido',
        'precio': 20.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Jugos Naturales',
        'whatsapp': '5556789012',
        'grupo': 'bebidas',
    },
    {
        'nombre': 'Galletas de Avena',
        'descripcion': 'Galletas artesanales de avena con chispas',
        'precio': 30.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Postres Caseros',
        'whatsapp': '5567890123',
        'grupo': 'postres',
    },
    {
        'nombre': 'Pay de Limón',
        'descripcion': 'Pay casero de limón con merengue',
        'precio': 40.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Repostería Dulce Vida',
        'whatsapp': '5578901234',
        'grupo': 'postres',
    },
    {
        'nombre': 'Chilaquiles Verdes',
        'descripcion': 'Chilaquiles bañados en salsa verde con pollo',
        'precio': 50.00,
        'disp': True,
        'imagen': None,
        'vendedor': 'Desayunos Don Pepe',
        'whatsapp': '5589012345',
        'grupo': 'comida',
    },
]

# Create your views here.
def index(request):
    # Detectar si estamos en Vercel (producción sin base de datos)
    is_vercel = os.environ.get('VERCEL', False)
    
    if is_vercel:
        # Usar datos simulados en Vercel
        productos_data = random.sample(MOCK_PRODUCTOS, min(8, len(MOCK_PRODUCTOS)))
        seleccion_diaria_existente = None
    else:
        # Usar base de datos en desarrollo local
        today = date.today()
        seleccion_diaria_existente = SeleccionDiaria.objects.filter(fecha_seleccion=today).first()

        if not seleccion_diaria_existente:
            prodDisp = Producto.objects.filter(disponibilidad=True)
            selDiaria = random.sample(list(prodDisp), min(8, prodDisp.count()))
            nueva_SelDiaria = SeleccionDiaria.objects.create(
                fecha_seleccion=today
            )
            nueva_SelDiaria.productos.set(selDiaria)
        else:
            selDiaria = seleccion_diaria_existente.productos.all()

        productos_data = []
        for producto in selDiaria:
            producto_data = {
                'nombre': producto.nombreProd,
                'descripcion': producto.descProd,
                'precio': producto.precioProd,
                'disp': producto.disponibilidad,
                'imagen': producto.imagen,
                'vendedor': producto.vendedor,
                'whatsapp': producto.vendedor.whatsapp,
            }
            productos_data.append(producto_data)

    context = {'productos_data': productos_data, 'seleccion_diaria': seleccion_diaria_existente}

    return render(request, 'UPIICSA_STORE/index.html', context)

def groups(request):
    return render(request, 'UPIICSA_STORE/groups.html')

def section(request, section):
    img_url = f'UPIICSA_STORE/images/{section}.jpg'
    
    # Detectar si estamos en Vercel (producción sin base de datos)
    is_vercel = os.environ.get('VERCEL', False)
    
    if is_vercel:
        # Usar datos simulados en Vercel
        productos_data = [p for p in MOCK_PRODUCTOS if p['grupo'] == section.lower()]
    else:
        # Usar base de datos en desarrollo local
        select = Producto.objects.filter(grupo=f'{section.lower()}')

        productos_data = []
        for producto in select:
            producto_data = {
                'nombre': producto.nombreProd,
                'descripcion': producto.descProd,
                'precio': producto.precioProd,
                'disp': producto.disponibilidad,
                'imagen': producto.imagen,
                'vendedor': producto.vendedor,
                'whatsapp': producto.vendedor.whatsapp,
            }
            productos_data.append(producto_data)

    tamano = len(productos_data)

    return render(request, 'UPIICSA_STORE/section.html',{
        'section': section,
        'img_url': img_url,
        'productos_data': productos_data,
        'tamano': tamano,
    })

def cuenta(request):
    if not request.user.is_authenticated:
        return render(request, "UPIICSA_STORE/login.html")
    else:
        # Detectar si estamos en Vercel
        is_vercel = os.environ.get('VERCEL', False)
        
        if is_vercel:
            # En Vercel, mostrar datos simulados o deshabilitar funcionalidad
            return render(request, "UPIICSA_STORE/cuenta.html",{
                'Usuario': None,
                'is_vercel': True,
                'message': 'Esta funcionalidad solo está disponible en desarrollo local.'
            })
        else:
            # En desarrollo, usar base de datos
            usuario = Usuario.objects.get(usuario=request.user)
            return render(request, "UPIICSA_STORE/cuenta.html",{
                'Usuario': usuario,
                'is_vercel': False
            })

def login_view(request):
    # Detectar si estamos en Vercel
    is_vercel = os.environ.get('VERCEL', False)
    
    if is_vercel:
        # En Vercel, deshabilitar login
        return render(request, "UPIICSA_STORE/login.html", {
            'message': 'El login solo está disponible en desarrollo local.',
            'is_vercel': True
        })
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            usuario = Usuario.objects.get(usuario=request.user)
            return render(request, "UPIICSA_STORE/cuenta.html",{
            'Usuario': usuario
        })
        else:
            return render(request, "UPIICSA_STORE/login.html", {
                'message': 'Nombre o contraseña incorrecta'
            })

def signup_view(request):
    # Detectar si estamos en Vercel
    is_vercel = os.environ.get('VERCEL', False)
    
    if is_vercel:
        # En Vercel, deshabilitar registro
        return render(request, 'UPIICSA_STORE/signup.html', {
            'form': None,
            'message': 'El registro solo está disponible en desarrollo local.',
            'is_vercel': True
        })
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            usuario = Usuario.objects.create(
                usuario=user,
                whatsapp=form.cleaned_data['whatsapp']
            )
            login(request, user)
            return redirect('index')  # Cambia 'index' por la URL a la que quieres redirigir después del registro
    else:
        form = SignUpForm()

    return render(request, 'UPIICSA_STORE/signup.html', {'form': form})
    

def logout_view(request):
    logout(request)
    return render(request, "UPIICSA_STORE/index.html")

@login_required
def add_product(request):
    # Detectar si estamos en Vercel
    is_vercel = os.environ.get('VERCEL', False)
    
    if is_vercel:
        # En Vercel, deshabilitar agregar productos
        return render(request, "UPIICSA_STORE/add_product.html", {
            'form': None,
            'message': 'Esta funcionalidad solo está disponible en desarrollo local.',
            'is_vercel': True
        })
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            vendedor = Usuario.objects.get(usuario=request.user)
            producto = form.save(commit=False)
            producto.vendedor = vendedor
            producto.save()
            return redirect('add_product')
    else:
        form = ProductForm()
    return render(request, "UPIICSA_STORE/add_product.html", {'form': form})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        
        # Detectar si estamos en Vercel
        is_vercel = os.environ.get('VERCEL', False)
        
        if is_vercel:
            # Usar datos simulados en Vercel
            productos_data = [
                p for p in MOCK_PRODUCTOS 
                if search.lower() in p['nombre'].lower() or search.lower() in p['descripcion'].lower()
            ]
        else:
            # Usar base de datos en desarrollo local
            select = Producto.objects.filter(nombreProd__icontains=search)

            productos_data = []
            for producto in select:
                producto_data = {
                    'nombre': producto.nombreProd,
                    'descripcion': producto.descProd,
                    'precio': producto.precioProd,
                    'disp': producto.disponibilidad,
                    'imagen': producto.imagen,
                    'vendedor': producto.vendedor,
                    'whatsapp': producto.vendedor.whatsapp,
                }
                productos_data.append(producto_data)

        tamano = len(productos_data)

        return render(request, 'UPIICSA_STORE/search.html',{
            'section': section,
            'productos_data': productos_data,
            'tamano': tamano,
        })
    else:
        return redirect('search', section=section)

def error_404(request, exception):
    return render(request, 'UPIICSA_STORE/404.html', status=404)