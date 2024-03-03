from django.urls import path
from . import views
from . views import * 

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('create/', views.create_project, name='project_create'),
    path('my_projects/', MyProjectListView.as_view(), name='my_projects'),
]
