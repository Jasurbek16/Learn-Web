from django.shortcuts import render

def log_home(request):
    #The home page
    return render(request, 'l_logs/l_log_home.html')