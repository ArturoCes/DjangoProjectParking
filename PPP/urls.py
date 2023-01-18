"""PPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from parking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('depositar_vehiculo/', views.depositar_vehiculo_view, name='depositar_vehiculo'),
    path('retirar_vehiculo/', views.retirar_vehiculo_view, name='retirar_vehiculo'),
    path('depositar_abonado/', views.depositar_abonado_view, name='depositar_abonado'),
    path('retirar_abonado/', views.retirar_abonado_view, name='retirar_abonado'),
    path('facturacion/', views.facturacion_view, name='facturacion'),
    path('', views.main_view, name='main'),
    path('administrar_plazas/', views.administrar_plazas_view, name='administrar_plazas'),

]
