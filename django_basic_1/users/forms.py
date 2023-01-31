# users/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from .models import User
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "complete_name",
            "username",
            "email",
            "cpf",
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

class AlterPassword(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class AlterPasswordUserAdminForm(forms.ModelForm):
    """
    A form used to change the password of a user in the admin interface.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    required_css_class = "required"
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "autofocus": True}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        print("objeto...", kwargs)
        self.user = kwargs['instance']
        super(AlterPasswordUserAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = []
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self)
        return password2

    """
    def save(self, commit=True):
        "Save the new password."
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        self.user.especial_password = encrypt(password)
        if commit:
            self.user.save()
        return self.user
    #"""

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ["password"]
    
