"""
Main URLs module.
"""
# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    # Apps
    path('api/v1/', include(('mrental.machineries.urls', 'machineries'), namespace='machineries')),
    path('api/v1/', include(('mrental.clients.urls', 'clients'), namespace='clients')),
    path('api/v1/', include(('mrental.rents.urls', 'rents'), namespace='rents')),
    path('api/v1/', include(('mrental.users.urls', 'rents'), namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
