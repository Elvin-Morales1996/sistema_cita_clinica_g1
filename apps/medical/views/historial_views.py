from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from ..models import Paciente, HistorialClinico, ConsultaMedica, Cita
from ..forms_historial import HistorialClinicoForm, BuscarPacienteForm
from apps.core.services.auth_service import require_role

@require_role(['Administrador', 'Médico', 'Recepcionista'])
def buscar_pacientes(request):
    form = BuscarPacienteForm(request.GET or None)
    pacientes = Paciente.objects.all()
    search_value = ''
    search_type = 'identificacion'
    if form.is_valid():
        search_value = form.cleaned_data['search']
        search_type = form.cleaned_data['search_type']
        if search_value:
            if search_type == 'identificacion':
                pacientes = pacientes.filter(identificacion__icontains=search_value)
            elif search_type == 'nombre_apellido':
                # Split search_value into nombre and apellido
                parts = search_value.split()
                if len(parts) >= 2:
                    nombre = parts[0]
                    apellido = ' '.join(parts[1:])
                    pacientes = pacientes.filter(
                        Q(nombre__icontains=nombre) & Q(apellido__icontains=apellido)
                    )
                else:
                    pacientes = pacientes.filter(
                        Q(nombre__icontains=search_value) |
                        Q(apellido__icontains=search_value)
                    )

    # Agregar información del rol para el template
    rol_usuario = request.session.get('rol', 'Paciente')

    return render(request, 'medical/buscar_pacientes.html', {
        'form': form,
        'pacientes': pacientes,
        'search_value': search_value,
        'search_type': search_type,
        'rol_usuario': rol_usuario
    })
    form = BuscarPacienteForm(request.GET or None)
    pacientes = Paciente.objects.all()
    search_value = ''
    search_type = 'identificacion'
    if form.is_valid():
        search_value = form.cleaned_data['search']
        search_type = form.cleaned_data['search_type']
        if search_value:
            if search_type == 'identificacion':
                pacientes = pacientes.filter(identificacion__icontains=search_value)
            elif search_type == 'nombre_apellido':
                # Split search_value into nombre and apellido
                parts = search_value.split()
                if len(parts) >= 2:
                    nombre = parts[0]
                    apellido = ' '.join(parts[1:])
                    pacientes = pacientes.filter(
                        Q(nombre__icontains=nombre) & Q(apellido__icontains=apellido)
                    )
                else:
                    pacientes = pacientes.filter(
                        Q(nombre__icontains=search_value) |
                        Q(apellido__icontains=search_value)
                    )
    return render(request, 'medical/buscar_pacientes.html', {
        'form': form,
        'pacientes': pacientes,
        'search_value': search_value,
        'search_type': search_type
    })

@require_role(['Administrador', 'Médico', 'Recepcionista', 'Paciente'])
def ver_historial(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historial, created = HistorialClinico.objects.get_or_create(paciente=paciente)
    consultas = ConsultaMedica.objects.filter(paciente=paciente).order_by('-creado_en')
    citas_futuras = Cita.objects.filter(
        paciente=paciente,
        fecha__gte=timezone.now().date()
    ).exclude(
        # Exclude citas that already have consulta
        id__in=ConsultaMedica.objects.values_list('cita_id', flat=True)
    ).order_by('fecha', 'hora')

    # Agregar información del rol para mostrar/ocultar botones de edición
    rol_usuario = request.session.get('rol', 'Paciente')

    return render(request, 'medical/ver_historial.html', {
        'paciente': paciente,
        'historial': historial,
        'consultas': consultas,
        'citas_futuras': citas_futuras,
        'rol_usuario': rol_usuario,
        'puede_editar': rol_usuario in ['Administrador', 'Médico']
    })

@require_role(['Administrador', 'Médico'])
def editar_historial(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historial, created = HistorialClinico.objects.get_or_create(paciente=paciente)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historial actualizado correctamente.')
            return redirect('ver_historial', paciente_id=paciente_id)
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'medical/editar_historial.html', {'form': form, 'paciente': paciente})

@require_role(['Administrador', 'Médico'])
def eliminar_historial(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historial = get_object_or_404(HistorialClinico, paciente=paciente)
    if request.method == 'POST':
        historial.delete()
        messages.success(request, 'Historial eliminado correctamente.')
        return redirect('buscar_pacientes')
    return render(request, 'medical/eliminar_historial.html', {'paciente': paciente, 'historial': historial})