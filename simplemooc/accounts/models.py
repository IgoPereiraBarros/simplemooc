import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(
		_('nome do usuário'), max_length=30, unique=True,
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			'O nome de usuário só pode conter letras, dígitos ou os caracteres: @/./+/-/_',
			'invalied')]
	)
	email = models.EmailField(_('e-mail'), unique=True)
	first_name = models.CharField(_('primeiro nome'), max_length=100, blank=True)
	last_name = models.CharField(_('sobrenome'), max_length=100, blank=True)
	is_active = models.BooleanField(_('está ativo?'), blank=True, default=True)
	is_staff = models.BooleanField(_('é da equipe?'), blank=True, default=False)
	date_joined = models.DateTimeField(_('data de entrada'), auto_now_add=True)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username or self.first_name

	def get_short_name(self):
		return self.first_name

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	class Meta:

		verbose_name = _('Usuário')
		verbose_name_plural = _('Usuários')


class PasswordReset(models.Model):

	user = models.ForeignKey(
		   settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('usuario'), 
		   related_name='resets'
	)
	key = models.CharField(_('chave'), max_length=100, unique=True)
	created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
	confirmed = models.BooleanField(_('confirmado?'), default=False, blank=True)

	def __str__(self):
		return '{} em {}'.format(self.user, self.created_at)

	class Meta:

		verbose_name = _('Nova Senha')
		verbose_name_plural = _('Novas Senhas')
		ordering = ['-created_at']

