# apps/audit/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings
from functools import wraps

from .models import ActivityLog
from .forms import ActivityFilterForm

# --- Decorador local basado en sesión o auth de Django ---
def login_required_session(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        # Si tienes auth normal y estás logueado, pasa
        if getattr(request, "user", None) and request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # Si usas login propio por sesión, revisa la clave que guardas (ajústala si es distinta)
        if request.session.get("usuario_id"):  # <-- CAMBIA 'usuario_id' si tu login usa otra clave
            return view_func(request, *args, **kwargs)

        # Redirige al login del proyecto
        login_url = getattr(settings, "LOGIN_URL", "/login/")
        return redirect(f"{login_url}?next={request.get_full_path()}")
    return _wrapped

# --- Helper de rol admin: acepta superuser o rol en sesión ---
def _is_admin(request):
    # Vía auth de Django
    if getattr(request, "user", None) and request.user.is_authenticated and request.user.is_superuser:
        return True
    # Vía sesión propia
    return str(request.session.get("rol", "")).lower() == "administrador"

@login_required_session
def logs_list(request):
    if not _is_admin(request):
        return redirect("home")

    form = ActivityFilterForm(request.GET or None)
    qs = ActivityLog.objects.all()

    if form.is_valid():
        sd = form.cleaned_data.get("start_date")
        ed = form.cleaned_data.get("end_date")
        user = form.cleaned_data.get("user")
        action = form.cleaned_data.get("action")

        if sd:
            qs = qs.filter(created_at__date__gte=sd)
        if ed:
            qs = qs.filter(created_at__date__lte=ed)
        if user:
            qs = qs.filter(user=user)
        if action:
            qs = qs.filter(action__icontains=action)

    qs = qs.order_by("-created_at")
    page_obj = Paginator(qs, 25).get_page(request.GET.get("page"))

    # Mapeo a las claves que espera tu template audit_logs.html
    audit_logs = [
        {
            "usuario": log.user,          # ajusta si tu modelo usa 'usuario'
            "accion": log.action,         # ajusta si tu modelo usa 'accion'
            "detalles": log.details,      # ajusta si tu modelo usa 'detalles'
            "fecha_hora": log.created_at, # ajusta si tu modelo usa 'fecha_hora'
        }
        for log in page_obj
    ]

    return render(request, "audit/audit_logs.html", {
        "form": form,
        "audit_logs": audit_logs,
        "page_obj": page_obj,
    })

@login_required_session
def log_detail(request, log_id):
    if not _is_admin(request):
        return redirect("home")
    log = get_object_or_404(ActivityLog, id=log_id)
    return render(request, "audit/log_detail.html", {"log": log})
