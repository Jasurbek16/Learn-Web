from django.shortcuts import render

# Information about the places where I've studied
def education(request):
    return render(request, 'Education/education.html')
