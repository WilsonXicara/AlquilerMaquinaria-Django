"""
User model.
"""
# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
# Utilities
from mrental.utils.models import MRBaseModel, MRAbstractBaseModel

class User(MRAbstractBaseModel, AbstractUser):
    """
    User model.

    Extend from Django's Abstract User, change de username field
    to email and add some extra fields.
    """
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with than email alredy exists.'       # Mensaje de error en la creación de un registro
        }
    )
    is_client = models.BooleanField(
        'client status',
        default=False,
        help_text=('For future use. User account for a customer')
    )
    # Redefiniendo el campo principal
    USERNAME_FIELD = 'email'
    # Campos indispensables para crear un usuario (no es necesario indicar 'email' porque está configurado como 'unique' y por tanto es requerido)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """
        Return username.
        """
        return self.username
    
    def get_short_name(self):
        """
        Return username.
        """
        return self.username
