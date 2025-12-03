from django.http import JsonResponse
from vendas.models import Venda, OrdemServico
from django.utils import timezone
from datetime import date
import json
from estoque.forms import ProdutoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F, Q, Avg, Min, Max, Prefetch
from datetime import datetime, timedelta
from clientes.models import Cliente, Veiculo
from estoque.models import Grupo, Subgrupo
from estoque.models import AmperagemBateria
from estoque.models import (
    Produto, Categoria, Subcategoria, Fabricante,
    Fornecedor, CotacaoFornecedor, Montadora, 
    VeiculoModelo, VeiculoVersao,
    MovimentacaoEstoque,AmperagemBateria, EstoqueCasco,
    MovimentacaoCasco, ItemVendaBateria,  # ✅ CORRIGIDO: Adicionado import que faltava
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
    produtos = Produto.objects.filter(filtros).select_related('categoria', 'fabricante', 'amperagem_bateria')[:50]
    
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

            # ========== CAMPOS DE BATERIA ==========
            'amperagem_bateria_id': p.amperagem_bateria_id if p.amperagem_bateria else None,
            'amperagem_nome': p.amperagem_bateria.amperagem if p.amperagem_bateria else None,
            'valor_casco': float(p.amperagem_bateria.valor_casco_troca) if p.amperagem_bateria else 0,
            'is_bateria': p.amperagem_bateria is not None,
            # ========================================
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
    """Lista produtos do estoque com filtros avançados multi-seleção"""
    
    # Parâmetros de busca
    busca = request.GET.get('busca', '')
    situacao = request.GET.get('situacao', '')
    
    # Filtros multi-seleção (podem ser múltiplos valores)
    categorias_ids = request.GET.getlist('categorias')
    subcategorias_ids = request.GET.getlist('subcategorias')
    grupos_ids = request.GET.getlist('grupos')
    subgrupos_ids = request.GET.getlist('subgrupos')
    montadoras_ids = request.GET.getlist('montadoras')
    
    # QuerySet base
    produtos = Produto.objects.filter(ativo=True)
    
    # ============================================================
    # BUSCA FUZZY - Todas as palavras devem ser encontradas
    # ============================================================
    if busca:
        palavras = busca.split()
        for palavra in palavras:
            produtos = produtos.filter(
                Q(codigo__icontains=palavra) |
                Q(descricao__icontains=palavra) |
                Q(codigo_sku__icontains=palavra) |
                Q(codigo_barras__icontains=palavra) |
                Q(referencia_fabricante__icontains=palavra)
            )
    
    # ============================================================
    # FILTROS DE CATEGORIZAÇÃO (Multi-seleção)
    # ============================================================
    if categorias_ids:
        produtos = produtos.filter(categoria_id__in=categorias_ids)
    
    if subcategorias_ids:
        produtos = produtos.filter(subcategoria_id__in=subcategorias_ids)
    
    if grupos_ids:
        produtos = produtos.filter(grupo_id__in=grupos_ids)
    
    if subgrupos_ids:
        produtos = produtos.filter(subgrupo_id__in=subgrupos_ids)
    
    # ============================================================
    # FILTRO DE MONTADORAS (via versões compatíveis)
    # ============================================================
    if montadoras_ids:
        produtos = produtos.filter(
            versoes_compativeis__modelo__montadora_id__in=montadoras_ids
        ).distinct()
    
    # ============================================================
    # FILTRO POR SITUAÇÃO DE ESTOQUE
    # ============================================================
    if situacao == 'critico':
        produtos = produtos.filter(estoque_atual__lte=F('estoque_minimo'))
    elif situacao == 'baixo':
        produtos = produtos.filter(
            estoque_atual__gt=F('estoque_minimo'),
            estoque_atual__lte=F('estoque_minimo') * 2
        )
    elif situacao == 'normal':
        produtos = produtos.filter(estoque_atual__gt=F('estoque_minimo') * 2)
    
    # ============================================================
    # OTIMIZAÇÃO DE QUERIES
    # ============================================================
    produtos = produtos.select_related(
        'categoria', 
        'subcategoria',
        'grupo',
        'subgrupo',
        'fabricante', 
        'fornecedor_principal'
    ).order_by('descricao')
    
    # ============================================================
    # PAGINAÇÃO
    # ============================================================
    paginator = Paginator(produtos, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ============================================================
    # DADOS PARA OS FILTROS
    # ============================================================
    todas_categorias = Categoria.objects.filter(ativo=True).order_by('nome')
    todas_montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    
    # Subcategorias, grupos e subgrupos filtrados (para cascata inicial)
    todas_subcategorias = Subcategoria.objects.filter(ativo=True).order_by('nome')
    todos_grupos = Grupo.objects.filter(ativo=True).order_by('nome')
    todos_subgrupos = Subgrupo.objects.filter(ativo=True).order_by('nome')
    
    # Se há categorias selecionadas, filtrar subcategorias
    if categorias_ids:
        todas_subcategorias = todas_subcategorias.filter(categoria_id__in=categorias_ids)
    
    # Se há subcategorias selecionadas, filtrar grupos
    if subcategorias_ids:
        todos_grupos = todos_grupos.filter(subcategoria_id__in=subcategorias_ids)
    
    # Se há grupos selecionados, filtrar subgrupos
    if grupos_ids:
        todos_subgrupos = todos_subgrupos.filter(grupo_id__in=grupos_ids)
    
    # ============================================================
    # ESTATÍSTICAS
    # ============================================================
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

        # Produtos com estoque CRÍTICO
    produtos_criticos = Produto.objects.filter(
        ativo=True,
        estoque_minimo__gt=0,
        estoque_atual__lte=F('estoque_minimo')
    ).select_related('categoria').order_by('estoque_atual', 'descricao')[:50]

    # Produtos com estoque BAIXO
    produtos_baixo_estoque = Produto.objects.filter(
        ativo=True,
        estoque_minimo__gt=0,
        estoque_atual__gt=F('estoque_minimo'),
        estoque_atual__lte=F('estoque_minimo') * 2
    ).select_related('categoria').order_by('estoque_atual', 'descricao')[:50]

    context = {
        'page_obj': page_obj,
        'busca': busca,
        'situacao': situacao,
        'total_produtos': produtos.count(),
        'stats': stats,
        
        # Dados para os filtros
        'categorias': todas_categorias,
        'subcategorias': todas_subcategorias,
        'grupos': todos_grupos,
        'subgrupos': todos_subgrupos,
        'montadoras': todas_montadoras,
        
        # Seleções atuais (para manter estado)
        'categorias_selecionadas': categorias_ids,
        'subcategorias_selecionadas': subcategorias_ids,
        'grupos_selecionados': grupos_ids,
        'subgrupos_selecionados': subgrupos_ids,
        'montadoras_selecionadas': montadoras_ids,

         # Estoque minimo e baixo
        'produtos_criticos': produtos_criticos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
    }
    
    return render(request, 'core/estoque_lista.html', context)


# ============================================================
# APIs PARA CASCATA DINÂMICA (AJAX)
# ============================================================

@login_required
def api_subcategorias_por_categorias(request):
    """
    Retorna subcategorias filtradas pelas categorias selecionadas.
    GET params: categorias (lista de IDs)
    """
    categorias_ids = request.GET.getlist('categorias')
    
    if categorias_ids:
        subcategorias = Subcategoria.objects.filter(
            categoria_id__in=categorias_ids,
            ativo=True
        ).order_by('nome')
    else:
        subcategorias = Subcategoria.objects.filter(ativo=True).order_by('nome')
    
    data = [
        {'id': s.id, 'nome': s.nome, 'categoria_id': s.categoria_id}
        for s in subcategorias
    ]
    
    return JsonResponse({'subcategorias': data})


@login_required
def api_grupos_por_subcategorias(request):
    """
    Retorna grupos filtrados pelas subcategorias selecionadas.
    GET params: subcategorias (lista de IDs)
    """
    subcategorias_ids = request.GET.getlist('subcategorias')
    
    if subcategorias_ids:
        grupos = Grupo.objects.filter(
            subcategoria_id__in=subcategorias_ids,
            ativo=True
        ).order_by('nome')
    else:
        grupos = Grupo.objects.filter(ativo=True).order_by('nome')
    
    data = [
        {'id': g.id, 'nome': g.nome, 'subcategoria_id': g.subcategoria_id}
        for g in grupos
    ]
    
    return JsonResponse({'grupos': data})


@login_required
def api_subgrupos_por_grupos(request):
    """
    Retorna subgrupos filtrados pelos grupos selecionados.
    GET params: grupos (lista de IDs)
    """
    grupos_ids = request.GET.getlist('grupos')
    
    if grupos_ids:
        subgrupos = Subgrupo.objects.filter(
            grupo_id__in=grupos_ids,
            ativo=True
        ).order_by('nome')
    else:
        subgrupos = Subgrupo.objects.filter(ativo=True).order_by('nome')
    
    data = [
        {'id': s.id, 'nome': s.nome, 'grupo_id': s.grupo_id}
        for s in subgrupos
    ]
    
    return JsonResponse({'subgrupos': data})


@login_required  
def api_filtros_estoque(request):
    """
    API unificada que retorna todos os dados de filtro de uma vez.
    Útil para carregar filtros iniciais ou resetar.
    """
    categorias = Categoria.objects.filter(ativo=True).order_by('nome')
    subcategorias = Subcategoria.objects.filter(ativo=True).order_by('nome')
    grupos = Grupo.objects.filter(ativo=True).order_by('nome')
    subgrupos = Subgrupo.objects.filter(ativo=True).order_by('nome')
    montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    
    return JsonResponse({
        'categorias': [{'id': c.id, 'nome': c.nome} for c in categorias],
        'subcategorias': [{'id': s.id, 'nome': s.nome, 'categoria_id': s.categoria_id} for s in subcategorias],
        'grupos': [{'id': g.id, 'nome': g.nome, 'subcategoria_id': g.subcategoria_id} for g in grupos],
        'subgrupos': [{'id': s.id, 'nome': s.nome, 'grupo_id': s.grupo_id} for s in subgrupos],
        'montadoras': [{'id': m.id, 'nome': m.nome} for m in montadoras],
    })



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
        'categorias': Categoria.objects.filter(ativo=True).order_by('nome'),
        'editando': False,
        'amperagens': AmperagemBateria.objects.filter(ativo=True).order_by('ordem'),
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
        'categorias': Categoria.objects.filter(ativo=True).order_by('nome'),
        'editando': True,
        'produto': produto,
        'amperagens': AmperagemBateria.objects.filter(ativo=True).order_by('ordem'),
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
    API para buscar modelos de veículos
    """
    montadora_id = request.GET.get('montadora_id')
    
    if not montadora_id:
        return JsonResponse({'success': False, 'modelos': []})
    
    modelos = VeiculoModelo.objects.filter(
        montadora_id=montadora_id,
        ativo=True
    ).order_by('-popular', 'nome')
    
    resultados = [
        {
            'id': m.id,
            'nome': m.nome,
            'descricao': m.nome,
            'popular': m.popular,
        }
        for m in modelos
    ]
    
    return JsonResponse({
        'success': True,
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
    """Lista de orçamentos com filtros avançados"""
    
    # Parâmetros de filtro
    status_selecionado = request.GET.get('status', '')
    busca = request.GET.get('busca', '')
    vendedor_selecionado = request.GET.get('vendedor', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # QuerySet base
    orcamentos = Orcamento.objects.all().select_related(
        'cliente', 
        'vendedor', 
        'veiculo_modelo',
        'veiculo_modelo__montadora'
    ).order_by('-data_orcamento')
    
    # Filtro por status
    if status_selecionado:
        orcamentos = orcamentos.filter(status=status_selecionado)
    
    # Filtro por busca (número ou cliente)
    if busca:
        orcamentos = orcamentos.filter(
            Q(numero__icontains=busca) |
            Q(cliente__nome__icontains=busca) |
            Q(cliente__cpf_cnpj__icontains=busca)
        )
    
    # Filtro por vendedor
    if vendedor_selecionado:
        orcamentos = orcamentos.filter(vendedor_id=vendedor_selecionado)
    
    # Filtro por período
    if data_inicio:
        orcamentos = orcamentos.filter(data_orcamento__date__gte=data_inicio)
    if data_fim:
        orcamentos = orcamentos.filter(data_orcamento__date__lte=data_fim)
    
    # Paginação
    paginator = Paginator(orcamentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    todos_orcamentos = Orcamento.objects.all()
    stats = {
        'total_orcamentos': todos_orcamentos.count(),
        'valor_total': todos_orcamentos.aggregate(total=Sum('total'))['total'] or 0,
        'abertos': todos_orcamentos.filter(status='ABERTO').count(),
        'aprovados': todos_orcamentos.filter(status='APROVADO').count(),
    }
    
    # Lista de vendedores para o filtro
    from django.contrib.auth import get_user_model
    User = get_user_model()
    vendedores = User.objects.filter(
        orcamentos__isnull=False
    ).distinct().order_by('first_name', 'username')
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'status_selecionado': status_selecionado,
        'busca': busca,
        'vendedor_selecionado': vendedor_selecionado,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'vendedores': vendedores,
        'hoje': timezone.now().date(),
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
    """Edição de orçamento com filtros avançados de categorização"""
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    itens = orcamento.itens.all().select_related('produto', 'produto__fabricante')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_item':
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade', 1))
            produto = get_object_or_404(Produto, id=produto_id)
            
            # Determinar preço baseado na forma de pagamento
            precos = {
                'DINHEIRO': produto.preco_venda_dinheiro,
                'DEBITO': produto.preco_venda_debito,
                'CREDITO': produto.preco_venda_credito,
                'ATACADO': produto.preco_atacado or produto.preco_venda_dinheiro,
            }
            preco_unitario = precos.get(orcamento.forma_pagamento, produto.preco_venda_dinheiro)
            
            # Criar ou atualizar item
            item, created = ItemOrcamento.objects.get_or_create(
                orcamento=orcamento,
                produto=produto,
                defaults={'quantidade': quantidade, 'preco_unitario': preco_unitario}
            )
            if not created:
                item.quantidade += quantidade
                item.save()
            
            orcamento.atualizar_totais()
            messages.success(request, f'Produto {produto.codigo} adicionado!')
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'remove_item':
            item_id = request.POST.get('item_id')
            item = get_object_or_404(ItemOrcamento, id=item_id, orcamento=orcamento)
            item.delete()
            orcamento.atualizar_totais()
            messages.success(request, 'Item removido!')
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'update_desconto':
            desconto = Decimal(request.POST.get('desconto', '0'))
            orcamento.desconto = desconto
            orcamento.save()
            orcamento.atualizar_totais()
            messages.success(request, 'Desconto atualizado!')
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
        
        elif action == 'update_status':
            novo_status = request.POST.get('novo_status')
            if novo_status in ['ENVIADO', 'APROVADO', 'REJEITADO']:
                orcamento.status = novo_status
                if novo_status == 'APROVADO':
                    orcamento.data_aprovacao = timezone.now()
                orcamento.save()
                messages.success(request, f'Status atualizado para {orcamento.get_status_display()}!')
            return redirect('editar_orcamento', orcamento_id=orcamento.id)
    
    # Dados para os filtros avançados
    montadoras = Montadora.objects.filter(ativa=True).order_by('ordem', 'nome')
    categorias = Categoria.objects.filter(ativo=True).order_by('nome')
    subcategorias = Subcategoria.objects.filter(ativo=True).order_by('nome')
    grupos = Grupo.objects.filter(ativo=True).order_by('nome')
    subgrupos = Subgrupo.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'orcamento': orcamento,
        'itens': itens,
        'montadoras': montadoras,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'grupos': grupos,
        'subgrupos': subgrupos,
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
    Busca rápida de produtos com filtros de montadora, modelo e categorização
    Retorna JSON para uso com AJAX
    """
    busca = request.GET.get('q', '')
    montadora_id = request.GET.get('montadora', '')
    modelo_id = request.GET.get('modelo', '')
    limite = int(request.GET.get('limite', 30))
    
    # Filtros de categorização (multi-seleção)
    categorias_ids = request.GET.getlist('categorias')
    subcategorias_ids = request.GET.getlist('subcategorias')
    grupos_ids = request.GET.getlist('grupos')
    subgrupos_ids = request.GET.getlist('subgrupos')
    
    # Busca base
    produtos = Produto.objects.filter(ativo=True)
    
    # Filtro por texto (código, SKU, descrição)
    if busca:
        produtos = busca_fuzzy(
            produtos, 
            ['codigo', 'codigo_sku', 'codigo_barras', 'descricao', 'aplicacao_generica'], 
            busca
        )
    
    # Filtros de categorização
    if categorias_ids:
        produtos = produtos.filter(categoria_id__in=categorias_ids)
    
    if subcategorias_ids:
        produtos = produtos.filter(subcategoria_id__in=subcategorias_ids)
    
    if grupos_ids:
        produtos = produtos.filter(grupo_id__in=grupos_ids)
    
    if subgrupos_ids:
        produtos = produtos.filter(subgrupo_id__in=subgrupos_ids)
    
    # Filtro por montadora (via versões compatíveis)
    if montadora_id:
        produtos = produtos.filter(
            versoes_compativeis__modelo__montadora_id=montadora_id
        ).distinct()
    
    # Filtro por modelo específico (via versões compatíveis)
    if modelo_id:
        produtos = produtos.filter(
            versoes_compativeis__modelo_id=modelo_id
        ).distinct()
    
    # Selecionar campos necessários e limitar
    produtos = produtos.select_related(
        'categoria', 'subcategoria', 'grupo', 'subgrupo', 'fabricante'
    ).prefetch_related(
        'versoes_compativeis__modelo__montadora'
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
        
        # Aplicações (versões compatíveis)
        aplicacoes_list = []
        for versao in p.versoes_compativeis.all()[:3]:
            aplicacoes_list.append({
                'montadora': versao.modelo.montadora.nome,
                'modelo': versao.modelo.nome,
                'versao': versao.nome,
                'anos': f"{versao.ano_inicial}-{versao.ano_final or 'atual'}"
            })
        
        # Categoria completa
        categoria_completa = p.categoria.nome if p.categoria else ''
        if p.subcategoria:
            categoria_completa += f' > {p.subcategoria.nome}'
        
        resultados.append({
            'id': p.id,
            'codigo': p.codigo,
            'codigo_sku': p.codigo_sku or '',
            'descricao': p.descricao,
            'categoria': p.categoria.nome if p.categoria else '',
            'categoria_completa': categoria_completa,
            'subcategoria': p.subcategoria.nome if p.subcategoria else '',
            'grupo': p.grupo.nome if p.grupo else '',
            'subgrupo': p.subgrupo.nome if p.subgrupo else '',
            'fabricante': p.fabricante.nome if p.fabricante else '',
            'preco_dinheiro': float(p.preco_venda_dinheiro or 0),
            'preco_debito': float(p.preco_venda_debito or 0),
            'preco_credito': float(p.preco_venda_credito or 0),
            'preco_atacado': float(p.preco_atacado) if p.preco_atacado else float(p.preco_venda_dinheiro or 0),
            'estoque_atual': p.estoque_atual,
            'estoque_disponivel': getattr(p, 'estoque_disponivel', p.estoque_atual),
            'status_estoque': status_estoque,
            'situacao': situacao,
            'aplicacoes': aplicacoes_list,
            'localizacao': p.get_localizacao_completa() if hasattr(p, 'get_localizacao_completa') else '',
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
    ).order_by('nome')
    
    resultados = []
    for m in modelos:
        # Buscar versões do modelo
        versoes = m.versoes.filter(ativo=True).order_by('-ano_inicial')
        
        resultados.append({
            'id': m.id,
            'nome': m.nome,
            'descricao': m.nome,  # Para compatibilidade
            'tipo': m.tipo,
            'popular': m.popular,
            'versoes': [
                {
                    'id': v.id,
                    'nome': v.nome,
                    'ano_inicial': v.ano_inicial,
                    'ano_final': v.ano_final,
                    'motorizacoes': v.motorizacoes,
                }
                for v in versoes
            ]
        })
    
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


# ==========================================
# MÓDULO DE CATEGORIAS E SUBCATEGORIAS
# ==========================================

@login_required
def lista_categorias(request):
    """Lista todas as categorias com suas subcategorias"""
    categorias = Categoria.objects.filter(ativo=True).prefetch_related('subcategorias')
    
    # Estatísticas
    stats = {
        'total_categorias': Categoria.objects.filter(ativo=True).count(),
        'total_subcategorias': Subcategoria.objects.filter(ativo=True).count(),
        'total_grupos': Grupo.objects.filter(ativo=True).count(),
        'total_subgrupos': Subgrupo.objects.filter(ativo=True).count(),
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
    

    
# ==========================================
# API PARA SALVAR VENDA DO PDV
# ==========================================
from vendas.models import Venda, ItemVenda
from financeiro.models import ContaReceber, VendaParcelada, CategoriaReceita
import json

@login_required
def api_salvar_venda_pdv(request):
    """API para salvar venda do PDV e criar parcelas no financeiro se necessário"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    try:
        dados = json.loads(request.body)
        
        cliente_id = dados.get('cliente_id')
        forma_pagamento = dados.get('forma_pagamento')
        itens = dados.get('itens', [])
        subtotal = Decimal(str(dados.get('subtotal', 0)))
        desconto = Decimal(str(dados.get('desconto', 0)))
        acrescimo = Decimal(str(dados.get('acrescimo', 0)))
        total = Decimal(str(dados.get('total', 0)))
        parcelas = int(dados.get('parcelas', 1))
        observacoes = dados.get('observacoes', '')
        
        # Validações
        if not itens:
            return JsonResponse({'success': False, 'error': 'Carrinho vazio'})
        
        if not forma_pagamento:
            return JsonResponse({'success': False, 'error': 'Forma de pagamento não informada'})
        
        # Se for crediário, cliente é obrigatório
        if forma_pagamento == 'CR' and not cliente_id:
            return JsonResponse({'success': False, 'error': 'Cliente obrigatório para crediário'})
        
        # Mapear forma de pagamento do PDV para o modelo
        mapa_forma = {
            'DI': 'DI',  # Dinheiro
            'PI': 'PI',  # PIX
            'DB': 'CD',  # Débito
            'CC': 'CC',  # Crédito à vista
            'CP': 'CC',  # Crédito parcelado (ainda é cartão de crédito)
            'CR': 'CR',  # Crediário
        }
        forma_pagamento_db = mapa_forma.get(forma_pagamento, 'DI')
        
        with transaction.atomic():
            # Gerar número da venda
            ultima_venda = Venda.objects.order_by('-id').first()
            if ultima_venda and ultima_venda.numero:
                try:
                    ultimo_num = int(ultima_venda.numero.replace('V', '').replace('-', ''))
                    novo_num = ultimo_num + 1
                except:
                    novo_num = 1
            else:
                novo_num = 1
            numero_venda = f"V{novo_num:06d}"
            
            # Buscar cliente se informado
            cliente = None
            if cliente_id:
                cliente = Cliente.objects.filter(id=cliente_id).first()
            
            # Se não tem cliente, criar/buscar cliente genérico
            if not cliente:
                cliente, _ = Cliente.objects.get_or_create(
                    cpf_cnpj='00000000000',
                    defaults={
                        'nome': 'Cliente não identificado',
                        'ativo': True
                    }
                )
            
            # Criar a venda
            venda = Venda.objects.create(
                numero=numero_venda,
                cliente=cliente,
                forma_pagamento=forma_pagamento_db,
                status='F',  # Finalizada
                subtotal=subtotal,
                desconto=desconto,
                total=total,
                observacoes=observacoes,
                vendedor=request.user.username
            )
            
            # Criar itens da venda e baixar estoque
            for item in itens:
                produto = Produto.objects.get(id=item['id'])
                quantidade = Decimal(str(item['quantidade']))
                preco_unitario = Decimal(str(item['preco']))
                total_item = quantidade * preco_unitario
                
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=int(quantidade),
                    valor_unitario=preco_unitario,
                    total=total_item
                )
                
                # Baixar estoque
                produto.estoque_atual -= quantidade
                produto.save()

                # ============================================
                # MOVIMENTACAO DE CASCOS (BATERIAS)
                # ============================================
                if item.get('is_bateria') and produto.amperagem_bateria:
                    info_casco = item.get('info_casco', {})
                    amperagem_vendida = produto.amperagem_bateria
                    trouxe_casco = info_casco.get('trouxe_casco', False) if info_casco else False
                    
                    if trouxe_casco:
                        # Cliente trouxe casco
                        amperagem_casco_id = info_casco.get('amperagem_casco_id')
                        
                        if amperagem_casco_id:
                            amperagem_casco = AmperagemBateria.objects.filter(id=amperagem_casco_id).first()
                            
                            if amperagem_casco and amperagem_casco.id != amperagem_vendida.id:
                                # Amperagens diferentes: saida da vendida, entrada da recebida
                                
                                # Saida do casco da bateria vendida
                                MovimentacaoCasco.objects.create(
                                    amperagem=amperagem_vendida,
                                    tipo='S',
                                    motivo='VENDA_COM_TROCA',
                                    quantidade=int(quantidade),
                                    observacao=f'Venda {numero_venda} - Troca por casco {amperagem_casco.amperagem}',
                                    usuario=request.user,
                                    venda=venda
                                )
                                
                                # Entrada do casco recebido
                                MovimentacaoCasco.objects.create(
                                    amperagem=amperagem_casco,
                                    tipo='E',
                                    motivo='VENDA_COM_TROCA',
                                    quantidade=int(quantidade),
                                    observacao=f'Venda {numero_venda} - Casco recebido em troca de {amperagem_vendida.amperagem}',
                                    usuario=request.user,
                                    venda=venda
                                )
                            # Se mesma amperagem, nao precisa movimentar (entra e sai igual)
                    else:
                        # Cliente NAO trouxe casco - diminui estoque de casco
                        MovimentacaoCasco.objects.create(
                            amperagem=amperagem_vendida,
                            tipo='S',
                            motivo='VENDA_SEM_TROCA',
                            quantidade=int(quantidade),
                            observacao=f'Venda {numero_venda} - Sem troca de casco',
                            usuario=request.user,
                            venda=venda
                        )

            # Se for CREDIARIO, criar parcelas no financeiro
            if forma_pagamento == 'CR' and parcelas > 0:
                # Buscar ou criar categoria de receita padrão
                categoria_receita, _ = CategoriaReceita.objects.get_or_create(
                    nome='Vendas de Peças',
                    defaults={
                        'tipo': 'VENDA',
                        'icone': 'bi-box-seam',
                        'cor': '#22c55e'
                    }
                )
                
                # Criar VendaParcelada
                venda_parcelada = VendaParcelada.objects.create(
                    descricao=f'Venda {numero_venda}',
                    categoria=categoria_receita,
                    cliente=cliente,
                    venda=venda,
                    valor_total=total,
                    numero_parcelas=parcelas,
                    data_primeira_parcela=date.today() + timedelta(days=30),
                    intervalo_tipo='MENSAL',
                    forma_cobranca='FIADO',
                    usuario_cadastro=request.user
                )
                
                # Gerar as parcelas
                venda_parcelada.gerar_parcelas()
            
            # Se for cartão de crédito parcelado no cartão (loja não recebe parcelado)
            # Criar receita única pois a administradora paga à vista
            elif forma_pagamento in ['DI', 'PI', 'DB', 'CC', 'CP']:
                # Buscar ou criar categoria de receita padrão
                categoria_receita, _ = CategoriaReceita.objects.get_or_create(
                    nome='Vendas de Peças',
                    defaults={
                        'tipo': 'VENDA',
                        'icone': 'bi-box-seam',
                        'cor': '#22c55e'
                    }
                )
                
                # Criar receita única (já recebida)
                ContaReceber.objects.create(
                    descricao=f'Venda {numero_venda}',
                    categoria=categoria_receita,
                    tipo='VENDA',
                    valor=total,
                    data_vencimento=date.today(),
                    data_recebimento=date.today(),
                    status='RECEBIDO',
                    forma_cobranca='DINHEIRO' if forma_pagamento in ['DI', 'PI'] else 'CARTAO',
                    cliente=cliente if cliente.cpf_cnpj != '00000000000' else None,
                    venda=venda,
                    valor_recebido=total,
                    usuario_cadastro=request.user
                )
        
        return JsonResponse({
            'success': True,
            'venda_id': venda.id,
            'numero': numero_venda,
            'message': f'Venda {numero_venda} realizada com sucesso!'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

# ==========================================
# EDITAR E CANCELAR VENDA
# ==========================================

@login_required
def editar_venda(request, venda_id):
    """Editar venda existente"""
    venda = get_object_or_404(Venda.objects.select_related('cliente').prefetch_related('itens__produto'), id=venda_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # CANCELAR VENDA
        if action == 'cancelar':
            if venda.status != 'C':  # Se ainda não está cancelada
                with transaction.atomic():
                    # Devolver estoque de todos os itens
                    for item in venda.itens.all():
                        item.produto.estoque_atual += item.quantidade
                        item.produto.save()
                    
                    # Cancelar parcelas no financeiro (se houver)
                    ContaReceber.objects.filter(venda=venda, status__in=['PENDENTE', 'ATRASADO']).update(status='CANCELADO')
                    
                    # Marcar venda como cancelada
                    venda.status = 'C'
                    venda.save()
                    
                    messages.success(request, f'Venda {venda.numero} cancelada e estoque devolvido!')
            else:
                messages.warning(request, 'Esta venda já está cancelada.')
            
            return redirect('lista_vendas')
        
        # ATUALIZAR DADOS DA VENDA
        elif action == 'atualizar':
            try:
                venda.observacoes = request.POST.get('observacoes', '')
                
                # Atualizar cliente se informado
                cliente_id = request.POST.get('cliente_id')
                if cliente_id:
                    venda.cliente = Cliente.objects.get(id=cliente_id)
                
                venda.save()
                messages.success(request, f'Venda {venda.numero} atualizada!')
                
            except Exception as e:
                messages.error(request, f'Erro ao atualizar: {str(e)}')
            
            return redirect('editar_venda', venda_id=venda.id)
        
        # REMOVER ITEM
        elif action == 'remover_item':
            item_id = request.POST.get('item_id')
            try:
                with transaction.atomic():
                    item = venda.itens.get(id=item_id)
                    
                    # Devolver estoque
                    item.produto.estoque_atual += item.quantidade
                    item.produto.save()
                    
                    # Atualizar total da venda
                    venda.total -= item.total
                    venda.subtotal -= item.total
                    venda.save()
                    
                    # Remover item
                    item.delete()
                    
                    messages.success(request, f'Item removido e estoque devolvido!')
                    
            except Exception as e:
                messages.error(request, f'Erro ao remover item: {str(e)}')
            
            return redirect('editar_venda', venda_id=venda.id)
    
    # GET - Exibir página
    clientes = Cliente.objects.filter(ativo=True).order_by('nome')
    
    # Buscar parcelas financeiras vinculadas
    parcelas = ContaReceber.objects.filter(venda=venda).order_by('parcela_atual')
    
    context = {
        'venda': venda,
        'clientes': clientes,
        'parcelas': parcelas,
    }
    
    return render(request, 'core/venda_editar.html', context)


@login_required
def api_cancelar_venda(request, venda_id):
    """API para cancelar venda via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    try:
        venda = Venda.objects.get(id=venda_id)
        
        if venda.status == 'C':
            return JsonResponse({'success': False, 'error': 'Venda já está cancelada'})
        
        with transaction.atomic():
            # Devolver estoque
            for item in venda.itens.all():
                item.produto.estoque_atual += item.quantidade
                item.produto.save()
            
            # Cancelar parcelas no financeiro
            ContaReceber.objects.filter(venda=venda, status__in=['PENDENTE', 'ATRASADO']).update(status='CANCELADO')
            
            # Cancelar venda
            venda.status = 'C'
            venda.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Venda {venda.numero} cancelada com sucesso!'
        })
        
    except Venda.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Venda não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    


@login_required
def api_buscar_grupos(request):
    """API: Buscar grupos de uma subcategoria"""
    from estoque.models import Grupo
    
    subcategoria_id = request.GET.get('subcategoria_id')
    
    if not subcategoria_id:
        return JsonResponse({'success': False, 'grupos': []})
    
    try:
        grupos = Grupo.objects.filter(
            subcategoria_id=subcategoria_id,
            ativo=True
        ).order_by('nome')
        
        resultados = [
            {
                'id': g.id,
                'nome': g.nome,
            }
            for g in grupos
        ]
        
        return JsonResponse({'success': True, 'grupos': resultados})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def api_buscar_subgrupos(request):
    """API: Buscar subgrupos de um grupo"""
    from estoque.models import Subgrupo
    
    grupo_id = request.GET.get('grupo_id')
    
    if not grupo_id:
        return JsonResponse({'success': False, 'subgrupos': []})
    
    try:
        subgrupos = Subgrupo.objects.filter(
            grupo_id=grupo_id,
            ativo=True
        ).order_by('nome')
        
        resultados = [
            {
                'id': s.id,
                'nome': s.nome,
            }
            for s in subgrupos
        ]
        
        return JsonResponse({'success': True, 'subgrupos': resultados})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def criar_grupo(request, subcategoria_id):
    """Criar novo grupo dentro de uma subcategoria"""
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        ativo = request.POST.get('ativo') == 'on'
        
        if not nome:
            messages.error(request, 'O nome do grupo é obrigatório!')
        elif Grupo.objects.filter(subcategoria=subcategoria, nome__iexact=nome).exists():
            messages.error(request, f'Já existe um grupo "{nome}" nesta subcategoria!')
        else:
            Grupo.objects.create(
                subcategoria=subcategoria,
                nome=nome,
                descricao=descricao,
                ativo=ativo
            )
            messages.success(request, f'Grupo "{nome}" criado com sucesso!')
            return redirect('lista_categorias')
    
    context = {
        'subcategoria': subcategoria,
        'editando': False,
    }
    return render(request, 'core/grupo_form.html', context)


@login_required
def editar_grupo(request, grupo_id):
    """Editar grupo existente"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        ativo = request.POST.get('ativo') == 'on'
        
        if not nome:
            messages.error(request, 'O nome do grupo é obrigatório!')
        elif Grupo.objects.filter(subcategoria=grupo.subcategoria, nome__iexact=nome).exclude(id=grupo.id).exists():
            messages.error(request, f'Já existe um grupo "{nome}" nesta subcategoria!')
        else:
            grupo.nome = nome
            grupo.descricao = descricao
            grupo.ativo = ativo
            grupo.save()
            messages.success(request, f'Grupo "{nome}" atualizado com sucesso!')
            return redirect('lista_categorias')
    
    context = {
        'grupo': grupo,
        'subcategoria': grupo.subcategoria,
        'editando': True,
    }
    return render(request, 'core/grupo_form.html', context)


@login_required
def deletar_grupo(request, grupo_id):
    """Deletar grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    nome = grupo.nome
    
    # Verificar se tem subgrupos
    if grupo.subgrupos.exists():
        messages.error(request, f'Não é possível remover o grupo "{nome}" pois possui subgrupos vinculados!')
    # Verificar se tem produtos
    elif grupo.produtos.exists():
        messages.error(request, f'Não é possível remover o grupo "{nome}" pois possui produtos vinculados!')
    else:
        grupo.delete()
        messages.success(request, f'Grupo "{nome}" removido com sucesso!')
    
    return redirect('lista_categorias')


# ============================================================
# SUBGRUPO - CRUD
# ============================================================

@login_required
def criar_subgrupo(request, grupo_id):
    """Criar novo subgrupo dentro de um grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        ativo = request.POST.get('ativo') == 'on'
        
        if not nome:
            messages.error(request, 'O nome do subgrupo é obrigatório!')
        elif Subgrupo.objects.filter(grupo=grupo, nome__iexact=nome).exists():
            messages.error(request, f'Já existe um subgrupo "{nome}" neste grupo!')
        else:
            Subgrupo.objects.create(
                grupo=grupo,
                nome=nome,
                descricao=descricao,
                ativo=ativo
            )
            messages.success(request, f'Subgrupo "{nome}" criado com sucesso!')
            return redirect('lista_categorias')
    
    context = {
        'grupo': grupo,
        'editando': False,
    }
    return render(request, 'core/subgrupo_form.html', context)


@login_required
def editar_subgrupo(request, subgrupo_id):
    """Editar subgrupo existente"""
    subgrupo = get_object_or_404(Subgrupo, id=subgrupo_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        ativo = request.POST.get('ativo') == 'on'
        
        if not nome:
            messages.error(request, 'O nome do subgrupo é obrigatório!')
        elif Subgrupo.objects.filter(grupo=subgrupo.grupo, nome__iexact=nome).exclude(id=subgrupo.id).exists():
            messages.error(request, f'Já existe um subgrupo "{nome}" neste grupo!')
        else:
            subgrupo.nome = nome
            subgrupo.descricao = descricao
            subgrupo.ativo = ativo
            subgrupo.save()
            messages.success(request, f'Subgrupo "{nome}" atualizado com sucesso!')
            return redirect('lista_categorias')
    
    context = {
        'subgrupo': subgrupo,
        'grupo': subgrupo.grupo,
        'editando': True,
    }
    return render(request, 'core/subgrupo_form.html', context)


@login_required
def deletar_subgrupo(request, subgrupo_id):
    """Deletar subgrupo"""
    subgrupo = get_object_or_404(Subgrupo, id=subgrupo_id)
    nome = subgrupo.nome
    
    # Verificar se tem produtos
    if subgrupo.produtos.exists():
        messages.error(request, f'Não é possível remover o subgrupo "{nome}" pois possui produtos vinculados!')
    else:
        subgrupo.delete()
        messages.success(request, f'Subgrupo "{nome}" removido com sucesso!')
    
    return redirect('lista_categorias')



@login_required
def api_amperagens_bateria(request):
    """Retorna lista de amperagens para o modal de troca de casco"""
    amperagens = AmperagemBateria.objects.filter(ativo=True).order_by('ordem')
    
    dados = [
        {
            'id': a.id,
            'amperagem': a.amperagem,
            'nome_tecnico': a.nome_tecnico or '',
            'valor_casco_troca': float(a.valor_casco_troca),
            'peso_kg': float(a.peso_kg),
        }
        for a in amperagens
    ]
    
    return JsonResponse({'success': True, 'amperagens': dados})


# ============================================================
# API: Calcular diferença de casco
# ============================================================
@login_required
def api_calcular_casco(request):
    """
    Calcula a diferença de valor do casco.
    
    Parâmetros:
    - amperagem_vendida_id: ID da amperagem da bateria vendida
    - trouxe_casco: 'true' ou 'false'
    - amperagem_casco_id: ID da amperagem do casco trazido (se trouxe)
    
    Retorna:
    - diferenca: valor positivo (acréscimo) ou negativo (desconto)
    - valor_casco_vendido: valor do casco da bateria vendida
    - valor_casco_recebido: valor do casco trazido (se trouxe)
    """
    amperagem_vendida_id = request.GET.get('amperagem_vendida_id')
    trouxe_casco = request.GET.get('trouxe_casco', 'false') == 'true'
    amperagem_casco_id = request.GET.get('amperagem_casco_id')
    
    if not amperagem_vendida_id:
        return JsonResponse({'success': False, 'error': 'Amperagem da bateria não informada'})
    
    try:
        amperagem_vendida = AmperagemBateria.objects.get(id=amperagem_vendida_id)
        valor_casco_vendido = float(amperagem_vendida.valor_casco_troca)
        
        if not trouxe_casco:
            # Cliente não trouxe casco = paga o valor do casco
            return JsonResponse({
                'success': True,
                'trouxe_casco': False,
                'valor_casco_vendido': valor_casco_vendido,
                'valor_casco_recebido': 0,
                'diferenca': valor_casco_vendido,  # Acréscimo
                'mensagem': f'Acréscimo de R$ {valor_casco_vendido:.2f} (sem casco)'
            })
        
        # Cliente trouxe casco
        if not amperagem_casco_id:
            return JsonResponse({'success': False, 'error': 'Amperagem do casco não informada'})
        
        amperagem_casco = AmperagemBateria.objects.get(id=amperagem_casco_id)
        valor_casco_recebido = float(amperagem_casco.valor_casco_troca)
        
        diferenca = valor_casco_vendido - valor_casco_recebido
        
        if diferenca > 0:
            mensagem = f'Acréscimo de R$ {diferenca:.2f} (casco menor)'
        elif diferenca < 0:
            mensagem = f'Desconto de R$ {abs(diferenca):.2f} (casco maior)'
        else:
            mensagem = 'Troca normal (mesmo valor de casco)'
        
        return JsonResponse({
            'success': True,
            'trouxe_casco': True,
            'valor_casco_vendido': valor_casco_vendido,
            'valor_casco_recebido': valor_casco_recebido,
            'diferenca': diferenca,
            'mensagem': mensagem
        })
        
    except AmperagemBateria.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Amperagem não encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================================
# API: Estoque de cascos
# ============================================================
@login_required
def api_estoque_cascos(request):
    """Retorna o estoque atual de cascos por amperagem"""
    estoques = EstoqueCasco.objects.select_related('amperagem').filter(
        amperagem__ativo=True
    ).order_by('amperagem__ordem')
    
    dados = [
        {
            'amperagem': e.amperagem.amperagem,
            'nome_tecnico': e.amperagem.nome_tecnico or '',
            'quantidade': e.quantidade,
            'peso_total_kg': float(e.peso_total),
            'valor_total_troca': float(e.valor_total_troca),
            'valor_total_compra': float(e.valor_total_compra),
        }
        for e in estoques
    ]
    
    # Totais
    total_cascos = sum(e.quantidade for e in estoques)
    total_peso = sum(float(e.peso_total) for e in estoques)
    total_valor_troca = sum(float(e.valor_total_troca) for e in estoques)
    total_valor_compra = sum(float(e.valor_total_compra) for e in estoques)
    
    return JsonResponse({
        'success': True,
        'estoques': dados,
        'totais': {
            'cascos': total_cascos,
            'peso_kg': total_peso,
            'valor_troca': total_valor_troca,
            'valor_compra': total_valor_compra,
        }
    })


# ============================================================
# API: Registrar movimentação de casco manual
# ============================================================
@login_required
def api_movimentar_casco(request):
    """
    Registra entrada ou saída manual de casco.
    
    POST:
    - amperagem_id: ID da amperagem
    - tipo: 'E' (entrada) ou 'S' (saída)
    - quantidade: quantidade a movimentar
    - motivo: motivo da movimentação
    - observacao: observação opcional
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    try:
        import json
        dados = json.loads(request.body)
        
        amperagem_id = dados.get('amperagem_id')
        tipo = dados.get('tipo')
        quantidade = int(dados.get('quantidade', 1))
        motivo = dados.get('motivo', 'AJUSTE')
        observacao = dados.get('observacao', '')
        
        if not amperagem_id or not tipo:
            return JsonResponse({'success': False, 'error': 'Dados incompletos'})
        
        amperagem = AmperagemBateria.objects.get(id=amperagem_id)
        
        # Verificar se tem estoque suficiente para saída
        if tipo == 'S':
            estoque = EstoqueCasco.objects.get_or_create(
                amperagem=amperagem,
                defaults={'quantidade': 0}
            )[0]
            
            if estoque.quantidade < quantidade:
                return JsonResponse({
                    'success': False, 
                    'error': f'Estoque insuficiente. Disponível: {estoque.quantidade}'
                })
        
        # Criar movimentação (o save() atualiza o estoque automaticamente)
        mov = MovimentacaoCasco.objects.create(
            amperagem=amperagem,
            tipo=tipo,
            motivo=motivo,
            quantidade=quantidade,
            observacao=observacao,
            usuario=request.user
        )
        
        # Buscar estoque atualizado
        estoque = EstoqueCasco.objects.get(amperagem=amperagem)
        
        return JsonResponse({
            'success': True,
            'message': f'Movimentação registrada! Estoque atual: {estoque.quantidade}',
            'estoque_atual': estoque.quantidade
        })
        
    except AmperagemBateria.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Amperagem não encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# CONTROLE DE CASCOS DE BATERIA
# ============================================

@login_required
def controle_cascos(request):
    """Pagina principal de controle de cascos de bateria"""
    
    # Buscar todas as amperagens com estoque
    amperagens = AmperagemBateria.objects.filter(ativo=True).order_by('ordem', 'amperagem')
    
    # Buscar estoque de cada amperagem
    estoques = EstoqueCasco.objects.select_related('amperagem').all()
    estoque_dict = {e.amperagem_id: e for e in estoques}
    
    # Montar dados consolidados
    dados_cascos = []
    total_quantidade = 0
    total_peso = 0
    total_valor = 0
    
    for amp in amperagens:
        estoque = estoque_dict.get(amp.id)
        quantidade = estoque.quantidade if estoque else 0
        peso_unitario = float(amp.peso_kg) if amp.peso_kg else 0
        valor_unitario = float(amp.valor_casco_troca) if amp.valor_casco_troca else 0
        
        peso_total = quantidade * peso_unitario
        valor_total = quantidade * valor_unitario
        
        dados_cascos.append({
            'amperagem': amp,
            'quantidade': quantidade,
            'peso_unitario': peso_unitario,
            'peso_total': peso_total,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
        })
        
        total_quantidade += quantidade
        total_peso += peso_total
        total_valor += valor_total
    
    # Buscar movimenta��es recentes
    movimentacoes = MovimentacaoCasco.objects.select_related(
        'amperagem', 'usuario'
    ).order_by('-data_movimentacao')[:50]
    
    context = {
        'dados_cascos': dados_cascos,
        'total_quantidade': total_quantidade,
        'total_peso': total_peso,
        'total_valor': total_valor,
        'movimentacoes': movimentacoes,
        'amperagens': amperagens,
    }
    
    return render(request, 'core/controle_cascos.html', context)


@login_required
def editar_amperagem(request, amperagem_id):
    """Editar valores de uma amperagem"""
    amperagem = get_object_or_404(AmperagemBateria, id=amperagem_id)
    
    if request.method == 'POST':
        amperagem.valor_casco_troca = request.POST.get('valor_casco_troca', 0)
        amperagem.valor_casco_compra = request.POST.get('valor_casco_compra', 0)
        amperagem.peso_kg = request.POST.get('peso_kg', 0)
        amperagem.save()
        
        messages.success(request, f'Amperagem {amperagem.amperagem} atualizada!')
        return redirect('controle_cascos')
    
    return JsonResponse({'error': 'M�todo n�o permitido'}, status=405)


@login_required  
def criar_amperagem(request):
    """Criar nova amperagem"""
    if request.method == 'POST':
        try:
            AmperagemBateria.objects.create(
                amperagem=request.POST.get('amperagem'),
                nome_tecnico=request.POST.get('nome_tecnico', ''),
                peso_kg=request.POST.get('peso_kg', 0),
                valor_casco_troca=request.POST.get('valor_casco_troca', 0),
                valor_casco_compra=request.POST.get('valor_casco_compra', 0),
                aplicacao=request.POST.get('aplicacao', ''),
                ativo=True
            )
            messages.success(request, 'Amperagem cadastrada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
        
        return redirect('controle_cascos')
    
    return JsonResponse({'error': 'M�todo n�o permitido'}, status=405)
