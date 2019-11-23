"""
Users serializers.
"""
# Django REST Framework
from rest_framework import serializers
# Models
from mrental.users.models import User

class UserModelSerializaer(serializers.ModelSerializer):
    """
    User model serializaer.
    """
    
    class Meta:
        """
        Meta class.
        """
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active'
        )