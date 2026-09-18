from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('projects/new/', views.project_form, name='project_new'),
    path('projects/<int:pk>/', views.project_detail, name='project'),
    path('projects/<int:pk>/edit/', views.project_form, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
