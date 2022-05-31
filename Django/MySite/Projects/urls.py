from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.projects, name="allProjects"),
    path("projects/<str:pk>/", views.project, name="singleProject"),
    path("create-project/", views.createProject, name="create-project"),
    path("update-project/<str:pk>/", views.updateProject, name="update-project"),
    path("delete-project/<str:pk>/", views.deleteProject, name="delete-project"),
]
