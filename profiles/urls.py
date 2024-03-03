from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('static/profile_images/<str:username>/<str:image_name>/', views.profile_image, name='profile_image'),


]
