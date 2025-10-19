from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages

def require_role(allowed_roles):
    """
    Decorador para requerir roles específicos.
    allowed_roles: lista de roles permitidos (ej. ['Administrador', 'Médico'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get('rol')
            if not user_role:
                messages.error(request, 'Debe iniciar sesión para acceder a esta página.')
                return redirect('login')

            if user_role not in allowed_roles:
                messages.error(request, 'No tiene permisos para acceder a esta página.')
                return redirect('home')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def get_user_permissions(rol):
    """
    Retorna los permisos según el rol del usuario.
    """
    permissions = {
        'Administrador': {
            'can_manage_users': True,
            'can_manage_doctors': True,
            'can_manage_patients': True,
            'can_manage_appointments': True,
            'can_view_reports': True,
            'can_manage_consultations': True,
            'can_view_audit': True,
            'can_auto_assign': True,
        },
        'Médico': {
            'can_manage_users': False,
            'can_manage_doctors': False,
            'can_manage_patients': True,  # Gestión completa de pacientes
            'can_manage_appointments': True,
            'can_view_reports': True,
            'can_manage_consultations': True,
            'can_view_audit': False,
            'can_auto_assign': True,  # Acceso a asignación automática
        },
        'Recepcionista': {
            'can_manage_users': False,
            'can_manage_doctors': False,
            'can_manage_patients': True,  # Gestión completa de pacientes
            'can_manage_appointments': True,
            'can_view_reports': True,  # Acceso a reportes
            'can_manage_consultations': False,
            'can_view_audit': False,
            'can_auto_assign': True,  # Acceso a asignación automática
        },
        'Paciente': {
            'can_manage_users': False,
            'can_manage_doctors': False,
            'can_manage_patients': False,  # Solo solicitud de cita
            'can_manage_appointments': True,  # Para solicitar citas
            'can_view_reports': False,
            'can_manage_consultations': False,
            'can_view_audit': False,
            'can_auto_assign': False,
        }
    }
    return permissions.get(rol, {})