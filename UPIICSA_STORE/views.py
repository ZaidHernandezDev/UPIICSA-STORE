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

# Create your views here.
def index(request):
    today = date.today()
    seleccion_diaria_existente = SeleccionDiaria.objects.filter(fecha_seleccion=today).first()

    if not seleccion_diaria_existente:

        prodDisp = Producto.objects.filter(disponibilidad=True)
        selDiaria = random.sample(list(prodDisp), 8)
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
        usuario = Usuario.objects.get(usuario=request.user)
        return render(request, "UPIICSA_STORE/cuenta.html",{
            'Usuario': usuario
        })

def login_view(request):
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