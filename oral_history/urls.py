from django.urls import path
from . import views

urlpatterns = [
    path('projects/new', views.projects_new, name='projects_new'),
    path('projects/table', views.projects_table, name='projects_table'),
]
