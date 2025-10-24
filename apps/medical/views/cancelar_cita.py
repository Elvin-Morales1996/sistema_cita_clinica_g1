# apps/medical/views/cancelar_cita.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        cita.estado = 'cancelada'  # coincide con tus choices
        cita.save(update_fields=['estado'])
        messages.success(request, '¡La cita ha sido cancelada con éxito!')
        return redirect('home')

    # 👇 IMPORTANTE: sin coma al final
    return render(request, 'medical/cancelar_cita.html', {'cita': cita})
