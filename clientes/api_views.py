from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Veiculo
from .serializers import ClienteSerializer, ClienteListSerializer, VeiculoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo', 'cidade', 'estado']
    search_fields = ['nome', 'cpf_cnpj', 'telefone', 'email']
    ordering_fields = ['nome', 'data_cadastro']
    ordering = ['-data_cadastro']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        return ClienteSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cliente', 'marca', 'modelo']
    search_fields = ['placa', 'marca', 'modelo', 'chassi']
    ordering_fields = ['placa', 'data_cadastro']
    ordering = ['-data_cadastro']
