from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectForm

# Information about my projects


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "Projects/projects.html", context)


# Information about an individual project


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tag.all()
    # reviews = projectObj.review_set.all()
    context = {"project": projectObj}
    return render(request, "Projects/project.html", context)


def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("allProjects")

    context = {"form": form}
    return render(request, "Projects/project-form.html", context)


def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("allProjects")

    context = {"form": form}
    return render(request, "Projects/project-form.html", context)


def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("allProjects")
    return render(request, "Projects/delete.html", {"object": project})
