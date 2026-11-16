from django.conf import settings
from django.db import models


class Perfil(models.Model):
    ADMIN = 'admin'
    GUIA = 'guia'
    TURISTA = 'turista'
    ROLES = [
        (ADMIN, 'Administrador'),
        (GUIA, 'Guía / Operador'),
        (TURISTA, 'Turista'),
    ]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROLES, default=TURISTA)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'
