
from django.urls import path
from apps.medical.views import plantilla_correo_views

urlpatterns = [
    # ... otras rutas de medical
     path("plantillas/", plantilla_correo_views.listar_plantillas, name="listar_plantillas"),
    path("plantillas/crear/", plantilla_correo_views.crear_plantilla, name="crear_plantilla"),
    path("plantillas/editar/<int:pk>/", plantilla_correo_views.editar_plantilla, name="editar_plantilla"),
    path("plantillas/eliminar/<int:pk>/", plantilla_correo_views.eliminar_plantilla, name="eliminar_plantilla"),
]
