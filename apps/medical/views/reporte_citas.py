from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from apps.medical.models import Cita
from apps.core.services.auth_service import require_role
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@require_role(['Administrador', 'Médico', 'Recepcionista'])
def reporte_citas(request):
    citas = Cita.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    medico = request.GET.get('medico')
    especialidad = request.GET.get('especialidad')

    if fecha_inicio and fecha_fin:
        citas = citas.filter(fecha__range=[fecha_inicio, fecha_fin])

    if medico:
        citas = citas.filter(medico__nombre__icontains=medico)

    if especialidad:
        citas = citas.filter(medico__especialidad__icontains=especialidad)

    if 'export_pdf' in request.GET:
        return generar_pdf(citas)

    if 'export_excel' in request.GET:
        return generar_excel(citas)

    return render(request, 'medical/reporte_citas.html', {
        'citas': citas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


def generar_pdf(citas):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Reporte de Citas Agendadas")
    p.setFont("Helvetica", 10)
    y -= 40

    for cita in citas:
        p.drawString(50, y, f"Paciente: {cita.paciente.nombre} {cita.paciente.apellido}")
        p.drawString(250, y, f"Médico: {cita.medico.nombre} - {cita.medico.especialidad}")
        p.drawString(480, y, f"Fecha: {cita.fecha}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def generar_excel(citas):
    data = []
    for cita in citas:
        data.append({
            'Paciente': f"{cita.paciente.nombre} {cita.paciente.apellido}",
            'Médico': cita.medico.nombre,
            'Especialidad': cita.medico.especialidad,
            'Fecha': cita.fecha,
            'Hora': cita.hora,
        })

    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Citas')

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_citas.xlsx"'
    return response
