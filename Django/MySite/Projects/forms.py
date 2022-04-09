from pyexpat import model
from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['date_started', 'id', 'vote_total', 'vote_ratio']
