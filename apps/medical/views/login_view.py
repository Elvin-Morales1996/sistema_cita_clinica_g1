from django.shortcuts import render, redirect

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            return redirect('home')
        else:
            error_message = "Usuario o contraseña incorrectos"

    return render(request, 'medical/login.html', {'error': error_message})