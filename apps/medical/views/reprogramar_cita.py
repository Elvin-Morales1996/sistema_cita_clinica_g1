# apps/views/reprogramar_cita.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse

from apps.medical.models.cita import Cita, CitaReprogramacion
from apps.forms_reprogramacion import ReprogramarCitaForm

MAX_REPROGRAMACIONES = 2

def reprogramar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    raiz = cita.raiz()  # la cita original

    # regla: máx. 2 reprogramaciones acumuladas sobre la raíz
    if raiz.reprogramaciones_total >= MAX_REPROGRAMACIONES:
        messages.error(request, "Esta cita ya alcanzó el límite de 2 reprogramaciones.")
        return redirect("home")

    if request.method == "POST":
        form = ReprogramarCitaForm(request.POST, cita_actual=cita)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]
            medico = form.cleaned_data["medico"]
            motivo = form.cleaned_data.get("motivo", "")

            # crear nueva cita manteniendo paciente y (por defecto) médico seleccionado
            nueva = Cita.objects.create(
                paciente=cita.paciente,
                fecha=fecha,
                hora=hora,
                medico=medico,
                estado="confirmada",   # o "pendiente" si prefieres confirmar luego
                cita_origen=raiz,      # SIEMPRE apunta a la raíz
            )

            # marcar la anterior como reprogramada (no se borra)
            cita.estado = "reprogramada"
            cita.save(update_fields=["estado"])

            # incrementar contador en la raíz
            raiz.reprogramaciones_total += 1
            raiz.save(update_fields=["reprogramaciones_total"])

            # historial/auditoría
            CitaReprogramacion.objects.create(
                cita_origen=raiz,
                cita_anterior=cita,
                cita_nueva=nueva,
                motivo=motivo or None,
            )

            # Confirmación al paciente (aquí con mensajes; si tienes email/SMS, llama tu servicio)
            messages.success(
                request,
                f"¡Cita reprogramada! Nueva cita: {nueva.fecha} a las {nueva.hora} con {nueva.medico}."
            )
            return redirect("home")
    else:
        form = ReprogramarCitaForm(
            initial={"fecha": cita.fecha, "hora": cita.hora, "medico": cita.medico},
            cita_actual=cita
        )

    return render(request, "medical/reprogramar_cita.html", {"form": form, "cita": cita, "max": MAX_REPROGRAMACIONES, "usadas": raiz.reprogramaciones_total})
