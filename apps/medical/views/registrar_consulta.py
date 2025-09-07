from django.shortcuts import render, redirect, get_object_or_404
from apps.forms_consulta import ConsultaMedicaForm
from apps.medical.models import Cita  # o Appointment, depende de tu modelo
from apps.medical.models.ConsultaMedica import ConsultaMedica
from django.http import HttpResponseBadRequest



def registrar_consulta(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    # Si ya existe una consulta ligada a esta cita → borrarla
    if hasattr(cita, "consultamedica"):
        cita.consultamedica.delete()

    if request.method == "POST":
        form = ConsultaMedicaForm(request.POST, request.FILES)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.cita = cita
            consulta.paciente = cita.paciente
            consulta.medico = cita.medico
            consulta.save()
            return redirect("detalle_consulta", consulta.id)
    else:
        form = ConsultaMedicaForm()

    return render(request, "medical/registrar_consulta.html", {"form": form, "cita": cita})



