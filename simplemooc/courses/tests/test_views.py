from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.core import mail

from django.conf import settings

from simplemooc.courses.models import Course



class HomeViewTest(TestCase):

	def test_home(self):
		client = Client()
		response = client.get(reverse('core:home'))
		self.assertEqual(response.status_code, 200)

	def test_home_template_used(self):
		client = Client()
		response = client.get(reverse('core:home'))
		self.assertTemplateUsed(response, 'home.html')

class ContactCourseTestCase(TestCase):

	def setUp(self):
		self.course = Course.objects.create(name='Django', slug='django')
	def tearDown(self):
		self.course.delete()

	def test_contact_form_error(self):
		data = {'name': 'Igo', 'email': '', 'message': ''}
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
		self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

	def test_contact_form_success(self):
		data = {'name': 'Igo Pereira Barros', 'email': 'igorestacioceut@gmail.com', 'message': 'bla'}
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])

