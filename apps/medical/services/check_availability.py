# apps/medical/services/check_availability.py
import datetime as dt
from typing import Dict, List

from apps.medical.models.medico import Medico
from apps.medical.services.availability import disponibilidad_por_fecha

class CheckAvailabilityUC:
    """
    Consolida la disponibilidad de un médico en un rango de días.
    """
    def __init__(self, slot_min: int = 30):
        self.slot_min = slot_min

    def _filtra_slots_pasados_hoy(self, items: List[Dict]) -> List[Dict]:
        """Si la fecha del item es hoy, elimina los slots cuyo inicio ya pasó."""
        now = dt.datetime.now()
        today = now.date()

        for it in items:
            # it["fecha"] puede venir como date o como string ISO
            fecha_item = it.get("fecha")
            if isinstance(fecha_item, str):
                try:
                    fecha_item = dt.date.fromisoformat(fecha_item)
                except Exception:
                    continue

            if fecha_item == today:
                futuros = []
                for s in it.get("slots", []):
                    inicio = s.get("inicio")
                    # Soportar datetime ISO o solo "HH:MM"
                    inicio_dt = None
                    if isinstance(inicio, str):
                        try:
                            # caso ISO: "2025-10-08T09:30:00"
                            inicio_dt = dt.datetime.fromisoformat(inicio)
                        except Exception:
                            try:
                                hh, mm = map(int, inicio[:5].split(":"))
                                inicio_dt = dt.datetime.combine(today, dt.time(hh, mm))
                            except Exception:
                                pass
                    elif isinstance(inicio, dt.datetime):
                        inicio_dt = inicio

                    if inicio_dt is not None and inicio_dt >= now:
                        futuros.append(s)
                it["slots"] = futuros
        return items

    def execute(self, medico_id: int, start: dt.date, days: int) -> Dict:
        medico = (
            Medico.objects
            .filter(pk=medico_id)  # tu modelo no tiene 'activo'
            .first()
        )
        if not medico:
            return {"items": [], "version": f"no-medico-{dt.datetime.now().timestamp()}"}

        items: List[Dict] = []
        for i in range(int(days)):
            fecha = start + dt.timedelta(days=i)
            items.append(disponibilidad_por_fecha(medico, fecha, self.slot_min))

        # Filtro de slots pasados solo para el día de hoy
        items = self._filtra_slots_pasados_hoy(items)

        version = f"{medico_id}-{start.isoformat()}-{days}-{int(dt.datetime.now().timestamp() // 60)}"
        return {"items": items, "version": version}
