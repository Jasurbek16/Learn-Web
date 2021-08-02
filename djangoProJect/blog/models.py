from django.db import models
from django.utils import timezone
# ^ takes the current timezone settings into consideration
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100) 
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ^ if the user is deleted, then delete the posts related as well
    
    def __str__(self):
        return self.title 
