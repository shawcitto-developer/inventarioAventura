from cuentas.utils import rol_de


def rol(request):
    return {'rol': rol_de(request.user)}


#@rol_requerido('admin', 'guia') encima de una vista significa: “solo entran estos roles”. 
#Si no hay sesión, manda al login (es el login_required de siempre, por dentro). 
#Si hay sesión pero el rol no corresponde, responde 403 y se muestra la página amable 403.html.

#rol_de() trata a todo superusuario como administrador, y a quien no tenga perfil como turista. 
# Es una red de seguridad, no debería pasar si usas la señal.

#El menú lateral y los botones también se ocultan según {{ rol }}, pero eso es solo cosmética
#La seguridad real está en el decorador y en el queryset de la vista: aunque alguien escriba la dirección a mano, no pasa.

