import os
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def project_folder_upload_path(instance, filename):
    # Upload each project folder to a unique directory based on project id
    return f"projects/user_projects/{instance.project_id}/{filename}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.AutoField(primary_key=True)
    project_title = models.CharField(max_length=100)
    project_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recent_update = models.DateTimeField(auto_now=True)
    project_folder = models.FileField(upload_to=project_folder_upload_path)  # Path to project files folder
    project_tech_stack = models.TextField(default='Python', blank=False, null=False)  # New field for project tech stack with default value
    stars = models.IntegerField(default=0)  # Field to store the count of stars

    def save(self, *args, **kwargs):
        # Generate the project ID if it's not already set
        if not self.project_id:
            max_id = Project.objects.aggregate(models.Max('project_id'))['project_id__max'] or 0
            self.project_id = max_id + 1
        # Update the project folder path using the generated project ID
        self.project_folder.name = project_folder_upload_path(self, os.path.basename(self.project_folder.name))
        super().save(*args, **kwargs)

class StarredProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    starred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')  # Ensures a user cannot star a project more than once

    def save(self, *args, **kwargs):
        # Check if the user has already starred a project within the past 24 hours
        last_24_hours = timezone.now() - timedelta(hours=24)
        starred_projects = StarredProject.objects.filter(user=self.user, starred_at__gte=last_24_hours)
        if starred_projects.exists():
            # User has already starred a project within the past 24 hours, prevent saving the new star
            return
        super().save(*args, **kwargs)
