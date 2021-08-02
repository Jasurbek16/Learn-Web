from django.contrib import admin
from .models import Post

# registering with the admin site
admin.site.register(Post)