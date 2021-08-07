# A model tells Django how to work with the data
# that will be stored in the app

from django.db import models

class Topic(models.Model):
    # A topic the user is learning about
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    # Something specific learned about a topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # holds extra info for managing the model
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text[:50]
