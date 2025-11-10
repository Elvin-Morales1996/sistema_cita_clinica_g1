from django.contrib import admin
from .models import ActivityLog, AlertRule, AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'accion', 'detalles', 'fecha_hora')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario_sistema__usuario', 'usuario_admin__username', 'accion', 'detalles')

    def get_usuario(self, obj):
        """Mostrar nombre del usuario según su tipo"""
        if obj.usuario_sistema:
            return f"{obj.usuario_sistema.usuario} (sistema)"
        elif obj.usuario_admin:
            return f"{obj.usuario_admin.username} (admin)"
        return "Desconocido"

    get_usuario.short_description = "Usuario"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'details', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'details')


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'action', 'threshold', 'window_minutes', 'enabled')
    list_filter = ('enabled',)
    search_fields = ('name', 'action')
