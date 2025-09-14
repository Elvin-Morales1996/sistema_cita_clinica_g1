from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.medical.models.medico import Medico

@require_GET
def medicos_especialidad(request):
    esp = request.GET.get("especialidad", "").strip()
    data = []
    if esp:
        qs = Medico.objects.filter(especialidad=esp).order_by("nombre")
        data = [{"id": m.id, "nombre": m.nombre} for m in qs]
    return JsonResponse({"medicos": data})
