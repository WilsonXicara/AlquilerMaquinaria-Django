"""
Django models base.
"""
from django.db import models

class MRBaseModel(models.Model):
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#abstract-base-classes
    """
    Base model for machinery rental.

    Abstract base class for all application models.
    This class will provide all models with the following attributes:
        + created (DateTime): The datetime the object was created.
        + modified (DateTime): The last datetime the object was modified.
    """
    created = models.DateTimeField(
        'created at',               # Texto de ayuda
        auto_now_add=True,          # Guarda la fecha en la que se crea
        help_text='Date time on wich the object was created.'
    )
    modified = models.DateTimeField(
        'modified at',               # Texto de ayuda
        auto_now=True,               # Guarda la fecha cada vez que se llama a .save()
        help_text='Date time on wich the object was last modified.'
    )
    class Meta:
        """
        Meta option.
        """
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']    # '-' indica que sea descendente