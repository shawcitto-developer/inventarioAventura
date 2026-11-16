from django.contrib import admin

from .models import Categoria, Experiencia, Inscripcion

admin.site.register(Categoria)
admin.site.register(Inscripcion)


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio', 'cupo_maximo', 'fecha_hora', 'creador', 'activa')
