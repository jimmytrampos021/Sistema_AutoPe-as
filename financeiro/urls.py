from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # Dashboard Financeiro
    path('', views.dashboard_financeiro, name='dashboard'),
    
    # Contas a Pagar
    path('contas/', views.lista_contas_pagar, name='lista_contas'),
    path('contas/nova/', views.criar_conta_pagar, name='criar_conta'),
    path('contas/<int:conta_id>/', views.detalhe_conta_pagar, name='detalhe_conta'),
    path('contas/<int:conta_id>/editar/', views.editar_conta_pagar, name='editar_conta'),
    path('contas/<int:conta_id>/pagar/', views.pagar_conta, name='pagar_conta'),
    path('contas/<int:conta_id>/cancelar/', views.cancelar_conta, name='cancelar_conta'),
    
    # Despesas Fixas
    path('despesas-fixas/', views.lista_despesas_fixas, name='lista_despesas_fixas'),
    path('despesas-fixas/nova/', views.criar_despesa_fixa, name='criar_despesa_fixa'),
    path('despesas-fixas/<int:despesa_id>/editar/', views.editar_despesa_fixa, name='editar_despesa_fixa'),
    path('despesas-fixas/<int:despesa_id>/deletar/', views.deletar_despesa_fixa, name='deletar_despesa_fixa'),
    path('despesas-fixas/gerar-mes/', views.gerar_despesas_mes, name='gerar_despesas_mes'),
    
    # Compras Parceladas
    path('parcelados/', views.lista_parcelados, name='lista_parcelados'),
    path('parcelados/novo/', views.criar_parcelado, name='criar_parcelado'),
    path('parcelados/<int:parcelado_id>/', views.detalhe_parcelado, name='detalhe_parcelado'),
    
    # Faturamento e Tributos
    path('faturamento/', views.lista_faturamento, name='lista_faturamento'),
    path('faturamento/novo/', views.criar_faturamento, name='criar_faturamento'),
    path('faturamento/<int:faturamento_id>/gerar-tributo/', views.gerar_tributo, name='gerar_tributo'),
    path('faturamento/calcular-automatico/', views.calcular_faturamento_automatico, name='calcular_faturamento_automatico'),
    
    # Categorias
    path('categorias/', views.lista_categorias_despesa, name='lista_categorias'),
    path('categorias/nova/', views.criar_categoria_despesa, name='criar_categoria'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria_despesa, name='editar_categoria'),
    path('categorias/<int:categoria_id>/deletar/', views.deletar_categoria_despesa, name='deletar_categoria'),
    
    # Configurações
    path('configuracoes/', views.configuracoes_financeiro, name='configuracoes'),
    
    # APIs
    path('api/stats/', views.api_stats_financeiro, name='api_stats'),
    path('api/grafico-mensal/', views.api_grafico_mensal, name='api_grafico_mensal'),
]