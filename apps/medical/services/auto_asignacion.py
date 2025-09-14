import datetime as dt
from django.utils import timezone
from apps.medical.models.cita import Cita
from apps.medical.models.medico import Medico
from .turnos import TURNOS_MAP

def _generar_slots(fecha: dt.date, desde: dt.time, hasta: dt.time, paso_min=30):
    cur = dt.datetime.combine(fecha, desde)
    fin = dt.datetime.combine(fecha, hasta)
    while cur <= fin - dt.timedelta(minutes=paso_min):
        yield cur.time()
        cur += dt.timedelta(minutes=paso_min)

def _slots_para_medico_en_fecha(medico: Medico, fecha: dt.date,
                                pref_horas: tuple[dt.time|None, dt.time|None] = (None, None)):
    info = TURNOS_MAP.get(medico.horario)
    if not info:
        return []

    wd = fecha.weekday()
    h_from_pref, h_to_pref = pref_horas

    def _range_with_prefs(start: dt.time, end: dt.time):
        s = h_from_pref or start
        e = h_to_pref or end
        s = max(s, start)
        e = min(e, end)
        return [] if s >= e else list(_generar_slots(fecha, s, e, 30))

    if medico.horario != "turno_noche_2":
        if wd not in info["dias"]:
            return []
        return _range_with_prefs(info["inicio"], info["fin"])

    # turno nocturno dividido en dos tramos
    slots = []
    if wd in info["dias_tarde"]:
        slots += _range_with_prefs(info["inicio_tarde"], info["fin_tarde"])
    if wd in info["dias_maniana"]:
        slots += _range_with_prefs(info["inicio_maniana"], info["fin_maniana"])
    return slots

def primera_cita_disponible(*, especialidad: str, medico_id: int | None,
                            dias_preferidos: set[int] | None,
                            hora_desde: dt.time | None,
                            hora_hasta: dt.time | None,
                            horizonte_dias: int = 30):
    qs_medicos = Medico.objects.filter(especialidad__iexact=especialidad)
    if medico_id:
        qs_medicos = qs_medicos.filter(pk=medico_id)
    if not qs_medicos.exists():
        return None

    hoy = timezone.localdate()

    for d in range(horizonte_dias):
        fecha = hoy + dt.timedelta(days=d)
        if dias_preferidos is not None and fecha.weekday() not in dias_preferidos:
            continue

        for medico in qs_medicos:
            slots = _slots_para_medico_en_fecha(medico, fecha, (hora_desde, hora_hasta))
            if not slots:
                continue

            ocupadas = set(
                Cita.objects.filter(medico=medico, fecha=fecha)
                .values_list("hora", flat=True)
            )
            for slot in slots:
                if slot not in ocupadas:
                    return {"medico": medico, "fecha": fecha, "hora": slot}
    return None
