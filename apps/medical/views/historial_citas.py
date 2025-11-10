# apps/medical/views/historial_citas.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
import csv

from apps.medical.models.paciente import Paciente
from apps.medical.models.cita import Cita
from apps.core.services.auth_service import require_role  # ya lo usas en otras vistas


def _citas_pasadas_q():
    """
    Regla para considerar una cita como 'pasada':
    - fecha < hoy
    - o fecha == hoy y hora <= ahora
    - o estado en ('atendida', 'cancelada', 'reprogramada')
    """
    now = timezone.localtime()
    hoy = now.date()
    hora_actual = now.time()

    return (
        Q(fecha__lt=hoy)
        | (Q(fecha=hoy) & Q(hora__lte=hora_actual))
        | Q(estado__in=['atendida', 'cancelada', 'reprogramada'])
    )


@require_role(['Administrador', 'Médico', 'Recepcionista'])  # ajusta si quieres permitir Paciente
def historial_citas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Filtros opcionales por rango (desde/hasta)
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    qs = (
        Cita.objects
        .filter(paciente=paciente)
        .filter(_citas_pasadas_q())
        .select_related('medico', 'paciente')
        .order_by('-fecha', '-hora')
    )

    if desde:
        qs = qs.filter(fecha__gte=desde)
    if hasta:
        qs = qs.filter(fecha__lte=hasta)

    paginator = Paginator(qs, 25)
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)

    # URLs de exportación
    export_urls = {
        "csv": request.build_absolute_uri(f"/pacientes/{paciente.id}/citas/historial/export/csv/"),
        "print": request.build_absolute_uri(f"/pacientes/{paciente.id}/citas/historial/imprimir/"),
        # Si luego agregas PDF/XLSX, solo añade aquí
    }

    context = {
        "paciente": paciente,
        "citas": citas,
        "desde": desde or "",
        "hasta": hasta or "",
        "export_urls": export_urls,
        "puede_exportar": True,  # puedes condicionar por rol si quieres
    }
    return render(request, "medical/historial_citas.html", context)


@require_role(['Administrador', 'Médico', 'Recepcionista'])
def exportar_historial_citas_csv(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    qs = (
        Cita.objects
        .filter(paciente=paciente)
        .filter(_citas_pasadas_q())
        .select_related('medico', 'paciente')
        .order_by('-fecha', '-hora')
    )

    # Cabeceras CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = f"historial_citas_{paciente.id}_{timezone.localdate()}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        "Paciente",
        "Identificación",
        "Fecha",
        "Hora",
        "Profesional",
        "Especialidad",
        "Estado",
    ])

    for c in qs:
        writer.writerow([
            f"{c.paciente.nombre} {c.paciente.apellido}",
            getattr(c.paciente, "identificacion", ""),
            c.fecha.isoformat(),
            c.hora.strftime("%H:%M"),
            c.medico.nombre,
            c.medico.especialidad,
            c.estado,
        ])

    return response


@require_role(['Administrador', 'Médico', 'Recepcionista'])
def imprimir_historial_citas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    qs = (
        Cita.objects
        .filter(paciente=paciente)
        .filter(_citas_pasadas_q())
        .select_related('medico', 'paciente')
        .order_by('-fecha', '-hora')
    )

    context = {
        "paciente": paciente,
        "citas": qs,  # sin paginar para impresión
    }
    return render(request, "medical/historial_citas_print.html", context)
