from django import forms
from django.contrib.auth.hashers import make_password
from apps.medical.models.usuario import Usuario

class UsuarioForm(forms.ModelForm):
    # Campo NO mapeado al modelo; así no pisa la clave existente en edición
    clave = forms.CharField(
        label="Clave",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingrese contraseña"}),
        required=False,
    )

    class Meta:
        model = Usuario
        fields = ["usuario", "rol"]
        widgets = {
            "usuario": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese nombre de usuario"}),
            "rol": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "usuario": "Usuario",
            "rol": "Rol",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # creación: clave obligatoria; edición: opcional
        self.is_create = not bool(self.instance and self.instance.pk)
        self.fields["clave"].required = self.is_create

    def clean_usuario(self):
        u = self.cleaned_data["usuario"].strip()
        qs = Usuario.objects.filter(usuario__iexact=u)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # permitir el mismo usuario del registro actual
        if qs.exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")
        return u

    def clean(self):
        data = super().clean()
        # reglas mínimas de clave si se envía
        clave = data.get("clave") or ""
        if clave and len(clave) < 6:
            self.add_error("clave", "La clave debe tener al menos 6 caracteres.")
        if self.is_create and not clave:
            self.add_error("clave", "La clave es obligatoria.")
        return data

    def save(self, commit=True):
        """
        - CREAR: siempre hashea y guarda la clave.
        - EDITAR: solo cambia la clave si el usuario ingresó una nueva; si no, conserva la anterior.
        """
        obj = super().save(commit=False)
        clave_nueva = self.cleaned_data.get("clave")

        if clave_nueva:
            obj.clave = make_password(clave_nueva)
        # si no hay clave nueva y es edición -> no tocar obj.clave (se mantiene)

        if commit:
            obj.save()
        return obj