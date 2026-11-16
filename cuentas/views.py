from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.utils import respuesta_modal
from .decorators import rol_requerido
from .forms import RegistroForm, UsuarioForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@rol_requerido('admin')
def usuario_lista(request):
    usuarios = User.objects.select_related('perfil').order_by('username')
    return render(request, 'cuentas/usuario_lista.html', {'usuarios': usuarios})


@rol_requerido('admin')
def usuario_form(request, id=None):
    usuario = get_object_or_404(User, id=id) if id else None
    form = UsuarioForm(request.POST or None, instance=usuario)
    return respuesta_modal(request, form, 'Editar usuario' if id else 'Nuevo usuario')
