from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from taggit.managers import TaggableManager

class Thread(models.Model):

	title = models.CharField(_('título'), max_length=100)
	slug = models.SlugField(_('identificador'), max_length=100)
	body = models.TextField(_('mensagem'))
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		verbose_name=_('autor'), related_name='threads'
	)
	views = models.IntegerField(_('visualização'), blank=True, default=0)
	answers = models.IntegerField(_('respostas'), blank=True, default=0)

	created = models.DateTimeField(_('criado em'), auto_now_add=True)
	modified = models.DateTimeField(_('modificado em'), auto_now=True)

	tags = TaggableManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('forum:thread', args=[str(self.slug)])

	class Meta:

		verbose_name = _('tópico')
		verbose_name_plural = _('tópicos')
		ordering = ['-modified']

class Reply(models.Model):

	thread = models.ForeignKey(
		Thread, on_delete=models.CASCADE, verbose_name=_('tópicos'),
		related_name='replies'
	)
	reply = models.TextField(_('resposta'))
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		verbose_name=_('autor'), related_name='replies'
	)
	correct = models.BooleanField(_('correta?'), blank=True, default=False)

	created = models.DateTimeField(_('criado em'), auto_now_add=True)
	modified = models.DateTimeField(_('modificado em'), auto_now=True)

	def __str__(self):
		return self.reply[:100]

	class Meta:

		verbose_name = _('resposta')
		verbose_name_plural = _('respostas')
		ordering = ['-correct', 'created']

def post_save_reply(created, instance, **kwargs):
	instance.thread.answers = instance.thread.replies.count()
	instance.thread.save()
	if instance.correct:
		instance.thread.replies.exclude(pk=instance.pk).update(
			correct=False
		)

def post_delete_reply(instance, **kwargs):
	instance.thread.answers = instance.thread.replies.count()
	instance.thread.save()

models.signals.post_save.connect(
	post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
	post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)