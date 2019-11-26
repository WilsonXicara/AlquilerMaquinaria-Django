"""
Machinery model.
"""
# Django
from django.db import models
# Utilities
from mrental.utils.models import MRBaseModel

MACHINERY_IMAGE_DIR = 'machineries/pictures/'

class Machinery(MRBaseModel):
    """
    Machinery model.
    """
    code = models.SlugField(
        unique=True,
        max_length=50
    )
    machinery_type = models.CharField(
        'machinery type',
        max_length=75
    )
    name = models.CharField(
        'machinery name',
        max_length=75
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    picture = models.ImageField(
        upload_to=MACHINERY_IMAGE_DIR,
        blank=True,
        null=True
    )
    is_rented = models.BooleanField(
        default=False
    )
    default_amount = models.FloatField(
        default=0.0,
        help_text='The default amount for renting this machinery'
    )

    def __str__(self):
        """
        Return name.
        """
        return str(self.name)
