from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from .forms import CustomUserChangeForm, CustomUserCreationForm, AlterPasswordUserAdminForm
from .models import User
from main.encryption_tool import encrypt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    #add_form = UserCreationForm
    #form = UserChangeForm
    #add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        #(None, {'fields': ('email', 'password', )}),
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('complete_name', 'cpf', 'date_of_born', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    #"""
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'password1', 'password2'),
            }),
        )
    #"""
        
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ('username', 'complete_name', 'email', 'first_name', 'last_name')
    ordering = ('username', )

    

