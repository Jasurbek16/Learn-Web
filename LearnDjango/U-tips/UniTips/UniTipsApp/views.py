from django.shortcuts import render
from .models import Subjects


def home(request):
    # The home page
    return render(request, 'UniTipsApp/home.html')


def about(request):
    return render(request, 'UniTipsApp/about.html', {'title': 'About'})


def subjects(request):
    #Shows all subjects
    subjects = Subjects.objects.order_by('date_added')
    on_topics = Subjects.objects.order_by('date_added')
    context = {
        'subjects': subjects,
        'topics':on_topics
    }
    return render(request, 'UniTipsApp/subjects.html', context)
