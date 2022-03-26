from django.shortcuts import render

projectsList = [
    {
        'id': '1',
        'title': 'Utipss',
        'description': 'Helping students finding their way...'
    },
    {
        'id': '2',
        'title': 'HelpQR',
        'description': 'Find your child by QR'
    },
    {
        'id': '3',
        'title': 'MySite',
        'description': 'A personal website that used ML applications'
    }
]


# Information about my projects


def projects(request):
    context = {'projects':projectsList}
    return render(request, 'Projects/projects.html', context)

# Information about an individual project


def project(request, pk):
    chosenProject = None

    for project in projectsList:
        if project["id"] == str(pk):
            chosenProject = project

    return render(request, 'Projects/project.html', {'project': chosenProject})
