# apps/medical/views/buscar_medicos.py
from datetime import date
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.medical.models.medico import Medico

def buscar_medicos(request):
    # texto opcional para buscar por nombre
    q = request.GET.get("q", "").strip()

    # NUEVO: especialidad seleccionada desde el <select>
    selected_specialty = request.GET.get("specialty", "").strip()

    # Query base
    qs = Medico.objects.all()

    # Filtro por especialidad (si el usuario eligió una)
    if selected_specialty:
        qs = qs.filter(especialidad=selected_specialty)

    # Filtro por nombre (opcional, si escriben en el input de texto)
    if q:
        qs = qs.filter(nombre__icontains=q)

    # Paginación
    page_obj = Paginator(qs.order_by("nombre"), 10).get_page(request.GET.get("page"))

    # Construir lista de especialidades para el select
    specialties = (
        Medico.objects
        .exclude(especialidad__isnull=True)
        .exclude(especialidad__exact="")
        .values_list("especialidad", flat=True)
        .distinct()
        .order_by("especialidad")
    )

    return render(request, "medical/buscar_medicos.html", {
        "q": q,
        "page_obj": page_obj,
        "specialties": specialties,           # lista para el select
        "selected_specialty": selected_specialty,  # para dejar seleccionado lo elegido
        "today": date.today(),
    })
