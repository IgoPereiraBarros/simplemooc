from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.conf import settings

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) | \
			models.Q(description__icontains=query)
		)

class Course(models.Model):

	name = models.CharField('nome', max_length=100)
	slug = models.SlugField('atalho')
	description = models.TextField('descricao simples', blank=True)
	about = models.TextField('sobre o curso', blank=True)
	start_date = models.DateField(
		'data_inicio', null=True, blank=True
	)
	image = models.ImageField(
		upload_to='courses/images', verbose_name='imagem',
		null=True, blank=True
	)
	created_at = models.DateTimeField(
		'criado_em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'atualizado_em', auto_now=True
	)

	objects = CourseManager()

	def __str__(self):
		return self.name


	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('courses:details', args=[str(self.slug)]) # (namespace:nome do arquivo html,
															#  tupla vazia, discinário)

	def release_lessons(self):
		today = timezone.now().date()
		# verifica se o dia do release_date é maior ou igual ao dia atual
		return self.lessons.filter(release_date__lte=today)

	class Meta:

		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name'] # descrescente --> ['-name']

class Lesson(models.Model):

	name = models.CharField(_('nome'), max_length=100)
	description = models.TextField(_('descrição'), blank=True)
	number = models.IntegerField(_('número (ordem)'), blank=True, default=0)
	release_date = models.DateField(_('data de liberação'), blank=True, null=True)

	course = models.ForeignKey(
		Course, on_delete=models.CASCADE, verbose_name=_('curso'),
		related_name='lessons'
	)

	created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
	updated_at = models.DateTimeField(_('atualizado em'), auto_now_add=True)

	def __str__(self):
		return self.name

	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date <= today
		return False

	class Meta:
		verbose_name = _('aula')
		verbose_name_plural = _('aulas')
		ordering = ['number']

class Material(models.Model):

	name = models.CharField(_('name'), max_length=100)
	embedded = models.TextField(_('vídeo embedded'), blank=True)
	file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

	lesson = models.ForeignKey(
		Lesson, on_delete=models.CASCADE, verbose_name=_('aula'), 
		related_name='materials'
	)

	def is_embedded(self):
		return bool(self.embedded)

	def __str__(self):
		return self.name

	class Meta:

		verbose_name = _('material')
		verbose_name_plural = _('meteriais')

class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('usuário'),
		related_name='enrollments'
	)
	course = models.ForeignKey(
		Course, on_delete=models.CASCADE, verbose_name=_('curso'),
		related_name='enrollments'
	)
	status = models.IntegerField(
		_('situação'), choices=STATUS_CHOICES, default=0, blank=True
	)
	created_at = models.DateTimeField(_('criado em '), auto_now_add=True)
	updated_at = models.DateTimeField(_('atualizado em'), auto_now_add=True)

	def __str__(self):
		return self.created_at

	def active(self):
		self.status = 1
		self.save()

	def is_status(self):
		return self.status == 1

	class Meta:

		verbose_name = _('inscrição')
		verbose_name_plural = _('inscrições')
		unique_together = (('user', 'course'),)
		ordering = ['-created_at']

class Announcement(models.Model):

	course = models.ForeignKey(
		Course, on_delete=models.CASCADE, verbose_name=_('curso'),
		related_name='announcements'
	)
	title = models.CharField(_('título'), max_length=100)
	content = models.TextField(_('conteúdo'))

	created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
	updated_at = models.DateTimeField(_('atualizado em'), auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:

		verbose_name = _('Anúncio')
		verbose_name_plural = _('Anúncios')
		ordering = ['-created_at']

class Comment(models.Model):

	announcement = models.ForeignKey(
		Announcement, on_delete=models.CASCADE, verbose_name=_('anúncio'),
		related_name='comments'
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('usuário')
	)
	comment = models.TextField(_('comentário'))

	created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
	updated_at = models.DateTimeField(_('atualizado em'), auto_now_add=True)


	def __str__(self):
		return self.comment[:50] + '...'

	class Meta:
		verbose_name = _('comentário')
		verbose_name_plural = _('comentários')
		ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs):
	if created:
		subject = instance.title
		context = {
			'announcement': instance
		}
		template_name = 'courses/announcement_mail.html'
		enrollments = Enrollment.objects.filter(course=instance.course, status=1)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
	post_save_announcement, sender=Announcement, 
	dispatch_uid='post_save_announcement'
)