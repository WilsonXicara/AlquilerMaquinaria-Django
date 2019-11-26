"""
Client serializers.
"""
# Django REST Framework
from rest_framework import serializers
# Model
from mrental.clients.models import Client
# Utilities
import random
from string import ascii_uppercase, digits

class ClientModelSerializer(serializers.ModelSerializer):
    """
    Client model serializer.
    """
    CODE_LENGTH = 15
    POOL = ascii_uppercase + digits

    class Meta:
        model = Client
        fields = (
            'code', 'name',
            'address', 'phone_number',
        )
        # Campos que no pueden ser sobreescritos
        read_only_fields = (
            'is_active',
        )
    
    def validate_empty_values(self, data):
        """
        Validates that the code provided by the user is unique,
        or generates a unique code if the user does not provide it.
        """
        # Se crea un nuevo código único
        code = data.get('code', None)
        if code is None:
            code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
            while Client.objects.filter(code=code, is_active=True).exists():
                code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
            data['code'] = code
        return super(ClientModelSerializer, self).validate_empty_values(data)
