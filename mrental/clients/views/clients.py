"""
Client views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
# Models
from mrental.clients.models import Client
# Serializers
from mrental.clients.serializers import ClientModelSerializer

class ClientViewSet(mixins.CreateModelMixin,     # Crear nuevos registros
                    mixins.RetrieveModelMixin,   # Obtener un registro específico
                    mixins.ListModelMixin,       # LIstar todos los registros
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