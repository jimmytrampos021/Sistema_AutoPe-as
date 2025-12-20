"""
Views do Módulo de Compras/Entrada de Mercadorias
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from decimal import Decimal
import json

from .models import NotaFiscalEntrada, ItemNotaEntrada, LogEntradaMercadoria
from .forms import (
    ImportarXMLForm, ImportarPDFForm, NotaFiscalEntradaManualForm, ItemNotaEntradaForm,
    ConferirItemForm, FiltroEntradasForm, CadastrarProdutoForm
)
from .services import EntradaMercadoriaService


@login_required
def lista_entradas(request):
    """Lista todas as entradas de mercadoria"""
    
    form_filtro = FiltroEntradasForm(request.GET)
    entradas = NotaFiscalEntrada.objects.all().select_related('fornecedor')
    
    # Aplica filtros
    if form_filtro.is_valid():
        data_inicio = form_filtro.cleaned_data.get('data_inicio')
        data_fim = form_filtro.cleaned_data.get('data_fim')
        status = form_filtro.cleaned_data.get('status')
        tipo_entrada = form_filtro.cleaned_data.get('tipo_entrada')
        fornecedor = form_filtro.cleaned_data.get('fornecedor')
        numero_nf = form_filtro.cleaned_data.get('numero_nf')
        
        if data_inicio:
            entradas = entradas.filter(data_entrada__gte=data_inicio)
        if data_fim:
            entradas = entradas.filter(data_entrada__lte=data_fim)
        if status:
            entradas = entradas.filter(status=status)
        if tipo_entrada:
            entradas = entradas.filter(tipo_entrada=tipo_entrada)
        if fornecedor:
            entradas = entradas.filter(
                Q(fornecedor__nome_fantasia__icontains=fornecedor) |
                Q(fornecedor__razao_social__icontains=fornecedor)
            )
        if numero_nf:
            entradas = entradas.filter(numero_nf__icontains=numero_nf)
    
    # Ordenação
    entradas = entradas.order_by('-data_entrada', '-created_at')
    
    # Paginação
    paginator = Paginator(entradas, 20)
    page = request.GET.get('page', 1)
    entradas_page = paginator.get_page(page)
    
    # Estatísticas
    stats = {
        'total': NotaFiscalEntrada.objects.count(),
        'pendentes': NotaFiscalEntrada.objects.filter(status__in=['P', 'E']).count(),
        'finalizadas_mes': NotaFiscalEntrada.objects.filter(
            status='F',
            data_finalizacao__month=timezone.now().month,
            data_finalizacao__year=timezone.now().year
        ).count(),
        'valor_mes': NotaFiscalEntrada.objects.filter(
            status='F',
            data_finalizacao__month=timezone.now().month,
            data_finalizacao__year=timezone.now().year
        ).aggregate(total=Sum('valor_total'))['total'] or 0,
    }
    
    context = {
        'entradas': entradas_page,
        'form_filtro': form_filtro,
        'stats': stats,
        'titulo': 'Entradas de Mercadoria',
    }
    
    return render(request, 'compras/entrada_lista.html', context)


@login_required
def importar_xml(request):
    """View para importar XML de NF-e"""
    
    if request.method == 'POST':
        form = ImportarXMLForm(request.POST, request.FILES)
        
        if form.is_valid():
            arquivo_xml = form.cleaned_data['arquivo_xml']
            
            config = {
                'atualizar_preco_custo': form.cleaned_data.get('atualizar_preco_custo', True),
                'atualizar_preco_venda': form.cleaned_data.get('atualizar_preco_venda', False),
                'margem_padrao': form.cleaned_data.get('margem_padrao', Decimal('50.00')),
                'ratear_frete': form.cleaned_data.get('ratear_frete', True),
                'atualizar_cotacao': form.cleaned_data.get('atualizar_cotacao', True),
            }
            
            service = EntradaMercadoriaService(usuario=request.user)
            success, nota, warnings = service.importar_xml(arquivo_xml, config)
            
            if success:
                messages.success(request, f'XML importado com sucesso! NF {nota.numero_nf}')
                
                for warning in warnings:
                    messages.warning(request, warning)
                
                return redirect('compras:detalhe_entrada', pk=nota.pk)
            else:
                for error in warnings:
                    messages.error(request, error)
    else:
        form = ImportarXMLForm()
    
    context = {
        'form': form,
        'titulo': 'Importar XML de NF-e',
    }
    
    return render(request, 'compras/entrada_xml.html', context)


@login_required
def entrada_manual(request):
    """View para criar entrada manual"""
    
    if request.method == 'POST':
        form = NotaFiscalEntradaManualForm(request.POST)
        
        if form.is_valid():
            nota = form.save(commit=False)
            nota.tipo_entrada = 'M'
            nota.status = 'P'
            nota.usuario_cadastro = request.user
            nota.save()
            
            # Log
            LogEntradaMercadoria.objects.create(
                nota=nota,
                acao='CRIAR',
                descricao=f'Nota fiscal criada manualmente',
                usuario=request.user
            )
            
            messages.success(request, f'Nota fiscal {nota.numero_nf} criada com sucesso!')
            return redirect('compras:detalhe_entrada', pk=nota.pk)
    else:
        form = NotaFiscalEntradaManualForm(initial={
            'data_emissao': timezone.now().date(),
            'data_entrada': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'titulo': 'Entrada Manual',
    }
    
    return render(request, 'compras/entrada_manual.html', context)


@login_required
def importar_pdf(request):
    """View para importar PDF de pedido de fornecedor"""
    
    if request.method == 'POST':
        form = ImportarPDFForm(request.POST, request.FILES)
        
        if form.is_valid():
            arquivo_pdf = form.cleaned_data['arquivo_pdf']
            
            config = {
                'atualizar_preco_custo': form.cleaned_data.get('atualizar_preco_custo', True),
                'atualizar_preco_venda': form.cleaned_data.get('atualizar_preco_venda', False),
                'margem_padrao': form.cleaned_data.get('margem_padrao', Decimal('50.00')),
                'ratear_frete': form.cleaned_data.get('ratear_frete', True),
                'atualizar_cotacao': form.cleaned_data.get('atualizar_cotacao', True),
            }
            
            service = EntradaMercadoriaService(usuario=request.user)
            success, nota, warnings = service.importar_pdf(arquivo_pdf, config)
            
            if success:
                messages.success(request, f'PDF importado com sucesso! Pedido {nota.numero_nf}')
                
                for warning in warnings:
                    messages.warning(request, warning)
                
                return redirect('compras:detalhe_entrada', pk=nota.pk)
            else:
                for error in warnings:
                    messages.error(request, error)
    else:
        form = ImportarPDFForm()
    
    context = {
        'form': form,
        'titulo': 'Importar PDF de Pedido',
    }
    
    return render(request, 'compras/entrada_pdf.html', context)


@login_required
def detalhe_entrada(request, pk):
    """View de detalhe da entrada com conferência"""
    
    nota = get_object_or_404(
        NotaFiscalEntrada.objects.select_related('fornecedor'),
        pk=pk
    )
    
    itens = nota.itens.all().select_related('produto').order_by('numero_item')
    logs = nota.logs.all().order_by('-created_at')[:20]
    
    # Formulário para adicionar item manual
    form_item = ItemNotaEntradaForm()
    
    context = {
        'nota': nota,
        'itens': itens,
        'logs': logs,
        'form_item': form_item,
        'titulo': f'NF {nota.numero_nf}/{nota.serie}',
    }
    
    return render(request, 'compras/entrada_detalhe.html', context)


@login_required
@require_POST
def adicionar_item(request, nota_id):
    """Adiciona item manualmente à nota"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    if nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível adicionar itens a esta nota'
        })
    
    form = ItemNotaEntradaForm(request.POST)
    
    if form.is_valid():
        item = form.save(commit=False)
        item.nota = nota
        item.numero_item = nota.itens.count() + 1
        item.valor_total = item.quantidade * item.valor_unitario - item.valor_desconto
        item.save()
        
        # Tenta vincular automaticamente
        item.vincular_produto_automatico()
        
        # Recalcula totais
        nota.calcular_totais()
        
        return JsonResponse({
            'success': True,
            'message': 'Item adicionado com sucesso',
            'item_id': item.id
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Erro ao adicionar item',
        'errors': form.errors
    })


@login_required
@require_POST
def remover_item(request, item_id):
    """Remove item da nota"""
    
    item = get_object_or_404(ItemNotaEntrada, pk=item_id)
    nota = item.nota
    
    if nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível remover itens desta nota'
        })
    
    item.delete()
    
    # Renumera itens
    for i, it in enumerate(nota.itens.all().order_by('numero_item'), 1):
        it.numero_item = i
        it.save()
    
    # Recalcula totais
    nota.calcular_totais()
    
    return JsonResponse({
        'success': True,
        'message': 'Item removido com sucesso'
    })


@login_required
@require_POST
def vincular_produto(request, item_id):
    """Vincula produto a um item da nota"""
    
    item = get_object_or_404(ItemNotaEntrada, pk=item_id)
    
    if item.nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    try:
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
    except:
        produto_id = request.POST.get('produto_id')
    
    if not produto_id:
        return JsonResponse({
            'success': False,
            'message': 'Produto não informado'
        })
    
    service = EntradaMercadoriaService(usuario=request.user)
    success, message = service.vincular_produto(item_id, produto_id)
    
    return JsonResponse({
        'success': success,
        'message': message
    })


@login_required
@require_POST
def desvincular_produto(request, item_id):
    """Remove vínculo do produto com o item"""
    
    item = get_object_or_404(ItemNotaEntrada, pk=item_id)
    
    if item.nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    item.produto = None
    item.save()
    
    LogEntradaMercadoria.objects.create(
        nota=item.nota,
        item=item,
        acao='DESVINCULAR',
        descricao=f'Produto desvinculado do item {item.numero_item}',
        usuario=request.user
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Produto desvinculado'
    })


@login_required
@require_POST
def cadastrar_produto(request, item_id):
    """Cadastra novo produto a partir do item"""
    
    item = get_object_or_404(ItemNotaEntrada, pk=item_id)
    
    if item.nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    if item.produto:
        return JsonResponse({
            'success': False,
            'message': 'Item já está vinculado a um produto'
        })
    
    try:
        data = json.loads(request.body)
    except:
        data = request.POST.dict()
    
    service = EntradaMercadoriaService(usuario=request.user)
    success, produto_id, message = service.cadastrar_produto_do_item(item_id, data)
    
    return JsonResponse({
        'success': success,
        'message': message,
        'produto_id': produto_id
    })


@login_required
@require_POST
def conferir_item(request, item_id):
    """Marca item como conferido"""
    
    item = get_object_or_404(ItemNotaEntrada, pk=item_id)
    
    if item.nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    try:
        data = json.loads(request.body)
        quantidade = Decimal(str(data.get('quantidade', item.quantidade)))
        observacao = data.get('observacao', '')
    except:
        quantidade = Decimal(request.POST.get('quantidade', item.quantidade))
        observacao = request.POST.get('observacao', '')
    
    service = EntradaMercadoriaService(usuario=request.user)
    success, message = service.conferir_item(item_id, quantidade, observacao)
    
    # Retorna dados atualizados do item
    item.refresh_from_db()
    
    return JsonResponse({
        'success': success,
        'message': message,
        'item': {
            'id': item.id,
            'conferido': item.conferido,
            'quantidade_conferida': str(item.quantidade_conferida),
            'divergencia': item.divergencia,
            'valor_custo_unitario': str(item.valor_custo_unitario),
        },
        'nota': {
            'status': item.nota.status,
            'percentual_conferencia': item.nota.percentual_conferencia,
        }
    })


@login_required
@require_POST
def finalizar_entrada(request, nota_id):
    """Finaliza a entrada de mercadoria"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    service = EntradaMercadoriaService(usuario=request.user)
    success, message, resumo = service.finalizar_entrada(nota_id)
    
    if success:
        messages.success(request, message)
        
        # Detalhes do resumo
        if resumo.get('estoque_atualizado'):
            messages.info(request, f"Estoque atualizado: {resumo['estoque_atualizado']} produtos")
        if resumo.get('precos_atualizados'):
            messages.info(request, f"Preços recalculados: {resumo['precos_atualizados']} produtos")
        if resumo.get('cotacoes_criadas'):
            messages.info(request, f"Cotações criadas: {resumo['cotacoes_criadas']}")
        
        for erro in resumo.get('erros', []):
            messages.warning(request, erro)
    else:
        messages.error(request, message)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': success,
            'message': message,
            'resumo': resumo
        })
    
    return redirect('compras:detalhe_entrada', pk=nota_id)


@login_required
@require_POST
def cancelar_entrada(request, nota_id):
    """Cancela a entrada de mercadoria"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    # Tenta ler dados JSON
    is_ajax = request.content_type == 'application/json'
    
    try:
        if is_ajax:
            data = json.loads(request.body)
            motivo = data.get('motivo', '')
        else:
            motivo = request.POST.get('motivo', '')
    except:
        motivo = request.POST.get('motivo', '')
    
    service = EntradaMercadoriaService(usuario=request.user)
    success, message = service.cancelar_entrada(nota_id, motivo)
    
    if is_ajax:
        return JsonResponse({
            'success': success,
            'message': message
        })
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('compras:detalhe_entrada', pk=nota_id)


@login_required
@require_GET
def buscar_produtos(request):
    """API para buscar produtos (autocomplete)"""
    
    termo = request.GET.get('q', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'produtos': []})
    
    service = EntradaMercadoriaService()
    produtos = service.buscar_produtos_para_vincular(termo, limit=15)
    
    return JsonResponse({'produtos': produtos})


@login_required
@require_GET
def get_categorias_fabricantes(request):
    """API para obter categorias, subcategorias, grupos, subgrupos e fabricantes"""
    from estoque.models import Categoria, Fabricante, Subcategoria, Grupo, Subgrupo
    
    categorias = [
        {'id': c.id, 'nome': c.nome}
        for c in Categoria.objects.filter(ativo=True).order_by('nome')
    ]
    
    subcategorias = [
        {'id': s.id, 'nome': s.nome, 'categoria_id': s.categoria_id}
        for s in Subcategoria.objects.filter(ativo=True).order_by('nome')
    ]
    
    grupos = [
        {'id': g.id, 'nome': g.nome, 'subcategoria_id': g.subcategoria_id}
        for g in Grupo.objects.filter(ativo=True).order_by('nome')
    ]
    
    subgrupos = [
        {'id': sg.id, 'nome': sg.nome, 'grupo_id': sg.grupo_id}
        for sg in Subgrupo.objects.filter(ativo=True).order_by('nome')
    ]
    
    fabricantes = [
        {'id': f.id, 'nome': f.nome}
        for f in Fabricante.objects.filter(ativo=True).order_by('nome')
    ]
    
    return JsonResponse({
        'categorias': categorias,
        'subcategorias': subcategorias,
        'grupos': grupos,
        'subgrupos': subgrupos,
        'fabricantes': fabricantes
    })


@login_required
@require_POST
def criar_fabricante(request):
    """API para criar fabricante rapidamente"""
    from estoque.models import Fabricante
    
    try:
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        
        if not nome:
            return JsonResponse({'success': False, 'message': 'Nome do fabricante é obrigatório'})
        
        # Verifica se já existe
        if Fabricante.objects.filter(nome__iexact=nome).exists():
            fab = Fabricante.objects.get(nome__iexact=nome)
            return JsonResponse({'success': True, 'id': fab.id, 'nome': fab.nome, 'message': 'Fabricante já existe'})
        
        fab = Fabricante.objects.create(nome=nome, ativo=True)
        return JsonResponse({'success': True, 'id': fab.id, 'nome': fab.nome, 'message': 'Fabricante criado com sucesso'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao criar fabricante: {str(e)}'})


@login_required
def conferencia_rapida(request, nota_id):
    """View para conferência rápida (modo simplificado)"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    if nota.status in ['F', 'X']:
        messages.warning(request, 'Esta nota não pode mais ser conferida')
        return redirect('compras:detalhe_entrada', pk=nota_id)
    
    itens = nota.itens.all().select_related('produto').order_by('numero_item')
    
    context = {
        'nota': nota,
        'itens': itens,
        'titulo': f'Conferência Rápida - NF {nota.numero_nf}',
    }
    
    return render(request, 'compras/conferencia_rapida.html', context)


@login_required
@require_POST
def conferir_todos(request, nota_id):
    """Confere todos os itens com quantidade da NF"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    if nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    service = EntradaMercadoriaService(usuario=request.user)
    conferidos = 0
    erros = []
    
    for item in nota.itens.filter(conferido=False):
        success, message = service.conferir_item(
            item.id,
            item.quantidade,
            'Conferência em lote'
        )
        if success:
            conferidos += 1
        else:
            erros.append(f"Item {item.numero_item}: {message}")
    
    return JsonResponse({
        'success': len(erros) == 0,
        'message': f'{conferidos} itens conferidos' + (f', {len(erros)} erros' if erros else ''),
        'conferidos': conferidos,
        'erros': erros
    })


@login_required
@require_POST  
def vincular_automatico(request, nota_id):
    """Tenta vincular automaticamente todos os itens pendentes"""
    
    nota = get_object_or_404(NotaFiscalEntrada, pk=nota_id)
    
    if nota.status in ['F', 'X']:
        return JsonResponse({
            'success': False,
            'message': 'Nota já finalizada ou cancelada'
        })
    
    vinculados = 0
    
    for item in nota.itens.filter(produto__isnull=True):
        produto = item.vincular_produto_automatico()
        if produto:
            vinculados += 1
            
            LogEntradaMercadoria.objects.create(
                nota=nota,
                item=item,
                acao='VINCULAR',
                descricao=f'Vinculação automática: {produto.descricao[:50]}',
                usuario=request.user
            )
    
    pendentes = nota.itens.filter(produto__isnull=True).count()
    
    return JsonResponse({
        'success': True,
        'message': f'{vinculados} produtos vinculados automaticamente',
        'vinculados': vinculados,
        'pendentes': pendentes
    })
