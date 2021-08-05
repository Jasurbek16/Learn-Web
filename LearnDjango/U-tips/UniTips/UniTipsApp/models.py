from django.db import models
from datetime import datetime

class Subjects(models.Model):
    # A subject the user wants to share info about
    subj_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.now)
    # Additional info and the main content
    on_topic = models.CharField(max_length = 50, default='General')
    subj_content = models.TextField(default=None)
    subj_prof = models.CharField(max_length = 50, default=None)

    class Meta:
        verbose_name_plural = 'subjects'

    def __str__(self):
        return f'-> ({self.subj_name})'
