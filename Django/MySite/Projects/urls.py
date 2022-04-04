from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name="allProjects"),
    path('projects/<str:pk>/', views.project, name="singleProject"),
]
