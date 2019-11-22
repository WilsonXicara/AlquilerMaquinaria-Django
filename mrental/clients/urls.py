"""
Clients URLs.
"""

# Django
from django.urls import path, include
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from .views import clients as client_views

router = DefaultRouter()
router.register(
    'clients',                      # Path base
    client_views.ClientViewSet,
    basename='client'
)

urlpatterns = [
    path('', include(router.urls)),
]
