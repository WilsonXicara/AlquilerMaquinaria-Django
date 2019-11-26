"""
Rental serializers.
"""
# Django REST Framework
from rest_framework import serializers
# Models
from mrental.clients.models import Client
from mrental.machineries.models import Machinery
from mrental.rents.models import Rental
from mrental.users.models import User
# Serializers
from mrental.clients.serializers import ClientModelSerializer
from mrental.machineries.serializers import MachineryModelSerializer
from mrental.users.serializers import UserModelSerializaer
# Utilities
from datetime import timedelta
import random
from string import ascii_uppercase, digits
from django.utils import timezone

class RentalModelSerializer(serializers.ModelSerializer):
    """
    Rental model serializaer.
    """
    machinery = MachineryModelSerializer(read_only=True)
    client = ClientModelSerializer(read_only=True)
    rented_by = UserModelSerializaer(read_only=True)
    
    class Meta:
        """
        Meta class.
        """
        model = Rental
        fields = (
            'code',
            'machinery', 'client', 'rented_by',
            'rental_amount', 'start_date', 'end_date',
            'rental_address', 'description',
            'is_active', 'elimination_reason',
        )
        # Atributos que no van a cambiar
        read_only_fields = (
            'is_active',
        )

class CreateRentalSerializer(serializers.ModelSerializer):
    """
    Create Rental serializer
    """
    CODE_LENGTH = 20
    POOL = ascii_uppercase + digits
    # De esta forma el client_id es requerido
    client_code = serializers.CharField()
    rental_amount = serializers.FloatField()
    code = serializers.CharField(required=False)

    class Meta:
        """
        Meta class.
        """
        model = Rental
        exclude = (
            'rented_by',
        )
    
    def validate_rental_amount(self, data):
        """
        Validate that the rental_amount is greater than zero
        """
        if data < 0.0:
            raise serializers.ValidationError('The rental_amount must be greater than or equal to zero')
        return data

    def validate(self, data):
        """
        Validate:
            + That the Machinery is not rented
            + That the end_date is greater than or equal to the start_date.
            + That the Client exists and is active.
        Replace the client_code with the Client object.
        """
        # @Pendiente. El Usuario admin se obtendrá desde el Request
        if self.context['machinery'].is_rented:
            raise serializers.ValidationError('The machinery is already rented')
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError('The end_date must be greater than or equal to the start_date')
        client_code = data['client_code']
        try:
            client = Client.objects.get(code=client_code, is_active=True)
            self.context['client'] = client
        except Client.DoesNotExist:
            raise serializers.ValidationError('There is no active Client with the specified code')
        return data
    
    def create(self, data):
        """
        Create rental and update machinery.
        A unique code is generated to identify the rental.
        """
        # Generando el código único para el alquiler
        code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
        while Rental.objects.filter(code=code, is_active=True).exists():
            code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
        data.pop('client_code')
        machinery = self.context['machinery']
        client = self.context['client']
        rented_by = self.context['request'].user
        rental = Rental.objects.create(
            **data,
            code=code,
            machinery=machinery,
            client=client,
            rented_by=rented_by
        )
        # Update the Machinery
        machinery.is_rented = True
        machinery.save()
        return rental

class FinishRentalSerializer(serializers.Serializer):
    """
    The rental of a machinery ends.
    The machinery is available for new rentals (is_rented=False)
    """
    comments = serializers.CharField()

    class Meta:
        """
        Meta class.
        """
        model = Rental
        fields = ('comments',)

    def validate(self, data):
        """
        Validate:
            + That a comment be specified
            + That the rental can be finalized
        """
        # if data.get('comments', None) is None:
        #     raise serializers.ValidationError('No comment provided')
        rental = self.context['rental']
        if not rental.is_active:
            raise serializers.ValidationError('The rental has already been finalized')
        return data
    
    def update(self, instance, data):
        """
        Finish the rental and start the machinery as available to be rented
        """
        # @Pendiente. Asociar User que realiza la finalización del alquiler
        rental = self.context['rental']
        machinery = self.context['machinery']
        # Update Rental
        rental.is_active = False
        rental.elimination_reason = data.pop('comments')
        rental.save()
        # Update Machinery
        machinery.is_rented = False
        machinery.save()
        return rental
