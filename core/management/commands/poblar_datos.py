from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from cuentas.models import Perfil
from experiencias.models import Categoria, Experiencia, Inscripcion

CLAVE = 'Aventura2026!'


class Command(BaseCommand):
    help = 'Crea los usuarios, categorías, experiencias y reservas de prueba de la EV3'

    def usuario(self, username, rol, nombre, apellido, admin=False):
        u, creado = User.objects.get_or_create(username=username, defaults={
            'first_name': nombre, 'last_name': apellido,
            'email': f'{username}@aventurasdelsur.cl',
            'is_staff': admin, 'is_superuser': admin,
        })
        if creado:
            u.set_password(CLAVE)
            u.save()
        u.perfil.rol = rol
        u.perfil.save()
        return u

    def handle(self, *args, **opciones):
        admin = self.usuario('admin_parque', Perfil.ADMIN, 'Camila', 'Rojas', admin=True)
        guia1 = self.usuario('guia_pedro', Perfil.GUIA, 'Pedro', 'Soto')
        guia2 = self.usuario('guia_ana', Perfil.GUIA, 'Ana', 'Muñoz')
        tur1 = self.usuario('turista_luis', Perfil.TURISTA, 'Luis', 'Vera')
        tur2 = self.usuario('turista_sofia', Perfil.TURISTA, 'Sofía', 'Pino')

        cat = {n: Categoria.objects.get_or_create(nombre=n, defaults={'descripcion': d})[0] for n, d in [
            ('Trekking', 'Caminatas guiadas por senderos del parque'),
            ('Canopy', 'Circuito de tirolesas entre los árboles'),
            ('Kayak', 'Navegación por el lago y el río'),
            ('Arriendo de equipos', 'Arriendo de equipo outdoor por día'),
        ]}

        ahora = timezone.now().replace(minute=0, second=0, microsecond=0)
        catalogo = [
            (guia1, 'Trekking Sendero Cóndor', 'Caminata de 6 horas con vista a la cordillera.', 25000, 12, 3, 'Trekking'),
            (guia1, 'Trekking Bosque Nativo', 'Recorrido corto entre lengas y coihues.', 15000, 15, 5, 'Trekking'),
            (guia1, 'Canopy Aventura', 'Doce tirolesas sobre el bosque.', 32000, 10, 7, 'Canopy'),
            (guia1, 'Canopy Nocturno', 'Tirolesas con linternas al atardecer.', 38000, 8, 10, 'Canopy'),
            (guia2, 'Kayak Lago Azul', 'Remada tranquila de 2 horas.', 20000, 14, 4, 'Kayak'),
            (guia2, 'Kayak Río Rápido', 'Descenso con nivel intermedio.', 28000, 8, 8, 'Kayak'),
            (guia2, 'Arriendo Equipo Camping', 'Carpa, saco y cocinilla por día.', 18000, 20, 2, 'Arriendo de equipos'),
            (guia2, 'Arriendo Bicicleta de Montaña', 'Bicicleta con casco por día.', 12000, 15, 6, 'Arriendo de equipos'),
        ]
        exps = []
        for creador, titulo, desc, precio, cupo, dias, c in catalogo:
            e, _ = Experiencia.objects.get_or_create(titulo=titulo, defaults={
                'descripcion': desc, 'precio': precio, 'cupo_maximo': cupo,
                'fecha_hora': ahora + timedelta(days=dias), 'categoria': cat[c], 'creador': creador,
            })
            exps.append(e)

        for turista, indices in [(tur1, [0, 2, 4]), (tur2, [1, 3, 6])]:
            for n, i in enumerate(indices):
                Inscripcion.objects.get_or_create(usuario=turista, experiencia=exps[i], defaults={
                    'estado_pago': Inscripcion.CONFIRMADO if n == 0 else Inscripcion.PENDIENTE,
                })

        self.stdout.write(self.style.SUCCESS(f'Listo. Contraseña de todos los usuarios de prueba: {CLAVE}'))

