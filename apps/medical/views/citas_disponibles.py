from datetime import date, datetime
from django.shortcuts import render
from apps.medical.models.medico import Medico
from apps.medical.services.check_availability import CheckAvailabilityUC

def citas_disponibles(request):
    specialty_id = request.GET.get("specialty")   # nombre (string)
    doctor_id    = request.GET.get("doctor")
    start_str    = request.GET.get("fecha")
    days         = int(request.GET.get("days", 7))
    DAYS_CHOICES = [7, 14, 30]

    today = date.today()
    start = today
    if start_str:
        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            pass
    if start < today:
        start = today

    # 💡 Si llega doctor pero no specialty, dedúcela del médico
    if doctor_id and not specialty_id:
        try:
            m = Medico.objects.get(pk=int(doctor_id))
            specialty_id = m.especialidad
        except (Medico.DoesNotExist, ValueError):
            doctor_id = None  # invalida el doctor si no existe

    # Especialidades para el select
    especialidades_distintas = (
        Medico.objects
        .exclude(especialidad__isnull=True)
        .exclude(especialidad__exact="")
        .values_list("especialidad", flat=True)
        .distinct()
        .order_by("especialidad")
    )
    specialties = [{"id": e, "name": e} for e in especialidades_distintas]

    # Doctores (filtrados por especialidad si aplica)
    doctors = Medico.objects.all().order_by("nombre")
    if specialty_id:
        doctors = doctors.filter(especialidad=specialty_id)

    # 💡 Si mandaron un doctor que no está en la especialidad actual, invalídalo
    if doctor_id:
        try:
            doctor_pk = int(doctor_id)
        except ValueError:
            doctor_pk = None

        if doctor_pk and not doctors.filter(pk=doctor_pk).exists():
            doctor_id = None  # fuerza a que no calcule items si no corresponde

    items = []
    if doctor_id:
        data  = CheckAvailabilityUC().execute(medico_id=int(doctor_id), start=start, days=days)
        items = data["items"]

    return render(request, "medical/citas_disponibles.html", {
        "specialties": specialties,
        "doctors": doctors,
        "selected_specialty": specialty_id or None,
        "selected_doctor": int(doctor_id) if doctor_id else None,
        "start": start,
        "days": days,
        "items": items,
        "days_choices": DAYS_CHOICES,
        "today": today,  # min del calendario
    })
