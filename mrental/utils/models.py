"""
Django models base.
"""
from django.db import models

class MRAbstractBaseModel(models.Model):
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#abstract-base-classes
    """
    Abstract base model for machinery rental.

    Abstract base class for all application models.
    This class will provide all models with the following attributes:
        + created  (DateTime): The datetime the object was created.
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

class MRBaseModel(MRAbstractBaseModel):
    """
    Base model for machinery rental.

    Abstract base class for all application models.
    This class will provide all models with the following attributes:
        + is_active          (Boolean): Indicates whether the object is active or not
        + elimination_reason (String):  Indicate the reason why the object was deleted
    """
    is_active = models.BooleanField(
        'is active',
        default=True,
        help_text='Indicates whether the object is active or not'
    )
    elimination_reason = models.CharField(
        'elimination reason',
        max_length=255,
        null=True,
        blank=True,
        help_text='Indicates the reason for removing the object'
    )

    class Meta(MRAbstractBaseModel.Meta):
        abstract = True