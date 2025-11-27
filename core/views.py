from django.http import JsonResponse
from vendas.models import Venda, OrdemServico
from django.utils import timezone
import json
from estoque.forms import ProdutoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F, Q, Avg, Min, Max, Prefetch
from datetime import datetime, timedelta
from clientes.models import Cliente, Veiculo
from estoque.models import (
    Produto, Categoria, Subcategoria, Fabricante,
    Fornecedor, CotacaoFornecedor, Montadora, 
    VeiculoModelo, VeiculoVersao,
    MovimentacaoEstoque,  # ✅ CORRIGIDO: Adicionado import que faltava
)
from vendas.models import (
    Venda, ItemVenda, OrdemServico, PecaOS,   # ← ADICIONE ItemVenda aqui
    ServicoOS, Orcamento, ItemOrcamento
)


# ============================================
# FUNÇÃO DE BUSCA FUZZY - TODAS AS PALAVRAS
# ============================================
def busca_fuzzy(queryset, campos, termo_busca):
    """
    Realiza busca fuzzy onde TODAS as palavras devem ser encontradas.
    
    Args:
        queryset: QuerySet do Django
        campos: Lista de campos para buscar (ex: ['codigo', 'descricao'])
        termo_busca: String de busca (ex: 'oleo 20w50')
    
    Returns:
        QuerySet filtrado
    """
    if not termo_busca:
        return queryset
    
    # Divide a busca em palavras (ignora palavras muito curtas)
    palavras = [p for p in termo_busca.split() if len(p) >= 2]
    
    if not palavras:
        return queryset
    
    # Para cada palavra, ela deve estar em PELO MENOS UM dos campos
    for palavra in palavras:
        filtro_palavra = Q()
        for campo in campos:
            filtro_palavra |= Q(**{f'{campo}__icontains': palavra})
        queryset = queryset.filter(filtro_palavra)
    
    return queryset

@login_required
def dashboard(request):
    """Dashboard principal com indicadores"""
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    
    # Vendas do dia
    vendas_hoje = Venda.objects.filter(
        data_venda__date=hoje,
        status='F'
    )
    
    # Vendas do mês
    vendas_mes = Venda.objects.filter(
        data_venda__date__gte=mes_atual,
        status='F'
    )
    
    # OS em aberto
    os_abertas = OrdemServico.objects.filter(
        status__in=['AB', 'EA', 'AG']
    )
    
    # Produtos com estoque baixo
    produtos_criticos = Produto.objects.filter(
        estoque_atual__lte=F('estoque_minimo'),
        ativo=True
    )
    
    context = {
        'vendas_hoje_total': vendas_hoje.aggregate(Sum('total'))['total__sum'] or 0,
        'vendas_hoje_qtd': vendas_hoje.count(),
        'vendas_mes_total': vendas_mes.aggregate(Sum('total'))['total__sum'] or 0,
        'vendas_mes_qtd': vendas_mes.count(),
        'os_abertas_qtd': os_abertas.count(),
        'os_abertas_total': os_abertas.aggregate(Sum('total'))['total__sum'] or 0,
        'produtos_criticos_qtd': produtos_criticos.count(),
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
        'vendas_recentes': Venda.objects.filter(status='F').order_by('-data_venda')[:10],
        'os_recentes': OrdemServico.objects.order_by('-data_entrada')[:10],
        'produtos_criticos': produtos_criticos[:10],
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def pdv(request):
    """Ponto de Venda - Interface de vendas rápida OTIMIZADA"""
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    
    # OTIMIZADO: Carrega apenas 20 produtos iniciais (mais vendidos ou recentes)
    produtos_iniciais = Produto.objects.filter(
        ativo=True,
        estoque_atual__gt=0  # Apenas com estoque
    ).select_related('categoria', 'fabricante').order_by('-id')[:20]
    
    context = {
        'clientes': clientes,
        'produtos': produtos_iniciais,  # Apenas 20 iniciais
        'total_produtos': Produto.objects.filter(ativo=True).count(),  # Total para mostrar
    }
    
    return render(request, 'core/pdv.html', context)

@login_required
def api_buscar_produtos_pdv(request):
    """
    API para buscar produtos no PDV via AJAX
    Retorna JSON com produtos filtrados
    BUSCA FUZZY: Busca múltiplas palavras separadas
    """
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'produtos': []})
    
    # Dividir query em palavras (busca fuzzy)
    palavras = query.split()
    
    # Construir filtros para cada palavra
    filtros = Q(ativo=True)
    
    for palavra in palavras:
        if palavra:  # Ignorar strings vazias
            filtros &= (
                Q(codigo__icontains=palavra) |
                Q(descricao__icontains=palavra) |
                Q(codigo_barras__icontains=palavra) |
                Q(codigo_sku__icontains=palavra)
            )
    
    # Buscar produtos que contenham TODAS as palavras
    produtos = Produto.objects.filter(filtros).select_related('categoria', 'fabricante')[:50]
    
    # Serializa os produtos para JSON
    produtos_data = []
    for p in produtos:
        produtos_data.append({
            'id': p.id,
            'codigo': p.codigo,
            'codigo_barras': p.codigo_barras or '',
            'descricao': p.descricao,
            'preco_venda_dinheiro': float(p.preco_venda_dinheiro) if p.preco_venda_dinheiro else 0,
            'preco_venda_debito': float(p.preco_venda_debito) if p.preco_venda_debito else 0,
            'preco_venda_credito': float(p.preco_venda_credito) if p.preco_venda_credito else 0,
            'estoque_atual': float(p.estoque_atual) if p.estoque_atual else 0,
            'aplicar_imposto_4': p.aplicar_imposto_4 if hasattr(p, 'aplicar_imposto_4') else False,
            'preco_customizado_cartao': p.preco_customizado_cartao if hasattr(p, 'preco_customizado_cartao') else False,
            'precos_credito': {
                '2x': float(p.preco_credito_2x) if hasattr(p, 'preco_credito_2x') and p.preco_credito_2x else 0,
                '3x': float(p.preco_credito_3x) if hasattr(p, 'preco_credito_3x') and p.preco_credito_3x else 0,
                '4x': float(p.preco_credito_4x) if hasattr(p, 'preco_credito_4x') and p.preco_credito_4x else 0,
                '5x': float(p.preco_credito_5x) if hasattr(p, 'preco_credito_5x') and p.preco_credito_5x else 0,
                '6x': float(p.preco_credito_6x) if hasattr(p, 'preco_credito_6x') and p.preco_credito_6x else 0,
                '7x': float(p.preco_credito_7x) if hasattr(p, 'preco_credito_7x') and p.preco_credito_7x else 0,
                '8x': float(p.preco_credito_8x) if hasattr(p, 'preco_credito_8x') and p.preco_credito_8x else 0,
                '9x': float(p.preco_credito_9x) if hasattr(p, 'preco_credito_9x') and p.preco_credito_9x else 0,
                '10x': float(p.preco_credito_10x) if hasattr(p, 'preco_credito_10x') and p.preco_credito_10x else 0,
                '11x': float(p.preco_credito_11x) if hasattr(p, 'preco_credito_11x') and p.preco_credito_11x else 0,
                '12x': float(p.preco_credito_12x) if hasattr(p, 'preco_credito_12x') and p.preco_credito_12x else 0,
            },
            'categoria': p.categoria.nome if p.categoria else '',
            'fabricante': p.fabricante.nome if p.fabricante else '',
        })
    
    return JsonResponse({
        'produtos': produtos_data,
        'total': len(produtos_data)
    })


@login_required
def relatorios(request):
    """Página de relatórios gerenciais"""
    # Período padrão: últimos 30 dias
    data_fim = timezone.now().date()
    data_inicio = data_fim - timedelta(days=30)
    
    # Vendas no período
    vendas_periodo = Venda.objects.filter(
        status='F',
        data_venda__date__gte=data_inicio,
        data_venda__date__lte=data_fim
    )
    
    # Top 10 produtos mais vendidos
    top_produtos = ItemVenda.objects.filter(
        venda__status='F',
        venda__data_venda__date__gte=data_inicio
    ).values(
        'produto__descricao'
    ).annotate(
        quantidade_total=Sum('quantidade'),
        valor_total=Sum('total')
    ).order_by('-quantidade_total')[:10]
    
    context = {
        'vendas_periodo': vendas_periodo,
        'total_vendido': vendas_periodo.aggregate(Sum('total'))['total__sum'] or 0,
        'top_produtos': top_produtos,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'core/relatorios.html', context)


# ============================================
# VIEWS DE CLIENTES
# ============================================

@login_required
def lista_clientes(request):
    """Lista todos os clientes com filtros"""
    busca = request.GET.get('busca', '')
    tipo = request.GET.get('tipo', '')
    ativo = request.GET.get('ativo', '')
    
    clientes = Cliente.objects.all()
    
    if busca:
        clientes = busca_fuzzy(clientes, ['nome', 'cpf_cnpj', 'telefone', 'email'], busca)
    
    if tipo:
        clientes = clientes.filter(tipo=tipo)
    
    if ativo:
        clientes = clientes.filter(ativo=ativo == 'true')
    
    clientes = clientes.order_by('nome')
    
    # Paginação
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busca': busca,
        'tipo_selecionado': tipo,
        'ativo_selecionado': ativo,
        'total_clientes': clientes.count(),
    }
    
    return render(request, 'core/clientes_lista.html', context)


@login_required
def detalhe_cliente(request, cliente_id):
    """Detalhes de um cliente específico"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    veiculos = cliente.veiculos.all()
    vendas = cliente.venda_set.filter(status='F').order_by('-data_venda')[:20]
    ordens_servico = cliente.ordemservico_set.all().order_by('-data_entrada')[:20]
    
    # Estatísticas
    stats = {
        'total_compras': vendas.aggregate(Sum('total'))['total__sum'] or 0,
        'total_vendas': vendas.count(),
        'total_os': ordens_servico.count(),
        'total_veiculos': veiculos.count(),
    }
    
    context = {
        'cliente': cliente,
        'veiculos': veiculos,
        'vendas': vendas,
        'ordens_servico': ordens_servico,
        'stats': stats,
    }
    return render(request, 'core/cliente_detalhe.html', context)


# ============================================
# VIEWS DE ESTOQUE
# ============================================

@login_required
def lista_estoque(request):
    """Lista produtos do estoque com filtros avançados"""
    busca = request.GET.get('busca', '')
    categoria_id = request.GET.get('categoria', '')
    situacao = request.GET.get('situacao', '')
    
    # ✅ NOVO: Filtros de montadora, modelo e versão
    montadoras_ids = request.GET.getlist('montadoras')
    modelos_ids = request.GET.getlist('modelos')
    versoes_ids = request.GET.getlist('versoes')
    
    produtos = Produto.objects.filter(ativo=True)
    
    # Busca por texto - TODAS as palavras devem ser encontradas
    if busca:
        palavras = busca.split()
        for palavra in palavras:
            produtos = produtos.filter(
                Q(codigo__icontains=palavra) |
                Q(descricao__icontains=palavra) |
                Q(codigo_sku__icontains=palavra) |
                Q(codigo_barras__icontains=palavra)
            )
    
    # Filtro por categoria
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    # Filtro por situação de estoque
    if situacao == 'critico':
        produtos = produtos.filter(estoque_atual__lte=F('estoque_minimo'))
    elif situacao == 'baixo':
        produtos = produtos.filter(
            estoque_atual__gt=F('estoque_minimo'),
            estoque_atual__lte=F('estoque_minimo') * 2
        )
    elif situacao == 'normal':
        produtos = produtos.filter(estoque_atual__gt=F('estoque_minimo') * 2)
    
    # ✅ NOVO: Filtros de aplicação por veículo
    if montadoras_ids:
        produtos = produtos.filter(
            versoes_compativeis__modelo__montadora_id__in=montadoras_ids
        ).distinct()
    
    if modelos_ids:
        produtos = produtos.filter(
            versoes_compativeis__modelo_id__in=modelos_ids
        ).distinct()
    
    if versoes_ids:
        produtos = produtos.filter(
            versoes_compativeis__id__in=versoes_ids
        ).distinct()
    
    # Otimização de queries
    produtos = produtos.select_related(
        'categoria', 
        'subcategoria',
        'fabricante', 
        'fornecedor_principal'
    ).prefetch_related(
        'versoes_compativeis',
        'versoes_compativeis__modelo',
        'versoes_compativeis__modelo__montadora'
    ).order_by('descricao')
    
    # Paginação
    paginator = Paginator(produtos, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ✅ NOVO: Dados para os filtros em cascata
    montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    categorias = Categoria.objects.filter(ativo=True).order_by('nome')
    
    todos_produtos = Produto.objects.filter(ativo=True)
    stats = {
        'total_produtos': todos_produtos.count(),
        'total_estoque_critico': todos_produtos.filter(estoque_atual__lte=F('estoque_minimo')).count(),
        'total_estoque_baixo': todos_produtos.filter(
            estoque_atual__gt=F('estoque_minimo'),
            estoque_atual__lte=F('estoque_minimo') * 2
        ).count(),
        'total_estoque_normal': todos_produtos.filter(estoque_atual__gt=F('estoque_minimo') * 2).count(),
        'valor_custo_estoque': todos_produtos.aggregate(
            total=Sum(F('estoque_atual') * F('preco_custo'))
        )['total'] or 0,
        'valor_venda_estoque': todos_produtos.aggregate(
            total=Sum(F('estoque_atual') * F('preco_venda_dinheiro'))
        )['total'] or 0,
        'total_itens': todos_produtos.aggregate(total=Sum('estoque_atual'))['total'] or 0,
    }

    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'montadoras': montadoras,
        'busca': busca,
        'categoria_selecionada': categoria_id,
        'situacao': situacao,
        'montadoras_selecionadas': montadoras_ids,
        'modelos_selecionados': modelos_ids,
        'versoes_selecionadas': versoes_ids,
        'total_produtos': produtos.count(),
        'stats': stats,
    }
    return render(request, 'core/estoque_lista.html', context)
    
    return render(request, 'core/estoque_lista.html', context)


@login_required
def detalhe_produto(request, produto_id):
    """Detalhes de um produto específico com indicadores financeiros"""
    produto = get_object_or_404(Produto.objects.select_related(
        'categoria', 'subcategoria', 'fabricante', 'fornecedor_principal'
    ).prefetch_related(
        'versoes_compativeis',
        'versoes_compativeis__modelo',
        'versoes_compativeis__modelo__montadora'
    ), id=produto_id)
    
    # Movimentações de estoque
    movimentacoes = MovimentacaoEstoque.objects.filter(
        produto=produto
    ).order_by('-data_movimentacao')[:30]

    # Estatísticas de vendas
    vendas_stats = ItemVenda.objects.filter(
        produto=produto,
        venda__status='F'
    ).aggregate(
        total_vendido=Sum('quantidade'),
        valor_total=Sum('total')
    )
    
    # Calcular indicadores financeiros
    from financeiro.models import TaxaCartao, calcular_indicadores_produto
    from decimal import Decimal
    
    indicadores = calcular_indicadores_produto(produto)
    taxas = TaxaCartao.get_todas_taxas()

    context = {
        'produto': produto,
        'movimentacoes': movimentacoes,
        'vendas_stats': vendas_stats,
        'indicadores': indicadores,
        'taxas': taxas,
    }
    return render(request, 'core/produto_detalhe.html', context)


# ============================================
# CRUD DE PRODUTOS - CORRIGIDO
# ============================================

@login_required
def criar_produto(request):
    """
    Criar novo produto com versões compatíveis
    ✅ CORRIGIDO: Agora apenas DESCRIÇÃO é obrigatória
    """
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Salvar produto
                produto = form.save()
                
                # ✅ Salvar versões compatíveis (ManyToMany)
                versoes_ids = request.POST.getlist('versoes_compativeis')
                if versoes_ids:
                    produto.versoes_compativeis.set(versoes_ids)
                
                messages.success(request, f'✅ Produto "{produto.codigo}" cadastrado com sucesso!')
                return redirect('detalhe_produto', produto_id=produto.id)
            
            except Exception as e:
                messages.error(request, f'❌ Erro ao cadastrar produto: {str(e)}')
        else:
            # Mostrar erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = ProdutoForm()
    
    # Buscar montadoras para o filtro em cascata
    montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    
    context = {
        'form': form,
        'montadoras': montadoras,
        'editando': False,
    }
    return render(request, 'core/produto_form.html', context)


@login_required
def editar_produto(request, produto_id):
    """Editar produto existente"""
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        
        if form.is_valid():
            try:
                produto = form.save()
                
                # Atualizar versões
                versoes_ids = request.POST.getlist('versoes_compativeis')
                produto.versoes_compativeis.set(versoes_ids)
                
                messages.success(request, f'✅ Produto "{produto.codigo}" atualizado!')
                return redirect('detalhe_produto', produto_id=produto.id)
            
            except Exception as e:
                messages.error(request, f'❌ Erro ao atualizar produto: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = ProdutoForm(instance=produto)
    
    montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    
    context = {
        'form': form,
        'produto': produto,
        'montadoras': montadoras,
        'editando': True,
    }
    return render(request, 'core/produto_form.html', context)


@login_required
def deletar_produto(request, produto_id):
    """Desativar produto (soft delete)"""
    produto = get_object_or_404(Produto, id=produto_id)
    produto.ativo = False
    produto.save()
    messages.success(request, f'✅ Produto {produto.codigo} desativado com sucesso!')
    return redirect('lista_estoque')


# ============================================
# APIs PARA FILTROS EM CASCATA
# ✅ NOVO: Suporte para seleção múltipla
# ============================================

@login_required
def api_buscar_modelos(request):
    """
    API: Buscar modelos de uma ou várias montadoras
    ✅ NOVO: Suporta múltiplas montadoras
    """
    montadoras_ids = request.GET.getlist('montadora_id[]')
    if not montadoras_ids:
        montadoras_ids = [request.GET.get('montadora_id')]
    
    if not any(montadoras_ids):
        return JsonResponse({'success': False, 'error': 'Montadora não informada'})
    
    # Remover valores None ou vazios
    montadoras_ids = [m for m in montadoras_ids if m]
    
    modelos = VeiculoModelo.objects.filter(
        montadora_id__in=montadoras_ids,
        ativo=True
    ).select_related('montadora').order_by('montadora__nome', 'nome')
    
    resultados = [
        {
            'id': m.id,
            'nome': m.nome,
            'montadora': m.montadora.nome,
            'tipo': m.get_tipo_display(),
            'popular': m.popular,
            'total_versoes': m.versoes.filter(ativo=True).count(),
        }
        for m in modelos
    ]
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'modelos': resultados
    })


@login_required
def api_buscar_versoes(request):
    """
    API: Buscar versões de um ou vários modelos
    ✅ NOVO: Suporta múltiplos modelos
    """
    modelos_ids = request.GET.getlist('modelo_id[]')
    if not modelos_ids:
        modelos_ids = [request.GET.get('modelo_id')]
    
    if not any(modelos_ids):
        return JsonResponse({'success': False, 'error': 'Modelo não informado'})
    
    # Remover valores None ou vazios
    modelos_ids = [m for m in modelos_ids if m]
    
    versoes = VeiculoVersao.objects.filter(
        modelo_id__in=modelos_ids,
        ativo=True
    ).select_related('modelo', 'modelo__montadora').order_by(
        'modelo__montadora__nome', 
        'modelo__nome', 
        '-ano_inicial', 
        'nome'
    )
    
    resultados = [
        {
            'id': v.id,
            'nome': v.nome,
            'modelo': v.modelo.nome,
            'montadora': v.modelo.montadora.nome,
            'descricao': v.get_descricao_completa(),
            'ano_inicial': v.ano_inicial,
            'ano_final': v.ano_final,
            'anos_range': v.get_anos_range(),
            'motorizacoes': v.motorizacoes,
        }
        for v in versoes
    ]
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'versoes': resultados
    })


@login_required
def api_buscar_subcategorias(request):
    """API: Buscar subcategorias de uma categoria"""
    categoria_id = request.GET.get('categoria_id')
    
    if not categoria_id:
        return JsonResponse({'success': False, 'error': 'Categoria não informada'})
    
    subcategorias = Subcategoria.objects.filter(
        categoria_id=categoria_id,
        ativo=True
    ).order_by('nome')
    
    resultados = [
        {
            'id': s.id,
            'nome': s.nome,
            'descricao': s.descricao or '',
        }
        for s in subcategorias
    ]
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'subcategorias': resultados
    })


# ============================================
# VIEWS DE VENDAS
# ============================================

@login_required
def lista_vendas(request):
    """Lista todas as vendas com filtros"""
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    status = request.GET.get('status', '')
    cliente_id = request.GET.get('cliente', '')
    
    vendas = Venda.objects.all()
    
    if data_inicio:
        vendas = vendas.filter(data_venda__date__gte=data_inicio)
    
    if data_fim:
        vendas = vendas.filter(data_venda__date__lte=data_fim)
    
    if status:
        vendas = vendas.filter(status=status)
    
    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)
    
    vendas = vendas.select_related('cliente').order_by('-data_venda')
    
    # Paginação
    paginator = Paginator(vendas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total_vendas': vendas.count(),
        'valor_total': vendas.aggregate(Sum('total'))['total__sum'] or 0,
        'ticket_medio': vendas.aggregate(Avg('total'))['total__avg'] or 0,
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'status_selecionado': status,
    }
    return render(request, 'core/vendas_lista.html', context)


@login_required
def detalhe_venda(request, venda_id):
    """Detalhes de uma venda específica"""
    venda = get_object_or_404(Venda.objects.select_related(
        'cliente', 'veiculo'
    ), id=venda_id)
    
    itens = venda.itens.select_related('produto').all()
    
    context = {
        'venda': venda,
        'itens': itens,
    }
    return render(request, 'core/venda_detalhe.html', context)


# ============================================
# VIEWS DE ORDEM DE SERVIÇO
# ============================================

@login_required
def lista_ordens_servico(request):
    """Lista todas as ordens de serviço"""
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    cliente_id = request.GET.get('cliente', '')
    
    ordens = OrdemServico.objects.all()
    
    if status:
        ordens = ordens.filter(status=status)
    
    if data_inicio:
        ordens = ordens.filter(data_entrada__date__gte=data_inicio)
    
    if data_fim:
        ordens = ordens.filter(data_entrada__date__lte=data_fim)
    
    if cliente_id:
        ordens = ordens.filter(cliente_id=cliente_id)
    
    ordens = ordens.select_related('cliente', 'veiculo').order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(ordens, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total_os': ordens.count(),
        'valor_total': ordens.aggregate(Sum('total'))['total__sum'] or 0,
        'abertas': ordens.filter(status='AB').count(),
        'em_andamento': ordens.filter(status='EA').count(),
        'finalizadas': ordens.filter(status='FI').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'status_selecionado': status,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'core/ordens_servico_lista.html', context)


@login_required
def detalhe_ordem_servico(request, os_id):
    """Detalhes de uma ordem de serviço específica"""
    ordem = get_object_or_404(OrdemServico.objects.select_related(
        'cliente', 'veiculo'
    ), id=os_id)
    
    pecas = ordem.pecas.select_related('produto').all()
    servicos = ordem.servicos.all()
    
    context = {
        'ordem': ordem,
        'pecas': pecas,
        'servicos': servicos,
    }
    return render(request, 'core/ordem_servico_detalhe.html', context)


# ============================================
# VIEWS DE FORNECEDORES
# ============================================

@login_required
def lista_fornecedores(request):
    """Lista todos os fornecedores com estatísticas"""
    fornecedores = Fornecedor.objects.filter(ativo=True).annotate(
        total_produtos=Count('produto_fornecedor_principal'),
        total_cotacoes=Count('cotacoes', filter=Q(cotacoes__ativo=True))
    ).order_by('nome_fantasia')
    
    context = {
        'fornecedores': fornecedores,
        'total_fornecedores': fornecedores.count(),
    }
    return render(request, 'estoque/fornecedores_lista.html', context)


# ============================================
# VIEWS AUXILIARES
# (Outras views que já existem no projeto)
# ============================================

# As demais views (fornecedores, orçamentos, categorias, etc)
# permanecem como estão, pois não têm erros críticos

# ============================================
# FIM DO ARQUIVO
# ============================================

@login_required
def detalhe_fornecedor(request, fornecedor_id):
    """Mostra detalhes de um fornecedor específico"""
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    produtos = fornecedor.produto_set.filter(ativo=True)
    cotacoes = fornecedor.cotacoes.filter(ativo=True).order_by('-data_cotacao')[:20]
    
    # Estatísticas
    stats = {
        'total_produtos': produtos.count(),
        'total_cotacoes': cotacoes.count(),
        'preco_medio': cotacoes.aggregate(Avg('preco_unitario'))['preco_unitario__avg'] or 0,
        'prazo_medio': cotacoes.aggregate(Avg('prazo_entrega_dias'))['prazo_entrega_dias__avg'] or 0,
    }
    
    context = {
        'fornecedor': fornecedor,
        'produtos': produtos[:10],
        'cotacoes': cotacoes,
        'stats': stats,
    }
    return render(request, 'estoque/fornecedor_detalhe.html', context)


@login_required
def comparador_precos(request):
    """Tela principal do comparador de preços"""
    
    # Filtros
    produto_id = request.GET.get('produto')
    categoria_id = request.GET.get('categoria')
    busca = request.GET.get('busca', '').strip()
    
    produtos = Produto.objects.filter(ativo=True)
    
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    if busca:
        produtos = produtos.filter(
            Q(codigo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )
    
    # Se um produto específico foi selecionado
    produto_selecionado = None
    cotacoes_produto = []
    melhor_preco = None
    economia_maxima = 0
    
    if produto_id:
        produto_selecionado = get_object_or_404(Produto, id=produto_id)
        
        # Verificar se o modelo CotacaoFornecedor existe
        try:
            cotacoes_produto = CotacaoFornecedor.objects.filter(
                produto=produto_selecionado,
                ativo=True
            ).select_related('fornecedor').order_by('preco_unitario')
            
            if cotacoes_produto.exists():
                melhor_preco = cotacoes_produto.first()
                
                # Calcula economia em relação ao preço atual
                if produto_selecionado.preco_custo > melhor_preco.preco_unitario:
                    economia_maxima = produto_selecionado.preco_custo - melhor_preco.preco_unitario
        except:
            # Se o modelo ainda não existe, não faz nada
            pass
    
    # Top 10 produtos com mais cotações
    produtos_top = []
    try:
        produtos_top = Produto.objects.filter(ativo=True).annotate(
            num_cotacoes=Count('cotacoes', filter=Q(cotacoes__ativo=True))
        ).filter(num_cotacoes__gt=0).order_by('-num_cotacoes')[:10]
    except:
        pass
    
    # Produtos que precisam de cotação (estoque baixo e sem cotações recentes)
    produtos_precisam_cotacao = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=F('estoque_minimo')
    )[:10]
    
    context = {
        'produtos': produtos[:50],
        'produto_selecionado': produto_selecionado,
        'cotacoes': cotacoes_produto,
        'melhor_preco': melhor_preco,
        'economia_maxima': economia_maxima,
        'produtos_top': produtos_top,
        'produtos_precisam_cotacao': produtos_precisam_cotacao,
        'busca': busca,
    }
    return render(request, 'estoque/comparador_precos.html', context)


@login_required
def relatorio_melhores_fornecedores(request):
    """Relatório mostrando os fornecedores com melhores preços"""
    
    # Buscar cotações ativas agrupadas por fornecedor
    fornecedores_stats = []
    produtos_maior_diferenca = []
    
    try:
        fornecedores_stats = Fornecedor.objects.filter(
            ativo=True,
            cotacoes__ativo=True
        ).annotate(
            num_cotacoes=Count('cotacoes'),
            preco_medio=Avg('cotacoes__preco_unitario'),
            preco_minimo=Min('cotacoes__preco_unitario'),
            prazo_medio=Avg('cotacoes__prazo_entrega_dias')
        ).order_by('preco_medio')
        
        # Top 5 fornecedores com melhores preços
        top_fornecedores = fornecedores_stats[:5]
        
        # Produtos com maior diferença de preço entre fornecedores
        produtos_com_cotacoes = Produto.objects.filter(
            cotacoes__ativo=True
        ).annotate(
            num_fornecedores=Count('cotacoes__fornecedor', distinct=True)
        ).filter(num_fornecedores__gte=2)
        
        for produto in produtos_com_cotacoes[:10]:
            cotacoes = produto.cotacoes.filter(ativo=True).aggregate(
                preco_min=Min('preco_unitario'),
                preco_max=Max('preco_unitario')
            )
            
            if cotacoes['preco_min'] and cotacoes['preco_max']:
                diferenca = cotacoes['preco_max'] - cotacoes['preco_min']
                if diferenca > 0:
                    economia_percentual = (diferenca / cotacoes['preco_max']) * 100
                    produtos_maior_diferenca.append({
                        'produto': produto,
                        'preco_min': cotacoes['preco_min'],
                        'preco_max': cotacoes['preco_max'],
                        'diferenca': diferenca,
                        'economia_percentual': economia_percentual,
                    })
        
        # Ordenar por economia percentual
        produtos_maior_diferenca.sort(key=lambda x: x['economia_percentual'], reverse=True)
        produtos_maior_diferenca = produtos_maior_diferenca[:10]
        
    except Exception as e:
        top_fornecedores = []
        print(f"Erro ao gerar relatório: {e}")
    
    context = {
        'top_fornecedores': top_fornecedores if fornecedores_stats else [],
        'produtos_maior_diferenca': produtos_maior_diferenca,
        'total_fornecedores': fornecedores_stats.count() if fornecedores_stats else 0,
    }
    return render(request, 'estoque/relatorio_melhores_fornecedores.html', context)


@login_required
def cadastrar_cotacao(request, produto_id=None):
    """Cadastra uma nova cotação"""
    
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        fornecedor_id = request.POST.get('fornecedor')
        preco_unitario = request.POST.get('preco_unitario')
        quantidade_minima = request.POST.get('quantidade_minima', 1)
        forma_pagamento = request.POST.get('forma_pagamento', '30DD')
        prazo_entrega = request.POST.get('prazo_entrega', 0)
        valor_frete = request.POST.get('valor_frete', 0)
        observacoes = request.POST.get('observacoes', '')
        
        try:
            cotacao = CotacaoFornecedor.objects.create(
                produto_id=produto_id,
                fornecedor_id=fornecedor_id,
                preco_unitario=preco_unitario,
                quantidade_minima=quantidade_minima,
                forma_pagamento=forma_pagamento,
                prazo_entrega_dias=prazo_entrega,
                valor_frete=valor_frete,
                observacoes=observacoes,
                usuario_cadastro=request.user.username if request.user.is_authenticated else 'Sistema',
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Cotação cadastrada com sucesso!',
                'cotacao_id': cotacao.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # GET - Mostrar formulário
    produto = None
    if produto_id:
        produto = get_object_or_404(Produto, id=produto_id)
    
    produtos = Produto.objects.filter(ativo=True).order_by('descricao')
    fornecedores = Fornecedor.objects.filter(ativo=True).order_by('nome_fantasia')
    
    context = {
        'produto': produto,
        'produtos': produtos,
        'fornecedores': fornecedores,
    }
    return render(request, 'estoque/cadastrar_cotacao.html', context)



@login_required
def api_cotacoes_produto(request, produto_id):
    """API que retorna todas as cotações de um produto"""
    try:
        cotacoes = CotacaoFornecedor.objects.filter(
            produto_id=produto_id,
            ativo=True
        ).select_related('fornecedor').order_by('preco_unitario')
        
        data = {
            'cotacoes': [
                {
                    'id': c.id,
                    'fornecedor': c.fornecedor.nome_fantasia,
                    'fornecedor_id': c.fornecedor.id,
                    'preco_unitario': float(c.preco_unitario),
                    'quantidade_minima': c.quantidade_minima,
                    'prazo_entrega': c.prazo_entrega_dias,
                    'forma_pagamento': c.get_forma_pagamento_display(),
                    'valor_frete': float(c.valor_frete),
                    'preco_total': float(c.get_preco_total()),
                    'economia': float(c.get_economia_percentual()),
                    'data_cotacao': c.data_cotacao.strftime('%d/%m/%Y'),
                    'valida': c.esta_valida(),
                }
                for c in cotacoes
            ]
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'cotacoes': [],
            'error': str(e)
        })
    
@login_required
def lista_fornecedores(request):
    """Lista todos os fornecedores com filtros e busca"""
    
    # Busca
    busca = request.GET.get('busca', '')
    filtro_ativo = request.GET.get('ativo', '')
    
    # Query base
    fornecedores = Fornecedor.objects.annotate(
        total_cotacoes=Count('cotacoes'),
        media_preco=Avg('cotacoes__preco_unitario')
    )
    
    # Aplicar filtros
    if busca:
        fornecedores = busca_fuzzy(fornecedores, ['nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'email'], busca)
    
    if filtro_ativo == 'sim':
        fornecedores = fornecedores.filter(ativo=True)
    elif filtro_ativo == 'nao':
        fornecedores = fornecedores.filter(ativo=False)
    
    # Ordenação
    ordem = request.GET.get('ordem', '-total_cotacoes')
    fornecedores = fornecedores.order_by(ordem)
    
    # Paginação
    paginator = Paginator(fornecedores, 12)
    page = request.GET.get('page', 1)
    fornecedores_page = paginator.get_page(page)
    
    # Estatísticas
    stats = {
        'total_fornecedores': Fornecedor.objects.filter(ativo=True).count(),
        'total_inativos': Fornecedor.objects.filter(ativo=False).count(),
        'total_cotacoes': CotacaoFornecedor.objects.filter(ativo=True).count(),
        'fornecedores_sem_cotacao': Fornecedor.objects.annotate(
            num_cotacoes=Count('cotacoes')
        ).filter(num_cotacoes=0, ativo=True).count(),
    }
    
    context = {
        'fornecedores': fornecedores_page,
        'stats': stats,
        'busca': busca,
        'filtro_ativo': filtro_ativo,
        'ordem': ordem,
    }
    
    return render(request, 'fornecedores/lista_fornecedores.html', context)


@login_required
def detalhes_fornecedor(request, fornecedor_id):
    """Exibe detalhes completos de um fornecedor"""
    
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    # Cotações do fornecedor
    cotacoes = CotacaoFornecedor.objects.filter(
        fornecedor=fornecedor
    ).select_related('produto').order_by('-data_cotacao')[:20]
    
    # Estatísticas
    stats_cotacoes = CotacaoFornecedor.objects.filter(
        fornecedor=fornecedor,
        ativo=True
    ).aggregate(
        total_cotacoes=Count('id'),
        preco_medio=Avg('preco_unitario'),
        preco_min=Avg('preco_unitario'),
        preco_max=Avg('preco_unitario'),
    )
    
    # Produtos mais cotados deste fornecedor
    produtos_top = Produto.objects.filter(
        cotacoes__fornecedor=fornecedor
    ).annotate(
        num_cotacoes=Count('cotacoes')
    ).order_by('-num_cotacoes')[:5]
    
    context = {
        'fornecedor': fornecedor,
        'cotacoes': cotacoes,
        'stats': stats_cotacoes,
        'produtos_top': produtos_top,
    }
    
    return render(request, 'fornecedores/detalhes_fornecedor.html', context)


@login_required
def adicionar_fornecedor(request):
    """Adiciona um novo fornecedor"""
    
    if request.method == 'POST':
        try:
            fornecedor = Fornecedor.objects.create(
                cnpj=request.POST.get('cnpj'),
                razao_social=request.POST.get('razao_social'),
                nome_fantasia=request.POST.get('nome_fantasia'),
                inscricao_estadual=request.POST.get('inscricao_estadual', ''),
                telefone=request.POST.get('telefone'),
                celular=request.POST.get('celular', ''),
                email=request.POST.get('email'),
                site=request.POST.get('site', ''),
                contato_principal=request.POST.get('contato_principal', ''),
                cep=request.POST.get('cep'),
                logradouro=request.POST.get('logradouro'),
                numero=request.POST.get('numero'),
                complemento=request.POST.get('complemento', ''),
                bairro=request.POST.get('bairro'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                observacoes=request.POST.get('observacoes', ''),
                classificacao=int(request.POST.get('classificacao', 3)),
                ativo=True
            )
            
            messages.success(request, f'Fornecedor {fornecedor.nome_fantasia} cadastrado com sucesso!')
            return redirect('detalhes_fornecedor', fornecedor_id=fornecedor.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar fornecedor: {str(e)}')
            return redirect('adicionar_fornecedor')
    
    return render(request, 'fornecedores/form_fornecedor.html', {
        'titulo': 'Adicionar Fornecedor',
        'acao': 'adicionar'
    })


@login_required
def editar_fornecedor(request, fornecedor_id):
    """Edita um fornecedor existente"""
    
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    if request.method == 'POST':
        try:
            fornecedor.cnpj = request.POST.get('cnpj')
            fornecedor.razao_social = request.POST.get('razao_social')
            fornecedor.nome_fantasia = request.POST.get('nome_fantasia')
            fornecedor.inscricao_estadual = request.POST.get('inscricao_estadual', '')
            fornecedor.telefone = request.POST.get('telefone')
            fornecedor.celular = request.POST.get('celular', '')
            fornecedor.email = request.POST.get('email')
            fornecedor.site = request.POST.get('site', '')
            fornecedor.contato_principal = request.POST.get('contato_principal', '')
            fornecedor.cep = request.POST.get('cep')
            fornecedor.logradouro = request.POST.get('logradouro')
            fornecedor.numero = request.POST.get('numero')
            fornecedor.complemento = request.POST.get('complemento', '')
            fornecedor.bairro = request.POST.get('bairro')
            fornecedor.cidade = request.POST.get('cidade')
            fornecedor.estado = request.POST.get('estado')
            fornecedor.observacoes = request.POST.get('observacoes', '')
            fornecedor.classificacao = int(request.POST.get('classificacao', 3))
            fornecedor.ativo = request.POST.get('ativo') == 'on'
            
            fornecedor.save()
            
            messages.success(request, f'Fornecedor {fornecedor.nome_fantasia} atualizado com sucesso!')
            return redirect('detalhes_fornecedor', fornecedor_id=fornecedor.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar fornecedor: {str(e)}')
    
    return render(request, 'fornecedores/form_fornecedor.html', {
        'titulo': 'Editar Fornecedor',
        'acao': 'editar',
        'fornecedor': fornecedor
    })


@login_required
def deletar_fornecedor(request, fornecedor_id):
    """Desativa um fornecedor (soft delete)"""
    
    if request.method == 'POST':
        try:
            fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
            fornecedor.ativo = False
            fornecedor.save()
            
            messages.success(request, f'Fornecedor {fornecedor.nome_fantasia} desativado com sucesso!')
            return redirect('lista_fornecedores')
            
        except Exception as e:
            messages.error(request, f'Erro ao desativar fornecedor: {str(e)}')
            return redirect('lista_fornecedores')
    
    return redirect('lista_fornecedores')


@login_required
def comparador_precos_fornecedores(request):
    """Interface de comparação de preços integrada ao módulo de fornecedores"""
    
    # Busca de produto
    busca = request.GET.get('busca', '')
    produto_id = request.GET.get('produto', '')
    
    produtos = []
    produto_selecionado = None
    cotacoes = []
    economia_maxima = 0
    
    # Se há busca, procura produtos
    if busca:
        produtos = Produto.objects.filter(
            Q(codigo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        ).annotate(
            num_cotacoes=Count('cotacoes')
        )[:20]
    
    # Produtos mais cotados
    produtos_top = Produto.objects.annotate(
        num_cotacoes=Count('cotacoes')
    ).filter(num_cotacoes__gt=0).order_by('-num_cotacoes')[:10]
    
    # Se um produto foi selecionado
    if produto_id:
        produto_selecionado = get_object_or_404(Produto, id=produto_id)
        
        # Buscar cotações ativas ordenadas por preço
        cotacoes = CotacaoFornecedor.objects.filter(
            produto=produto_selecionado,
            ativo=True
        ).select_related('fornecedor').order_by('preco_unitario')
        
        # Calcular economia máxima
        if cotacoes.count() > 1:
            preco_min = cotacoes.first().preco_unitario
            preco_max = cotacoes.last().preco_unitario
            economia_maxima = preco_max - preco_min
    
    # Produtos que precisam de cotação
    produtos_precisam_cotacao = Produto.objects.filter(
        estoque_atual__lte=F('estoque_minimo'),
        ativo=True
    ).annotate(
        num_cotacoes=Count('cotacoes')
    ).filter(num_cotacoes=0)[:5]
    
    context = {
        'busca': busca,
        'produtos': produtos,
        'produto_selecionado': produto_selecionado,
        'cotacoes': cotacoes,
        'economia_maxima': economia_maxima,
        'produtos_top': produtos_top,
        'produtos_precisam_cotacao': produtos_precisam_cotacao,
    }
    
    return render(request, 'fornecedores/comparador_precos.html', context)


@login_required
def adicionar_cotacao(request):
    """Adiciona uma nova cotação de preço"""
    
    if request.method == 'POST':
        try:
            cotacao = CotacaoFornecedor.objects.create(
                produto_id=request.POST.get('produto_id'),
                fornecedor_id=request.POST.get('fornecedor_id'),
                preco_unitario=request.POST.get('preco_unitario'),
                quantidade_minima=request.POST.get('quantidade_minima', 1),
                forma_pagamento=request.POST.get('forma_pagamento', '30DD'),
                prazo_entrega_dias=request.POST.get('prazo_entrega', 0),
                valor_frete=request.POST.get('valor_frete', 0),
                observacoes=request.POST.get('observacoes', ''),
                usuario_cadastro=request.user.username,
                ativo=True
            )
            
            messages.success(request, 'Cotação adicionada com sucesso!')
            return redirect('comparador_precos_fornecedores' + f'?produto={cotacao.produto.id}')
            
        except Exception as e:
            messages.error(request, f'Erro ao adicionar cotação: {str(e)}')
    
    # Dados para o formulário
    fornecedores = Fornecedor.objects.filter(ativo=True).order_by('nome_fantasia')
    produtos = Produto.objects.filter(ativo=True).order_by('descricao')
    
    produto_id = request.GET.get('produto', '')
    produto_selecionado = None
    
    if produto_id:
        produto_selecionado = get_object_or_404(Produto, id=produto_id)
    
    context = {
        'fornecedores': fornecedores,
        'produtos': produtos,
        'produto_selecionado': produto_selecionado,
    }
    
    return render(request, 'fornecedores/form_cotacao.html', context)


@login_required
def buscar_cep(request):
    """API para buscar dados do CEP usando ViaCEP"""
    import requests
    
    cep = request.GET.get('cep', '').replace('-', '').replace('.', '')
    
    if len(cep) == 8:
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            if response.status_code == 200:
                dados = response.json()
                if 'erro' not in dados:
                    return JsonResponse({
                        'success': True,
                        'logradouro': dados.get('logradouro', ''),
                        'bairro': dados.get('bairro', ''),
                        'cidade': dados.get('localidade', ''),
                        'estado': dados.get('uf', ''),
                    })
        except:
            pass
    
    return JsonResponse({'success': False, 'message': 'CEP não encontrado'})


@login_required
def detalhe_venda(request, venda_id):
    """Detalhes de uma venda específica"""
    venda = get_object_or_404(Venda, id=venda_id)
    itens = venda.itens.all()
    
    context = {
        'venda': venda,
        'itens': itens,
    }
    return render(request, 'core/venda_detalhe.html', context)


# ==========================================
# VIEWS DE ORÇAMENTO
# ==========================================

@login_required
def lista_orcamentos(request):
    """Lista todos os orçamentos"""
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    cliente_id = request.GET.get('cliente', '')
    
    orcamentos = Orcamento.objects.all()
    
    if status:
        orcamentos = orcamentos.filter(status=status)
    
    if data_inicio:
        orcamentos = orcamentos.filter(data_orcamento__date__gte=data_inicio)
    
    if data_fim:
        orcamentos = orcamentos.filter(data_orcamento__date__lte=data_fim)
    
    if cliente_id:
        orcamentos = orcamentos.filter(cliente_id=cliente_id)
    
    orcamentos = orcamentos.select_related('cliente', 'vendedor', 'veiculo_modelo').order_by('-data_orcamento')
    
    # Paginação
    paginator = Paginator(orcamentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total_orcamentos': orcamentos.count(),
        'valor_total': orcamentos.aggregate(Sum('total'))['total__sum'] or 0,
        'abertos': orcamentos.filter(status='ABERTO').count(),
        'enviados': orcamentos.filter(status='ENVIADO').count(),
        'aprovados': orcamentos.filter(status='APROVADO').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'status_selecionado': status,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'core/orcamentos_lista.html', context)


@login_required
def criar_orcamento(request):
    """Criar novo orçamento"""
    if request.method == 'POST':
        # Processar criação do orçamento
        cliente_id = request.POST.get('cliente_id')
        veiculo_modelo_id = request.POST.get('veiculo_modelo_id')
        forma_pagamento = request.POST.get('forma_pagamento', 'DINHEIRO')
        
        if not cliente_id:
            messages.error(request, 'Selecione um cliente!')
            return redirect('criar_orcamento')
        
        # Gerar número do orçamento
        ultimo_orc = Orcamento.objects.order_by('-id').first()
        if ultimo_orc:
            numero = int(ultimo_orc.numero.split('-')[1]) + 1
        else:
            numero = 1
        numero_orcamento = f"ORC-{numero:06d}"
        
        # Criar orçamento
        orcamento = Orcamento.objects.create(
            numero=numero_orcamento,
            cliente_id=cliente_id,
            veiculo_modelo_id=veiculo_modelo_id if veiculo_modelo_id else None,
            vendedor=request.user,
            forma_pagamento=forma_pagamento,
            data_validade=datetime.now().date() + timedelta(days=15),
        )
        
        messages.success(request, f'Orçamento {numero_orcamento} criado com sucesso!')
        return redirect('editar_orcamento', orcamento_id=orcamento.id)
    
    # GET - Exibir formulário
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    montadoras = Montadora.objects.filter(ativa=True).order_by('nome')
    
    context = {
        'clientes': clientes,
        'montadoras': montadoras,
    }
    return render(request, 'core/orcamento_criar.html', context)


@login_required
def editar_orcamento(request, orcamento_id):
    """Editar orçamento (adicionar/remover itens)"""
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_item':
            # Adicionar item ao orçamento
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade', 1))
            
            if produto_id:
                produto = get_object_or_404(Produto, id=produto_id)
                
                # Verificar estoque
                if produto.estoque_disponivel < quantidade:
                    messages.warning(request, f'Estoque insuficiente! Disponível: {produto.estoque_disponivel}')
                
                # Determinar preço de acordo com forma de pagamento
                preco = produto.get_preco_venda_por_tipo(orcamento.forma_pagamento.lower())
                
                # Criar item
                ItemOrcamento.objects.create(
                    orcamento=orcamento,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco,
                )
                
                messages.success(request, 'Item adicionado ao orçamento!')
            
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'remove_item':
            # Remover item
            item_id = request.POST.get('item_id')
            if item_id:
                item = ItemOrcamento.objects.filter(id=item_id, orcamento=orcamento).first()
                if item:
                    item.delete()
                    messages.success(request, 'Item removido!')
            
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'update_desconto':
            # Atualizar desconto
            desconto = request.POST.get('desconto', 0)
            orcamento.desconto = Decimal(desconto)
            orcamento.calcular_totais()
            messages.success(request, 'Desconto atualizado!')
            
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'update_status':
            # Atualizar status
            novo_status = request.POST.get('status')
            if novo_status:
                orcamento.status = novo_status
                if novo_status == 'APROVADO':
                    orcamento.data_aprovacao = datetime.now()
                orcamento.save()
                messages.success(request, f'Status atualizado para {orcamento.get_status_display()}!')
            
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
    
    # GET - Exibir orçamento
    itens = orcamento.itens.select_related('produto').all()
    montadoras = Montadora.objects.filter(ativa=True).order_by('nome')
    
    context = {
        'orcamento': orcamento,
        'itens': itens,
        'montadoras': montadoras,
        'pode_converter': orcamento.pode_converter()[0],
    }
    return render(request, 'core/orcamento_editar.html', context)


@login_required
def detalhe_orcamento(request, orcamento_id):
    """Ver detalhes do orçamento (somente leitura)"""
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    itens = orcamento.itens.select_related('produto').all()
    
    context = {
        'orcamento': orcamento,
        'itens': itens,
    }
    return render(request, 'core/orcamento_detalhe.html', context)


@login_required
def buscar_produtos_rapido(request):
    """
    Busca rápida de produtos com filtros de montadora e modelo
    Retorna JSON para uso com AJAX
    """
    busca = request.GET.get('q', '')
    montadora_id = request.GET.get('montadora', '')
    modelo_id = request.GET.get('modelo', '')
    limite = int(request.GET.get('limite', 20))
    
    # Busca base
    produtos = Produto.objects.filter(ativo=True)
    
    # Filtro por texto (código, SKU, descrição)
    if busca:
        produtos = busca_fuzzy(produtos, ['codigo', 'codigo_sku', 'codigo_barras', 'descricao', 'aplicacao_generica'], busca)
    # Filtro por montadora
    if montadora_id:
        produtos = produtos.filter(
            aplicacoes__montadora_id=montadora_id
        ).distinct()
    
    # Filtro por modelo específico
    if modelo_id:
        produtos = produtos.filter(
            aplicacoes__id=modelo_id
        ).distinct()
    
    # Selecionar campos necessários e limitar
    produtos = produtos.select_related(
        'categoria', 'fabricante'
    ).prefetch_related(
        'aplicacoes__montadora'
    )[:limite]
    
    # Montar resposta JSON
    resultados = []
    for p in produtos:
        # Status de estoque
        situacao = p.get_situacao_estoque()
        status_estoque = {
            'critico': 'danger',
            'baixo': 'warning',
            'normal': 'success',
            'excesso': 'info'
        }.get(situacao, 'secondary')
        
        # Aplicações
        aplicacoes_list = [
            {
                'montadora': app.montadora.nome,
                'modelo': app.nome,
                'anos': f"{app.ano_inicial}-{app.ano_final or 'atual'}"
            }
            for app in p.aplicacoes.all()[:3]  # Primeiras 3
        ]
        
        resultados.append({
            'id': p.id,
            'codigo': p.codigo,
            'codigo_sku': p.codigo_sku,
            'descricao': p.descricao,
            'categoria': p.categoria.nome,
            'fabricante': p.fabricante.nome if p.fabricante else '',
            'preco_dinheiro': float(p.preco_venda_dinheiro),
            'preco_debito': float(p.preco_venda_debito),
            'preco_credito': float(p.preco_venda_credito),
            'preco_atacado': float(p.preco_atacado) if p.preco_atacado else float(p.preco_venda_dinheiro),
            'estoque_atual': p.estoque_atual,
            'estoque_disponivel': p.estoque_disponivel,
            'status_estoque': status_estoque,
            'situacao': situacao,
            'aplicacoes': aplicacoes_list,
            'localizacao': p.get_localizacao_completa(),
        })
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'produtos': resultados
    })


@login_required
def buscar_modelos_por_montadora(request):
    """
    Busca modelos de uma montadora específica
    Retorna JSON para uso com AJAX
    """
    montadora_id = request.GET.get('montadora_id')
    
    if not montadora_id:
        return JsonResponse({'success': False, 'error': 'Montadora não informada'})
    
    modelos = VeiculoModelo.objects.filter(
        montadora_id=montadora_id,
        ativo=True
    ).order_by('nome', '-ano_inicial')
    
    resultados = [
        {
            'id': m.id,
            'nome': m.nome,
            'descricao': m.get_descricao_completa(),
            'ano_inicial': m.ano_inicial,
            'ano_final': m.ano_final,
            'motorizacoes': m.motorizacoes,
            'popular': m.popular,
        }
        for m in modelos
    ]
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'modelos': resultados
    })


@login_required
def converter_orcamento_venda(request, orcamento_id):
    """Converte um orçamento aprovado em venda"""
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    # Verificar se pode converter
    pode, motivo = orcamento.pode_converter()
    if not pode:
        messages.error(request, f'Não é possível converter: {motivo}')
        return redirect('detalhe_orcamento', orcamento_id=orcamento.id)
    
    if request.method == 'POST':
        try:
            from vendas.models import Venda, ItemVenda
            from django.db import transaction
            
            with transaction.atomic():
                # Criar venda
                venda = Venda.objects.create(
                    cliente=orcamento.cliente,
                    forma_pagamento=orcamento.forma_pagamento,
                    status='A',  # Aberta
                    desconto=orcamento.desconto,
                    total=orcamento.total,
                )
                
                # Criar itens da venda
                for item_orc in orcamento.itens.all():
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=item_orc.produto,
                        quantidade=item_orc.quantidade,
                        preco_unitario=item_orc.preco_unitario,
                        desconto=item_orc.desconto_item,
                        total=item_orc.total,
                    )
                
                # Atualizar orçamento
                orcamento.status = 'CONVERTIDO'
                orcamento.data_conversao = datetime.now()
                orcamento.venda_gerada = venda
                orcamento.save()
                
                messages.success(request, f'Orçamento convertido em venda #{venda.id} com sucesso!')
                return redirect('detalhe_venda', venda_id=venda.id)
        
        except Exception as e:
            messages.error(request, f'Erro ao converter orçamento: {str(e)}')
            return redirect('detalhe_orcamento', orcamento_id=orcamento.id)
    
    context = {
        'orcamento': orcamento,
    }
    return render(request, 'core/orcamento_confirmar_conversao.html', context)


# ADICIONE ESTAS VIEWS NO core/views.py

from estoque.models import Categoria, Subcategoria, Fabricante

# ==========================================
# MÓDULO DE CATEGORIAS E SUBCATEGORIAS
# ==========================================

@login_required
def lista_categorias(request):
    """Lista todas as categorias com suas subcategorias"""
    categorias = Categoria.objects.filter(ativo=True).prefetch_related('subcategorias')
    
    # Estatísticas
    stats = {
        'total_categorias': categorias.count(),
        'total_subcategorias': Subcategoria.objects.filter(ativo=True).count(),
        'categorias_sem_produtos': categorias.filter(produtos__isnull=True).distinct().count(),
    }
    
    context = {
        'categorias': categorias,
        'stats': stats,
    }
    return render(request, 'core/categorias_lista.html', context)


@login_required
def criar_categoria(request):
    """Criar nova categoria"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        icone = request.POST.get('icone', 'bi-box')
        
        if nome:
            categoria = Categoria.objects.create(
                nome=nome,
                descricao=descricao,
                icone=icone,
                ativo=True
            )
            messages.success(request, f'Categoria "{nome}" criada com sucesso!')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Nome da categoria é obrigatório!')
    
    # Lista de ícones Bootstrap Icons disponíveis
    icones_disponiveis = [
        ('bi-box', 'Caixa'),
        ('bi-gear', 'Engrenagem'),
        ('bi-battery-charging', 'Bateria'),
        ('bi-shield', 'Escudo'),
        ('bi-droplet', 'Gota'),
        ('bi-speedometer', 'Velocímetro'),
        ('bi-wrench', 'Chave'),
        ('bi-tools', 'Ferramentas'),
        ('bi-lightning', 'Raio'),
        ('bi-grid', 'Grade'),
    ]
    
    context = {
        'icones': icones_disponiveis,
    }
    return render(request, 'core/categoria_form.html', context)


@login_required
def editar_categoria(request, categoria_id):
    """Editar categoria existente"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome', categoria.nome)
        categoria.descricao = request.POST.get('descricao', '')
        categoria.icone = request.POST.get('icone', categoria.icone)
        categoria.ativo = request.POST.get('ativo') == 'on'
        categoria.save()
        
        messages.success(request, f'Categoria "{categoria.nome}" atualizada!')
        return redirect('lista_categorias')
    
    icones_disponiveis = [
        ('bi-box', 'Caixa'),
        ('bi-gear', 'Engrenagem'),
        ('bi-battery-charging', 'Bateria'),
        ('bi-shield', 'Escudo'),
        ('bi-droplet', 'Gota'),
        ('bi-speedometer', 'Velocímetro'),
        ('bi-wrench', 'Chave'),
        ('bi-tools', 'Ferramentas'),
        ('bi-lightning', 'Raio'),
        ('bi-grid', 'Grade'),
    ]
    
    context = {
        'categoria': categoria,
        'icones': icones_disponiveis,
        'editando': True,
    }
    return render(request, 'core/categoria_form.html', context)


@login_required
def deletar_categoria(request, categoria_id):
    """Desativar categoria"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    # Verificar se tem produtos vinculados
    if categoria.produtos.exists():
        messages.warning(request, f'Categoria "{categoria.nome}" tem produtos vinculados. Foi desativada.')
        categoria.ativo = False
        categoria.save()
    else:
        categoria.delete()
        messages.success(request, f'Categoria "{categoria.nome}" removida!')
    
    return redirect('lista_categorias')


@login_required
def criar_subcategoria(request, categoria_id):
    """Criar subcategoria para uma categoria"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        
        if nome:
            subcategoria = Subcategoria.objects.create(
                categoria=categoria,
                nome=nome,
                descricao=descricao,
                ativo=True
            )
            messages.success(request, f'Subcategoria "{nome}" criada em "{categoria.nome}"!')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Nome da subcategoria é obrigatório!')
    
    context = {
        'categoria': categoria,
    }
    return render(request, 'core/subcategoria_form.html', context)


@login_required
def editar_subcategoria(request, subcategoria_id):
    """Editar subcategoria"""
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    
    if request.method == 'POST':
        subcategoria.nome = request.POST.get('nome', subcategoria.nome)
        subcategoria.descricao = request.POST.get('descricao', '')
        subcategoria.ativo = request.POST.get('ativo') == 'on'
        subcategoria.save()
        
        messages.success(request, f'Subcategoria "{subcategoria.nome}" atualizada!')
        return redirect('lista_categorias')
    
    context = {
        'subcategoria': subcategoria,
        'categoria': subcategoria.categoria,
        'editando': True,
    }
    return render(request, 'core/subcategoria_form.html', context)


@login_required
def deletar_subcategoria(request, subcategoria_id):
    """Desativar ou deletar subcategoria"""
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    
    # Verificar se tem produtos vinculados
    if subcategoria.produtos.exists():
        messages.warning(request, f'Subcategoria "{subcategoria.nome}" tem produtos. Foi desativada.')
        subcategoria.ativo = False
        subcategoria.save()
    else:
        categoria_nome = subcategoria.categoria.nome
        subcategoria.delete()
        messages.success(request, f'Subcategoria removida de "{categoria_nome}"!')
    
    return redirect('lista_categorias')


@login_required
def api_buscar_subcategorias(request):
    """API: Buscar subcategorias de uma categoria"""
    categoria_id = request.GET.get('categoria_id')
    
    if not categoria_id:
        return JsonResponse({'success': False, 'error': 'Categoria não informada'})
    
    subcategorias = Subcategoria.objects.filter(
        categoria_id=categoria_id,
        ativo=True
    ).order_by('nome')
    
    resultados = [
        {
            'id': s.id,
            'nome': s.nome,
            'descricao': s.descricao or '',
        }
        for s in subcategorias
    ]
    
    return JsonResponse({
        'success': True,
        'count': len(resultados),
        'subcategorias': resultados
    })



@login_required
def api_buscar_subcategorias(request):
    """API: Buscar subcategorias de uma categoria"""
    categoria_id = request.GET.get('categoria_id')
    
    if not categoria_id:
        return JsonResponse({'success': False, 'error': 'Categoria não informada'})
    
    try:
        subcategorias = Subcategoria.objects.filter(
            categoria_id=categoria_id,
            ativo=True
        ).order_by('nome')
        
        resultados = [
            {
                'id': s.id,
                'nome': s.nome,
                'descricao': s.descricao or '',
            }
            for s in subcategorias
        ]
        
        return JsonResponse({
            'success': True,
            'count': len(resultados),
            'subcategorias': resultados
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

    