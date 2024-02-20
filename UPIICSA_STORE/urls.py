from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("grupos", views.groups, name="groups"),
    path("grupos/<str:section>", views.section, name="section"),
    path("cuenta", views.cuenta, name="cuenta"),
    path("Login", views.login_view, name="login"),
    path("Logout", views.logout_view, name="logout"),
    path("Signup", views.signup_view, name="signup"),
    path("Agregar", views.add_product, name="add_product"),
    path("Buscar", views.search, name="search"),
]

handler404 = 'UPIICSA_STORE.views.error_404'