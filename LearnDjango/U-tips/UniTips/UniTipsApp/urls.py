'''Defines URL patterns for UniTipsApp'''
from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='Ut-home'),
    path('about/', views.about, name = 'Ut-about'),
    path('subjects/', views.subjects, name='Ut-subjects'),
]