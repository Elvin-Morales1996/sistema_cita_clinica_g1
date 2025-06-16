from django.shortcuts import render, get_object_or_404
from datetime import date
import calendar
from apps.medical.models.medico import Medico

MESES = [
    '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]
def ver_calendario(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    mes = int(request.GET.get('mes', date.today().month))
    año = int(request.GET.get('año', date.today().year))

    mes_anterior = mes - 1 if mes > 1 else 12
    año_anterior = año if mes > 1 else año - 1

    mes_siguiente = mes + 1 if mes < 12 else 1
    año_siguiente = año if mes < 12 else año + 1

    dias_laborales = dias_laborales_por_turno(medico.horario)

    cal = calendar.Calendar()
    semanas = cal.monthdays2calendar(año, mes)

    calendario_html = "<table class='table-calendario'><thead><tr>"
    for dia in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']:
        calendario_html += f"<th>{dia}</th>"
    calendario_html += "</tr></thead><tbody>"

    for semana in semanas:
        calendario_html += "<tr>"
        for dia, dia_semana in semana:
            if dia == 0:
                calendario_html += "<td></td>"
            else:
                clase = "dia-laboral" if dia_semana in dias_laborales else ""
                calendario_html += f"<td class='{clase}'>{dia}</td>"
        calendario_html += "</tr>"
    calendario_html += "</tbody></table>"

    return render(request, 'medical/ver_calendario.html', {
        'medico': medico,
        'mes': mes,
        'año': año,
        'mes_anterior': mes_anterior,
        'año_anterior': año_anterior,
        'mes_siguiente': mes_siguiente,
        'año_siguiente': año_siguiente,
        'nombre_mes': MESES[mes],
        'calendario': calendario_html,
    })
def dias_laborales_por_turno(turno):
    if turno == 'turno_dia_1':
        return [0, 1, 2, 3, 4]  # Lunes a Viernes (0 = lunes)
    elif turno == 'turno_dia_2':
        return [1, 2, 3, 4, 5]  # Martes a Sábado
    elif turno == 'turno_noche_1':
        return [0, 1, 2, 3, 4]  # Lunes a Viernes
    elif turno == 'turno_noche_2':
        return [2, 3, 4, 5, 6]  # Miércoles a Domingo
    return []