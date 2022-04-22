from django.urls import path
from . import views

urlpatterns = [
    path('projects/new', views.projects_new, name='projects_new'),
    path('table', views.projects_table, name='projects_table'),
    path('upload_file', views.upload_file, name='upload_file'),
]
