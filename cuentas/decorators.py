from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .utils import rol_de


def rol_requerido(*roles):
    """Uso: @rol_requerido('admin', 'guia'). Sin sesión -> login. Con rol incorrecto -> 403."""
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if rol_de(request.user) not in roles:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return login_required(envoltura)
    return decorador
