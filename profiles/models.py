from django.db import models
from django.contrib.auth.models import User

def profile_image_upload_path(instance, filename):
    return f"profiles/static/profile_images/{instance.user.username}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_image_upload_path)
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=250)
    skills = models.TextField(max_length=400)

    def __str__(self):
        return self.user.username
