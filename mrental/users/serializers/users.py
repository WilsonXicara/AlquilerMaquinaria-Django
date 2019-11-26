"""
Users serializers.
"""
# Django
from django.contrib.auth import authenticate, password_validation
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
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
            'username', 'email',
            'first_name', 'last_name',
            'is_active',
            'is_client', 'is_superuser',
        )
        # Campos que no pueden ser sobreescritos
        read_only_fields = (
            'username', 'email', 'is_active', 'is_client', 'is_superuser',
        )

class UserSignUpSerializer(serializers.Serializer):
    """
    User sign up serializaer.

    Handle sign up data validation and user creation.
    """
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        min_length=8,
        max_length=64
    )
    password_confirmation = serializers.CharField(
        min_length=8,
        max_length=64
    )
    # Name
    first_name = serializers.CharField(
        min_length=2,
        max_length=30
    )
    last_name = serializers.CharField(
        min_length=2,
        max_length=30
    )

    def validate(self, data):
        """
        Verify passwords match.
        """
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """
        Handle user and profile creation.
        """
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_client=False)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.

    Handle the login request data.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        max_length=64
    )

    def validate(self, data):
        """
        Check credentials.
        """
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, data):
        """
        Generate or retrieve new token.
        """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
