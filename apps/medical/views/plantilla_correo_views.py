from django.shortcuts import render, redirect, get_object_or_404
from apps.medical.models.plantilla_correo import PlantillaCorreo
from django.contrib.auth.decorators import user_passes_test
from apps.plantilla_correo_forms import PlantillaCorreoForm

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_superuser)(view_func)

@admin_required
def listar_plantillas(request):
    plantillas = PlantillaCorreo.objects.all()
    return render(request, "medical/plantilla_correo.html", {"plantillas": plantillas})

@admin_required
def crear_plantilla(request):
    if request.method == "POST":
        form = PlantillaCorreoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_plantillas")
    else:
        form = PlantillaCorreoForm()
    return render(request, "medical/crear.html", {"form": form})

@admin_required
def editar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaCorreo, pk=pk)
    if request.method == "POST":
        form = PlantillaCorreoForm(request.POST, instance=plantilla)
        if form.is_valid():
            form.save()
            return redirect("listar_plantillas")
    else:
        form = PlantillaCorreoForm(instance=plantilla)
    return render(request, "medical/crear.html", {"form": form})  # Reusa la plantilla crear.html

@admin_required
def eliminar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaCorreo, pk=pk)
    plantilla.delete()
    return redirect("listar_plantillas")
