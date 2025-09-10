# views/crear_cita.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.image import MIMEImage
import os
from apps.forms_cita import CitaForm

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()  # Guardamos la cita

            # Mensaje de éxito en pantalla
            messages.success(request, '¡La cita se registró con éxito!')

            # Enviar correo HTML al paciente con logo
            try:
                paciente_email = cita.paciente.contacto  # Asegúrate que sea EmailField
                logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')  # Ruta absoluta al logo

                html_content = f"""
                <html>
                    <body>
                        <p>Hola {cita.paciente.nombre} {cita.paciente.apellido},</p>
                        <p>Tu cita con el Dr. {cita.medico.nombre} para la fecha 
                        <strong>{cita.fecha}</strong> a las <strong>{cita.hora}</strong> 
                        ha sido registrada exitosamente.</p>
                        <p>Gracias por usar nuestro sistema.</p>
                        <br>
                        <p>Atentamente,<br>Clínica Salud Total</p>
                        <p><img src="cid:logo_image" alt="Logo" style="width:150px; height:auto;"></p>
                    </body>
                </html>
                """

                email = EmailMessage(
                    subject='Cita Registrada',
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[paciente_email],
                )
                email.content_subtype = "html"  # Importante para enviar como HTML

                # Adjuntar logo embebido
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as f:
                        logo_data = f.read()
                        image = MIMEImage(logo_data)
                        image.add_header("Content-ID", "<logo_image>")  # Debe coincidir con cid en el HTML
                        email.attach(image)

                email.send(fail_silently=False)

            except Exception as e:
                messages.warning(request, f'No se pudo enviar el correo: {e}')

            return redirect('crear_cita')  # Redirige a la misma página para limpiar el formulario
    else:
        form = CitaForm()

    return render(request, 'medical/Formulariocitas.html', {'form': form})
