from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import ActivityLog
from .forms import ActivityFilterForm
from django.core.paginator import Paginator

def is_admin(user):
    # Ajusta esto a tu lógica real; ejemplo con superuser o rol
    try:
        return user.is_superuser or getattr(user, "rol", "").lower() == "administrador"
    except Exception:
        return False

@user_passes_test(is_admin)
def logs_list(request):
    form = ActivityFilterForm(request.GET or None)
    qs = ActivityLog.objects.all()

    if form.is_valid():
        sd = form.cleaned_data.get("start_date")
        ed = form.cleaned_data.get("end_date")
        user = form.cleaned_data.get("user")
        action = form.cleaned_data.get("action")

        if sd:
            qs = qs.filter(created_at__date__gte=sd)
        if ed:
            qs = qs.filter(created_at__date__lte=ed)
        if user:
            qs = qs.filter(user=user)
        if action:
            qs = qs.filter(action__icontains=action)

    paginator = Paginator(qs, 25)
    page = request.GET.get("page")
    logs = paginator.get_page(page)

    return render(request, "audit/logs_list.html", {"form": form, "logs": logs})

@user_passes_test(is_admin)
def log_detail(request, log_id):
    log = get_object_or_404(ActivityLog, id=log_id)
    return render(request, "audit/log_detail.html", {"log": log})
