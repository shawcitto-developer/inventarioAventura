from django.contrib import messages
from django.db.models import Count, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.utils import eliminar_modal, respuesta_modal
from cuentas.decorators import rol_requerido
from cuentas.utils import rol_de
from .forms import CategoriaForm, ExperienciaForm
from .models import Categoria, Experiencia, Inscripcion


# ---------- Helpers ----------
def visibles(user):
    """Admin ve todas las experiencias; el Guía solo las que él creó."""
    qs = Experiencia.objects.select_related('categoria', 'creador')
    return qs if rol_de(user) == 'admin' else qs.filter(creador=user)


def con_cupos(qs):
    """Agrega 'inscritos' y 'disponibles' a cada experiencia."""
    return qs.annotate(inscritos=Count('inscripciones')).annotate(disponibles=F('cupo_maximo') - F('inscritos'))


def publicas():
    """Experiencias que un turista puede ver: activas, con categoría activa y futuras."""
    return Experiencia.objects.filter(
        activa=True, categoria__activo=True, fecha_hora__gte=timezone.now()
    ).select_related('categoria')


# ---------- Categorías (solo Administrador) ----------
@rol_requerido('admin')
def categoria_lista(request):
    return render(request, 'experiencias/categoria_lista.html', {'categorias': Categoria.objects.all()})


@rol_requerido('admin')
def categoria_form(request, id=None):
    categoria = get_object_or_404(Categoria, id=id) if id else None
    form = CategoriaForm(request.POST or None, instance=categoria)
    return respuesta_modal(request, form, 'Editar categoría' if id else 'Nueva categoría')


@rol_requerido('admin')
def categoria_eliminar(request, id):
    return eliminar_modal(request, get_object_or_404(Categoria, id=id), 'Categoría eliminada')


# ---------- Experiencias (Administrador y Guía) ----------
@rol_requerido('admin', 'guia')
def experiencia_lista(request):
    experiencias = con_cupos(visibles(request.user))
    return render(request, 'experiencias/experiencia_lista.html', {'experiencias': experiencias})


@rol_requerido('admin', 'guia')
def experiencia_form(request, id=None):
    # Si el Guía intenta editar una experiencia ajena, visibles() no la incluye y da 404.
    experiencia = get_object_or_404(visibles(request.user), id=id) if id else None
    form = ExperienciaForm(request.POST or None, instance=experiencia)

    def guardar(f):
        obj = f.save(commit=False)
        if not obj.pk:
            obj.creador = request.user   # el creador es quien tiene la sesión iniciada
        obj.save()

    return respuesta_modal(request, form, 'Editar experiencia' if id else 'Nueva experiencia', guardar)


@rol_requerido('admin')   # el Guía NO puede eliminar
def experiencia_eliminar(request, id):
    return eliminar_modal(request, get_object_or_404(Experiencia, id=id), 'Experiencia eliminada')


# ---------- Reservas (Administrador) ----------
@rol_requerido('admin')
def reserva_lista(request):
    reservas = Inscripcion.objects.select_related('usuario', 'experiencia')
    return render(request, 'experiencias/reserva_lista.html', {'reservas': reservas})


@rol_requerido('admin')
@require_POST
def reserva_confirmar(request, id):
    reserva = get_object_or_404(Inscripcion, id=id)
    reserva.estado_pago = Inscripcion.CONFIRMADO
    reserva.save()
    messages.success(request, f'Pago de {reserva.usuario.username} confirmado')
    return JsonResponse({'ok': True})


# ---------- Turista ----------
@rol_requerido('turista')
def catalogo(request):
    experiencias = con_cupos(publicas())
    inscritas = set(Inscripcion.objects.filter(usuario=request.user).values_list('experiencia_id', flat=True))
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'experiencias/catalogo.html', {
        'experiencias': experiencias, 'inscritas': inscritas, 'categorias': categorias,
    })


@rol_requerido('turista')
@require_POST
def inscribir(request, id):
    experiencia = get_object_or_404(con_cupos(publicas()), id=id)
    if experiencia.disponibles <= 0:
        messages.error(request, 'Esta experiencia ya no tiene cupos.')
    else:
        _, creada = Inscripcion.objects.get_or_create(usuario=request.user, experiencia=experiencia)
        if creada:
            messages.success(request, f'¡Listo! Quedaste inscrito en {experiencia.titulo}.')
        else:
            messages.info(request, 'Ya estabas inscrito en esta experiencia.')
    return JsonResponse({'ok': True})


@rol_requerido('turista')
def mis_reservas(request):
    reservas = Inscripcion.objects.filter(usuario=request.user).select_related('experiencia__categoria')
    return render(request, 'experiencias/mis_reservas.html', {'reservas': reservas})


@rol_requerido('turista')
def reserva_cancelar(request, id):
    # Solo sus propias reservas y solo si aún están pendientes de pago.
    reserva = get_object_or_404(Inscripcion, id=id, usuario=request.user, estado_pago=Inscripcion.PENDIENTE)
    return eliminar_modal(request, reserva, 'Reserva cancelada')

#visibles(user) es la restricción por queryset del enunciado: 
# el administrador ve todas las experiencias, el guía solo filter(creador=user). 
#Como la edición también usa visibles, si un guía escribe a mano el id de una experiencia ajena obtiene 404
#No un error de permisos ni un acceso indebido.
#con_cupos calcula inscritos y disponibles en la misma consulta con annotate. 
#Así el catálogo muestra los cupos sin hacer una consulta por tarjeta.
#publicas() define qué ve un turista: experiencias activas, de categoría activa y con fecha futura.
#@require_POST en inscribir y reserva_confirmar impide ejecutarlas escribiendo la dirección en el navegador: 
#solo funcionan con el botón.
#reserva_cancelar filtra por usuario=request.user y por estado pendiente: 
#un turista solo cancela sus propias reservas no pagadas.
#creador = request.user se asigna en la vista, no en el formulario: 
#así nadie puede crear una experiencia “a nombre de otro”.
