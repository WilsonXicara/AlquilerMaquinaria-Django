"""
Rents ViewSet
"""
# Django
from django.db.models import Avg, Sum
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# Models
from mrental.machineries.models import Machinery
from mrental.rents.models import Rental
# Serializers
from mrental.rents.serializers import (
    CreateRentalSerializer,
    RentalModelSerializer,
    FinishRentalSerializer,
)
# Permissions
from rest_framework.permissions import IsAuthenticated
# Utils
from datetime import timedelta
from django.utils import timezone

class RentalViewSet(mixins.ListModelMixin,      # Listar todos
                    mixins.CreateModelMixin,    # Crear uno nuevo
                    mixins.RetrieveModelMixin,  # Obtener un registro específico
                    mixins.UpdateModelMixin,    # Actualizar un registro específico
                    viewsets.GenericViewSet):
    """
    Rental view set.
    """
    lookup_field = 'code'
#     permission_classes = [IsAuthenticated,]
#     # Filters
#     # Tomar en cuenta que estos filtros se aplican sobre el QuerySet definido en el ViewSet
#     filter_backends = (SearchFilter, OrderingFilter,)
#     # Orden por defecto. No necesita especificarse entre los parámetros
#     ordering = ('departure_date', 'arrival_date', 'available_seats',)
#     # El filtro se aplica especificando uno de los campos aquí definidos. El parámetro es:
#     #   ordering=[-]FIELD_NAME          (El '-' indica que el orden será descendente)
#     ordering_fields = ('departure_date', 'arrival_date', 'available_seats',)
#     # El filtro se aplica a los campos especificados, con el parámetro 'search=VALOR'
#     search_fields = ('departure_location', 'arrival_location',)

    def dispatch(self, request, *args, **kwargs):
        """
        Verify that the machinery exists and is active.
        """
        # La Machinery está en el primer nivel de la URL, por lo que debería estar presente en todas las demas URL
        # Se verifica que cada vez que se valide esta vista, la Machinery esté disponible a toda la clase
        # Esto viene de la URL
        code = kwargs['code_machinery']
        self.machinery = get_object_or_404(Machinery, code=code, is_active=True)
        return super(RentalViewSet, self).dispatch(request, *args, **kwargs)

#     def get_permissions(self):
#         """
#         Assign permission based on action.
#         """
#         permissions = [IsAuthenticated, IsActiveCircleMemberPermission,]
#         if self.action in ['update', 'partial_update', 'finish']:
#             # Sólo el dueño del ride puede actualizar o finalizar el Ride
#             permissions.append(IsRideOwnerPermission)
#         return [permission() for permission in permissions]

    def get_serializer_context(self):
        """
        Add machinery to serializer context.
        """
        context = super(RentalViewSet, self).get_serializer_context()
        context['machinery'] = self.machinery
        return context
    
    def get_serializer_class(self):
        """
        Return serializer class
        """
        if self.action == 'create':
            return CreateRentalSerializer
        if self.action == 'finish':
            return FinishRentalSerializer
        return RentalModelSerializer
    
    def get_queryset(self):
        """
        Return active machinery's rents.
        """
        if self.action not in ['finish']:
            return self.machinery.rental_set.filter(
                is_active=True
            )
        return self.machinery.rental_set.all()
    
    def create(self, request, *args, **kwargs):
        """
        Create a Rental
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        data = RentalModelSerializer(rental).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """
        Call by Admin user to finish a Rental.
        """
        rental = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            rental,
            data=request.data,
            context={
                'rental': rental,
                'machinery': self.machinery
            }
        )
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        data = RentalModelSerializer(rental).data
        return Response(data, status=status.HTTP_200_OK)

class RentalResumeViewSet(mixins.ListModelMixin,      # Listar todos
                          viewsets.GenericViewSet):
    """
    Summary ViewSet
    """
    queryset = Rental.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Get the data according to the specified parameters.
        """
        total_rents = self.get_queryset()
        machinery_code = request.query_params.get('machinery_code', None)
        operation = request.query_params.get('operation', 'total')
        data = {
            'machinery': '__all__',
            'operation': 'total',
            'value': 0
        }
        # Filtrando registros
        if machinery_code is not None:
            total_rents = total_rents.filter(
                machinery__code=machinery_code
            )
            data['machinery'] = machinery_code
        # Aplicando la operación especificada
        if operation == 'average':
            data['operation'] = operation
            data['value'] = total_rents.aggregate(Avg('rental_amount'))['rental_amount__avg']
        else:
            data['operation'] = 'total'
            data['value'] = total_rents.aggregate(Sum('rental_amount'))['rental_amount__sum']
        return Response(data, status=status.HTTP_200_OK)
