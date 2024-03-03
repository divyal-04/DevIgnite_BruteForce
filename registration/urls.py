from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import static
from app1.views import *
from profiles.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name='message-list'),
    path('app1/', include('app1.urls')),  # Include app1 URLs
    path('profiles/', include('profiles.urls')),  # Include profiles URLs
    path('projects/', include('projects.urls')),  # Include projects URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)