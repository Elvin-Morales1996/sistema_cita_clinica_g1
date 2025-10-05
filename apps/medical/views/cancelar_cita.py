from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita

def cancelar_cita(request, cita_id):
    # Obtener la cita o devolver 404 si no existe
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        # Cambiar estado y guardar
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, '¡La cita ha sido cancelada con éxito!')

        # Redirigir al home
        return redirect('home')

    # Mostrar la plantilla de confirmación de cancelación
    return render(request, 'medical/cancelar_cita.html', {'cita': cita})
