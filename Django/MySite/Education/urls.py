from django.urls import path
from . import views

urlpatterns = [
    path("education/", views.education, name="educationInfo"),
]
