from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes.api_views import ClienteViewSet, VeiculoViewSet
from estoque.api_views import CategoriaViewSet, FornecedorViewSet, ProdutoViewSet, MovimentacaoEstoqueViewSet
from vendas.api_views import VendaViewSet, ItemVendaViewSet, OrdemServicoViewSet, PecaOSViewSet, ServicoOSViewSet

router = DefaultRouter()

# Clientes
router.register(r'clientes', ClienteViewSet)
router.register(r'veiculos', VeiculoViewSet)

# Estoque
router.register(r'categorias', CategoriaViewSet)
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'movimentacoes', MovimentacaoEstoqueViewSet)

# Vendas
router.register(r'vendas', VendaViewSet)
router.register(r'itens-venda', ItemVendaViewSet)
router.register(r'ordens-servico', OrdemServicoViewSet)
router.register(r'pecas-os', PecaOSViewSet)
router.register(r'servicos-os', ServicoOSViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
