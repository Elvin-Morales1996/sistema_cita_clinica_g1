# apps/medical/services/availability.py
from __future__ import annotations
from datetime import date, time, datetime, timedelta
from typing import Dict, List

# Configuramos los 4 turnos tal como están en tu modelo
# weekday(): 0=Lun ... 6=Dom
TURNOS_CFG: Dict[str, Dict] = {
    "turno_dia_1": {  # 7:00–15:00 (Lun a Vie; descansa Sáb y Dom)
        "workdays": {0, 1, 2, 3, 4},
        "start": time(7, 0),
        "end": time(15, 0),
    },
    "turno_dia_2": {  # 9:00–17:00 (Mar a Sáb; descansa Dom y Lun)
        "workdays": {1, 2, 3, 4, 5},
        "start": time(9, 0),
        "end": time(17, 0),
    },
    "turno_noche_1": {  # 15:00–23:00 (Lun a Vie; descansa Sáb y Dom)
        "workdays": {0, 1, 2, 3, 4},
        "start": time(15, 0),
        "end": time(23, 0),
    },
    "turno_noche_2": {  # 23:00–07:00 (Mié a Dom; descansa Lun y Mar)
        "workdays": {2, 3, 4, 5, 6},
        "start": time(23, 0),
        "end": time(7, 0),  # termina al día siguiente
    },
}


def _build_slots(start_dt: datetime, end_dt: datetime, slot_min: int) -> List[Dict]:
    """Genera slots cerrados [inicio, fin) cada `slot_min` minutos."""
    slots: List[Dict] = []
    step = timedelta(minutes=slot_min)
    cur = start_dt
    # Evitamos último slot que termine exactamente a end_dt+ (semicerrado)
    while cur + step <= end_dt:
        nxt = cur + step
        slots.append({
            # Importante: ISO 8601 para que JS `new Date(...)` lo entienda
            "inicio": cur.isoformat(),
            "fin": nxt.isoformat(),
        })
        cur = nxt
    return slots


def disponibilidad_por_fecha(medico, fecha: date, slot_min: int) -> Dict:
    """
    Devuelve la disponibilidad de *un médico* para una fecha dada.
    Estructura:
      {
        "fecha": "YYYY-MM-DD",
        "slots": [{"inicio": "...", "fin": "..."}]  # ISO 8601
      }
    """
    cfg = TURNOS_CFG.get(medico.horario)
    if not cfg:
        return {"fecha": fecha.isoformat(), "slots": []}

    wd = fecha.weekday()
    if wd not in cfg["workdays"]:
        return {"fecha": fecha.isoformat(), "slots": []}

    start_t: time = cfg["start"]
    end_t: time = cfg["end"]

    start_dt = datetime.combine(fecha, start_t)
    end_dt = datetime.combine(fecha, end_t)

    # Turno que cruza medianoche (p.ej. 23:00–07:00)
    if end_t <= start_t:
        end_dt += timedelta(days=1)

    return {
        "fecha": fecha.isoformat(),
        "slots": _build_slots(start_dt, end_dt, slot_min),
    }
