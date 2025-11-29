from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # ==========================================
    # DASHBOARD FINANCEIRO
    # ==========================================
    path('', views.dashboard_financeiro, name='dashboard'),
    
    # ==========================================
    # CONTAS A PAGAR (DESPESAS)
    # ==========================================
    path('contas/', views.lista_contas_pagar, name='lista_contas'),
    path('contas/nova/', views.criar_conta_pagar, name='criar_conta'),
    path('contas/<int:conta_id>/', views.detalhe_conta_pagar, name='detalhe_conta'),
    path('contas/<int:conta_id>/editar/', views.editar_conta_pagar, name='editar_conta'),
    path('contas/<int:conta_id>/pagar/', views.pagar_conta, name='pagar_conta'),
    path('contas/<int:conta_id>/cancelar/', views.cancelar_conta, name='cancelar_conta'),
    
    # ==========================================
    # CONTAS A RECEBER (RECEITAS) - NOVO
    # ==========================================
    path('receitas/', views.lista_contas_receber, name='lista_receitas'),
    path('receitas/nova/', views.criar_conta_receber, name='criar_receita'),
    path('receitas/<int:conta_id>/', views.detalhe_conta_receber, name='detalhe_receita'),
    path('receitas/<int:conta_id>/editar/', views.editar_conta_receber, name='editar_receita'),
    path('receitas/<int:conta_id>/receber/', views.receber_conta, name='receber_conta'),
    path('receitas/<int:conta_id>/cancelar/', views.cancelar_receita, name='cancelar_receita'),
    
    # ==========================================
    # VENDAS PARCELADAS (CREDIÁRIO) - NOVO
    # ==========================================
    path('crediario/', views.lista_vendas_parceladas, name='lista_crediario'),
    path('crediario/novo/', views.criar_venda_parcelada, name='criar_crediario'),
    path('crediario/<int:venda_id>/', views.detalhe_venda_parcelada, name='detalhe_crediario'),
    path('crediario/<int:venda_id>/cancelar/', views.cancelar_venda_parcelada, name='cancelar_crediario'),
    
    # ==========================================
    # DESPESAS FIXAS
    # ==========================================
    path('despesas-fixas/', views.lista_despesas_fixas, name='lista_despesas_fixas'),
    path('despesas-fixas/nova/', views.criar_despesa_fixa, name='criar_despesa_fixa'),
    path('despesas-fixas/<int:despesa_id>/editar/', views.editar_despesa_fixa, name='editar_despesa_fixa'),
    path('despesas-fixas/<int:despesa_id>/deletar/', views.deletar_despesa_fixa, name='deletar_despesa_fixa'),
    path('despesas-fixas/gerar-mes/', views.gerar_despesas_mes, name='gerar_despesas_mes'),
    
    # ==========================================
    # COMPRAS PARCELADAS
    # ==========================================
    path('parcelados/', views.lista_parcelados, name='lista_parcelados'),
    path('parcelados/novo/', views.criar_parcelado, name='criar_parcelado'),
    path('parcelados/<int:parcelado_id>/', views.detalhe_parcelado, name='detalhe_parcelado'),
    
    # ==========================================
    # FATURAMENTO E TRIBUTOS
    # ==========================================
    path('faturamento/', views.lista_faturamento, name='lista_faturamento'),
    path('faturamento/novo/', views.criar_faturamento, name='criar_faturamento'),
    path('faturamento/<int:faturamento_id>/gerar-tributo/', views.gerar_tributo, name='gerar_tributo'),
    path('faturamento/calcular-automatico/', views.calcular_faturamento_automatico, name='calcular_faturamento_automatico'),
    
    # ==========================================
    # CATEGORIAS DE DESPESA
    # ==========================================
    path('categorias/', views.lista_categorias_despesa, name='lista_categorias'),
    path('categorias/nova/', views.criar_categoria_despesa, name='criar_categoria'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria_despesa, name='editar_categoria'),
    path('categorias/<int:categoria_id>/deletar/', views.deletar_categoria_despesa, name='deletar_categoria'),
    
    # ==========================================
    # CATEGORIAS DE RECEITA - NOVO
    # ==========================================
    path('categorias-receita/', views.lista_categorias_receita, name='lista_categorias_receita'),
    path('categorias-receita/nova/', views.criar_categoria_receita, name='criar_categoria_receita'),
    path('categorias-receita/<int:categoria_id>/editar/', views.editar_categoria_receita, name='editar_categoria_receita'),
    path('categorias-receita/<int:categoria_id>/deletar/', views.deletar_categoria_receita, name='deletar_categoria_receita'),
    
    # ==========================================
    # CONFIGURAÇÕES
    # ==========================================
    path('configuracoes/', views.configuracoes_financeiro, name='configuracoes'),
    
    # ==========================================
    # APIs
    # ==========================================
    path('api/stats/', views.api_stats_financeiro, name='api_stats'),
    path('api/grafico-mensal/', views.api_grafico_mensal, name='api_grafico_mensal'),
    path('api/cliente/<int:cliente_id>/pendencias/', views.api_pendencias_cliente, name='api_pendencias_cliente'),
    path('api/fornecedor/<int:fornecedor_id>/pendencias/', views.api_pendencias_fornecedor, name='api_pendencias_fornecedor'),

    # ==========================================
    # FLUXO DE CAIXA
    # ==========================================
    path('caixa/', views.dashboard_caixa, name='dashboard_caixa'),
    path('caixa/movimentacoes/', views.lista_movimentacoes, name='lista_movimentacoes'),
    path('caixa/sangria/', views.registrar_sangria, name='registrar_sangria'),
    path('caixa/suprimento/', views.registrar_suprimento, name='registrar_suprimento'),
    path('caixa/transferencia/', views.registrar_transferencia, name='registrar_transferencia'),
    path('caixa/fechamento/', views.fechamento_caixa, name='fechamento_caixa'),
    path('caixa/fechamento/historico/', views.historico_fechamentos, name='historico_fechamentos'),
    path('caixa/cartoes-pendentes/', views.cartoes_pendentes, name='cartoes_pendentes'),
    path('caixa/cartoes-pendentes/confirmar/<int:recebimento_id>/', views.confirmar_recebimento_cartao, name='confirmar_recebimento_cartao'),
    path('caixa/contas/', views.gerenciar_contas_financeiras, name='gerenciar_contas'),
    path('caixa/contas/<int:conta_id>/atualizar-saldo/', views.atualizar_saldo_inicial, name='atualizar_saldo_inicial'),
    
    # APIs do Caixa
    path('caixa/api/resumo/', views.api_resumo_caixa, name='api_resumo_caixa'),
    path('caixa/api/grafico-fluxo/', views.api_grafico_fluxo, name='api_grafico_fluxo'),
    path('caixa/api/processar-vendas-dia/', views.api_processar_vendas_dia, name='api_processar_vendas_dia'),
]