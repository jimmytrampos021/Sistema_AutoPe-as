from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque
from .serializers import (CategoriaSerializer, FornecedorSerializer, 
                          ProdutoSerializer, ProdutoListSerializer, 
                          MovimentacaoEstoqueSerializer)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering = ['nome']


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'cidade', 'estado']
    search_fields = ['nome_fantasia', 'razao_social', 'cnpj']
    ordering = ['nome_fantasia']


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'fornecedor', 'ativo', 'marca_veiculo']
    search_fields = ['codigo', 'codigo_barras', 'descricao']
    ordering_fields = ['codigo', 'descricao', 'preco_venda', 'estoque_atual']
    ordering = ['descricao']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProdutoListSerializer
        return ProdutoSerializer
    
    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        """Retorna produtos com estoque abaixo do mínimo"""
        produtos = self.queryset.filter(estoque_atual__lte=models.F('estoque_minimo'))
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mais_vendidos(self, request):
        """Retorna os produtos mais vendidos"""
        # Implementar lógica de produtos mais vendidos
        return Response({'message': 'Em desenvolvimento'})


class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['produto', 'tipo']
    search_fields = ['produto__descricao', 'documento']
    ordering = ['-data_movimentacao']
