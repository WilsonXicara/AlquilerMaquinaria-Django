"""
Machinery views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
    
    @action(detail=False, methods=['get'])
    def rents(self, request, *args, **kwargs):
        """
        Get the list of available and rented machinery.
        """
        values = ('code','machinery_type','name','default_amount',)
        rented = Machinery.objects.filter(
            is_active=True,
            is_rented=True
        ).values(*values)
        not_rented = Machinery.objects.filter(
            is_active=True,
            is_rented=False
        ).values(*values)
        rented_json, not_rented_json = [], []
        for machinery in rented:
            machinery_data = {}
            for value in values:
                machinery_data[value] = machinery[value]
            rented_json.append(machinery_data)
        for machinery in not_rented:
            machinery_data = {}
            for value in values:
                machinery_data[value] = machinery[value]
            not_rented_json.append(machinery_data)
        data = {
            'rented': rented_json,
            'not_rented': not_rented_json
        }
        return Response(data=data)
