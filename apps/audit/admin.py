from django.contrib import admin
from .models import ActivityLog, AlertRule
from .models import AuditLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "ip")
    list_filter = ("action", "user")
    search_fields = ("details",)
    readonly_fields = [f.name for f in ActivityLog._meta.fields]  # logs no editables

@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "action", "threshold", "window_minutes", "enabled")
    list_editable = ("enabled",)
    
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora', 'detalles')
    list_filter = ('accion', 'fecha_hora', 'usuario')
    search_fields = ('usuario__username', 'accion', 'detalles')    
