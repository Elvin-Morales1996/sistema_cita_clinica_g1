# apps/medical/views/auto_asignacion.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.forms_medico import SolicitudAutoCitaForm
from apps.medical.services.auto_asignacion import primera_cita_disponible
from apps.medical.models.cita import Cita
from apps.medical.models.paciente import Paciente

@require_http_methods(["GET", "POST"])
def auto_asignacion(request):
    # NO bloquees aquí; deja que cualquiera vea el formulario y busque.
    paciente_id = request.session.get("paciente_id")
    paciente = Paciente.objects.filter(pk=paciente_id).first()

    # --- aceptar / rechazar desde la pantalla de resultado ---
    if request.method == "POST" and "accion" in request.POST:
        if request.POST["accion"] == "aceptar":
            # AQUÍ sí exigimos paciente (rol/sesión)
            if request.session.get("rol") != "paciente" or not paciente:
                messages.error(request, "Debes iniciar sesión como paciente para confirmar la cita.")
                return redirect("auto_asignacion")

            medico_id = int(request.POST["medico_id"])
            fecha = request.POST["fecha"]
            hora = request.POST["hora"]

            # evitar colisiones si otro tomó el slot
            if Cita.objects.filter(medico_id=medico_id, fecha=fecha, hora=hora).exists():
                messages.warning(request, "Ese horario acaba de ocuparse. Intentemos de nuevo.")
                return redirect("auto_asignacion")

            Cita.objects.create(
                paciente=paciente, medico_id=medico_id,
                fecha=fecha, hora=hora, estado="programada"
            )
            messages.success(request, "¡Cita confirmada!")
            return redirect("home")

        if request.POST["accion"] == "rechazar":
            messages.info(request, "Buscaremos otra opción. Puedes ajustar tus preferencias.")
            return redirect("auto_asignacion")

    # --- búsqueda inicial o repetición con criterios ---
    if request.method == "POST":
        form = SolicitudAutoCitaForm(request.POST)
        if form.is_valid():
            sugerencia = primera_cita_disponible(
                especialidad=form.cleaned_data["especialidad"],
                medico_id=form.cleaned_data["medico_id"].id if form.cleaned_data["medico_id"] else None,
                dias_preferidos=set(map(int, form.cleaned_data["dias_preferidos"])) if form.cleaned_data["dias_preferidos"] else None,
                hora_desde=form.cleaned_data["hora_desde"],
                hora_hasta=form.cleaned_data["hora_hasta"],
            )
            return render(request, "medical/auto_asignacion_resultado.html", {
                "form": form, "sugerencia": sugerencia
            })
    else:
        form = SolicitudAutoCitaForm()

    # nombre del template del formulario (sé consistente con el archivo que tengas)
    return render(request, "medical/auto_asignacion.html", {"form": form})
