from django.urls import path

from . import views

urlpatterns = [
    path('registro/', views.RegistroView.as_view(), name='signup'),
    path('usuarios/', views.usuario_lista, name='usuario_lista'),
    path('usuarios/nuevo/', views.usuario_form, name='usuario_form'),
    path('usuarios/<int:id>/editar/', views.usuario_form, name='usuario_editar'),
]
