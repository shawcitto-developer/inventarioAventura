from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.forms import BootstrapMixin
from .models import Perfil


class RegistroForm(BootstrapMixin, UserCreationForm):
    """Autoregistro público: el que se registra por aquí siempre queda como Turista."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class UsuarioForm(BootstrapMixin, forms.ModelForm):
    """Formulario del Administrador para crear/editar usuarios y asignarles rol."""
    rol = forms.ChoiceField(choices=Perfil.ROLES)
    password = forms.CharField(
        label='Contraseña', required=False, widget=forms.PasswordInput(render_value=False),
        help_text='Al editar, déjala vacía para no cambiarla.',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        labels = {'is_active': 'Cuenta activa'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['rol'].initial = self.instance.perfil.rol
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if self.cleaned_data['password']:
            usuario.set_password(self.cleaned_data['password'])
        usuario.save()
        perfil, _ = Perfil.objects.get_or_create(usuario=usuario)
        perfil.rol = self.cleaned_data['rol']
        perfil.save()
        return usuario


#Aca hay un par de cosas que hace falta explicar
#Type : date-time-local hace que eln avegador muestre un calendario con hora
#es de los que se ve mejor en el telefono, por eso se define format e input formats

#Ademas de categoria.objects.filter(activo=True) para que solo se muestren las categorias activas, si no se hace esto, 
# el admin puede crear experiencias con categorias inactivas, lo cual no tiene sentido.

#Finalmente en el campo usuarioForm, la contraseña es obligatoria al crear y opcional al editar
#(vacía significa “no la cambies”). set_password guarda la contraseña encriptada.

#pd: RegistroForm es el autoregistro público, y siempre produce turista : nadie puede "registrarse" como admin.


