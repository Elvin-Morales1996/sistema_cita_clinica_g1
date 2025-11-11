import json
from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive, get_current_timezone
from apps.audit.models import ActivityLog
from apps.medical.models.cita import Cita

def _require_session_admin(request):
    return request.session.get('user_id') and request.session.get('rol') == 'Administrador'

def _to_aware(dt):
    # Asegura timezone aware para restas correctas
    if dt is None:
        return None
    if is_naive(dt):
        return make_aware(dt, get_current_timezone())
    return dt

def reporte_tiempos_espera(request):
    if not _require_session_admin(request):
        return redirect('login')

    # Filtros GET
    agrupacion = request.GET.get('group_by', 'day')  # day|week|month
    hoy = datetime.now().date()
    default_start = hoy - timedelta(days=6)

    try:
        start_date = datetime.strptime(request.GET.get('start_date') or str(default_start), "%Y-%m-%d").date()
    except ValueError:
        start_date = default_start

    try:
        end_date = datetime.strptime(request.GET.get('end_date') or str(hoy), "%Y-%m-%d").date()
    except ValueError:
        end_date = hoy

    # Tomamos sólo eventos checkin/start_consult en rango por FECHA del timestamp dentro del JSON
    logs = ActivityLog.objects.filter(action__in=['checkin', 'start_consult']).order_by('created_at')

    # Armamos por cita_id: guardamos el primer checkin y el primer start_consult
    por_cita = defaultdict(lambda: {"checkin": None, "start": None, "paciente": "", "medico": ""})

    for log in logs:
        try:
            data = json.loads(log.details or "{}")
        except Exception:
            continue

        cita_id = data.get("cita_id")
        ts_str  = data.get("ts")
        if not cita_id or not ts_str:
            continue

        # parseamos ts (ISO)
        ts = parse_datetime(ts_str)
        ts = _to_aware(ts)
        if not ts:
            continue

        # Filtramos por rango de fechas según la fecha del evento
        # 1. Convertimos el timestamp de UTC a la zona horaria local (América/El_Salvador)
        ts_local = ts.astimezone(get_current_timezone())

        # 2. FILTRO CORREGIDO: Comparamos la fecha local (ts_local.date()) con la fecha local (end_date)
        if not (start_date <= ts_local.date() <= end_date):
            continue

        entry = por_cita[cita_id]
        entry["paciente"] = entry["paciente"] or data.get("paciente", "")
        entry["medico"]   = entry["medico"] or data.get("medico", "")

        if log.action == 'checkin' and entry["checkin"] is None:
            entry["checkin"] = ts
        elif log.action == 'start_consult' and entry["start"] is None:
            entry["start"] = ts

    # Construimos filas sólo con pares completos
    filas = []
    for cita_id, d in por_cita.items():
        if d["checkin"] and d["start"] and d["start"] >= d["checkin"]:
            espera_min = int((d["start"] - d["checkin"]).total_seconds() // 60)
            filas.append({
                "cita_id": cita_id,
                "paciente": d["paciente"],
                "medico": d["medico"],
                "hora_llegada": d["checkin"],
                "hora_inicio_consulta": d["start"],
                "espera_min": espera_min
            })

    # Orden por llegada
    filas.sort(key=lambda x: x["hora_llegada"])

    # Promedios por periodo en Python
    promedios_dict = defaultdict(list)
    for f in filas:
        dt = f["hora_llegada"]
        if agrupacion == 'week':
            # semana-ISO (año-semana) como clave
            key = f"{dt.isocalendar().year}-W{dt.isocalendar().week:02d}"
        elif agrupacion == 'month':
            key = dt.strftime("%Y-%m")
        else:
            key = dt.strftime("%Y-%m-%d")
        promedios_dict[key].append(f["espera_min"])

    promedios = [{"periodo": k, "promedio_min": sum(v)/len(v)} for k, v in sorted(promedios_dict.items())]

    ctx = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "group_by": agrupacion,
        "promedios": promedios,
        "lista_pacientes": filas,
    }
    
    return render(request, "medical/reporte_tiempos_espera.html", ctx)
