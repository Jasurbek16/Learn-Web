from django.contrib import admin
from django.urls import path, include


# URLs' list
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('my_projects/', include('Projects.urls')),
    path('my_education/', include('Education.urls')),
]
