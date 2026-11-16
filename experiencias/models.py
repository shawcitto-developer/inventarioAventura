from django.conf import settings
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='experiencias')
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='experiencias_creadas')
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['fecha_hora']

    def __str__(self):
        return self.titulo


class Inscripcion(models.Model):
    PENDIENTE = 'pendiente'
    CONFIRMADO = 'confirmado'
    ESTADOS = [(PENDIENTE, 'Pendiente'), (CONFIRMADO, 'Confirmado')]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscripciones')
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=12, choices=ESTADOS, default=PENDIENTE)

    class Meta:
        ordering = ['-fecha_inscripcion']
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'experiencia'], name='una_inscripcion_por_usuario'),
        ]

    def __str__(self):
        return f'{self.usuario.username} → {self.experiencia.titulo}'
