from django.shortcuts import render
from datetime import date
from apps.medical.models.cita import Cita

def home(request):
    hoy = date.today()
    citas_proximas = Cita.objects.filter(fecha__gte=hoy).order_by('fecha', 'hora')[:10]

    return render(request, 'medical/home.html', {
        'citas_proximas': citas_proximas
    })