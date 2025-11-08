from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from apps.medical.models import Cita, Medico
from apps.core.services.auth_service import require_role
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

@require_role(['Administrador', 'Médico', 'Recepcionista'])
def reporte_asistencia(request):
    citas = Cita.objects.all().order_by('fecha', 'hora')

    # Obtener listas para los filtros
    medicos = Medico.objects.all().order_by('nombre')
    especialidades = Medico.objects.values_list('especialidad', flat=True).distinct().order_by('especialidad')

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
        return generar_pdf_asistencia(citas)

    if 'export_excel' in request.GET:
        return generar_excel_asistencia(citas)

    return render(request, 'medical/reporte_asistencia.html', {
        'citas': citas,
        'medicos': medicos,
        'especialidades': especialidades,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'medico': medico,
        'especialidad': especialidad,
    })


def generar_pdf_asistencia(citas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo para el título principal
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centrado
    title_style.fontSize = 20
    title_style.spaceAfter = 30
    title_style.textColor = colors.HexColor('#2196F3')

    # Estilo para subtítulo
    subtitle_style = styles['Heading2']
    subtitle_style.alignment = 1
    subtitle_style.fontSize = 14
    subtitle_style.spaceAfter = 20
    subtitle_style.textColor = colors.HexColor('#666666')

    # Estilo para información
    info_style = styles['Normal']
    info_style.alignment = 1
    info_style.fontSize = 10
    info_style.spaceAfter = 30

    # Logo (simulado con texto ya que no podemos cargar imágenes fácilmente)
    logo_text = Paragraph('<b>CLÍNICA VITAL SALUD</b>', styles['Heading1'])
    logo_text.style = styles['Heading1']
    logo_text.style.alignment = 1
    logo_text.style.fontSize = 24
    logo_text.style.textColor = colors.HexColor('#2196F3')
    logo_text.style.spaceAfter = 10
    elements.append(logo_text)

    # Dirección simulada
    address = Paragraph('Centro Médico Especializado<br/>Dirección: Calle Principal #123, Ciudad<br/>Teléfono: (503) 1234-5678', info_style)
    elements.append(address)
    elements.append(Spacer(1, 0.3*inch))

    # Título del reporte
    title = Paragraph("REPORTE DE ASISTENCIA DE CITAS", title_style)
    elements.append(title)

    # Fecha de generación
    fecha_generacion = Paragraph(f"Fecha de Generación: {timezone.now().strftime('%d de %B de %Y %H:%M')}", info_style)
    elements.append(fecha_generacion)

    # Información del filtro aplicado
    if citas:
        filtros = []
        if hasattr(citas, 'query') and citas.query.where:
            filtros.append("Filtros aplicados según criterios de búsqueda")
        else:
            filtros.append("Reporte completo de todas las citas")

        filtros_text = Paragraph(" • ".join(filtros), info_style)
        elements.append(filtros_text)

    elements.append(Spacer(1, 0.4*inch))

    # Datos de la tabla
    data = [['Paciente', 'Fecha', 'Hora', 'Médico', 'Especialidad', 'Estado']]

    for cita in citas:
        estado_display = "✓ Asistió" if cita.estado == "atendida" else "✗ No Asistió"
        data.append([
            f"{cita.paciente.nombre}\n{cita.paciente.apellido}",
            cita.fecha.strftime('%d/%m/%Y'),
            cita.hora.strftime('%H:%M'),
            cita.medico.nombre,
            cita.medico.especialidad,
            estado_display
        ])

    # Crear tabla con mejor estilo
    table = Table(data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1*inch])

    # Estilo profesional para la tabla
    table_style = TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),

        # Cuerpo de la tabla
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),

        # Bordes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1976D2')),

        # Filas alternas
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#F8F9FA')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#F8F9FA')),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#F8F9FA')),
    ])

    table.setStyle(table_style)
    elements.append(table)

    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    footer_style = styles['Normal']
    footer_style.alignment = 1
    footer_style.fontSize = 8
    footer_style.textColor = colors.HexColor('#666666')

    footer = Paragraph("Este reporte es confidencial y propiedad de Clínica Vital Salud<br/>Sistema de Gestión de Citas Médicas", footer_style)
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="reporte_asistencia_clinica.pdf"'})


def generar_excel_asistencia(citas):
    data = []
    for cita in citas:
        estado_display = "Asistió" if cita.estado == "atendida" else "No Asistió"
        data.append({
            'Paciente': f"{cita.paciente.nombre} {cita.paciente.apellido}",
            'Fecha': cita.fecha.strftime('%d/%m/%Y'),
            'Hora': cita.hora.strftime('%H:%M'),
            'Médico': cita.medico.nombre,
            'Especialidad': cita.medico.especialidad,
            'Estado': estado_display,
        })

    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Asistencia')

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_asistencia.xlsx"'
    return response