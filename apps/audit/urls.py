from django.urls import path
from . import views

urlpatterns = [
    path("logs/", views.logs_list, name="audit_logs_list"),
    path("logs/<int:log_id>/", views.log_detail, name="audit_log_detail"),
]
