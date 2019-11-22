"""
Machinery serializers.
"""
# Django REST Framework
from rest_framework import serializers
# Model
from mrental.machineries.models import Machinery
# Utilities
import random
from string import ascii_uppercase, digits

class MachineryModelSerializer(serializers.ModelSerializer):
    """
    Machinery model serializer.
    """
    CODE_LENGTH = 15
    POOL = ascii_uppercase + digits
    default_amount = serializers.FloatField(
        required=True,
        min_value=0.0
    )
    is_rented = serializers.BooleanField(
        default=False
    )

    class Meta:
        model = Machinery
        fields = (
            'code', 'machinery_type', 'name',
            'description', 'picture',
            'default_amount',
            'is_rented'
        )
        # Campos que no pueden ser sobreescritos
        read_only_fields = (
            'is_rented', 'is_active'
        )
    
    def validate_default_amount(self, data):
        """
        Validate that the rental amount is a positive value
        """
        if data < 0.0:
            raise serializers.ValidationError('The value of the amount must be greater than 0.0')
        return data
    
    def validate_empty_values(self, data):
        """
        Validates that the code provided by the user is unique,
        or generates a unique code if the user does not provide it.
        """
        # Se crea un nuevo código único
        code = data.get('code', None)
        if code is None:
            code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
            while Machinery.objects.filter(code=code, is_active=True).exists():
                code = ''.join(random.choices(self.POOL, k=self.CODE_LENGTH))
            data['code'] = code
        return super(MachineryModelSerializer, self).validate_empty_values(data)
