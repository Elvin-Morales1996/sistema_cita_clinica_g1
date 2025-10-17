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
from django.urls import path,include
from django.shortcuts import render  # 👈 importante para el lambda
from apps.medical.views.login_view import login_view # 👈 importa tu vista
from apps.medical.views.crear_perfil_medico import crear_perfil_medico
from apps.medical.views.registrar_paciente import registrar_paciente
from apps.medical.views.ver_medico import listar_medicos
from apps.medical.views.ver_calendario import ver_calendario
from apps.medical.views.actualizar_medico import actualizar_medico
from apps.medical.views.crear_cita import crear_cita
from apps.medical.views.reprogramar_cita import reprogramar_cita
from apps.medical.views.home import home
from apps.medical.views.listar_pacientes import listar_pacientes
from apps.medical.views.editar_contacto_paciente import editar_contacto_paciente




from apps.medical.views.registrar_consulta import registrar_consulta
from apps.medical.views.detalle_consulta import detalle_consulta

from apps.medical.views.usuario import usuario
from apps.medical.views.crear_usuario import crear_usuario
from apps.medical.views.actualizar_usuario import actualizar_usuario
from apps.medical.views.eliminar_usuario import eliminar_usuario
from apps.medical.views.login_view import login_view, logout_view
from apps.medical.views.auto_asignacion import auto_asignacion
from apps.medical.views.medicos_especialidad import medicos_especialidad
from apps.medical.views.medicos_turno import turno_de_medico, disponibilidad_por_dia
from apps.medical.views.historial_views import buscar_pacientes, ver_historial, editar_historial, eliminar_historial
from apps.medical.views.editar_cita import editar_cita
from apps.medical.views.cancelar_cita import cancelar_cita
from apps.medical.views.citas_pendientes import citas_pendientes, confirmar_cita, cancelar_cita


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Home
    path('', login_view, name='login'),  # login como vista principal
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'), 

    #Medicos
    path('medicos/crear/', crear_perfil_medico, name='crear_perfil_medico'),
    path('pacientes/registrar/', registrar_paciente, name='registrar_paciente'),
    path('medicos/', listar_medicos, name='listar_medicos'),
    path('medico/<int:medico_id>/calendario/', ver_calendario, name='ver_calendario_medico'),
    path('medicos/<int:medico_id>/editar/', actualizar_medico, name='actualizar_medico'),
    path('citas/crear/', crear_cita, name='crear_cita'),
    path('citas/<int:cita_id>/editar/', editar_cita, name='editar_cita'),
    path('citas/<int:cita_id>/cancelar/', cancelar_cita, name='cancelar_cita'),
    path("citas/<int:pk>/reprogramar/", reprogramar_cita, name="reprogramar_cita"),

    path("consultas/registrar/<int:cita_id>/", registrar_consulta, name="registrar_consulta"),
    path("consultas/<int:consulta_id>/", detalle_consulta, name="detalle_consulta"),

    #usuarios
    path('usuario/', usuario, name='usuario'),
    path("usuarios/crear/", crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/actualizar/", actualizar_usuario, name="actualizar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", eliminar_usuario, name="eliminar_usuario"),

    # Auto-asignación
    path("citas/auto/", auto_asignacion, name="auto_asignacion"),
    path("api/medicos/medicos_especialidad/", medicos_especialidad, name="medicos_especialidad"),
    path("api/medicos/<int:medico_id>/turno/", turno_de_medico, name="api_turno_medico"),
    path("api/medicos/disponibilidad/", disponibilidad_por_dia, name="api_disponibilidad_medico"),

    # Historial Clínico / Reportes
    path("reportes/", buscar_pacientes, name="buscar_pacientes"),
    path("historial/<int:paciente_id>/", ver_historial, name="ver_historial"),
    path("historial/<int:paciente_id>/editar/", editar_historial, name="editar_historial"),
    path("historial/<int:paciente_id>/eliminar/", eliminar_historial, name="eliminar_historial"),

    #Para pacientes
    path("pacientes/listar/", listar_pacientes, name="listar_pacientes"),
    path("pacientes/editar/<int:paciente_id>/", editar_contacto_paciente, name="editar_contacto_paciente"),
    
    
    #Para citas pendientes
    path('citas/pendientes/', citas_pendientes, name='citas_pendientes'),
    path('citas/confirmar/<int:cita_id>/', confirmar_cita, name='confirmar_cita'),
    path('citas/cancelar/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),
    
    

    path("", include("apps.medical.urls")),
    
    
    path("audit/", include("apps.audit.urls")),


]
