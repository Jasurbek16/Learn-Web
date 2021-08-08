"""Defines URL patterns for UniTipsApp"""
from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path("", views.home, name="Ut-home"),
    path("about/", views.about, name="Ut-about"),
    path("subjects/<int:pk>/", views.subject_details, name="subject-details"),
    path("topics/<int:pk>", views.topic_details, name="topic-details"),
    path("addSubject/", views.addSubject, name="add-subject"),
    path("addTopic/", views.addTopic, name="add-topic"),
]
