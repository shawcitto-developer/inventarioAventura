from django import forms

from core.forms import BootstrapMixin
from .models import Categoria, Experiencia


class CategoriaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class ExperienciaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'precio', 'cupo_maximo', 'fecha_hora', 'categoria', 'activa']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M']        # formato del calendario del navegador
        self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)  # solo categorías activas
