from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

class RoleBasedAccessMiddleware:
    """
    Middleware para controlar el acceso basado en roles.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de URLs que requieren autenticación
        protected_urls = [
            '/home/',
            '/usuario/',
            '/usuarios/',
            '/medicos/',
            '/pacientes/',
            '/citas/',
            '/consultas/',
            '/reportes/',
            '/historial/',
            '/audit/',
        ]

        # Verificar si la URL actual requiere autenticación
        current_path = request.path
        requires_auth = any(current_path.startswith(url) for url in protected_urls)

        if requires_auth:
            user_role = request.session.get('rol')
            if not user_role:
                messages.error(request, 'Debe iniciar sesión para acceder a esta página.')
                return redirect('login')

            # Definir permisos por URL según el rol
            role_permissions = self.get_role_permissions(user_role)

            # Verificar permisos específicos para URLs
            if not self.has_permission(current_path, role_permissions):
                # Verificar si es una petición AJAX
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return HttpResponse('No tiene permisos para acceder a esta opción.', status=403)
                else:
                    # Mostrar mensaje emergente y redirigir
                    messages.error(request, 'No tiene permisos para acceder a esta opción.')
                    return redirect('home')

        response = self.get_response(request)
        return response

    def get_role_permissions(self, rol):
        """
        Retorna las URLs permitidas según el rol.
        """
        permissions = {
            'Administrador': [
                '/home/', '/usuario/', '/usuarios/', '/medicos/', '/pacientes/',
                '/citas/', '/consultas/', '/reportes/', '/historial/', '/audit/',
                '/citas/auto/'  # Asignación automática
            ],
            'Médico': [
                '/home/', '/medicos/', '/pacientes/', '/citas/', '/consultas/',
                '/reportes/', '/historial/', '/citas/auto/'  # Asignación automática
            ],
            'Recepcionista': [
                '/home/', '/pacientes/', '/citas/', '/reportes/', '/citas/auto/'  # Asignación automática
            ],
            'Paciente': [
                '/home/', '/citas/'  # Solo para solicitar citas
            ]
        }
        return permissions.get(rol, [])

    def has_permission(self, path, allowed_urls):
        """
        Verifica si la URL está permitida para el rol.
        """
        return any(path.startswith(url) for url in allowed_urls)