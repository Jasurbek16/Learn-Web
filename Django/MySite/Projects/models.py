import uuid
from django.db import models


# Table for individual projects
class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    # owner =
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contributors = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    source_code = models.URLField(null=True, blank=True)
    # featured_image =
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)


# Table for all projects
class Projects(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
