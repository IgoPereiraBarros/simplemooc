from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from simplemooc.accounts import views
from django.conf import settings

app_name = 'accounts'

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('sair/', LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),
	path('cadastre-se/', views.register, name='register'),
	path('nova-senha/', views.password_reset, name='password_reset'),
	path('confirmar-nova-senha/<str:key>/', views.password_reset_confirm, name='password_reset_confirm'),
	path('editar/', views.edit, name='edit'),
	path('editar-senha/', views.edit_password, name='edit_password')
]
