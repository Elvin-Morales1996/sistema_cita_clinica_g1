import datetime as dt

# 0=Lun, 1=Mar, 2=Mié, 3=Jue, 4=Vie, 5=Sáb, 6=Dom
TURNOS_MAP = {
    "turno_dia_1": {
        "dias": {0, 1, 2, 3, 4},        # Lun–Vie
        "inicio": dt.time(7, 0),
        "fin":    dt.time(15, 0),
    },
    "turno_dia_2": {
        "dias": {1, 2, 3, 4, 5},        # Mar–Sáb
        "inicio": dt.time(9, 0),
        "fin":    dt.time(17, 0),
    },
    "turno_noche_1": {
        "dias": {0, 1, 2, 3, 4},        # Lun–Vie
        "inicio": dt.time(15, 0),
        "fin":    dt.time(23, 0),
    },
    # Nocturno cruza medianoche: dividimos en dos tramos
    "turno_noche_2": {
        "dias_tarde":   {2, 3, 4, 5, 6},  # Mié–Dom 23:00–23:59
        "inicio_tarde": dt.time(23, 0),
        "fin_tarde":    dt.time(23, 59, 59),

        "dias_maniana": {3, 4, 5, 6, 0},  # Jue–Lun 00:00–07:00
        "inicio_maniana": dt.time(0, 0),
        "fin_maniana":    dt.time(7, 0),
    },
}
