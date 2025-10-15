# apps/audit/utils.py
from .models import ActivityLog

def log_action(user=None, action="", details="", ip=None):
    ActivityLog.objects.create(user=user, action=action, details=details, ip=ip)
