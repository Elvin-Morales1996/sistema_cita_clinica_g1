"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render  # 👈 importante para el lambda
from apps.medical.views.login_view import login_view # 👈 importa tu vista
from apps.medical.views.crear_perfil_medico import crear_perfil_medico
from apps.medical.views.registrar_paciente import registrar_paciente
from apps.medical.views.ver_medico import listar_medicos
from apps.medical.views.ver_calendario import ver_calendario
from apps.medical.views.actualizar_medico import actualizar_medico
from apps.medical.views.crear_cita import crear_cita
from apps.medical.views.home import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),  # login como vista principal
    path('home/', home, name='home'), 
    path('medicos/crear/', crear_perfil_medico, name='crear_perfil_medico'),
    path('pacientes/registrar/', registrar_paciente, name='registrar_paciente'),
    path('medicos/', listar_medicos, name='listar_medicos'),
    path('medico/<int:medico_id>/calendario/', ver_calendario, name='ver_calendario_medico'),
    path('medicos/<int:medico_id>/editar/', actualizar_medico, name='actualizar_medico'),
    path('citas/crear/', crear_cita, name='crear_cita'),

]
