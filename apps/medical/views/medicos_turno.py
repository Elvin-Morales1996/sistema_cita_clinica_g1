# apps/medical/views/medicos_turno_api.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.medical.models.medico import Medico
from apps.medical.services.turnos import TURNOS_MAP

# GET /api/medicos/<id>/turno/
@require_GET
def turno_de_medico(request, medico_id: int):
    m = Medico.objects.filter(pk=medico_id).first()
    if not m:
        return JsonResponse({"ok": False, "error": "Médico no encontrado"}, status=404)
    info = TURNOS_MAP.get(m.horario)
    if not info:
        return JsonResponse({"ok": False, "error": "Turno no configurado"}, status=400)

    # Formateamos horas para HTML <input type="time">
    desde = info["desde"].strftime("%H:%M")
    hasta = info["hasta"].strftime("%H:%M")

    return JsonResponse({
        "ok": True,
        "medico": {"id": m.id, "nombre": m.nombre, "especialidad": m.especialidad},
        "turno": {
            "label": info["label"],
            "dias": info["dias"],              # [0..6]
            "desde": desde,                    # "07:00"
            "hasta": hasta,                    # "15:00" (si cruza medianoche, igual devolvemos "07:00")
            "cruza_medianoche": info["desde"] > info["hasta"],  # True en turno noche 2
        }
    })

# GET /api/medicos/disponibilidad/?medico_id=..&weekday=0..6
@require_GET
def disponibilidad_por_dia(request):
    try:
        medico_id = int(request.GET.get("medico_id", "0"))
        weekday = int(request.GET.get("weekday", "-1"))
    except ValueError:
        return JsonResponse({"ok": False, "error": "Parámetros inválidos"}, status=400)

    m = Medico.objects.filter(pk=medico_id).first()
    if not m:
        return JsonResponse({"ok": False, "error": "Médico no encontrado"}, status=404)

    info = TURNOS_MAP.get(m.horario)
    if not info:
        return JsonResponse({"ok": False, "error": "Turno no configurado"}, status=400)

    # Disponibilidad "rápida": atiende ese día según su turno (no verifica huecos finos de Citas)
    disponible = weekday in info["dias"]

    return JsonResponse({
        "ok": True,
        "disponible": disponible,
        "mensaje": "Atiende ese día" if disponible else "No atiende ese día",
    })
