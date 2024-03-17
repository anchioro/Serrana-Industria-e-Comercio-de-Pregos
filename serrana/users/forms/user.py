from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "is_active", "is_staff"]
        widgets = {
            "password": forms.PasswordInput()
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        
        if self.instance and not self.instance._state.adding:
            self.fields["password"].required = False
            if "password" in self.data and self.data["password"] and not self.data["confirm_password"]:
                self.fields["confirm_password"].required = True
            else:
                self.fields["confirm_password"].required = False
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user
    
    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        
        if first_name == last_name:
            self.add_error("first_name", ValidationError("O primeiro nome não pode ser igual ao último nome."))
            self.add_error("last_name", ValidationError("O último nome não pode ser igual ao primeiro nome."))
        
        username = self.cleaned_data.get("username")
        
        try:
            validate_email(username)
        except ValidationError:
            self.add_error("username", ValidationError("O usuário deve conter um endereço de e-mail válido."))
        
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        
        if password and password != confirm_password:
            self.add_error("password", ValidationError("As senhas não coincidem."))
            self.add_error("confirm_password", ValidationError("As senhas não coincidem."))
        
        
        return super().clean()