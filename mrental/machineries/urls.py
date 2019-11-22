"""
Machineries URLs.
"""

# Django
from django.urls import path, include
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from .views import machineries as machinery_views

router = DefaultRouter()
router.register(
    'machineries',                      # Path base
    machinery_views.MachineryViewSet,
    basename='machinery'
)

urlpatterns = [
    path('', include(router.urls)),
]
