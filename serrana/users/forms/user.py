from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email", "is_active", "is_staff"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        self.by_admin = kwargs.pop("by_admin", False)
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

        if self.instance and not self.instance._state.adding:
            self.fields["password"].required = False
            if "password" in self.data and self.data["password"] and not self.data["confirm_password"]:
                self.fields["confirm_password"].required = True
            else:
                self.fields["confirm_password"].required = False

    def save(self, commit=True, by_admin=False):
        user = super().save(commit=False)
        
        new_password = self.cleaned_data.get("password")
        
        if not self.instance._state.adding:
            old_password_from_db = User.objects.get(pk=user.pk).password
            if check_password(new_password, old_password_from_db) or not new_password:
                user.password = old_password_from_db
            else:
                user.set_password(new_password)
        else:
            user.set_password(new_password)
        
        if self.by_admin:
            user.is_active = self.cleaned_data.get("is_active")
            user.is_staff = self.cleaned_data.get("is_staff")
        else:
            if not self.instance._state.adding:
                old_user = User.objects.get(pk=user.pk)
                user.is_active = old_user.is_active
                user.is_staff = old_user.is_staff
            
        if commit:
            user.save()

        return user