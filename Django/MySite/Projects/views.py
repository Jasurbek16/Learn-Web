from django.shortcuts import render
from .models import Project
from .forms import ProjectForm

# Information about my projects


def projects(request):
    projects = Project.objects.all()
    print(projects)
    context = {'projects': projects}
    return render(request, 'Projects/projects.html', context)

# Information about an individual project


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tag.all()
    # reviews = projectObj.review_set.all()
    context = {'project': projectObj}
    return render(request, 'Projects/project.html', context)
