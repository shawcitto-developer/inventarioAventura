from django.urls import path

from . import views

urlpatterns = [
    # Categorías
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/nueva/', views.categoria_form, name='categoria_form'),
    path('categorias/<int:id>/editar/', views.categoria_form, name='categoria_editar'),
    path('categorias/<int:id>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    # Experiencias
    path('', views.experiencia_lista, name='experiencia_lista'),
    path('nueva/', views.experiencia_form, name='experiencia_form'),
    path('<int:id>/editar/', views.experiencia_form, name='experiencia_editar'),
    path('<int:id>/eliminar/', views.experiencia_eliminar, name='experiencia_eliminar'),
    # Reservas (admin)
    path('reservas/', views.reserva_lista, name='reserva_lista'),
    path('reservas/<int:id>/confirmar/', views.reserva_confirmar, name='reserva_confirmar'),
    # Turista
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:id>/inscribir/', views.inscribir, name='inscribir'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('mis-reservas/<int:id>/cancelar/', views.reserva_cancelar, name='reserva_cancelar'),
]
