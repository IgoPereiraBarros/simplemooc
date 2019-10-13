from django.urls import path, re_path
from simplemooc.courses import views

app_name = 'courses'

urlpatterns = [
	path('', views.courses_index, name='index'),
	path('<str:slug>/', views.details, name='details'),
	path('<str:slug>/inscricao/', views.enrollment, name='enrollment'),
	path('<str:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'),
	path('<str:slug>/anuncios/', views.announcements, name='announcements'),
	re_path(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.show_announcement,
            name='show_announcement'),
	path('<str:slug>/aulas/', views.lessons, name='lessons'),
	re_path(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', views.lesson,
            name='lesson'),
	re_path(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$', views.material,
            name='material'),
]