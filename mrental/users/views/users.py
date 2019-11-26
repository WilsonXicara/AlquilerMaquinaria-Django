"""
Users views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
# Serializers
from mrental.users.serializers import (
    UserModelSerializaer,
    UserSignUpSerializer,
    UserLoginSerializer,
)
# Models
from mrental.users.models import User

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,        # Listar todos los registros
                  mixins.UpdateModelMixin,      # Para permitir la actualización de un registro
                  viewsets.GenericViewSet):
    """
    User view set.

    Handle sign up, login and account verification.
    """
    # Siempre que se incluye 'RetrieveModelMixin' hay que configurar un queryset base desde el cual se hará el queryset del detalle
    lookup_field = 'username'

    def get_queryset(self):
        """
        Restrict list to is_active only
        """
        queryset = User.objects.filter(is_active=True)
        return queryset

    def get_permissions(self):
        """
        Assign permissions based on action.
        """
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """
        Return serializer based on action.
        """
        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'login':
            return UserLoginSerializer
        return UserModelSerializaer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
        User sign up.
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializaer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        User login.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializaer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
