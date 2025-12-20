from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, date, timedelta
from decimal import Decimal
import json
import requests

from .models import (
    ConfiguracaoFiscal, NotaFiscal, ItemNotaFiscal, PagamentoNotaFiscal,
    DuplicataNotaFiscal, EventoNotaFiscal, Boleto, NCM, CFOP, InutilizacaoNumeracao
)


# ==========================================
# DASHBOARD FISCAL
# ==========================================
@login_required
def dashboard_fiscal(request):
    """Dashboard do módulo fiscal"""
    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    config = ConfiguracaoFiscal.get_config()
    
    # Estatísticas do mês
    notas_mes = NotaFiscal.objects.filter(
        data_emissao__month=mes_atual,
        data_emissao__year=ano_atual
    )
    
    stats = {
        'total_notas': notas_mes.count(),
        'notas_autorizadas': notas_mes.filter(status='AUTORIZADA').count(),
        'notas_canceladas': notas_mes.filter(status='CANCELADA').count(),
        'notas_rejeitadas': notas_mes.filter(status='REJEITADA').count(),
        'valor_total': notas_mes.filter(status='AUTORIZADA').aggregate(
            total=Sum('valor_total')
        )['total'] or Decimal('0'),
        'nfce_emitidas': notas_mes.filter(modelo='65', status='AUTORIZADA').count(),
        'nfe_emitidas': notas_mes.filter(modelo='55', status='AUTORIZADA').count(),
    }
    
    ultimas_notas = NotaFiscal.objects.all().order_by('-data_emissao')[:10]
    
    # Alertas
    alertas = []
    
    if config:
        if config.certificado_validade:
            dias_vencer = (config.certificado_validade - hoje).days
            if dias_vencer <= 30:
                alertas.append({
                    'tipo': 'warning' if dias_vencer > 0 else 'danger',
                    'mensagem': f"Certificado digital {'vence em ' + str(dias_vencer) + ' dias' if dias_vencer > 0 else 'VENCIDO'}!"
                })
        
        if config.ambiente == '2':
            alertas.append({
                'tipo': 'info',
                'mensagem': "Sistema em modo HOMOLOGAÇÃO (teste). Notas não têm validade fiscal."
            })
    else:
        alertas.append({
            'tipo': 'danger',
            'mensagem': "Configuração fiscal não encontrada. Configure os dados da empresa."
        })
    
    context = {
        'config': config,
        'stats': stats,
        'ultimas_notas': ultimas_notas,
        'alertas': alertas,
    }
    
    return render(request, 'fiscal/dashboard.html', context)


# ==========================================
# CONFIGURAÇÃO FISCAL
# ==========================================
@login_required
def configuracao_fiscal(request):
    """Tela de configuração fiscal"""
    config = ConfiguracaoFiscal.get_config()
    
    if request.method == 'POST':
        if not config:
            config = ConfiguracaoFiscal()
        
        # Dados da empresa
        config.razao_social = request.POST.get('razao_social', '')
        config.nome_fantasia = request.POST.get('nome_fantasia', '')
        config.cnpj = request.POST.get('cnpj', '')
        config.inscricao_estadual = request.POST.get('inscricao_estadual', '')
        config.inscricao_municipal = request.POST.get('inscricao_municipal', '')
        
        # Endereço
        config.cep = request.POST.get('cep', '')
        config.logradouro = request.POST.get('logradouro', '')
        config.numero = request.POST.get('numero', '')
        config.complemento = request.POST.get('complemento', '')
        config.bairro = request.POST.get('bairro', '')
        config.cidade = request.POST.get('cidade', '')
        config.uf = request.POST.get('uf', '')
        config.codigo_municipio = request.POST.get('codigo_municipio', '')
        
        # Contato
        config.telefone = request.POST.get('telefone', '')
        config.email = request.POST.get('email', '')
        
        # Fiscal
        config.regime_tributario = request.POST.get('regime_tributario', '1')
        config.ambiente = request.POST.get('ambiente', '2')
        
        # Certificado
        if 'certificado_arquivo' in request.FILES:
            config.certificado_arquivo = request.FILES['certificado_arquivo']
        config.certificado_senha = request.POST.get('certificado_senha', '')
        
        validade = request.POST.get('certificado_validade', '')
        if validade:
            config.certificado_validade = datetime.strptime(validade, '%Y-%m-%d').date()
        
        # API WebmaniaBR
        config.webmania_consumer_key = request.POST.get('webmania_consumer_key', '')
        config.webmania_consumer_secret = request.POST.get('webmania_consumer_secret', '')
        config.webmania_access_token = request.POST.get('webmania_access_token', '')
        config.webmania_access_token_secret = request.POST.get('webmania_access_token_secret', '')
        
        # NFC-e
        config.csc_id = request.POST.get('csc_id', '')
        config.csc_token = request.POST.get('csc_token', '')
        
        # Séries
        config.serie_nfe = int(request.POST.get('serie_nfe', 1) or 1)
        config.serie_nfce = int(request.POST.get('serie_nfce', 1) or 1)
        
        config.save()
        
        messages.success(request, 'Configuração fiscal salva com sucesso!')
        return redirect('fiscal:configuracao')
    
    context = {
        'config': config,
        'ufs': ConfiguracaoFiscal.UF_CHOICES,
    }
    
    return render(request, 'fiscal/configuracao.html', context)


# ==========================================
# LISTA DE NOTAS FISCAIS
# ==========================================
@login_required
def lista_notas(request):
    """Lista de notas fiscais emitidas"""
    notas = NotaFiscal.objects.all().order_by('-data_emissao')
    
    # Filtros
    modelo = request.GET.get('modelo', '')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    busca = request.GET.get('busca', '')
    
    if modelo:
        notas = notas.filter(modelo=modelo)
    
    if status:
        notas = notas.filter(status=status)
    
    if data_inicio:
        try:
            dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            notas = notas.filter(data_emissao__gte=dt)
        except:
            pass
    
    if data_fim:
        try:
            dt = datetime.strptime(data_fim, '%Y-%m-%d')
            notas = notas.filter(data_emissao__lte=dt)
        except:
            pass
    
    if busca:
        notas = notas.filter(
            Q(numero__icontains=busca) |
            Q(chave_acesso__icontains=busca) |
            Q(dest_nome__icontains=busca) |
            Q(dest_cpf_cnpj__icontains=busca)
        )
    
    paginator = Paginator(notas, 20)
    page = request.GET.get('page', 1)
    notas = paginator.get_page(page)
    
    context = {
        'notas': notas,
        'modelo': modelo,
        'status': status,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'busca': busca,
    }
    
    return render(request, 'fiscal/lista_notas.html', context)


# ==========================================
# DETALHES DA NOTA FISCAL
# ==========================================
@login_required
def detalhe_nota(request, pk):
    """Detalhes de uma nota fiscal"""
    nota = get_object_or_404(NotaFiscal, pk=pk)
    
    context = {
        'nota': nota,
        'itens': nota.itens.all(),
        'pagamentos': nota.pagamentos.all(),
        'duplicatas': nota.duplicatas.all(),
        'eventos': nota.eventos.all().order_by('-data_evento'),
    }
    
    return render(request, 'fiscal/detalhe_nota.html', context)


# ==========================================
# EMITIR NFC-e
# ==========================================
@login_required
def emitir_nfce(request, venda_id=None):
    """Tela para emitir NFC-e"""
    from vendas.models import Venda
    from .services import NotaFiscalService
    
    venda = None
    if venda_id:
        venda = get_object_or_404(Venda, pk=venda_id)
    
    if request.method == 'POST':
        venda_id = request.POST.get('venda_id')
        cpf_cliente = request.POST.get('cpf_cliente', '').strip()
        
        if not venda_id:
            messages.error(request, 'Selecione uma venda')
            return redirect('fiscal:emitir_nfce')
        
        venda = get_object_or_404(Venda, pk=venda_id)
        
        if NotaFiscal.objects.filter(venda=venda, status='AUTORIZADA').exists():
            messages.warning(request, 'Esta venda já possui uma nota fiscal autorizada')
            return redirect('fiscal:lista_notas')
        
        try:
            service = NotaFiscalService()
            resultado = service.criar_nfce_da_venda(venda, cpf_cliente or None)
            
            if resultado.get('sucesso'):
                messages.success(
                    request,
                    f"NFC-e emitida com sucesso! Número: {resultado.get('numero')} - "
                    f"Chave: {resultado.get('chave')}"
                )
                return redirect('fiscal:detalhe_nota', pk=resultado['nota_fiscal'].pk)
            else:
                messages.error(request, f"Erro ao emitir NFC-e: {resultado.get('erro', resultado.get('motivo', 'Erro desconhecido'))}")
        
        except Exception as e:
            messages.error(request, f"Erro ao emitir NFC-e: {str(e)}")
        
        return redirect('fiscal:emitir_nfce')
    
    vendas_disponiveis = Venda.objects.filter(
        status='F'
    ).exclude(
        notas_fiscais__status='AUTORIZADA'
    ).order_by('-data_venda')[:50]
    
    context = {
        'venda': venda,
        'vendas_disponiveis': vendas_disponiveis,
    }
    
    return render(request, 'fiscal/emitir_nfce.html', context)


# ==========================================
# EMITIR NF-e
# ==========================================
@login_required
def emitir_nfe(request, venda_id=None):
    """Tela para emitir NF-e"""
    from vendas.models import Venda
    from .services import NotaFiscalService
    
    venda = None
    if venda_id:
        venda = get_object_or_404(Venda, pk=venda_id)
    
    if request.method == 'POST':
        venda_id = request.POST.get('venda_id')
        
        if not venda_id:
            messages.error(request, 'Selecione uma venda')
            return redirect('fiscal:emitir_nfe')
        
        venda = get_object_or_404(Venda, pk=venda_id)
        
        if not venda.cliente or not venda.cliente.cpf_cnpj:
            messages.error(request, 'A venda precisa ter um cliente com CPF/CNPJ cadastrado')
            return redirect('fiscal:emitir_nfe')
        
        if NotaFiscal.objects.filter(venda=venda, status='AUTORIZADA', modelo='55').exists():
            messages.warning(request, 'Esta venda já possui uma NF-e autorizada')
            return redirect('fiscal:lista_notas')
        
        # Verificar pagamento a prazo
        forma_pagamento = request.POST.get('forma_pagamento', 'avista')
        duplicatas = None
        
        if forma_pagamento == 'prazo':
            num_parcelas = int(request.POST.get('num_parcelas', 1))
            dias_entre = int(request.POST.get('dias_entre', 30))
            
            valor_parcela = venda.total / num_parcelas
            duplicatas = []
            
            for i in range(num_parcelas):
                data_venc = date.today() + timedelta(days=dias_entre * (i + 1))
                duplicatas.append({
                    'data_vencimento': data_venc,
                    'valor': valor_parcela,
                })
        
        try:
            service = NotaFiscalService()
            resultado = service.criar_nfe_da_venda(venda, duplicatas)
            
            if resultado.get('sucesso'):
                messages.success(
                    request,
                    f"NF-e emitida com sucesso! Número: {resultado.get('numero')} - "
                    f"Chave: {resultado.get('chave')}"
                )
                return redirect('fiscal:detalhe_nota', pk=resultado['nota_fiscal'].pk)
            else:
                messages.error(request, f"Erro ao emitir NF-e: {resultado.get('erro', resultado.get('motivo', 'Erro desconhecido'))}")
        
        except Exception as e:
            messages.error(request, f"Erro ao emitir NF-e: {str(e)}")
        
        return redirect('fiscal:emitir_nfe')
    
    vendas_disponiveis = Venda.objects.filter(
        status='F',
        cliente__isnull=False,
    ).exclude(
        notas_fiscais__status='AUTORIZADA',
        notas_fiscais__modelo='55'
    ).order_by('-data_venda')[:50]
    
    context = {
        'venda': venda,
        'vendas_disponiveis': vendas_disponiveis,
    }
    
    return render(request, 'fiscal/emitir_nfe.html', context)


# ==========================================
# CANCELAR NOTA
# ==========================================
@login_required
@require_POST
def cancelar_nota(request, pk):
    """Cancela uma nota fiscal"""
    from .services import WebmaniaBRService
    
    nota = get_object_or_404(NotaFiscal, pk=pk)
    justificativa = request.POST.get('justificativa', '')
    
    if not nota.pode_cancelar:
        messages.error(request, 'Esta nota não pode mais ser cancelada (prazo expirado)')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    if len(justificativa) < 15:
        messages.error(request, 'A justificativa deve ter no mínimo 15 caracteres')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    try:
        service = WebmaniaBRService()
        resultado = service.cancelar_nota(nota, justificativa)
        
        if resultado.get('sucesso'):
            messages.success(request, f"Nota cancelada com sucesso! Protocolo: {resultado.get('protocolo')}")
        else:
            messages.error(request, f"Erro ao cancelar nota: {resultado.get('erro')}")
    
    except Exception as e:
        messages.error(request, f"Erro ao cancelar nota: {str(e)}")
    
    return redirect('fiscal:detalhe_nota', pk=pk)


# ==========================================
# CARTA DE CORREÇÃO
# ==========================================
@login_required
@require_POST
def carta_correcao(request, pk):
    """Emite carta de correção"""
    from .services import WebmaniaBRService
    
    nota = get_object_or_404(NotaFiscal, pk=pk)
    correcao = request.POST.get('correcao', '')
    
    if nota.status != 'AUTORIZADA':
        messages.error(request, 'Só é possível emitir carta de correção para notas autorizadas')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    if len(correcao) < 15:
        messages.error(request, 'A correção deve ter no mínimo 15 caracteres')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    try:
        service = WebmaniaBRService()
        resultado = service.carta_correcao(nota, correcao)
        
        if resultado.get('sucesso'):
            messages.success(request, f"Carta de correção emitida! Protocolo: {resultado.get('protocolo')}")
        else:
            messages.error(request, f"Erro ao emitir carta de correção: {resultado.get('erro')}")
    
    except Exception as e:
        messages.error(request, f"Erro ao emitir carta de correção: {str(e)}")
    
    return redirect('fiscal:detalhe_nota', pk=pk)


# ==========================================
# ENVIAR EMAIL
# ==========================================
@login_required
@require_POST
def enviar_email(request, pk):
    """Envia nota por email"""
    from .services import NotaFiscalService
    
    nota = get_object_or_404(NotaFiscal, pk=pk)
    email = request.POST.get('email', '')
    
    if not email and not nota.dest_email:
        messages.error(request, 'Informe um email para envio')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    try:
        service = NotaFiscalService()
        if service.enviar_nota_por_email(nota, email or None):
            messages.success(request, f"Nota enviada com sucesso para {email or nota.dest_email}")
        else:
            messages.error(request, "Erro ao enviar email")
    
    except Exception as e:
        messages.error(request, f"Erro ao enviar email: {str(e)}")
    
    return redirect('fiscal:detalhe_nota', pk=pk)


# ==========================================
# DOWNLOAD DANFE
# ==========================================
@login_required
def download_danfe(request, pk):
    """Download do DANFE (PDF)"""
    from .services import WebmaniaBRService
    
    nota = get_object_or_404(NotaFiscal, pk=pk)
    
    if nota.pdf_danfe:
        return FileResponse(nota.pdf_danfe.open(), as_attachment=True, filename=f'DANFE_{nota.numero}.pdf')
    
    if nota.chave_acesso:
        try:
            service = WebmaniaBRService()
            url_danfe = service.gerar_danfe(nota.chave_acesso)
            
            if url_danfe:
                return redirect(url_danfe)
        except:
            pass
    
    messages.error(request, 'DANFE não disponível')
    return redirect('fiscal:detalhe_nota', pk=pk)


# ==========================================
# DOWNLOAD XML
# ==========================================
@login_required
def download_xml(request, pk):
    """Download do XML da nota"""
    nota = get_object_or_404(NotaFiscal, pk=pk)
    
    xml_content = nota.xml_autorizado or nota.xml_envio
    
    if not xml_content:
        messages.error(request, 'XML não disponível')
        return redirect('fiscal:detalhe_nota', pk=pk)
    
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="NFe_{nota.chave_acesso or nota.numero}.xml"'
    return response


# ==========================================
# INUTILIZAR NUMERAÇÃO
# ==========================================
@login_required
def inutilizar_numeracao(request):
    """Inutilização de numeração"""
    from .services import WebmaniaBRService
    
    if request.method == 'POST':
        modelo = request.POST.get('modelo', '65')
        serie = int(request.POST.get('serie', 1))
        numero_inicial = int(request.POST.get('numero_inicial', 1))
        numero_final = int(request.POST.get('numero_final', 1))
        justificativa = request.POST.get('justificativa', '')
        
        if len(justificativa) < 15:
            messages.error(request, 'A justificativa deve ter no mínimo 15 caracteres')
            return redirect('fiscal:inutilizar')
        
        try:
            service = WebmaniaBRService()
            resultado = service.inutilizar_numeracao(
                modelo, serie, numero_inicial, numero_final, justificativa
            )
            
            if resultado.get('sucesso'):
                messages.success(request, f"Numeração inutilizada! Protocolo: {resultado.get('protocolo')}")
            else:
                messages.error(request, f"Erro ao inutilizar: {resultado.get('erro')}")
        
        except Exception as e:
            messages.error(request, f"Erro ao inutilizar: {str(e)}")
        
        return redirect('fiscal:inutilizar')
    
    inutilizacoes = InutilizacaoNumeracao.objects.all().order_by('-data_cadastro')[:20]
    
    context = {
        'inutilizacoes': inutilizacoes,
    }
    
    return render(request, 'fiscal/inutilizar.html', context)


# ==========================================
# API - EMITIR NFC-e (para PDV)
# ==========================================
@login_required
@require_POST
def api_emitir_nfce(request):
    """API para emitir NFC-e diretamente do PDV"""
    from vendas.models import Venda
    from .services import NotaFiscalService
    
    try:
        data = json.loads(request.body)
        venda_id = data.get('venda_id')
        cpf_cliente = data.get('cpf_cliente', '')
        
        if not venda_id:
            return JsonResponse({'sucesso': False, 'erro': 'Venda não informada'})
        
        venda = get_object_or_404(Venda, pk=venda_id)
        
        if NotaFiscal.objects.filter(venda=venda, status='AUTORIZADA').exists():
            nota = NotaFiscal.objects.filter(venda=venda, status='AUTORIZADA').first()
            return JsonResponse({
                'sucesso': True,
                'ja_emitida': True,
                'nota_id': nota.pk,
                'numero': nota.numero,
                'chave': nota.chave_acesso,
            })
        
        service = NotaFiscalService()
        resultado = service.criar_nfce_da_venda(venda, cpf_cliente or None)
        
        if resultado.get('sucesso'):
            return JsonResponse({
                'sucesso': True,
                'nota_id': resultado['nota_fiscal'].pk,
                'numero': resultado.get('numero'),
                'chave': resultado.get('chave'),
                'danfe_url': resultado.get('danfe_url'),
            })
        else:
            return JsonResponse({
                'sucesso': False,
                'erro': resultado.get('erro') or resultado.get('motivo', 'Erro desconhecido')
            })
    
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)})


# ==========================================
# API - CONSULTAR NOTA
# ==========================================
@login_required
def api_consultar_nota(request, chave):
    """API para consultar status de uma nota"""
    from .services import WebmaniaBRService
    
    try:
        service = WebmaniaBRService()
        resultado = service.consultar_nota(chave)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'error': str(e)})
