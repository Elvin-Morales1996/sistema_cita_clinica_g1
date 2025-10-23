from datetime import date, datetime
from django.http import JsonResponse
from apps.medical.services.check_availability import CheckAvailabilityUC

def api_disponibilidad(request):
    doctor_id = request.GET.get("doctor")
    start_str = request.GET.get("fecha")
    days = int(request.GET.get("days", 7))

    if not doctor_id:
        return JsonResponse({"items": [], "version": "no-doctor"})

    today = date.today()
    start = today
    if start_str:
        try:
            parsed = datetime.strptime(start_str, "%Y-%m-%d").date()
            start = parsed if parsed >= today else today   # ← mismo bloqueo
        except ValueError:
            start = today

    data = CheckAvailabilityUC().execute(medico_id=int(doctor_id), start=start, days=days)
    return JsonResponse(data)
