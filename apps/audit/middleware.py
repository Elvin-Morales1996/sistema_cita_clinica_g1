from .models import ActivityLog
from django.utils.deprecation import MiddlewareMixin

class LogActivityMiddleware(MiddlewareMixin):
    """
    Middleware simple que registra cada request POST de usuarios autenticados
    como una acción general. Ajusta según necesidades.
    """
    def process_request(self, request):
        # no bloquear request; guardar en process_response
        return None

    def process_response(self, request, response):
        try:
            if request.method in ("POST", "DELETE", "PUT", "PATCH"):
                user = getattr(request, "user", None)
                # evita loguear assets u admin estático o health checks
                path = request.path.lower()
                if "/static/" in path or path.startswith("/health"):
                    return response

                ip = request.META.get("REMOTE_ADDR")
                action = f"request:{request.method}:{request.path}"
                details = f"Status:{response.status_code} - POST data keys: {list(request.POST.keys())}"
                ActivityLog.objects.create(user=user if user.is_authenticated else None,
                                           action=action,
                                           ip=ip,
                                           details=details)
        except Exception:
            # Nunca romper la respuesta si falla el log
            pass
        return response
