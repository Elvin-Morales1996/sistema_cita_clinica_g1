from django.shortcuts import render
from apps.medical.models.usuario import Usuario
from apps.core.services.auth_service import require_role
from django.core.paginator import Paginator

@require_role(['Administrador'])
def usuario(request):
    usuarios = Usuario.objects.all()

    # Paginación: 5 usuarios por página
    paginator = Paginator(usuarios, 5)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, 'medical/usuario.html', {'usuarios': usuarios})
