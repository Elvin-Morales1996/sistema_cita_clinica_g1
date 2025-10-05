from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.image import MIMEImage
import os

def send_cita_notification_email(cita, subject, message_type, custom_message=None):
    """
    Send email notification for cita events
    message_type: 'created', 'modified', 'canceled'
    """
    try:
        paciente_email = cita.paciente.contacto
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')

        # Modern HTML template with project colors
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Notificación de Cita</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f9fafb;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #2196f3 0%, #f57c00 100%);
                    color: white;
                    padding: 30px 40px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 700;
                }}
                .content {{
                    padding: 40px;
                    color: #222222;
                    line-height: 1.6;
                }}
                .cita-card {{
                    background-color: #f8f9fa;
                    border-left: 5px solid #2196f3;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                }}
                .cita-detail {{
                    margin-bottom: 10px;
                }}
                .cita-label {{
                    font-weight: 600;
                    color: #f57c00;
                }}
                .footer {{
                    background-color: #222222;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    font-size: 14px;
                }}
                .logo {{
                    max-width: 120px;
                    height: auto;
                    margin-top: 20px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .highlight {{
                    color: #f57c00;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏥 Clínica Vital Salud</h1>
                    <p>Notificación de Cita Médica</p>
                </div>

                <div class="content">
                    <p>Hola <span class="highlight">{cita.paciente.nombre} {cita.paciente.apellido}</span>,</p>

                    {"<p>¡Tu cita ha sido <span class='highlight'>registrada exitosamente</span>!</p>" if message_type == 'created' else ""}
                    {"<p>Tu cita ha sido <span class='highlight'>modificada</span>.</p>" if message_type == 'modified' else ""}
                    {"<p>Tu cita ha sido <span class='highlight'>cancelada</span>.</p>" if message_type == 'canceled' else ""}

                    {custom_message if custom_message else ""}

                    <div class="cita-card">
                        <h3 style="margin-top: 0; color: #2196f3;">📅 Detalles de tu Cita</h3>
                        <div class="cita-detail">
                            <span class="cita-label">👨‍⚕️ Médico:</span> Dr. {cita.medico.nombre}
                        </div>
                        <div class="cita-detail">
                            <span class="cita-label">📆 Fecha:</span> {cita.fecha.strftime('%d/%m/%Y')}
                        </div>
                        <div class="cita-detail">
                            <span class="cita-label">⏰ Hora:</span> {cita.hora}
                        </div>
                        <div class="cita-detail">
                            <span class="cita-label">📍 Estado:</span> {cita.get_estado_display()}
                        </div>
                    </div>

                    <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>

                    <p style="margin-bottom: 30px;">
                        <strong>¡Gracias por confiar en nosotros!</strong>
                    </p>

                    <img src="cid:logo_image" alt="Logo Clínica Vital Salud" class="logo" />
                </div>

                <div class="footer">
                    <p>Atentamente,<br><strong>Equipo de Clínica Vital Salud</strong></p>
                    <p>📞 Teléfono: (503) 123-4567 | 📧 Email: info@clinicavitalsalud.com</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Set subject based on type
        if message_type == 'created':
            email_subject = '✅ Cita Registrada - Clínica Vital Salud'
        elif message_type == 'modified':
            email_subject = '🔄 Cita Modificada - Clínica Vital Salud'
        elif message_type == 'canceled':
            email_subject = '❌ Cita Cancelada - Clínica Vital Salud'
        else:
            email_subject = subject

        email = EmailMessage(
            subject=email_subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[paciente_email],
        )
        email.content_subtype = "html"

        # Attach logo
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_data = f.read()
                image = MIMEImage(logo_data)
                image.add_header("Content-ID", "<logo_image>")
                email.attach(image)

        # ✅ Aquí está el cambio importante
        email.send(fail_silently=True)
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
