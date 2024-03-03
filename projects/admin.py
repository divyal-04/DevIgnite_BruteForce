from django.contrib import admin
from .models import Project, StarredProject

# Register your models here.
admin.site.register(Project)
admin.site.register(StarredProject)
