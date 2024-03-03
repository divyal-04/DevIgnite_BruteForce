from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponse
from django.conf import settings
import os
from projects.models import StarredProject  # Importing StarredProject from the correct location

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        username = profile.user.username  # Get the username
        filename = profile.image.name.split('/')[-1]  # Get the filename
        starred_projects = StarredProject.starred_projects.all()
        return render(request, 'profiles/profile.html', {'profile': profile, 'username': username, 'filename': filename, 'starred_projects': starred_projects})
    except Profile.DoesNotExist:
        return redirect('create_profile')

from django.http import HttpResponse
from django.conf import settings
import os

def profile_image(request, username, image_name):
    image_path = os.path.join(settings.MEDIA_ROOT,  'profiles\\static\\profile_images', username, image_name)
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/jpeg')


