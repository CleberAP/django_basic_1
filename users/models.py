import re
#import uuid

from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from main.encryption_tool import decrypt, encrypt
 
# Classe manager deste model. Esta classe disponibiliza funções para criação e administração do usuário e superuser
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, complete_name, cpf, date_of_born, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        if not cpf:
            raise ValueError(_('The given cpf must be set'))
        email = self.normalize_email(email)
        complete_name_encrypted = encrypt(complete_name) if not complete_name is None else "Undefined Name"
        ##cpf = encrypt(cpf) if not cpf is None else cpf
        user = self.model(username=username, email=email, complete_name=complete_name_encrypted, cpf=cpf, date_of_born=date_of_born, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        if not complete_name is None:
            user.first_name = complete_name.split(" ")[0]
            user.last_name = complete_name.split(" ")[-1]
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, complete_name=None, cpf=None, date_of_born=None, **extra_fields):
        return self._create_user(username, email, password, complete_name, cpf, date_of_born, False, False, **extra_fields)

    def _create_superuser(self, username, email, password, complete_name, cpf, date_of_born, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        if not cpf:
            raise ValueError(_('The given cpf must be set'))
        email = self.normalize_email(email)
        complete_name_encrypted = encrypt(complete_name) if not complete_name is None else "Undefined Name"

        user = self.model(username=username, email=email, complete_name=complete_name_encrypted, cpf=cpf, date_of_born=date_of_born, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        if not complete_name is None:
            user.first_name = complete_name.split(" ")[0]
            user.last_name = complete_name.split(" ")[-1]
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_superuser(username, email, password, complete_name=None, cpf="superuser01", date_of_born=None, is_staff=True, is_superuser=True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):

    #uuid = models.UUIDField(_("User UUID"), editable=False, default=uuid.uuid4)
    email = models.EmailField(verbose_name='email Address', max_length=255, unique=True)
    complete_name = models.CharField(_('complete Name'), max_length=256)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    date_of_born = models.DateField(null=True, blank=True)
    
    # Diz se o usuário confirmou o email, ou seja, se é um usuário confiável
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))

    objects = UserManager()

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "auth_user"
        permissions = (
            ("ver_relatorio", "Pode ver tela de relatórios"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})

    #def save(self, *args, **kwargs):
    #    self.especial_password = self.


