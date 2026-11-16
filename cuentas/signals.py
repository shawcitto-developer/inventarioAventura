from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    """Cada vez que nace un User, nace su Perfil. El superusuario parte como Administrador."""
    if created:
        rol = Perfil.ADMIN if instance.is_superuser else Perfil.TURISTA
        Perfil.objects.create(usuario=instance, rol=rol)
