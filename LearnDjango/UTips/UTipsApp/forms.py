from django import forms
from .models import Subjects, Info


class AddSubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ["name", "professor"]
        label = {"subject": "", "professor": ""}


class AddTopicsForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ["subject", "topic", "text", "date_shared", "author"]
        label = {
            "subject": "",
            "topic": "",
            "text": "",
            "date_shared": "",
            "author": "",
        }
