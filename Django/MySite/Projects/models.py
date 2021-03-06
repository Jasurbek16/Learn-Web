from email.policy import default
import uuid
from django.db import models

# TODO: Fix the timing issue with the reviews

# Table for individual projects
class Project(models.Model):
    author = models.CharField(max_length=100)
    contributors = models.CharField(max_length=100, null=True, blank=True)
    date_started = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    # owner =
    link = models.URLField(null=True, blank=True)
    source_code = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    title = models.CharField(max_length=150)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)

    @property
    def imageURL(self):
        """Returns the URL of the project image if exists.
        Otherwise, returns an empty string.
        """
        try:
            img_url = self.featured_image.url
        except:
            img_url = ""
        return img_url

    def __str__(self):
        return self.title


# Table for all projects
class Projects(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# Table for reviews


class Review(models.Model):

    VOTE_TYPE = (
        ("up", "up"),
        ("down", "down"),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.value


# Table for tags


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
