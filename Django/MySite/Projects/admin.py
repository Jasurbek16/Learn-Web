from django.contrib import admin
from .models import Projects, Project, Review, Tag

admin.site.register(Projects)
admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
