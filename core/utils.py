from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string


def respuesta_modal(request, form, titulo, al_guardar=None):
    """
    Motor de todos los modales de crear/editar.
    - GET  -> devuelve solo el HTML del formulario (se pega dentro del modal).
    - POST válido -> guarda y responde JSON {ok: true}; el JS recarga la tabla.
    - POST inválido -> devuelve el formulario con errores (status 400) y el modal sigue abierto.
    """
    if request.method == 'POST' and form.is_valid():
        al_guardar(form) if al_guardar else form.save()
        messages.success(request, 'Guardado correctamente')
        return JsonResponse({'ok': True})
    html = render_to_string('includes/modal_form.html', {'form': form, 'titulo': titulo}, request=request)
    return HttpResponse(html, status=400 if request.method == 'POST' else 200)


def eliminar_modal(request, objeto, mensaje='Registro eliminado'):
    """GET -> modal de confirmación. POST -> elimina (y avisa si tiene datos asociados)."""
    if request.method == 'POST':
        try:
            objeto.delete()
            messages.success(request, mensaje)
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: tiene registros asociados.')
        return JsonResponse({'ok': True})
    html = render_to_string('includes/modal_eliminar.html', {'objeto': objeto}, request=request)
    return HttpResponse(html)

#Respuesta modal con GET devuelve el formulario, html parcial, con post válido guarda y responda JSON
#Con post invalido devuelve el formulario con errores y status 400, el modal sigue abierto - estatus 400.

#Eliminar modal con get devuelve el modal de confirmación, ¿"seguro que quieres eliminar?"
#  y con post elimina y si el registro está proteguido por ej una categoria con experiencias , captura ProtectError y avisa
#antes de caerse, o eso espero.

