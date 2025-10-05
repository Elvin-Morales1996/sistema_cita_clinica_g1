from django.shortcuts import render, redirect, get_object_or_404
from apps.medical.models.plantilla_correo import PlantillaCorreo
from apps.plantilla_correo_forms import PlantillaCorreoForm
from functools import wraps

# Decorador compatible con tu login basado en sesión
def admin_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica si hay sesión y si el rol es 'admin'
        if 'rol' not in request.session or request.session['rol'] != 'Administrador':
            return redirect('login')  # Si no es admin, va al login
        return view_func(request, *args, **kwargs)
    return wrapper

# ------------------- VISTAS -------------------

@admin_required_custom
def listar_plantillas(request):
    plantillas = PlantillaCorreo.objects.all()
    return render(request, "medical/plantilla_correo.html", {"plantillas": plantillas})

@admin_required_custom
def crear_plantilla(request):
    if request.method == "POST":
        form = PlantillaCorreoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_plantillas")
    else:
        form = PlantillaCorreoForm()
    return render(request, "medical/crear.html", {"form": form})

@admin_required_custom
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

@admin_required_custom
def eliminar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaCorreo, pk=pk)
    plantilla.delete()
    return redirect("listar_plantillas")
