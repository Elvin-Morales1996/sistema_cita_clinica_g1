from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.audit.models import AlertRule, ActivityLog
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Revisa reglas de AlertRule y envía notificaciones si se cumplen"

    def handle(self, *args, **options):
        now = timezone.now()
        for rule in AlertRule.objects.filter(enabled=True):
            window_start = now - timedelta(minutes=rule.window_minutes)
            count = ActivityLog.objects.filter(action__icontains=rule.action,
                                               created_at__gte=window_start).count()
            if count >= rule.threshold:
                self.stdout.write(self.style.WARNING(
                    f"Alerta: {rule.name} - {count} eventos de '{rule.action}' en {rule.window_minutes} minutos."
                ))
                if rule.notify_emails:
                    recipients = [e.strip() for e in rule.notify_emails.split(",") if e.strip()]
                    subject = f"[ALERTA] {rule.name}"
                    body = f"Se detectaron {count} eventos de '{rule.action}' durante los últimos {rule.window_minutes} minutos."
                    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)

        self.stdout.write(self.style.SUCCESS("Chequeo de alertas finalizado."))
