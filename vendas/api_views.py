from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import Venda, ItemVenda, OrdemServico, PecaOS, ServicoOS
from .serializers import (VendaSerializer, VendaListSerializer, ItemVendaSerializer,
                          OrdemServicoSerializer, OrdemServicoListSerializer,
                          PecaOSSerializer, ServicoOSSerializer)


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'forma_pagamento', 'cliente']
    search_fields = ['numero', 'cliente__nome']
    ordering = ['-data_venda']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VendaListSerializer
        return VendaSerializer
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de vendas"""
        vendas = self.queryset.filter(status='F')
        
        stats = {
            'total_vendas': vendas.count(),
            'valor_total': vendas.aggregate(Sum('total'))['total__sum'] or 0,
            'ticket_medio': vendas.aggregate(Sum('total'))['total__sum'] / vendas.count() if vendas.count() > 0 else 0,
            'por_forma_pagamento': {}
        }
        
        # Vendas por forma de pagamento
        for forma in vendas.values('forma_pagamento').annotate(
            total=Sum('total'), 
            quantidade=Count('id')
        ):
            stats['por_forma_pagamento'][forma['forma_pagamento']] = {
                'total': forma['total'],
                'quantidade': forma['quantidade']
            }
        
        return Response(stats)


class ItemVendaViewSet(viewsets.ModelViewSet):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['venda', 'produto']


class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'cliente', 'veiculo', 'mecanico']
    search_fields = ['numero', 'cliente__nome', 'veiculo__placa']
    ordering = ['-data_entrada']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrdemServicoListSerializer
        return OrdemServicoSerializer
    
    @action(detail=False, methods=['get'])
    def em_aberto(self, request):
        """Retorna OS em aberto"""
        os_abertas = self.queryset.filter(status__in=['AB', 'EA', 'AG'])
        serializer = self.get_serializer(os_abertas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de OS"""
        stats = {
            'total': self.queryset.count(),
            'abertas': self.queryset.filter(status='AB').count(),
            'em_andamento': self.queryset.filter(status='EA').count(),
            'aguardando_pecas': self.queryset.filter(status='AG').count(),
            'finalizadas': self.queryset.filter(status='FI').count(),
            'canceladas': self.queryset.filter(status='CA').count(),
        }
        return Response(stats)


class PecaOSViewSet(viewsets.ModelViewSet):
    queryset = PecaOS.objects.all()
    serializer_class = PecaOSSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ordem_servico', 'produto']


class ServicoOSViewSet(viewsets.ModelViewSet):
    queryset = ServicoOS.objects.all()
    serializer_class = ServicoOSSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ordem_servico']
