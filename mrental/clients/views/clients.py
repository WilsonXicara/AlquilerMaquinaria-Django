"""
Client views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
# Permissions
from rest_framework.permissions import IsAuthenticated
from mrental.users.permissions.users import IsSuperUserPermission
# Models
from mrental.clients.models import Client
# Serializers
from mrental.clients.serializers import ClientModelSerializer

class ClientViewSet(mixins.CreateModelMixin,     # Crear nuevos registros
                    mixins.RetrieveModelMixin,   # Obtener un registro específico
                    mixins.ListModelMixin,       # LIstar todos los registros
                    mixins.UpdateModelMixin,     # Actualizar un registro
                    viewsets.GenericViewSet):
    """
    Client view set.
    """
    serializer_class = ClientModelSerializer
    lookup_field = 'code'       # Se tomará el 'code' para agregarlo a la URL

    def get_queryset(self):
        """
        Restrict list to is_active only
        """
        queryset = Client.objects.filter(is_active=True)
        return queryset
    
    def get_permissions(self):
        """
        Assign permissions based on action.
        """
        permissions = [IsAuthenticated, IsSuperUserPermission]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """
        Return serializer based on action.
        """
        return ClientModelSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a Client
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
