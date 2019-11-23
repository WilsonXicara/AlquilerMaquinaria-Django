"""
Rents URLs.
"""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from .views import rents as rental_views

router = DefaultRouter()
router.register(
    r'machineries/(?P<code>[-a-zA-Z0-9_]+)/rents',
    rental_views.RentalViewSet,
    basename='rental'
)

urlpatterns = [
    path('', include(router.urls)),
]
