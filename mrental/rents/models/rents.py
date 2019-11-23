"""
Rental model.
"""
# Django
from django.db import models
# Utilities
from mrental.utils.models import MRBaseModel

class Rental(MRBaseModel):
    """
    Rental model.
    """
    code = models.SlugField(
        unique=True,
        max_length=50
    )
    machinery = models.ForeignKey(
        'machineries.Machinery',
        on_delete=models.SET_NULL,  # Se conserva el alquiler en caso de eliminar la maquinaria
        null=True
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.SET_NULL,  # Se conserva el alquiler en caso de eliminar el cliente
        null=True
    )
    rented_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,  # Se conserva el alquiler en caso de eliminar el usuario
        null=True
    )
    rental_amount = models.FloatField(
        default=0.0,
        help_text='The amount for the rental of the specified machinery'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rental_address = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        """
        Return rental details.
        """
        return 'Rented to {} for an amount of {}'.format(
            self.client.name,
            self.rental_amount
        )
