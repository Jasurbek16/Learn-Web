from django.db import models
from django.utils import timezone
# ^ takes the current timezone settings into consideration
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100) 
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ^ if the user is deleted, then delete the posts related as well
    
    def __str__(self):
        return self.title 

    # redirect will actually redirect you to a specific 
    # route but reverse will simply return the full 
    # URL to that route as a string and let the view 
    # handle the redirect for us

    # tell Django how to find the URL to any specific instance of a post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk':self.pk})
        # it needs a specific post    ^ 
        # with a primary key