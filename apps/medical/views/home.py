from django.shortcuts import render
from datetime import date
from apps.medical.models.cita import Cita
from django.contrib import messages

def home(request):
    # 🔹 Limpia mensajes antiguos (por ejemplo del login fallido)
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    hoy = date.today()
    citas_proximas = Cita.objects.filter(fecha__gte=hoy).exclude(estado='cancelada').order_by('fecha', 'hora')[:10]

    # Obtener rol del usuario desde la sesión o desde el usuario logueado
    rol_usuario = request.session.get('rol', 'Paciente')  # Ajusta según cómo guardes el rol

    return render(request, 'medical/home.html', {
        'citas_proximas': citas_proximas,
        'rol_usuario': rol_usuario
    })
