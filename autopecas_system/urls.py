"""
URL configuration for autopecas_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views



"""
URL configuration for autopecas_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('financeiro/', include('financeiro.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # <--- ADICIONE AQUI
    path('api/', include('autopecas_system.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', core_views.dashboard, name='dashboard'),
    path('pdv/', core_views.pdv, name='pdv'),
    path('relatorios/', core_views.relatorios, name='relatorios'),
    
    path('comparador/', core_views.comparador_precos_fornecedores, name='comparador_precos_fornecedores'),
    path('cotacao/nova/', core_views.cadastrar_cotacao, name='cadastrar_cotacao'),
    path('fornecedores/cotacao/adicionar/', core_views.adicionar_cotacao, name='adicionar_cotacao'),
    path('relatorio/fornecedores/', core_views.relatorio_melhores_fornecedores, name='relatorio_fornecedores'),
    # path('api/produto/buscar/', core_views.api_buscar_produto, name='api_buscar_produto'),
    path('api/produto/<int:produto_id>/cotacoes/', core_views.api_cotacoes_produto, name='api_cotacoes_produto'),
    
    # Fornecedores (UNIFICADO - apenas um bloco)
    path('fornecedores/', core_views.lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/adicionar/', core_views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('fornecedores/<int:fornecedor_id>/', core_views.detalhes_fornecedor, name='detalhes_fornecedor'),
    path('fornecedores/<int:fornecedor_id>/editar/', core_views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/<int:fornecedor_id>/deletar/', core_views.deletar_fornecedor, name='deletar_fornecedor'),
    path('fornecedor/<int:fornecedor_id>/', core_views.detalhe_fornecedor, name='detalhe_fornecedor'),
    
    # Clientes
    path('clientes/', core_views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', core_views.detalhe_cliente, name='detalhe_cliente'),
    
    # Estoque
    path('estoque/', core_views.lista_estoque, name='lista_estoque'),
    path('estoque/produto/<int:produto_id>/', core_views.detalhe_produto, name='detalhe_produto'),
    
    # Vendas
    path('vendas/', core_views.lista_vendas, name='lista_vendas'),
    path('vendas/<int:venda_id>/', core_views.detalhe_venda, name='detalhe_venda'),
    
    # Ordens de Serviço
    path('ordens-servico/', core_views.lista_ordens_servico, name='lista_ordens_servico'),
    path('ordens-servico/<int:os_id>/', core_views.detalhe_ordem_servico, name='detalhe_ordem_servico'),
    
    # URLs de Produtos
    path('estoque/produto/novo/', core_views.criar_produto, name='criar_produto'),
    path('estoque/produto/<int:produto_id>/editar/', core_views.editar_produto, name='editar_produto'),
    path('estoque/produto/<int:produto_id>/deletar/', core_views.deletar_produto, name='deletar_produto'),
     # URLs de Orçamento
    path('orcamentos/', core_views.lista_orcamentos, name='lista_orcamentos'),
    path('orcamentos/novo/', core_views.criar_orcamento, name='criar_orcamento'),
    path('orcamentos/<int:orcamento_id>/', core_views.detalhe_orcamento, name='detalhe_orcamento'),
    path('orcamentos/<int:orcamento_id>/editar/', core_views.editar_orcamento, name='editar_orcamento'),
    path('orcamentos/<int:orcamento_id>/converter/', core_views.converter_orcamento_venda, name='converter_orcamento_venda'),
    
    # APIs de Busca
    # path('api/buscar-produtos/', core_views.buscar_produtos_rapido, name='buscar_produtos_rapido'),
    path('api/pdv/buscar-produtos/', core_views.api_buscar_produtos_pdv, name='api_buscar_produtos_pdv'),
    path('api/buscar-modelos/', core_views.buscar_modelos_por_montadora, name='buscar_modelos_por_montadora'),
    # Categorias
    path('categorias/', core_views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', core_views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:categoria_id>/editar/', core_views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/deletar/', core_views.deletar_categoria, name='deletar_categoria'),
    
    # Subcategorias
    path('categorias/<int:categoria_id>/subcategoria/nova/', core_views.criar_subcategoria, name='criar_subcategoria'),
    path('subcategorias/<int:subcategoria_id>/editar/', core_views.editar_subcategoria, name='editar_subcategoria'),
    path('subcategorias/<int:subcategoria_id>/deletar/', core_views.deletar_subcategoria, name='deletar_subcategoria'),
    
    # APIs
    path('api/modelos/', core_views.api_buscar_modelos, name='api_buscar_modelos'),
    path('api/versoes/', core_views.api_buscar_versoes, name='api_buscar_versoes'),
    path('api/subcategorias/', core_views.api_buscar_subcategorias, name='api_buscar_subcategorias'),

]
   




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


   




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

