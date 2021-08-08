from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Subjects(models.Model):
    # A subject the user wants to share info about
    name = models.CharField(max_length=100)
    professor = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "subjects"

    def __str__(self):
        return f"{self.name}"


class Info(models.Model):
    # Additional info and the main content
    subject = models.ForeignKey(Subjects, on_delete=CASCADE)
    topic = models.CharField(max_length=50)
    text = models.TextField()
    date_shared = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)

    class Meta:
        verbose_name_plural = "info"

    def __str__(self):
        if len(self.topic) > 25:
            return f"{self.topic[:25]}..."
        else:
            return f"{self.topic}"
