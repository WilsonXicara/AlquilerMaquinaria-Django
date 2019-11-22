"""
Machinery views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
# Models
from mrental.machineries.models import Machinery
# Serializers
from mrental.machineries.serializers import MachineryModelSerializer

class MachineryViewSet(mixins.CreateModelMixin,     # Crear nuevos registros
                       mixins.RetrieveModelMixin,   # Obtener un registro específico
                       mixins.ListModelMixin,       # LIstar todos los registros
                       viewsets.GenericViewSet):
    """
    Machinery view set.
    """
    serializer_class = MachineryModelSerializer
    lookup_field = 'code'       # Se tomará el 'code' para agregarlo a la URL

    def get_queryset(self):
        """
        Restrict list to is_active only
        """
        queryset = Machinery.objects.filter(is_active=True)
        return queryset