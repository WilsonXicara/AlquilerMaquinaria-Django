"""
Machinery views.
"""
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# Permissions
from rest_framework.permissions import IsAuthenticated
from mrental.users.permissions.users import IsSuperUserPermission
# Models
from mrental.machineries.models import Machinery
from mrental.rents.models import Rental
# Serializers
from mrental.machineries.serializers import MachineryModelSerializer

class MachineryViewSet(mixins.CreateModelMixin,     # Crear nuevos registros
                       mixins.RetrieveModelMixin,   # Obtener un registro específico
                       mixins.ListModelMixin,       # LIstar todos los registros
                       mixins.UpdateModelMixin,     # Para actualizar un registro
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
        return MachineryModelSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a Machinery
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        machinery = serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def rents(self, request, *args, **kwargs):
        """
        Get the list of available and rented machinery.
        """
        rented_json, not_rented_json = [], []
        # Obteniendo las Maquinarias rentadas
        values_rented = ['code', 'rental_amount','machinery__code','machinery__machinery_type','machinery__name','machinery__default_amount',]
        rented = Rental.objects.filter(
            is_active=True,
            machinery__is_active=True
        ).values(*tuple(values_rented))
        values_rented.remove('code')
        values_rented.remove('rental_amount')
        for machinery in rented:
            machinery_data = {}
            machinery_data['rental_code'] = machinery['code']
            machinery_data['rental_amount'] = machinery['rental_amount']
            for value in values_rented:
                machinery_data[value.replace('machinery__','')] = machinery[value]
            rented_json.append(machinery_data)
        # Obteniendo las Maquinarias no rentadas
        values_not_rented = ['code','machinery_type','name','default_amount',]
        not_rented = Machinery.objects.filter(
            is_active=True,
            is_rented=False
        ).values(*tuple(values_not_rented))
        for machinery in not_rented:
            machinery_data = {}
            for value in values_not_rented:
                machinery_data[value] = machinery[value]
            not_rented_json.append(machinery_data)
        data = {
            'rented': rented_json,
            'not_rented': not_rented_json
        }
        return Response(data=data)
