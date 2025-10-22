from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("logs/", views.logs_list, name="audit_logs"),
    path("logs/<int:log_id>/", views.log_detail, name="audit_log_detail"),
]
