from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path("", include('core.urls')),
    path("", include('userprofiles.urls')),
    path("dashboard/", include('dashboard.urls')),
    path("dashboard/leads/", include('leads.urls')),
    path("dashboard/clients/", include('client.urls')),
    path("dashboard/teams/", include('team.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
