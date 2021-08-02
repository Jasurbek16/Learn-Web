from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    # the view to handle the logic at as 2nd arg
    path('about/', views.about, name='blog-about'),
]