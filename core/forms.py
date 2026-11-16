from django import forms


class BootstrapMixin:
    """Le pone la clase de Bootstrap correcta a cada campo, sin escribirla uno por uno."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                clase = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = 'form-select'
            else:
                clase = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {clase}".strip()
