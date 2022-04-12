from django.urls import path
from . import views

urlpatterns = [
    path('projects/new', views.projects_new, name='projects_new'),
    path('upload_test', views.upload_test, name='upload_test'),
]