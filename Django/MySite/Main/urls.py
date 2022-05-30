from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


# URLs' list
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Home.urls")),
    path("my_projects/", include("Projects.urls")),
    path("my_education/", include("Education.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
