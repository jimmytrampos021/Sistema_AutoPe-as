from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncMonth, Coalesce
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from calendar import monthrange
import json

from .models import (
    CategoriaDespesa, FormaPagamento, DespesaFixa, ContaPagar,
    CompraParcelada, FaturamentoMensal, ConfiguracaoTributo,
    # NOVOS
    CategoriaReceita, ContaReceber, VendaParcelada, ConfiguracaoFinanceiro
)
from clientes.models import Cliente
from estoque.models import Fornecedor

# ==========================================
# DASHBOARD FINANCEIRO
# ==========================================
@login_required
def dashboard_financeiro(request):
    """Dashboard principal do módulo financeiro"""
    hoje = date.today()
    primeiro_dia_mes = date(hoje.year, hoje.month, 1)
    
    # Contas do mês atual
    contas_mes = ContaPagar.objects.filter(
        data_vencimento__year=hoje.year,
        data_vencimento__month=hoje.month
    ).exclude(status='CANCELADO')
    
    # Estatísticas gerais
    stats = {
        'total_contas_mes': contas_mes.aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'total_pagas_mes': contas_mes.filter(status='PAGO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'total_pendentes_mes': contas_mes.filter(status='PENDENTE').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'total_atrasadas': ContaPagar.objects.filter(status='PENDENTE', data_vencimento__lt=hoje).exclude(status='CANCELADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'qtd_atrasadas': ContaPagar.objects.filter(status='PENDENTE', data_vencimento__lt=hoje).exclude(status='CANCELADO').count(),
    }
    
    # Contas vencendo nos próximos 7 dias
    proximos_7_dias = hoje + timedelta(days=7)
    contas_proximas = ContaPagar.objects.filter(
        data_vencimento__gte=hoje,
        data_vencimento__lte=proximos_7_dias,
        status='PENDENTE'
    ).order_by('data_vencimento')[:10]
    
    # Contas atrasadas
    contas_atrasadas = ContaPagar.objects.filter(
        data_vencimento__lt=hoje,
        status='PENDENTE'
    ).order_by('data_vencimento')[:10]
    
    # Despesas por categoria do mês
    despesas_categoria = contas_mes.values(
        'categoria__nome', 'categoria__cor', 'categoria__icone'
    ).annotate(
        total=Sum('valor')
    ).order_by('-total')[:8]
    
    # Faturamento dos últimos 6 meses
    faturamentos = FaturamentoMensal.objects.order_by('-ano', '-mes')[:6]
    
    # Despesas fixas vs variáveis do mês
    despesas_fixas_mes = contas_mes.filter(tipo='FIXA').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    despesas_variaveis_mes = contas_mes.filter(tipo='VARIAVEL').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    despesas_parceladas_mes = contas_mes.filter(tipo='PARCELADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    tributos_mes = contas_mes.filter(tipo='TRIBUTO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    
    # Dados para gráfico mensal (últimos 6 meses)
    dados_grafico = []
    for i in range(5, -1, -1):
        mes_ref = hoje - timedelta(days=30 * i)
        mes = mes_ref.month
        ano = mes_ref.year
        
        total_despesas = ContaPagar.objects.filter(
            data_vencimento__year=ano,
            data_vencimento__month=mes
        ).exclude(status='CANCELADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
        
        faturamento = FaturamentoMensal.objects.filter(mes=mes, ano=ano).first()
        valor_faturamento = faturamento.valor_faturamento if faturamento else Decimal('0')
        
        dados_grafico.append({
            'mes': f"{mes:02d}/{ano}",
            'despesas': float(total_despesas),
            'faturamento': float(valor_faturamento),
            'lucro': float(valor_faturamento - total_despesas)
        })
    
    context = {
        'stats': stats,
        'contas_proximas': contas_proximas,
        'contas_atrasadas': contas_atrasadas,
        'despesas_categoria': despesas_categoria,
        'faturamentos': faturamentos,
        'despesas_fixas_mes': despesas_fixas_mes,
        'despesas_variaveis_mes': despesas_variaveis_mes,
        'despesas_parceladas_mes': despesas_parceladas_mes,
        'tributos_mes': tributos_mes,
        'dados_grafico': json.dumps(dados_grafico),
        'mes_atual': hoje.strftime('%B/%Y'),
    }
    
    return render(request, 'financeiro/dashboard.html', context)


# ==========================================
# CONTAS A PAGAR
# ==========================================
@login_required
def lista_contas_pagar(request):
    """Lista todas as contas a pagar com filtros"""
    # Filtros
    busca = request.GET.get('busca', '')
    status_filtro = request.GET.get('status', '')
    tipo_filtro = request.GET.get('tipo', '')
    categoria_id = request.GET.get('categoria', '')
    mes = request.GET.get('mes', '')
    ano = request.GET.get('ano', '')
    
    contas = ContaPagar.objects.all().select_related('categoria', 'forma_pagamento')
    
    # Aplicar filtros
    if busca:
        contas = contas.filter(descricao__icontains=busca)
    
    if status_filtro:
        contas = contas.filter(status=status_filtro)
    
    if tipo_filtro:
        contas = contas.filter(tipo=tipo_filtro)
    
    if categoria_id:
        contas = contas.filter(categoria_id=categoria_id)
    
    if mes and ano:
        contas = contas.filter(data_vencimento__month=mes, data_vencimento__year=ano)
    elif ano:
        contas = contas.filter(data_vencimento__year=ano)
    
    # Atualizar status de contas atrasadas
    hoje = date.today()
    ContaPagar.objects.filter(
        status='PENDENTE',
        data_vencimento__lt=hoje
    ).update(status='ATRASADO')
    
    # Ordenação
    contas = contas.order_by('data_vencimento')
    
    # Estatísticas
    stats = {
        'total': contas.aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'pendentes': contas.filter(status='PENDENTE').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'pagas': contas.filter(status='PAGO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'atrasadas': contas.filter(status='ATRASADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'qtd_total': contas.count(),
        'qtd_pendentes': contas.filter(status='PENDENTE').count(),
        'qtd_atrasadas': contas.filter(status='ATRASADO').count(),
    }
    
    # Paginação
    paginator = Paginator(contas, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros
    categorias = CategoriaDespesa.objects.filter(ativo=True).order_by('nome')
    anos_disponiveis = ContaPagar.objects.dates('data_vencimento', 'year', order='DESC')
    
    # Formas de pagamento para o modal
    formas_pagamento = FormaPagamento.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'categorias': categorias,
        'anos_disponiveis': anos_disponiveis,
        'formas_pagamento': formas_pagamento,
        'today': date.today(),
        'busca': busca,
        'status_filtro': status_filtro,
        'tipo_filtro': tipo_filtro,
        'categoria_selecionada': categoria_id,
        'mes_selecionado': mes,
        'ano_selecionado': ano,
    }
    
    return render(request, 'financeiro/contas_lista.html', context)
@login_required
def criar_conta_pagar(request):
    """Criar nova conta a pagar"""
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(CategoriaDespesa, id=request.POST.get('categoria'))
            
            conta = ContaPagar.objects.create(
                descricao=request.POST.get('descricao'),
                categoria=categoria,
                tipo=request.POST.get('tipo', 'VARIAVEL'),
                valor=Decimal(request.POST.get('valor', '0').replace(',', '.')),
                data_vencimento=request.POST.get('data_vencimento'),
                observacoes=request.POST.get('observacoes', ''),
                usuario_cadastro=request.user
            )
            
            # Upload de comprovante
            if 'comprovante' in request.FILES:
                conta.comprovante = request.FILES['comprovante']
                conta.save()
            
            messages.success(request, f'Conta "{conta.descricao}" criada com sucesso!')
            return redirect('financeiro:lista_contas')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')
    
    categorias = CategoriaDespesa.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'financeiro/conta_form.html', context)


@login_required
def editar_conta_pagar(request, conta_id):
    """Editar conta a pagar"""
    conta = get_object_or_404(ContaPagar, id=conta_id)
    
    if request.method == 'POST':
        try:
            conta.descricao = request.POST.get('descricao')
            conta.categoria = get_object_or_404(CategoriaDespesa, id=request.POST.get('categoria'))
            conta.tipo = request.POST.get('tipo', 'VARIAVEL')
            conta.valor = Decimal(request.POST.get('valor', '0').replace(',', '.'))
            conta.data_vencimento = request.POST.get('data_vencimento')
            conta.observacoes = request.POST.get('observacoes', '')
            
            if 'comprovante' in request.FILES:
                conta.comprovante = request.FILES['comprovante']
            
            conta.save()
            
            messages.success(request, f'Conta "{conta.descricao}" atualizada com sucesso!')
            return redirect('financeiro:lista_contas')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar conta: {str(e)}')
    
    categorias = CategoriaDespesa.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    context = {
        'conta': conta,
        'categorias': categorias,
        'editando': True,
    }
    
    return render(request, 'financeiro/conta_form.html', context)


@login_required
def detalhe_conta_pagar(request, conta_id):
    """Detalhes de uma conta a pagar"""
    conta = get_object_or_404(ContaPagar.objects.select_related(
        'categoria', 'forma_pagamento', 'despesa_fixa', 'compra_parcelada', 'faturamento_referencia'
    ), id=conta_id)
    
    context = {
        'conta': conta,
    }
    
    return render(request, 'financeiro/conta_detalhe.html', context)


@login_required
def pagar_conta(request, conta_id):
    """Marcar conta como paga"""
    conta = get_object_or_404(ContaPagar, id=conta_id)
    
    if request.method == 'POST':
        try:
            forma_pagamento_id = request.POST.get('forma_pagamento')
            if forma_pagamento_id:
                conta.forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
            
            data_pagamento = request.POST.get('data_pagamento')
            conta.data_pagamento = data_pagamento if data_pagamento else date.today()
            conta.status = 'PAGO'
            
            if 'comprovante' in request.FILES:
                conta.comprovante = request.FILES['comprovante']
            
            conta.save()
            
            messages.success(request, f'Conta "{conta.descricao}" marcada como paga!')
            
        except Exception as e:
            messages.error(request, f'Erro ao pagar conta: {str(e)}')
    
    return redirect('financeiro:lista_contas')


@login_required
def cancelar_conta(request, conta_id):
    """Cancelar conta a pagar"""
    conta = get_object_or_404(ContaPagar, id=conta_id)
    
    if request.method == 'POST':
        conta.status = 'CANCELADO'
        conta.save()
        messages.success(request, f'Conta "{conta.descricao}" cancelada!')
    
    return redirect('financeiro:lista_contas')


# ==========================================
# DESPESAS FIXAS
# ==========================================
@login_required
def lista_despesas_fixas(request):
    """Lista todas as despesas fixas"""
    despesas = DespesaFixa.objects.filter(ativo=True).select_related('categoria').order_by('dia_vencimento')
    
    # Total mensal de despesas fixas
    total_mensal = despesas.aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    
    context = {
        'despesas': despesas,
        'total_mensal': total_mensal,
        'today': date.today(),
    }
    
    return render(request, 'financeiro/despesas_fixas_lista.html', context)


@login_required
def criar_despesa_fixa(request):
    """Criar nova despesa fixa"""
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(CategoriaDespesa, id=request.POST.get('categoria'))
            
            despesa = DespesaFixa.objects.create(
                descricao=request.POST.get('descricao'),
                categoria=categoria,
                valor=Decimal(request.POST.get('valor', '0').replace(',', '.')),
                dia_vencimento=int(request.POST.get('dia_vencimento', 1)),
                observacoes=request.POST.get('observacoes', ''),
                data_inicio=request.POST.get('data_inicio') or date.today(),
                data_fim=request.POST.get('data_fim') or None,
            )
            
            messages.success(request, f'Despesa fixa "{despesa.descricao}" criada com sucesso!')
            return redirect('financeiro:lista_despesas_fixas')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar despesa fixa: {str(e)}')
    
    categorias = CategoriaDespesa.objects.filter(ativo=True, tipo__in=['FIXA', 'AMBOS']).order_by('ordem', 'nome')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'financeiro/despesa_fixa_form.html', context)


@login_required
def editar_despesa_fixa(request, despesa_id):
    """Editar despesa fixa"""
    despesa = get_object_or_404(DespesaFixa, id=despesa_id)
    
    if request.method == 'POST':
        try:
            despesa.descricao = request.POST.get('descricao')
            despesa.categoria = get_object_or_404(CategoriaDespesa, id=request.POST.get('categoria'))
            despesa.valor = Decimal(request.POST.get('valor', '0').replace(',', '.'))
            despesa.dia_vencimento = int(request.POST.get('dia_vencimento', 1))
            despesa.observacoes = request.POST.get('observacoes', '')
            despesa.data_fim = request.POST.get('data_fim') or None
            despesa.save()
            
            messages.success(request, f'Despesa fixa "{despesa.descricao}" atualizada!')
            return redirect('financeiro:lista_despesas_fixas')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    categorias = CategoriaDespesa.objects.filter(ativo=True, tipo__in=['FIXA', 'AMBOS']).order_by('ordem', 'nome')
    
    context = {
        'despesa': despesa,
        'categorias': categorias,
        'editando': True,
    }
    
    return render(request, 'financeiro/despesa_fixa_form.html', context)


@login_required
def deletar_despesa_fixa(request, despesa_id):
    """Desativar despesa fixa"""
    despesa = get_object_or_404(DespesaFixa, id=despesa_id)
    
    if request.method == 'POST':
        despesa.ativo = False
        despesa.save()
        messages.success(request, f'Despesa fixa "{despesa.descricao}" desativada!')
    
    return redirect('financeiro:lista_despesas_fixas')


@login_required
def gerar_despesas_mes(request):
    """Gerar contas a pagar baseado nas despesas fixas para um mês"""
    if request.method == 'POST':
        mes = int(request.POST.get('mes', date.today().month))
        ano = int(request.POST.get('ano', date.today().year))
        
        despesas_fixas = DespesaFixa.objects.filter(ativo=True)
        contas_criadas = 0
        
        for despesa in despesas_fixas:
            conta = despesa.gerar_conta_mes(mes, ano)
            if conta:
                contas_criadas += 1
        
        if contas_criadas > 0:
            messages.success(request, f'{contas_criadas} contas geradas para {mes:02d}/{ano}!')
        else:
            messages.info(request, f'Nenhuma conta nova gerada para {mes:02d}/{ano}.')
    
    return redirect('financeiro:lista_despesas_fixas')


# ==========================================
# COMPRAS PARCELADAS
# ==========================================
@login_required
def lista_parcelados(request):
    """Lista todas as compras parceladas"""
    parcelados = CompraParcelada.objects.all().select_related('categoria').order_by('-data_cadastro')
    
    context = {
        'parcelados': parcelados,
    }
    
    return render(request, 'financeiro/parcelados_lista.html', context)


@login_required
def criar_parcelado(request):
    """Criar nova compra parcelada"""
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(CategoriaDespesa, id=request.POST.get('categoria'))
            
            parcelado = CompraParcelada.objects.create(
                descricao=request.POST.get('descricao'),
                categoria=categoria,
                valor_total=Decimal(request.POST.get('valor_total', '0').replace(',', '.')),
                numero_parcelas=int(request.POST.get('numero_parcelas', 1)),
                data_primeira_parcela=request.POST.get('data_primeira_parcela'),
                observacoes=request.POST.get('observacoes', ''),
            )
            
            # Gerar as parcelas automaticamente
            parcelado.gerar_parcelas()
            
            messages.success(request, f'Compra parcelada "{parcelado.descricao}" criada com {parcelado.numero_parcelas} parcelas!')
            return redirect('financeiro:lista_parcelados')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar compra parcelada: {str(e)}')
    
    categorias = CategoriaDespesa.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'financeiro/parcelado_form.html', context)


@login_required
def detalhe_parcelado(request, parcelado_id):
    """Detalhes de uma compra parcelada"""
    parcelado = get_object_or_404(CompraParcelada.objects.select_related('categoria'), id=parcelado_id)
    parcelas = parcelado.parcelas.all().order_by('parcela_atual')
    
    context = {
        'parcelado': parcelado,
        'parcelas': parcelas,
    }
    
    return render(request, 'financeiro/parcelado_detalhe.html', context)


# ==========================================
# FATURAMENTO E TRIBUTOS
# ==========================================
@login_required
def lista_faturamento(request):
    """Lista faturamentos mensais"""
    faturamentos = FaturamentoMensal.objects.all().order_by('-ano', '-mes')
    
    # Configuração atual do tributo
    config_tributo = ConfiguracaoTributo.get_configuracao_ativa()
    
    context = {
        'faturamentos': faturamentos,
        'config_tributo': config_tributo,
    }
    
    return render(request, 'financeiro/faturamento_lista.html', context)


@login_required
def criar_faturamento(request):
    """Criar/atualizar faturamento mensal"""
    if request.method == 'POST':
        try:
            mes = int(request.POST.get('mes'))
            ano = int(request.POST.get('ano'))
            valor = Decimal(request.POST.get('valor_faturamento', '0').replace(',', '.'))
            dia_vencimento = int(request.POST.get('dia_vencimento', 20))
            
            # Atualizar configuração do dia de vencimento
            config = ConfiguracaoTributo.get_configuracao_ativa()
            config.dia_vencimento = dia_vencimento
            config.save()
            
            faturamento, created = FaturamentoMensal.objects.update_or_create(
                mes=mes,
                ano=ano,
                defaults={
                    'valor_faturamento': valor,
                    'calculado_automaticamente': False,
                    'observacoes': request.POST.get('observacoes', ''),
                }
            )
            
            action = 'criado' if created else 'atualizado'
            messages.success(request, f'Faturamento de {mes:02d}/{ano} {action} com sucesso!')
            return redirect('financeiro:lista_faturamento')
            
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
    
    config_tributo = ConfiguracaoTributo.get_configuracao_ativa()
    
    context = {
        'config_tributo': config_tributo,
        'mes_atual': date.today().month,
        'ano_atual': date.today().year,
    }
    
    return render(request, 'financeiro/faturamento_form.html', context)


@login_required
def gerar_tributo(request, faturamento_id):
    """Gerar conta a pagar do tributo"""
    faturamento = get_object_or_404(FaturamentoMensal, id=faturamento_id)
    
    if request.method == 'POST':
        if faturamento.tributo_gerado:
            messages.warning(request, 'Tributo já foi gerado para este faturamento!')
        else:
            conta = faturamento.gerar_tributo()
            if conta:
                messages.success(request, f'Tributo de R$ {conta.valor} gerado com vencimento em {conta.data_vencimento.strftime("%d/%m/%Y")}!')
            else:
                messages.error(request, 'Erro ao gerar tributo.')
    
    return redirect('financeiro:lista_faturamento')


@login_required
def calcular_faturamento_automatico(request):
    """Calcular faturamento baseado nas vendas do sistema"""
    if request.method == 'POST':
        mes = int(request.POST.get('mes', date.today().month))
        ano = int(request.POST.get('ano', date.today().year))
        
        valor = FaturamentoMensal.calcular_faturamento_vendas(mes, ano)
        
        if valor > 0:
            faturamento, created = FaturamentoMensal.objects.update_or_create(
                mes=mes,
                ano=ano,
                defaults={
                    'valor_faturamento': valor,
                    'calculado_automaticamente': True,
                }
            )
            messages.success(request, f'Faturamento de R$ {valor} calculado para {mes:02d}/{ano}!')
        else:
            messages.warning(request, f'Nenhuma venda encontrada para {mes:02d}/{ano}.')
    
    return redirect('financeiro:lista_faturamento')


# ==========================================
# CATEGORIAS DE DESPESA
# ==========================================
@login_required
def lista_categorias_despesa(request):
    """Lista todas as categorias de despesa"""
    categorias = CategoriaDespesa.objects.all().order_by('ordem', 'nome')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'financeiro/categorias_lista.html', context)


@login_required
def criar_categoria_despesa(request):
    """Criar nova categoria de despesa"""
    if request.method == 'POST':
        try:
            categoria = CategoriaDespesa.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo', 'AMBOS'),
                icone=request.POST.get('icone', 'bi-folder'),
                cor=request.POST.get('cor', '#6c757d'),
                ordem=int(request.POST.get('ordem', 0)),
            )
            
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('financeiro:lista_categorias')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar categoria: {str(e)}')
    
    return render(request, 'financeiro/categoria_form.html', {})


@login_required
def editar_categoria_despesa(request, categoria_id):
    """Editar categoria de despesa"""
    categoria = get_object_or_404(CategoriaDespesa, id=categoria_id)
    
    if request.method == 'POST':
        try:
            categoria.nome = request.POST.get('nome')
            categoria.tipo = request.POST.get('tipo', 'AMBOS')
            categoria.icone = request.POST.get('icone', 'bi-folder')
            categoria.cor = request.POST.get('cor', '#6c757d')
            categoria.ordem = int(request.POST.get('ordem', 0))
            categoria.ativo = request.POST.get('ativo') == 'on'
            categoria.save()
            
            messages.success(request, f'Categoria "{categoria.nome}" atualizada!')
            return redirect('financeiro:lista_categorias')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    context = {
        'categoria': categoria,
        'editando': True,
    }
    
    return render(request, 'financeiro/categoria_form.html', context)


@login_required
def deletar_categoria_despesa(request, categoria_id):
    """Desativar categoria de despesa"""
    categoria = get_object_or_404(CategoriaDespesa, id=categoria_id)
    
    if request.method == 'POST':
        # Verificar se há contas usando esta categoria
        if ContaPagar.objects.filter(categoria=categoria).exists():
            categoria.ativo = False
            categoria.save()
            messages.warning(request, f'Categoria "{categoria.nome}" desativada (possui contas vinculadas).')
        else:
            nome = categoria.nome
            categoria.delete()
            messages.success(request, f'Categoria "{nome}" excluída!')
    
    return redirect('financeiro:lista_categorias')


# ==========================================
# CONFIGURAÇÕES
# ==========================================
@login_required
def configuracoes_financeiro(request):
    """Configurações do módulo financeiro"""
    config_tributo = ConfiguracaoTributo.get_configuracao_ativa()
    formas_pagamento = FormaPagamento.objects.all().order_by('nome')
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        if acao == 'tributo':
            config_tributo.aliquota = Decimal(request.POST.get('aliquota', '4.00').replace(',', '.'))
            config_tributo.dia_vencimento = int(request.POST.get('dia_vencimento', 20))
            config_tributo.save()
            messages.success(request, 'Configuração de tributo atualizada!')
        
        elif acao == 'forma_pagamento':
            FormaPagamento.objects.create(
                nome=request.POST.get('nome'),
                icone=request.POST.get('icone', 'bi-wallet'),
            )
            messages.success(request, 'Forma de pagamento criada!')
        
        return redirect('financeiro:configuracoes')
    
    context = {
        'config_tributo': config_tributo,
        'formas_pagamento': formas_pagamento,
    }
    
    return render(request, 'financeiro/configuracoes.html', context)


# ==========================================
# APIs
# ==========================================
@login_required
def api_stats_financeiro(request):
    """API com estatísticas do financeiro"""
    hoje = date.today()
    
    stats = {
        'total_pendente': float(ContaPagar.objects.filter(status='PENDENTE').aggregate(
            total=Coalesce(Sum('valor'), Decimal('0')))['total']),
        'total_atrasado': float(ContaPagar.objects.filter(status='ATRASADO').aggregate(
            total=Coalesce(Sum('valor'), Decimal('0')))['total']),
        'qtd_atrasadas': ContaPagar.objects.filter(status='ATRASADO').count(),
    }
    
    return JsonResponse(stats)


@login_required
def api_grafico_mensal(request):
    """API com dados para gráfico mensal"""
    hoje = date.today()
    dados = []
    
    for i in range(11, -1, -1):
        mes_ref = hoje - timedelta(days=30 * i)
        mes = mes_ref.month
        ano = mes_ref.year
        
        despesas = ContaPagar.objects.filter(
            data_vencimento__year=ano,
            data_vencimento__month=mes
        ).exclude(status='CANCELADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
        
        faturamento = FaturamentoMensal.objects.filter(mes=mes, ano=ano).first()
        valor_fat = faturamento.valor_faturamento if faturamento else Decimal('0')
        
        dados.append({
            'mes': f"{mes:02d}/{ano}",
            'despesas': float(despesas),
            'faturamento': float(valor_fat),
        })
    
    return JsonResponse({'dados': dados})


# ==========================================
# CONTAS A RECEBER (RECEITAS)
# ==========================================

@login_required
def lista_contas_receber(request):
    """Lista todas as contas a receber com filtros"""
    busca = request.GET.get('busca', '')
    status_filtro = request.GET.get('status', '')
    tipo_filtro = request.GET.get('tipo', '')
    categoria_id = request.GET.get('categoria', '')
    cliente_id = request.GET.get('cliente', '')
    forma_cobranca = request.GET.get('forma_cobranca', '')
    mes = request.GET.get('mes', '')
    ano = request.GET.get('ano', '')
    
    contas = ContaReceber.objects.all().select_related(
        'categoria', 'cliente', 'venda', 'forma_pagamento', 'venda_parcelada'
    )
    
    if busca:
        contas = contas.filter(
            Q(descricao__icontains=busca) |
            Q(cliente__nome__icontains=busca) |
            Q(documento_referencia__icontains=busca)
        )
    
    if status_filtro:
        contas = contas.filter(status=status_filtro)
    
    if tipo_filtro:
        contas = contas.filter(tipo=tipo_filtro)
    
    if categoria_id:
        contas = contas.filter(categoria_id=categoria_id)
    
    if cliente_id:
        contas = contas.filter(cliente_id=cliente_id)
    
    if forma_cobranca:
        contas = contas.filter(forma_cobranca=forma_cobranca)
    
    if mes and ano:
        contas = contas.filter(data_vencimento__month=mes, data_vencimento__year=ano)
    elif ano:
        contas = contas.filter(data_vencimento__year=ano)
    
    # Atualizar status de contas atrasadas
    hoje = date.today()
    ContaReceber.objects.filter(
        status='PENDENTE',
        data_vencimento__lt=hoje
    ).update(status='ATRASADO')
    
    contas = contas.order_by('data_vencimento')
    
    # Estatísticas
    stats = {
        'total': contas.aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'pendentes': contas.filter(status='PENDENTE').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'recebidas': contas.filter(status='RECEBIDO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'atrasadas': contas.filter(status='ATRASADO').aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total'],
        'qtd_total': contas.count(),
        'qtd_pendentes': contas.filter(status='PENDENTE').count(),
        'qtd_atrasadas': contas.filter(status='ATRASADO').count(),
    }
    
    paginator = Paginator(contas, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categorias = CategoriaReceita.objects.filter(ativo=True).order_by('nome')
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    anos_disponiveis = ContaReceber.objects.dates('data_vencimento', 'year', order='DESC')
    formas_pagamento = FormaPagamento.objects.filter(
        Q(tipo='AMBOS') | Q(tipo='RECEITA'), ativo=True
    ).order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'categorias': categorias,
        'clientes': clientes,
        'anos_disponiveis': anos_disponiveis,
        'formas_pagamento': formas_pagamento,
        'today': date.today(),
        'busca': busca,
        'status_filtro': status_filtro,
        'tipo_filtro': tipo_filtro,
        'categoria_selecionada': categoria_id,
        'cliente_selecionado': cliente_id,
        'forma_cobranca_selecionada': forma_cobranca,
        'mes_selecionado': mes,
        'ano_selecionado': ano,
    }
    
    return render(request, 'financeiro/receitas_lista.html', context)


@login_required
def criar_conta_receber(request):
    """Criar nova conta a receber"""
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(CategoriaReceita, id=request.POST.get('categoria'))
            
            cliente = None
            if request.POST.get('cliente'):
                cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
            
            conta = ContaReceber.objects.create(
                descricao=request.POST.get('descricao'),
                categoria=categoria,
                tipo=request.POST.get('tipo', 'AVULSO'),
                valor=Decimal(request.POST.get('valor', '0').replace(',', '.')),
                data_vencimento=request.POST.get('data_vencimento'),
                forma_cobranca=request.POST.get('forma_cobranca', 'FIADO'),
                cliente=cliente,
                documento_referencia=request.POST.get('documento_referencia', ''),
                aplica_juros=request.POST.get('aplica_juros') == 'on',
                percentual_juros_dia=Decimal(request.POST.get('percentual_juros_dia', '0').replace(',', '.')),
                aplica_multa=request.POST.get('aplica_multa') == 'on',
                percentual_multa=Decimal(request.POST.get('percentual_multa', '0').replace(',', '.')),
                observacoes=request.POST.get('observacoes', ''),
                usuario_cadastro=request.user
            )
            
            if 'comprovante' in request.FILES:
                conta.comprovante = request.FILES['comprovante']
                conta.save()
            
            messages.success(request, f'Receita "{conta.descricao}" criada com sucesso!')
            return redirect('financeiro:lista_receitas')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar receita: {str(e)}')
    
    categorias = CategoriaReceita.objects.filter(ativo=True).order_by('ordem', 'nome')
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    config = ConfiguracaoFinanceiro.get_config()
    
    context = {
        'categorias': categorias,
        'clientes': clientes,
        'config': config,
        'today': date.today(),
    }
    
    return render(request, 'financeiro/receita_form.html', context)


@login_required
def detalhe_conta_receber(request, conta_id):
    """Detalhes de uma conta a receber"""
    conta = get_object_or_404(
        ContaReceber.objects.select_related(
            'categoria', 'cliente', 'venda', 'ordem_servico', 
            'forma_pagamento', 'venda_parcelada', 'usuario_cadastro'
        ),
        id=conta_id
    )
    
    outras_parcelas = None
    if conta.venda_parcelada:
        outras_parcelas = conta.venda_parcelada.parcelas.exclude(id=conta_id).order_by('parcela_atual')
    
    formas_pagamento = FormaPagamento.objects.filter(
        Q(tipo='AMBOS') | Q(tipo='RECEITA'), ativo=True
    ).order_by('nome')
    
    context = {
        'conta': conta,
        'outras_parcelas': outras_parcelas,
        'formas_pagamento': formas_pagamento,
        'today': date.today(),
    }
    
    return render(request, 'financeiro/receita_detalhe.html', context)


@login_required
def editar_conta_receber(request, conta_id):
    """Editar conta a receber"""
    conta = get_object_or_404(ContaReceber, id=conta_id)
    
    if conta.status == 'RECEBIDO':
        messages.warning(request, 'Não é possível editar uma receita já recebida.')
        return redirect('financeiro:detalhe_receita', conta_id=conta_id)
    
    if request.method == 'POST':
        try:
            conta.descricao = request.POST.get('descricao')
            conta.categoria = get_object_or_404(CategoriaReceita, id=request.POST.get('categoria'))
            conta.tipo = request.POST.get('tipo', 'AVULSO')
            conta.valor = Decimal(request.POST.get('valor', '0').replace(',', '.'))
            conta.data_vencimento = request.POST.get('data_vencimento')
            conta.forma_cobranca = request.POST.get('forma_cobranca', 'FIADO')
            
            if request.POST.get('cliente'):
                conta.cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
            else:
                conta.cliente = None
            
            conta.documento_referencia = request.POST.get('documento_referencia', '')
            conta.aplica_juros = request.POST.get('aplica_juros') == 'on'
            conta.percentual_juros_dia = Decimal(request.POST.get('percentual_juros_dia', '0').replace(',', '.'))
            conta.aplica_multa = request.POST.get('aplica_multa') == 'on'
            conta.percentual_multa = Decimal(request.POST.get('percentual_multa', '0').replace(',', '.'))
            conta.observacoes = request.POST.get('observacoes', '')
            
            if 'comprovante' in request.FILES:
                conta.comprovante = request.FILES['comprovante']
            
            conta.save()
            
            messages.success(request, f'Receita "{conta.descricao}" atualizada!')
            return redirect('financeiro:lista_receitas')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    categorias = CategoriaReceita.objects.filter(ativo=True).order_by('ordem', 'nome')
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'conta': conta,
        'categorias': categorias,
        'clientes': clientes,
        'editando': True,
    }
    
    return render(request, 'financeiro/receita_form.html', context)


@login_required
def receber_conta(request, conta_id):
    """Registrar recebimento de uma conta"""
    conta = get_object_or_404(ContaReceber, id=conta_id)
    
    if request.method == 'POST':
        try:
            conta.calcular_juros_multa()
            
            conta.data_recebimento = request.POST.get('data_recebimento') or date.today()
            
            if request.POST.get('forma_pagamento'):
                conta.forma_pagamento = get_object_or_404(
                    FormaPagamento, id=request.POST.get('forma_pagamento')
                )
            
            valor_recebido = request.POST.get('valor_recebido', '')
            if valor_recebido:
                conta.valor_recebido = Decimal(valor_recebido.replace(',', '.'))
            else:
                conta.valor_recebido = conta.valor_total_devido
            
            conta.status = 'RECEBIDO'
            conta.save()
            
            messages.success(request, f'Recebimento de R$ {conta.valor_recebido:.2f} registrado!')
            
        except Exception as e:
            messages.error(request, f'Erro ao registrar recebimento: {str(e)}')
    
    return redirect('financeiro:lista_receitas')


@login_required
def cancelar_receita(request, conta_id):
    """Cancelar conta a receber"""
    conta = get_object_or_404(ContaReceber, id=conta_id)
    
    if request.method == 'POST':
        conta.status = 'CANCELADO'
        conta.save()
        messages.success(request, f'Receita "{conta.descricao}" cancelada!')
    
    return redirect('financeiro:lista_receitas')


# ==========================================
# VENDAS PARCELADAS (CREDIÁRIO)
# ==========================================

@login_required
def lista_vendas_parceladas(request):
    """Lista todas as vendas parceladas (crediário)"""
    busca = request.GET.get('busca', '')
    cliente_id = request.GET.get('cliente', '')
    status_filtro = request.GET.get('status', '')
    
    vendas = VendaParcelada.objects.all().select_related(
        'cliente', 'categoria', 'venda'
    ).prefetch_related('parcelas')
    
    if busca:
        vendas = vendas.filter(
            Q(descricao__icontains=busca) |
            Q(cliente__nome__icontains=busca)
        )
    
    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)
    
    if status_filtro == 'com_atraso':
        vendas = vendas.filter(parcelas__status='ATRASADO').distinct()
    elif status_filtro == 'em_dia':
        vendas = vendas.exclude(parcelas__status='ATRASADO').filter(
            parcelas__status='PENDENTE'
        ).distinct()
    elif status_filtro == 'quitado':
        vendas = vendas.exclude(
            parcelas__status__in=['PENDENTE', 'ATRASADO']
        ).distinct()
    
    vendas = vendas.order_by('-data_cadastro')
    
    total_credito = vendas.aggregate(total=Coalesce(Sum('valor_total'), Decimal('0')))['total']
    total_recebido = ContaReceber.objects.filter(
        venda_parcelada__in=vendas,
        status='RECEBIDO'
    ).aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    total_pendente = ContaReceber.objects.filter(
        venda_parcelada__in=vendas,
        status__in=['PENDENTE', 'ATRASADO']
    ).aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    total_atrasado = ContaReceber.objects.filter(
        venda_parcelada__in=vendas,
        status='ATRASADO'
    ).aggregate(total=Coalesce(Sum('valor'), Decimal('0')))['total']
    
    stats = {
        'total_credito': total_credito,
        'total_recebido': total_recebido,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'qtd_clientes': vendas.values('cliente').distinct().count(),
    }
    
    paginator = Paginator(vendas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    clientes = Cliente.objects.filter(
        vendas_parceladas__isnull=False
    ).distinct().order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'clientes': clientes,
        'busca': busca,
        'cliente_selecionado': cliente_id,
        'status_filtro': status_filtro,
    }
    
    return render(request, 'financeiro/crediario_lista.html', context)


@login_required
def criar_venda_parcelada(request):
    """Criar nova venda parcelada (crediário)"""
    if request.method == 'POST':
        try:
            cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
            categoria = get_object_or_404(CategoriaReceita, id=request.POST.get('categoria'))
            
            venda_parcelada = VendaParcelada.objects.create(
                descricao=request.POST.get('descricao'),
                categoria=categoria,
                cliente=cliente,
                valor_total=Decimal(request.POST.get('valor_total', '0').replace(',', '.')),
                numero_parcelas=int(request.POST.get('numero_parcelas', 1)),
                data_primeira_parcela=request.POST.get('data_primeira_parcela'),
                intervalo_tipo=request.POST.get('intervalo_tipo', 'MENSAL'),
                intervalo_dias=int(request.POST.get('intervalo_dias', 30) or 30),
                forma_cobranca=request.POST.get('forma_cobranca', 'FIADO'),
                aplica_juros=request.POST.get('aplica_juros') == 'on',
                percentual_juros_dia=Decimal(request.POST.get('percentual_juros_dia', '0').replace(',', '.') or '0'),
                aplica_multa=request.POST.get('aplica_multa') == 'on',
                percentual_multa=Decimal(request.POST.get('percentual_multa', '0').replace(',', '.') or '0'),
                observacoes=request.POST.get('observacoes', ''),
                usuario_cadastro=request.user
            )
            
            venda_parcelada.gerar_parcelas()
            
            messages.success(
                request, 
                f'Crediário de {venda_parcelada.numero_parcelas}x de R$ {venda_parcelada.valor_parcela:.2f} '
                f'para {cliente.nome} criado com sucesso!'
            )
            return redirect('financeiro:detalhe_crediario', venda_id=venda_parcelada.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao criar crediário: {str(e)}')
    
    categorias = CategoriaReceita.objects.filter(ativo=True).order_by('ordem', 'nome')
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    config = ConfiguracaoFinanceiro.get_config()
    
    context = {
        'categorias': categorias,
        'clientes': clientes,
        'config': config,
        'today': date.today(),
    }
    
    return render(request, 'financeiro/crediario_form.html', context)



@login_required
def detalhe_venda_parcelada(request, venda_id):
    """Detalhes de uma venda parcelada com todas as parcelas"""
    venda = get_object_or_404(
        VendaParcelada.objects.select_related('cliente', 'categoria', 'venda'),
        id=venda_id
    )
    
    parcelas = venda.parcelas.all().order_by('parcela_atual')
    
    stats = {
        'total': venda.valor_total,
        'recebido': parcelas.filter(status='RECEBIDO').aggregate(
            total=Coalesce(Sum('valor'), Decimal('0'))
        )['total'],
        'pendente': parcelas.filter(status='PENDENTE').aggregate(
            total=Coalesce(Sum('valor'), Decimal('0'))
        )['total'],
        'atrasado': parcelas.filter(status='ATRASADO').aggregate(
            total=Coalesce(Sum('valor'), Decimal('0'))
        )['total'],
        'qtd_pagas': parcelas.filter(status='RECEBIDO').count(),
        'qtd_pendentes': parcelas.filter(status='PENDENTE').count(),
        'qtd_atrasadas': parcelas.filter(status='ATRASADO').count(),
    }
    
    formas_pagamento = FormaPagamento.objects.filter(
        Q(tipo='AMBOS') | Q(tipo='RECEITA'), ativo=True
    ).order_by('nome')
    
    context = {
        'venda': venda,
        'parcelas': parcelas,
        'stats': stats,
        'formas_pagamento': formas_pagamento,
        'today': date.today(),
    }
    
    return render(request, 'financeiro/crediario_detalhe.html', context)


@login_required
def cancelar_venda_parcelada(request, venda_id):
    """Cancelar venda parcelada e todas as parcelas pendentes"""
    venda = get_object_or_404(VendaParcelada, id=venda_id)
    
    if request.method == 'POST':
        parcelas_canceladas = venda.parcelas.filter(
            status__in=['PENDENTE', 'ATRASADO']
        ).update(status='CANCELADO')
        
        messages.success(
            request, 
            f'{parcelas_canceladas} parcelas canceladas do crediário de {venda.cliente.nome}!'
        )
    
    return redirect('financeiro:lista_crediario')


# ==========================================
# CATEGORIAS DE RECEITA
# ==========================================

@login_required
def lista_categorias_receita(request):
    """Lista todas as categorias de receita"""
    categorias = CategoriaReceita.objects.all().order_by('ordem', 'nome')
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'financeiro/categorias_receita_lista.html', context)


@login_required
def criar_categoria_receita(request):
    """Criar nova categoria de receita"""
    if request.method == 'POST':
        try:
            categoria = CategoriaReceita.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo', 'VENDA'),
                icone=request.POST.get('icone', 'bi-cash'),
                cor=request.POST.get('cor', '#22c55e'),
                ordem=int(request.POST.get('ordem', 0) or 0),
            )
            
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('financeiro:lista_categorias_receita')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar categoria: {str(e)}')
    
    return render(request, 'financeiro/categoria_receita_form.html', {})


@login_required
def editar_categoria_receita(request, categoria_id):
    """Editar categoria de receita"""
    categoria = get_object_or_404(CategoriaReceita, id=categoria_id)
    
    if request.method == 'POST':
        try:
            categoria.nome = request.POST.get('nome')
            categoria.tipo = request.POST.get('tipo', 'VENDA')
            categoria.icone = request.POST.get('icone', 'bi-cash')
            categoria.cor = request.POST.get('cor', '#22c55e')
            categoria.ordem = int(request.POST.get('ordem', 0) or 0)
            categoria.ativo = request.POST.get('ativo') == 'on'
            categoria.save()
            
            messages.success(request, f'Categoria "{categoria.nome}" atualizada!')
            return redirect('financeiro:lista_categorias_receita')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    context = {
        'categoria': categoria,
        'editando': True,
    }
    
    return render(request, 'financeiro/categoria_receita_form.html', context)


@login_required
def deletar_categoria_receita(request, categoria_id):
    """Desativar categoria de receita"""
    categoria = get_object_or_404(CategoriaReceita, id=categoria_id)
    
    if request.method == 'POST':
        if ContaReceber.objects.filter(categoria=categoria).exists():
            categoria.ativo = False
            categoria.save()
            messages.warning(request, f'Categoria "{categoria.nome}" desativada (possui receitas vinculadas).')
        else:
            categoria.delete()
            messages.success(request, f'Categoria "{categoria.nome}" excluída!')
    
    return redirect('financeiro:lista_categorias_receita')


# ==========================================
# APIs
# ==========================================

@login_required
def api_pendencias_cliente(request, cliente_id):
    """API: Retorna pendências financeiras de um cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    pendencias = ContaReceber.objects.filter(
        cliente=cliente,
        status__in=['PENDENTE', 'ATRASADO']
    ).order_by('data_vencimento')
    
    dados = {
        'cliente': {
            'id': cliente.id,
            'nome': cliente.nome,
        },
        'resumo': {
            'total_pendente': float(pendencias.aggregate(
                total=Coalesce(Sum('valor'), Decimal('0'))
            )['total']),
            'qtd_parcelas': pendencias.count(),
            'qtd_atrasadas': pendencias.filter(status='ATRASADO').count(),
        },
        'parcelas': [
            {
                'id': p.id,
                'descricao': p.descricao,
                'valor': float(p.valor),
                'data_vencimento': p.data_vencimento.strftime('%d/%m/%Y'),
                'status': p.status,
                'dias_atraso': p.dias_atraso,
                'parcela': f"{p.parcela_atual}/{p.total_parcelas}" if p.total_parcelas > 1 else None,
            }
            for p in pendencias
        ]
    }
    
    return JsonResponse(dados)


@login_required
def api_pendencias_fornecedor(request, fornecedor_id):
    """API: Retorna pendências financeiras com um fornecedor"""
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    pendencias = ContaPagar.objects.filter(
        fornecedor=fornecedor,
        status__in=['PENDENTE', 'ATRASADO']
    ).order_by('data_vencimento')
    
    dados = {
        'fornecedor': {
            'id': fornecedor.id,
            'nome': str(fornecedor),
        },
        'resumo': {
            'total_pendente': float(pendencias.aggregate(
                total=Coalesce(Sum('valor'), Decimal('0'))
            )['total']),
            'qtd_contas': pendencias.count(),
            'qtd_atrasadas': pendencias.filter(status='ATRASADO').count(),
        },
        'contas': [
            {
                'id': c.id,
                'descricao': c.descricao,
                'valor': float(c.valor),
                'data_vencimento': c.data_vencimento.strftime('%d/%m/%Y'),
                'status': c.status,
                'dias_atraso': c.dias_atraso,
            }
            for c in pendencias
        ]
    }
    
    return JsonResponse(dados)