# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from apps.medical.views.login_view import login_view, logout_view
from apps.medical.views.home import home

from apps.medical.views.crear_perfil_medico import crear_perfil_medico
from apps.medical.views.registrar_paciente import registrar_paciente
from apps.medical.views.ver_medico import listar_medicos
from apps.medical.views.ver_calendario import ver_calendario
from apps.medical.views.actualizar_medico import actualizar_medico
from apps.medical.views.crear_cita import crear_cita

from apps.medical.views.registrar_consulta import registrar_consulta
from apps.medical.views.detalle_consulta import detalle_consulta

from apps.medical.views.usuario import usuario
from apps.medical.views.crear_usuario import crear_usuario
from apps.medical.views.actualizar_usuario import actualizar_usuario
from apps.medical.views.eliminar_usuario import eliminar_usuario

from apps.medical.views.auto_asignacion import auto_asignacion
from apps.medical.views.medicos_especialidad import medicos_especialidad
from apps.medical.views.medicos_turno import turno_de_medico, disponibilidad_por_dia, disponibilidad_slots_por_fecha

from apps.medical.views.citas_disponibles import citas_disponibles
from apps.medical.views.citas_disponibles_api import api_disponibilidad
from apps.medical.views.buscar_medicos import buscar_medicos
from apps.medical.views.to_usuario import toggle_usuario

urlpatterns = [
    path('admin/', admin.site.urls),    

    # Login canonical en /login/ y la raíz redirige al login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Home
    path('home/', home, name='home'),

    # Médicos / Pacientes / Citas
    path('medicos/crear/', crear_perfil_medico, name='crear_perfil_medico'),
    path('pacientes/registrar/', registrar_paciente, name='registrar_paciente'),
    path('medicos/', listar_medicos, name='listar_medicos'),
    path('medico/<int:medico_id>/calendario/', ver_calendario, name='ver_calendario_medico'),
    path('medicos/<int:medico_id>/editar/', actualizar_medico, name='actualizar_medico'),
    path('citas/crear/', crear_cita, name='crear_cita'),

    path('consultas/registrar/<int:cita_id>/', registrar_consulta, name='registrar_consulta'),
    path('consultas/<int:consulta_id>/', detalle_consulta, name='detalle_consulta'),

    # Usuarios
    path('usuario/', usuario, name='usuario'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/<int:usuario_id>/actualizar/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/toggle/', toggle_usuario, name='toggle_usuario'),

    # Auto-asignación / Disponibilidad / Búsquedas
    path('citas/auto/', auto_asignacion, name='auto_asignacion'),
    path('api/medicos/medicos_especialidad/', medicos_especialidad, name='medicos_especialidad'),
    path('api/medicos/<int:medico_id>/turno/', turno_de_medico, name='api_turno_medico'),
    path('api/medicos/disponibilidad/', disponibilidad_por_dia, name='api_disponibilidad_medico'),

    path('citas/citas_disponibles/', citas_disponibles, name='citas_disponibles'),
    path('api/medicos/disponibilidad/slots/', disponibilidad_slots_por_fecha, name='api_disponibilidad_slots'),
    path('api/citas/disponibilidad/', api_disponibilidad, name='api_disponibilidad'),

    path('medicos/buscar/', buscar_medicos, name='buscar_medicos'),

    #Audit (usa los names definidos en apps/audit/urls.py)
    path('audit/', include('apps.audit.urls')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
]
