from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .models import Project, StarredProject
import os
from datetime import datetime, timedelta
from django.views.generic import DetailView
from django.http import HttpResponseForbidden, HttpResponseRedirect
import os


# views.py
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        tech_stacks = self.request.GET.getlist('tech_stack')
        if tech_stacks:
            # Filter projects based on selected tech stacks (case-insensitive)
            query = Q()
            for stack in tech_stacks:
                query |= Q(project_tech_stack__icontains=stack)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract unique tech stack values
        tech_stacks = Project.objects.values_list('project_tech_stack', flat=True).distinct()
        unique_tech_stacks = set(stack.strip() for stacks in tech_stacks for stack in stacks.split(','))
        context['tech_stacks'] = unique_tech_stacks
        return context



from django.http import HttpResponseRedirect, HttpResponseForbidden

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        project_folder_path = os.path.join("D:/School api/django-chat-app-main/django-chat-app-main/projects/user_projects/", str(project.project_id))

        # Retrieve file names and their content for .py files
        files = []
        for filename in os.listdir(project_folder_path):
            file_path = os.path.join(project_folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(('.py', '.js', '.html')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    files.append({'name': filename, 'content': content})
                except UnicodeDecodeError:
                    # Handle UnicodeDecodeError, e.g., by skipping the file or logging the error
                    pass
        
        
        context['files'] = files

        if self.request.user.is_authenticated:
            context['project'].starred_by_user = StarredProject.objects.filter(user=self.request.user, project=project).exists()
        else:
            context['project'].starred_by_user = False
            
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        project_folder_path = os.path.join("D:/School api/django-chat-app-main/django-chat-app-main/projects/user_projects/", str(project.project_id))
        
        # Check if the user is the owner of the project
        if request.user != project.user:
            # If not the owner, allow to star the project
            if 'star_project' in request.POST:
                starred_project, created = StarredProject.objects.get_or_create(user=request.user, project=project)
                if created:
                    project.stars += 1
                    project.save()
                return HttpResponseRedirect(request.path)
            else:
                return HttpResponseForbidden("You do not have permission to edit this project.")
        
        # If the user is the owner, proceed with saving changes
        if request.POST:
            for file in request.POST:
                if file.startswith('content_'):
                    file_name = file.split('_')[1]
                    file_path = os.path.join(project_folder_path, file_name)
                    new_content = request.POST[file]
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
        
            # Update recent_update field
            project.recent_update = datetime.now()
            project.save()
        
        return HttpResponseRedirect(request.path)

    
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project

class MyProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/my_projects.html'
    context_object_name = 'my_projects'

    def get_queryset(self):
        # Filter projects where the owner is the logged-in user
        return Project.objects.filter(user=self.request.user)



@login_required
def create_project(request):
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        project_desc = request.POST.get('project_desc')
        project_folder = request.FILES.getlist('project_folder')
        project_tech_stack = request.POST.get('project_tech_stack', 'Python')  # Default value if not provided

        project = Project.objects.create(
            user=request.user,
            project_title=project_title,
            project_desc=project_desc,
            project_tech_stack=project_tech_stack
        )

        # Save the files within the uploaded folder
        project_folder_path = os.path.join('projects', 'user_projects', str(project.project_id))
        os.makedirs(project_folder_path, exist_ok=True)
        for file in project_folder:
            with open(os.path.join(project_folder_path, file.name), 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return redirect('project_list')  # Redirect to project list after creation

    return render(request, 'projects/project_form.html')