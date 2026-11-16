from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from cuentas.utils import rol_de
from experiencias.models import Experiencia, Inscripcion
from experiencias.views import publicas


def landing(request):
    """Página pública de bienvenida (no pide sesión)."""
    return render(request, 'core/landing.html', {'destacadas': publicas()[:6]})


@login_required
def panel(request):
    rol = rol_de(request.user)
    if rol == 'admin':
        datos = {
            'usuarios': User.objects.count(),
            'experiencias': Experiencia.objects.count(),
            'reservas': Inscripcion.objects.count(),
            'pendientes': Inscripcion.objects.filter(estado_pago='pendiente').count(),
        }
    elif rol == 'guia':
        datos = {
            'experiencias': Experiencia.objects.filter(creador=request.user).count(),
            'inscritos': Inscripcion.objects.filter(experiencia__creador=request.user).count(),
        }
    else:
        datos = {
            'reservas': Inscripcion.objects.filter(usuario=request.user).count(),
            'disponibles': publicas().count(),
        }
    return render(request, 'core/panel.html', {'datos': datos})

#La landing (/) es pública y no pide sesión. 
#El panel muestra números distintos según el rol, usando .count() como en la guía universal.

