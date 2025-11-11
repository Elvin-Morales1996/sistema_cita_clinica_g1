import json
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden
from apps.audit.models import ActivityLog   # ajusta el path si difiere
from apps.medical.models.cita import Cita   # ajusta el path si difiere

def _require_session_admin(request):
    # Ajusta si usas otro control; aquí pedimos sesión + rol Admin
    return request.session.get('user_id') and request.session.get('rol') == 'Administrador'

def marcar_llegada(request, cita_id):
    if not _require_session_admin(request):
        return redirect('login')

    cita = get_object_or_404(Cita, id=cita_id)
    payload = {
        "cita_id": cita.id,
        "paciente": getattr(cita.paciente, "nombre", ""),
        "medico": getattr(cita.medico, "nombre", ""),
        "ts": timezone.now().isoformat()
    }
    ActivityLog.objects.create(
        user=None,            # ó el usuario en sesión si tu modelo lo requiere
        action='checkin',
        details=json.dumps(payload)
    )
    # Redirige a donde te convenga (cola, home, etc.)
    return redirect('home')

def iniciar_consulta(request, cita_id):
    if not _require_session_admin(request):
        return redirect('login')

    cita = get_object_or_404(Cita, id=cita_id)
    payload = {
        "cita_id": cita.id,
        "paciente": getattr(cita.paciente, "nombre", ""),
        "medico": getattr(cita.medico, "nombre", ""),
        "ts": timezone.now().isoformat()
    }
    ActivityLog.objects.create(
        user=None,
        action='start_consult',
        details=json.dumps(payload)
    )
    return redirect('home')
