from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from .models import Producto


class SignUpForm(UserCreationForm):

    username = forms.CharField(
        label='Nombre de usuario',
        help_text='Solo letras, dígitos y @/./+/-/_ permitidos.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Contraseña',
        help_text=(
            'Tu contraseña no puede ser demasiado similar a tu nombre de usuario.<br>'
            'Tu contraseña debe contener al menos 8 caracteres.<br>'
            'Tu contraseña no puede ser una contraseña común.<br>'
            'Tu contraseña no puede ser completamente numérica.'
        ),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        help_text='Confirma tu contraseña.',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    whatsapp = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Ingrese solo números.',
                code='invalid_whatsapp'
            ),
            MinLengthValidator(limit_value=10),

        ],
        max_length=10,
        widget=forms.TextInput(attrs={'type': 'number','class': 'form-control'}),
    )
    nombre = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Ingrese su nombre o nombres.'
    )
    apellido= forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Ingrese sus apellidos.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'whatsapp', 'nombre', 'apellido']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombreProd', 'descProd', 'precioProd', 'grupo', 'imagen']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombreProd'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['descProd'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción del producto'})
        self.fields['precioProd'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio del producto'})
        self.fields['grupo'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control mb-2', 'accept': 'image/*'})
