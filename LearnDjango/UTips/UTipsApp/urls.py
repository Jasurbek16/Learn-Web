"""Defines URL patterns for UniTipsApp"""
from django.urls import path
from .views import SubjectListView, TopicEditView
from . import views

urlpatterns = [
    # Home Page
    path("", SubjectListView.as_view(), name="Ut-home"),
    path("about/", views.about, name="Ut-about"),
    path("subjects/<int:pk>/", views.subject_details, name="subject-details"),
    path("topics/<int:pk>/", views.topic_details, name="topic-details"),
    path("topics/<int:pk>/edit/", TopicEditView.as_view(), name="edit-topic"),
    path("subjects/new/", views.addSubject, name="add-subject"),
    path("topics/new/", views.addTopic, name="add-topic"),
]
