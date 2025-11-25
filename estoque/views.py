from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Avg, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from estoque.models import Fornecedor, Produto, CotacaoFornecedor


@login_required
def lista_fornecedores(request):
    """Lista todos os fornecedores com estatísticas"""
    fornecedores = Fornecedor.objects.filter(ativo=True).annotate(
        total_produtos=Count('produto'),
        total_cotacoes=Count('cotacoes', filter=Q(cotacoes__ativo=True))
    ).order_by('nome_fantasia')
    
    context = {
        'fornecedores': fornecedores,
        'total_fornecedores': fornecedores.count(),
    }
    return render(request, 'estoque/fornecedores_lista.html', context)


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
        cotacoes_produto = CotacaoFornecedor.objects.filter(
            produto=produto_selecionado,
            ativo=True
        ).select_related('fornecedor').order_by('preco_unitario')
        
        if cotacoes_produto.exists():
            melhor_preco = cotacoes_produto.first()
            
            # Calcula economia em relação ao preço atual
            if produto_selecionado.preco_custo > melhor_preco.preco_unitario:
                economia_maxima = produto_selecionado.preco_custo - melhor_preco.preco_unitario
    
    # Top 10 produtos com mais cotações
    produtos_top = Produto.objects.filter(ativo=True).annotate(
        num_cotacoes=Count('cotacoes', filter=Q(cotacoes__ativo=True))
    ).filter(num_cotacoes__gt=0).order_by('-num_cotacoes')[:10]
    
    # Produtos que precisam de cotação (estoque baixo e sem cotações recentes)
    produtos_precisam_cotacao = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=models.F('estoque_minimo')
    ).annotate(
        num_cotacoes_recentes=Count(
            'cotacoes',
            filter=Q(
                cotacoes__ativo=True,
                cotacoes__data_cotacao__gte=timezone.now().date() - timedelta(days=30)
            )
        )
    ).filter(num_cotacoes_recentes=0)[:10]
    
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
    from django.db.models import Avg, Count, Min
    
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
    produtos_maior_diferenca = []
    
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
    
    context = {
        'top_fornecedores': top_fornecedores,
        'produtos_maior_diferenca': produtos_maior_diferenca,
        'total_fornecedores': fornecedores_stats.count(),
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
def api_buscar_produto(request):
    """API para buscar produtos (para autocomplete)"""
    termo = request.GET.get('q', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'produtos': []})
    
    produtos = Produto.objects.filter(
        Q(codigo__icontains=termo) |
        Q(descricao__icontains=termo) |
        Q(codigo_barras__icontains=termo),
        ativo=True
    )[:10]
    
    data = {
        'produtos': [
            {
                'id': p.id,
                'codigo': p.codigo,
                'descricao': p.descricao,
                'preco_custo': float(p.preco_custo),
                'preco_venda': float(p.preco_venda),
                'estoque': p.estoque_atual,
            }
            for p in produtos
        ]
    }
    
    return JsonResponse(data)


@login_required
def api_cotacoes_produto(request, produto_id):
    """API que retorna todas as cotações de um produto"""
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