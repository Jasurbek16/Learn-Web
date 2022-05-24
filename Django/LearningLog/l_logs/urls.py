'''"""Defines URL patterns for l_logs'''
from django.conf.urls import url
from . import views

urlpatterns = [

    # Home page
    url(r'^$', views.log_home, name='l_log_home'),
]