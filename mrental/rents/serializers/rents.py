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
        fields = '__all__'
        # Atributos que no van a cambiar
        read_only_fields = (
            'is_active',
        )

class CreateRentalSerializer(serializers.ModelSerializer):
    """
    Create Rental serializer
    """
    # De esta forma el client_id es requerido
    client_code = serializers.CharField()
    rental_amount = serializers.FloatField()

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
        except Client.DoesNotExists:
            raise serializers.ValidationError('There is no active Client with the specified code')
        return data
    
    def create(self, data):
        """
        Create rental and update machinery
        """
        data.pop('client_code')
        machinery = self.context['machinery']
        client = self.context['client']
        rented_by = None    # @Pendiente. Obtener el usuario desde el request
        rental = Rental.objects.create(
            **data,
            machinery=machinery,
            client=client,
            rented_by=rented_by
        )
        # Update the Machinery
        machinery.is_rented = True
        machinery.save()
        return rental
