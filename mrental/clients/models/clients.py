"""
Client model.
"""
# Django
from django.db import models
from django.core.validators import RegexValidator
# Utilities
from mrental.utils.models import MRBaseModel

class Client(MRBaseModel):
    """
    Client model.

    A client is the one who can make machinery rentals
    """
    code = models.SlugField(
        unique=True,
        max_length=50
    )
    name = models.CharField(
        'client name',
        max_length=255
    )
    address = models.CharField(
        'client address',
        max_length=500
    )
    phone_regex = RegexValidator(
        regex=r'\+?\d{8,15}$',
        message='Phone number must be entered in the format: +50212345678. Up to 15 digits allowed.'
    )
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        validators=[phone_regex]
    )

    def __str__(self):
        """
        Return name.
        """
        return str(self.name)
