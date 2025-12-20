"""
URLs do Módulo de Compras
"""

from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    # Lista e Dashboard
    path('', views.lista_entradas, name='lista_entradas'),
    
    # Criação de entrada
    path('importar-xml/', views.importar_xml, name='importar_xml'),
    path('importar-pdf/', views.importar_pdf, name='importar_pdf'),
    path('entrada-manual/', views.entrada_manual, name='entrada_manual'),
    
    # Detalhe e Conferência
    path('<int:pk>/', views.detalhe_entrada, name='detalhe_entrada'),
    path('<int:nota_id>/conferencia-rapida/', views.conferencia_rapida, name='conferencia_rapida'),
    
    # Ações na Nota
    path('<int:nota_id>/finalizar/', views.finalizar_entrada, name='finalizar_entrada'),
    path('<int:nota_id>/cancelar/', views.cancelar_entrada, name='cancelar_entrada'),
    path('<int:nota_id>/conferir-todos/', views.conferir_todos, name='conferir_todos'),
    path('<int:nota_id>/vincular-automatico/', views.vincular_automatico, name='vincular_automatico'),
    
    # Itens
    path('<int:nota_id>/adicionar-item/', views.adicionar_item, name='adicionar_item'),
    path('item/<int:item_id>/remover/', views.remover_item, name='remover_item'),
    path('item/<int:item_id>/vincular/', views.vincular_produto, name='vincular_produto'),
    path('item/<int:item_id>/desvincular/', views.desvincular_produto, name='desvincular_produto'),
    path('item/<int:item_id>/cadastrar-produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('item/<int:item_id>/conferir/', views.conferir_item, name='conferir_item'),
    
    # APIs
    path('api/buscar-produtos/', views.buscar_produtos, name='buscar_produtos'),
    path('api/categorias-fabricantes/', views.get_categorias_fabricantes, name='get_categorias_fabricantes'),
    path('api/criar-fabricante/', views.criar_fabricante, name='criar_fabricante'),
]
