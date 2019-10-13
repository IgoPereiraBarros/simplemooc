from django.urls import path

from simplemooc.forum import views

app_name = 'forum'

urlpatterns = [
	path('', views.index, name='index'),
	path('tags/<str:tag>/', views.index, name='index_tagged'),
	path('<str:slug>/', views.thread, name='thread'),
	path('repostas/<int:pk>/correta/', views.reply_correct, name='reply_correct'),
	path('repostas/<int:pk>/incorreta/', views.reply_incorrect, name='reply_incorrect'),
]