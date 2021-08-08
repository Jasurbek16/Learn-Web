from django.shortcuts import render, redirect
from .models import Subjects, Info
from .forms import AddSubjectsForm, AddTopicsForm
from django.contrib import messages


def home(request):
    # The home page
    subjects = Subjects.objects.order_by("name")
    context = {"subjects": subjects}
    return render(request, "UTipsApp/home.html", context)


def about(request):
    return render(request, "UTipsApp/about.html", {"title": "About"})


def subject_details(request, pk):
    # For the single subject
    subject = Subjects.objects.get(id=pk)
    topics = subject.info_set.order_by("-date_shared")
    context = {"subject": subject, "topics": topics}
    return render(request, "UTipsApp/topics_list.html", context)


def topic_details(request, pk):
    # For the single topic
    topic = Info.objects.get(id=pk)
    subject = Subjects.objects.get(id=topic.subject.id)
    context = {"topic": topic, "subject": subject}
    return render(request, "UTipsApp/topics.html", context)


def addSubject(request):
    if request.method != "POST":
        form = AddSubjectsForm()
    else:
        form = AddSubjectsForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("name")
            messages.success(request, f"The {name} has been added successfully 👏")
            return redirect("Ut-home")

    context = {"form": form}
    return render(request, "UTipsApp/add_subject.html", context)


def addTopic(request):
    if request.method != "POST":
        form = AddTopicsForm()
    else:
        form = AddTopicsForm(request.POST)
        if form.is_valid():
            form.save()
            topic = form.cleaned_data.get("topic")
            messages.success(request, f"The {topic} has been added successfully 👏")
            return redirect("Ut-home")

    context = {"form": form}
    return render(request, "UTipsApp/add_topic.html", context)
