from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from apps.medical.models.usuario import Usuario
from apps.audit.models import AuditLog
from django.utils import timezone


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validación de campos vacíos
        if not username or not password:
            error_message = "Usuario y contraseña son requeridos"
        else:
            try:
                usuario = Usuario.objects.get(usuario__iexact=username)
                
                if check_password(password, usuario.clave):
                    # ✅ LOGIN EXITOSO
                    request.session['user_id'] = usuario.id
                    request.session['username'] = usuario.usuario
                    request.session['rol'] = usuario.rol
                    
                    # Registrar en AuditLog SOLO si login es exitoso
                    AuditLog.objects.create(
                        usuario=None,  # ← Usar None temporalmente
                        accion='login',
                        detalles=f"Inicio de sesión exitoso para el usuario '{usuario.usuario}'"
                    )
                    return redirect('home')
                else:
                    # ❌ CONTRASEÑA INCORRECTA
                    error_message = "Usuario o contraseña incorrectos"
                    
            except Usuario.DoesNotExist:
                # ❌ USUARIO NO EXISTE
                error_message = "Usuario o contraseña incorrectos"

    return render(request, 'medical/login.html', {'error': error_message})


def logout_view(request):
    # Registrar logout si hay usuario en sesión
    if 'user_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['user_id'])
            AuditLog.objects.create(
                usuario=None,  # ← Usar None temporalmente
                accion='logout', 
                detalles=f"Cierre de sesión para el usuario '{usuario.usuario}'"
            )
        except Usuario.DoesNotExist:
            pass
    
    request.session.flush()  
    return redirect('login')