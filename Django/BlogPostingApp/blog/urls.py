from django.urls import path
from .views import (PostListView, 
                    PostDetailView, 
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView)
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    #            ^ converting into an actual view
    # the view to handle the ^ logic at as 2nd arg
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #        ^ that would be grabbed from the URL
    # ^ creating a route with a var |   pk -> prim key of the post
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    # ^ uses the same template as PostCreateView named post_form.html
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]






