from django.shortcuts import render, get_object_or_404
from apps.medical.models import ConsultaMedica

def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(ConsultaMedica, id=consulta_id)
    return render(request, "medical/detalle_consulta.html", {"consulta": consulta})