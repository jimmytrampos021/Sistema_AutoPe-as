"""
Serviço de integração com WebmaniaBR para emissão de NF-e e NFC-e
Documentação: https://webmaniabr.com/docs/rest-api-nfe/
"""

import requests
import json
from decimal import Decimal
from datetime import datetime
from django.conf import settings


class WebmaniaBRService:
    """Serviço para emissão de NF-e/NFC-e via WebmaniaBR"""
    
    BASE_URL = "https://webmaniabr.com/api/1/nfe"
    
    def __init__(self, config=None):
        """
        Inicializa o serviço com as credenciais
        
        Args:
            config: Instância de ConfiguracaoFiscal ou None para buscar automaticamente
        """
        if config is None:
            from fiscal.models import ConfiguracaoFiscal
            config = ConfiguracaoFiscal.get_config()
        
        if not config:
            raise ValueError("Configuração fiscal não encontrada")
        
        self.config = config
        self.headers = {
            "Content-Type": "application/json",
            "X-Consumer-Key": config.webmania_consumer_key or "",
            "X-Consumer-Secret": config.webmania_consumer_secret or "",
            "X-Access-Token": config.webmania_access_token or "",
            "X-Access-Token-Secret": config.webmania_access_token_secret or "",
        }
    
    def _decimal_to_float(self, value):
        """Converte Decimal para float para JSON"""
        if isinstance(value, Decimal):
            return float(value)
        return value
    
    def _request(self, endpoint, method="POST", data=None):
        """
        Faz uma requisição para a API
        
        Args:
            endpoint: Endpoint da API (ex: /emissao)
            method: Método HTTP
            data: Dados a enviar
        
        Returns:
            dict: Resposta da API
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=60)
            elif method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=60)
            else:
                raise ValueError(f"Método {method} não suportado")
            
            return response.json()
        
        except requests.exceptions.Timeout:
            return {"error": "Timeout na comunicação com a SEFAZ"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro de conexão: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Resposta inválida da API"}
    
    def emitir_nfce(self, nota_fiscal):
        """
        Emite uma NFC-e (Nota Fiscal de Consumidor Eletrônica)
        
        Args:
            nota_fiscal: Instância de NotaFiscal com modelo='65'
        
        Returns:
            dict: Resposta da API com status, chave, protocolo, etc.
        """
        from fiscal.models import ItemNotaFiscal, PagamentoNotaFiscal
        
        # Montar dados da nota
        dados = {
            "ID": str(nota_fiscal.uuid),
            "url_notificacao": "",  # Webhook para retorno
            "operacao": 1,  # 1 = Saída
            "natureza_operacao": nota_fiscal.natureza_operacao,
            "modelo": 2,  # 2 = NFC-e (modelo 65)
            "finalidade": 1,  # 1 = Normal
            "ambiente": int(self.config.ambiente),  # 1 = Produção, 2 = Homologação
        }
        
        # Destinatário (opcional para NFC-e)
        if nota_fiscal.dest_cpf_cnpj:
            cpf_cnpj = nota_fiscal.dest_cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
            if len(cpf_cnpj) == 11:
                dados["cliente"] = {
                    "cpf": cpf_cnpj,
                    "nome_completo": nota_fiscal.dest_nome or "CONSUMIDOR",
                }
            else:
                dados["cliente"] = {
                    "cnpj": cpf_cnpj,
                    "razao_social": nota_fiscal.dest_nome or "CONSUMIDOR",
                    "ie": nota_fiscal.dest_ie or "",
                }
        
        # Produtos
        produtos = []
        for item in nota_fiscal.itens.all():
            produto = {
                "nome": item.descricao[:120],
                "codigo": item.codigo[:60],
                "ncm": item.ncm,
                "cfop": item.cfop,
                "unidade": item.unidade,
                "quantidade": self._decimal_to_float(item.quantidade),
                "subtotal": self._decimal_to_float(item.valor_unitario),
                "total": self._decimal_to_float(item.valor_total),
                "impostos": {
                    "icms": {
                        "origem": item.origem,
                        "csosn": item.csosn,
                    }
                }
            }
            
            if item.valor_desconto > 0:
                produto["desconto"] = self._decimal_to_float(item.valor_desconto)
            
            produtos.append(produto)
        
        dados["produtos"] = produtos
        
        # Pagamentos
        pagamentos = []
        for pag in nota_fiscal.pagamentos.all():
            pagamento = {
                "forma_pagamento": pag.forma_pagamento,
                "valor": self._decimal_to_float(pag.valor),
            }
            
            # Cartão de crédito/débito
            if pag.forma_pagamento in ["03", "04"]:
                pagamento["cartao"] = {
                    "bandeira": pag.bandeira or "99",
                }
                if pag.autorizacao:
                    pagamento["cartao"]["autorizacao"] = pag.autorizacao
                if pag.cnpj_credenciadora:
                    pagamento["cartao"]["cnpj_credenciadora"] = pag.cnpj_credenciadora
            
            pagamentos.append(pagamento)
        
        # Se não houver pagamentos, adicionar "Sem Pagamento"
        if not pagamentos:
            pagamentos = [{"forma_pagamento": "90", "valor": 0}]
        
        dados["pedido"] = {
            "pagamento": pagamentos,
            "presenca": int(nota_fiscal.presenca),
        }
        
        # Informações complementares
        if nota_fiscal.informacoes_complementares:
            dados["pedido"]["informacoes_complementares"] = nota_fiscal.informacoes_complementares
        
        # Enviar para API
        response = self._request("/emissao", "POST", dados)
        
        return self._processar_resposta(nota_fiscal, response)
    
    def emitir_nfe(self, nota_fiscal):
        """
        Emite uma NF-e (Nota Fiscal Eletrônica)
        
        Args:
            nota_fiscal: Instância de NotaFiscal com modelo='55'
        
        Returns:
            dict: Resposta da API com status, chave, protocolo, etc.
        """
        from fiscal.models import ItemNotaFiscal, PagamentoNotaFiscal, DuplicataNotaFiscal
        
        # Montar dados da nota
        dados = {
            "ID": str(nota_fiscal.uuid),
            "url_notificacao": "",
            "operacao": 1,  # 1 = Saída
            "natureza_operacao": nota_fiscal.natureza_operacao,
            "modelo": 1,  # 1 = NF-e (modelo 55)
            "finalidade": int(nota_fiscal.finalidade),
            "ambiente": int(self.config.ambiente),
        }
        
        # Destinatário (obrigatório para NF-e)
        cpf_cnpj = nota_fiscal.dest_cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
        
        if len(cpf_cnpj) == 11:
            dados["cliente"] = {
                "cpf": cpf_cnpj,
                "nome_completo": nota_fiscal.dest_nome,
                "endereco": nota_fiscal.dest_logradouro,
                "numero": nota_fiscal.dest_numero,
                "complemento": nota_fiscal.dest_complemento or "",
                "bairro": nota_fiscal.dest_bairro,
                "cidade": nota_fiscal.dest_cidade,
                "uf": nota_fiscal.dest_uf,
                "cep": nota_fiscal.dest_cep.replace("-", ""),
                "telefone": nota_fiscal.dest_telefone or "",
                "email": nota_fiscal.dest_email or "",
            }
        else:
            dados["cliente"] = {
                "cnpj": cpf_cnpj,
                "razao_social": nota_fiscal.dest_nome,
                "ie": nota_fiscal.dest_ie or "",
                "endereco": nota_fiscal.dest_logradouro,
                "numero": nota_fiscal.dest_numero,
                "complemento": nota_fiscal.dest_complemento or "",
                "bairro": nota_fiscal.dest_bairro,
                "cidade": nota_fiscal.dest_cidade,
                "uf": nota_fiscal.dest_uf,
                "cep": nota_fiscal.dest_cep.replace("-", ""),
                "telefone": nota_fiscal.dest_telefone or "",
                "email": nota_fiscal.dest_email or "",
            }
        
        # Produtos
        produtos = []
        for item in nota_fiscal.itens.all():
            produto = {
                "nome": item.descricao[:120],
                "codigo": item.codigo[:60],
                "ncm": item.ncm,
                "cfop": item.cfop,
                "unidade": item.unidade,
                "quantidade": self._decimal_to_float(item.quantidade),
                "subtotal": self._decimal_to_float(item.valor_unitario),
                "total": self._decimal_to_float(item.valor_total),
                "impostos": {
                    "icms": {
                        "origem": item.origem,
                        "csosn": item.csosn,
                    }
                }
            }
            
            if item.valor_desconto > 0:
                produto["desconto"] = self._decimal_to_float(item.valor_desconto)
            
            produtos.append(produto)
        
        dados["produtos"] = produtos
        
        # Pagamentos
        pagamentos = []
        for pag in nota_fiscal.pagamentos.all():
            pagamento = {
                "forma_pagamento": pag.forma_pagamento,
                "valor": self._decimal_to_float(pag.valor),
            }
            pagamentos.append(pagamento)
        
        # Duplicatas (para pagamento a prazo)
        duplicatas = nota_fiscal.duplicatas.all()
        if duplicatas.exists():
            fatura = {
                "numero": str(nota_fiscal.numero),
                "valor": self._decimal_to_float(nota_fiscal.valor_total),
                "desconto": self._decimal_to_float(nota_fiscal.valor_desconto),
                "valor_liquido": self._decimal_to_float(nota_fiscal.valor_total - nota_fiscal.valor_desconto),
            }
            
            parcelas = []
            for dup in duplicatas:
                parcela = {
                    "numero": dup.numero,
                    "vencimento": dup.data_vencimento.strftime("%Y-%m-%d"),
                    "valor": self._decimal_to_float(dup.valor),
                }
                parcelas.append(parcela)
            
            dados["pedido"] = {
                "pagamento": pagamentos,
                "presenca": int(nota_fiscal.presenca),
                "fatura": fatura,
                "parcelas": parcelas,
            }
        else:
            dados["pedido"] = {
                "pagamento": pagamentos,
                "presenca": int(nota_fiscal.presenca),
            }
        
        # Informações complementares
        if nota_fiscal.informacoes_complementares:
            dados["pedido"]["informacoes_complementares"] = nota_fiscal.informacoes_complementares
        
        # Enviar para API
        response = self._request("/emissao", "POST", dados)
        
        return self._processar_resposta(nota_fiscal, response)
    
    def _processar_resposta(self, nota_fiscal, response):
        """
        Processa a resposta da API e atualiza a nota fiscal
        
        Args:
            nota_fiscal: Instância de NotaFiscal
            response: Resposta da API
        
        Returns:
            dict: Resposta processada
        """
        if "error" in response:
            nota_fiscal.status = "REJEITADA"
            nota_fiscal.motivo_rejeicao = response.get("error", "Erro desconhecido")
            nota_fiscal.save()
            return {
                "sucesso": False,
                "erro": response.get("error"),
                "nota_fiscal": nota_fiscal,
            }
        
        status = response.get("status", "")
        
        if status == "aprovado":
            nota_fiscal.status = "AUTORIZADA"
            nota_fiscal.chave_acesso = response.get("chave", "")
            nota_fiscal.protocolo = response.get("protocolo", "")
            nota_fiscal.data_autorizacao = datetime.now()
            nota_fiscal.xml_autorizado = response.get("xml", "")
            
            # Salvar DANFE se disponível
            danfe_url = response.get("danfe", "")
            if danfe_url:
                nota_fiscal.informacoes_complementares = (
                    nota_fiscal.informacoes_complementares or ""
                ) + f"\nDANFE: {danfe_url}"
            
            nota_fiscal.save()
            
            return {
                "sucesso": True,
                "status": "AUTORIZADA",
                "chave": response.get("chave", ""),
                "protocolo": response.get("protocolo", ""),
                "numero": response.get("nfe", ""),
                "danfe_url": response.get("danfe", ""),
                "xml_url": response.get("xml", ""),
                "nota_fiscal": nota_fiscal,
            }
        
        elif status == "reprovado":
            nota_fiscal.status = "REJEITADA"
            nota_fiscal.motivo_rejeicao = response.get("motivo", "")
            nota_fiscal.codigo_status_sefaz = response.get("codigo", "")
            nota_fiscal.save()
            
            return {
                "sucesso": False,
                "status": "REJEITADA",
                "codigo": response.get("codigo", ""),
                "motivo": response.get("motivo", ""),
                "nota_fiscal": nota_fiscal,
            }
        
        elif status == "processamento":
            nota_fiscal.status = "PROCESSANDO"
            nota_fiscal.save()
            
            return {
                "sucesso": True,
                "status": "PROCESSANDO",
                "mensagem": "Nota em processamento. Consulte novamente em alguns segundos.",
                "nota_fiscal": nota_fiscal,
            }
        
        else:
            nota_fiscal.status = "REJEITADA"
            nota_fiscal.motivo_rejeicao = json.dumps(response)
            nota_fiscal.save()
            
            return {
                "sucesso": False,
                "status": "ERRO",
                "erro": "Resposta inesperada da API",
                "resposta_completa": response,
                "nota_fiscal": nota_fiscal,
            }
    
    def consultar_nota(self, chave_acesso):
        """
        Consulta o status de uma nota fiscal pela chave de acesso
        
        Args:
            chave_acesso: Chave de acesso de 44 dígitos
        
        Returns:
            dict: Status da nota
        """
        dados = {"chave": chave_acesso}
        return self._request("/consulta", "GET", dados)
    
    def cancelar_nota(self, nota_fiscal, justificativa):
        """
        Cancela uma nota fiscal autorizada
        
        Args:
            nota_fiscal: Instância de NotaFiscal
            justificativa: Motivo do cancelamento (mínimo 15 caracteres)
        
        Returns:
            dict: Resultado do cancelamento
        """
        from fiscal.models import EventoNotaFiscal
        
        if not nota_fiscal.chave_acesso:
            return {"sucesso": False, "erro": "Nota sem chave de acesso"}
        
        if len(justificativa) < 15:
            return {"sucesso": False, "erro": "Justificativa deve ter no mínimo 15 caracteres"}
        
        dados = {
            "chave": nota_fiscal.chave_acesso,
            "motivo": justificativa,
        }
        
        response = self._request("/cancelar", "POST", dados)
        
        # Criar evento de cancelamento
        evento = EventoNotaFiscal.objects.create(
            nota_fiscal=nota_fiscal,
            tipo="CANCELAMENTO",
            justificativa=justificativa,
            xml_retorno=json.dumps(response),
        )
        
        if response.get("status") == "cancelado":
            nota_fiscal.status = "CANCELADA"
            nota_fiscal.save()
            
            evento.status = "AUTORIZADO"
            evento.protocolo = response.get("protocolo", "")
            evento.save()
            
            return {
                "sucesso": True,
                "status": "CANCELADA",
                "protocolo": response.get("protocolo", ""),
            }
        else:
            evento.status = "REJEITADO"
            evento.motivo = response.get("motivo", response.get("error", ""))
            evento.save()
            
            return {
                "sucesso": False,
                "status": "ERRO",
                "erro": response.get("motivo", response.get("error", "")),
            }
    
    def carta_correcao(self, nota_fiscal, correcao):
        """
        Emite uma Carta de Correção para a nota fiscal
        
        Args:
            nota_fiscal: Instância de NotaFiscal
            correcao: Texto da correção (mínimo 15 caracteres)
        
        Returns:
            dict: Resultado da carta de correção
        """
        from fiscal.models import EventoNotaFiscal
        
        if not nota_fiscal.chave_acesso:
            return {"sucesso": False, "erro": "Nota sem chave de acesso"}
        
        if len(correcao) < 15:
            return {"sucesso": False, "erro": "Correção deve ter no mínimo 15 caracteres"}
        
        # Contar sequência de CCe
        sequencia = EventoNotaFiscal.objects.filter(
            nota_fiscal=nota_fiscal,
            tipo="CARTA_CORRECAO",
            status="AUTORIZADO"
        ).count() + 1
        
        dados = {
            "chave": nota_fiscal.chave_acesso,
            "correcao": correcao,
        }
        
        response = self._request("/cartacorrecao", "POST", dados)
        
        # Criar evento
        evento = EventoNotaFiscal.objects.create(
            nota_fiscal=nota_fiscal,
            tipo="CARTA_CORRECAO",
            sequencia=sequencia,
            correcao=correcao,
            xml_retorno=json.dumps(response),
        )
        
        if response.get("status") == "aprovado":
            evento.status = "AUTORIZADO"
            evento.protocolo = response.get("protocolo", "")
            evento.save()
            
            return {
                "sucesso": True,
                "status": "AUTORIZADA",
                "protocolo": response.get("protocolo", ""),
                "sequencia": sequencia,
            }
        else:
            evento.status = "REJEITADO"
            evento.motivo = response.get("motivo", response.get("error", ""))
            evento.save()
            
            return {
                "sucesso": False,
                "status": "ERRO",
                "erro": response.get("motivo", response.get("error", "")),
            }
    
    def inutilizar_numeracao(self, modelo, serie, numero_inicial, numero_final, justificativa):
        """
        Inutiliza uma faixa de numeração
        
        Args:
            modelo: '55' para NF-e ou '65' para NFC-e
            serie: Série da nota
            numero_inicial: Número inicial da faixa
            numero_final: Número final da faixa
            justificativa: Motivo da inutilização (mínimo 15 caracteres)
        
        Returns:
            dict: Resultado da inutilização
        """
        from fiscal.models import InutilizacaoNumeracao
        
        if len(justificativa) < 15:
            return {"sucesso": False, "erro": "Justificativa deve ter no mínimo 15 caracteres"}
        
        dados = {
            "modelo": 1 if modelo == "55" else 2,
            "serie": serie,
            "inicio": numero_inicial,
            "final": numero_final,
            "motivo": justificativa,
        }
        
        response = self._request("/inutilizar", "POST", dados)
        
        # Criar registro
        inutilizacao = InutilizacaoNumeracao.objects.create(
            modelo=modelo,
            serie=serie,
            numero_inicial=numero_inicial,
            numero_final=numero_final,
            justificativa=justificativa,
            xml_retorno=json.dumps(response),
        )
        
        if response.get("status") == "aprovado":
            inutilizacao.status = "APROVADO"
            inutilizacao.protocolo = response.get("protocolo", "")
            inutilizacao.data_inutilizacao = datetime.now()
            inutilizacao.save()
            
            return {
                "sucesso": True,
                "status": "APROVADO",
                "protocolo": response.get("protocolo", ""),
            }
        else:
            inutilizacao.status = "REJEITADO"
            inutilizacao.save()
            
            return {
                "sucesso": False,
                "status": "ERRO",
                "erro": response.get("motivo", response.get("error", "")),
            }
    
    def gerar_danfe(self, chave_acesso):
        """
        Obtém a URL do DANFE de uma nota autorizada
        
        Args:
            chave_acesso: Chave de acesso de 44 dígitos
        
        Returns:
            str: URL do DANFE
        """
        dados = {"chave": chave_acesso}
        response = self._request("/danfe", "GET", dados)
        return response.get("danfe", "")
    
    def obter_xml(self, chave_acesso):
        """
        Obtém o XML de uma nota autorizada
        
        Args:
            chave_acesso: Chave de acesso de 44 dígitos
        
        Returns:
            str: XML da nota
        """
        dados = {"chave": chave_acesso}
        response = self._request("/xml", "GET", dados)
        return response.get("xml", "")


class NotaFiscalService:
    """Serviço de alto nível para gerenciar notas fiscais"""
    
    def __init__(self):
        self.webmania = WebmaniaBRService()
    
    def criar_nfce_da_venda(self, venda, cpf_cliente=None):
        """
        Cria e emite uma NFC-e a partir de uma venda
        
        Args:
            venda: Instância de Venda
            cpf_cliente: CPF do cliente (opcional)
        
        Returns:
            dict: Resultado da emissão
        """
        from fiscal.models import (
            NotaFiscal, ItemNotaFiscal, PagamentoNotaFiscal, ConfiguracaoFiscal
        )
        from vendas.models import ItemVenda
        
        config = ConfiguracaoFiscal.get_config()
        if not config:
            return {"sucesso": False, "erro": "Configuração fiscal não encontrada"}
        
        # Criar nota fiscal
        nota = NotaFiscal.objects.create(
            modelo="65",
            serie=config.serie_nfce,
            numero=config.get_proximo_numero_nfce(),
            natureza_operacao="VENDA DE MERCADORIA",
            tipo_operacao="1",
            finalidade="1",
            presenca="1",
            venda=venda,
            cliente=venda.cliente,
            valor_produtos=venda.subtotal,
            valor_desconto=venda.desconto,
            valor_total=venda.total,
        )
        
        # Destinatário
        if cpf_cliente:
            nota.dest_cpf_cnpj = cpf_cliente
            if venda.cliente:
                nota.dest_nome = venda.cliente.nome
        elif venda.cliente and venda.cliente.cpf_cnpj:
            nota.dest_cpf_cnpj = venda.cliente.cpf_cnpj
            nota.dest_nome = venda.cliente.nome
        
        nota.save()
        
        # Itens
        for idx, item_venda in enumerate(venda.itens.all(), 1):
            produto = item_venda.produto
            
            # Determinar CFOP e CSOSN
            cfop = "5405" if produto.tem_st else "5102"
            csosn = "500" if produto.tem_st else "102"
            
            ItemNotaFiscal.objects.create(
                nota_fiscal=nota,
                produto=produto,
                numero_item=idx,
                codigo=produto.codigo,
                descricao=produto.descricao[:120],
                ncm=produto.ncm or "00000000",
                cfop=cfop,
                unidade=produto.unidade or "UN",
                quantidade=item_venda.quantidade,
                valor_unitario=item_venda.preco_unitario,
                valor_total=item_venda.total,
                valor_desconto=item_venda.desconto or 0,
                origem="0",
                csosn=csosn,
            )
        
        # Pagamento
        forma_pagamento_map = {
            "DI": "01",  # Dinheiro
            "PI": "17",  # PIX
            "CD": "04",  # Cartão Débito
            "CC": "03",  # Cartão Crédito
            "BO": "15",  # Boleto
            "CR": "05",  # Crediário
        }
        
        forma = forma_pagamento_map.get(venda.forma_pagamento, "99")
        
        PagamentoNotaFiscal.objects.create(
            nota_fiscal=nota,
            forma_pagamento=forma,
            valor=venda.total,
        )
        
        # Emitir
        resultado = self.webmania.emitir_nfce(nota)
        
        return resultado
    
    def criar_nfe_da_venda(self, venda, duplicatas=None):
        """
        Cria e emite uma NF-e a partir de uma venda (para empresas)
        
        Args:
            venda: Instância de Venda
            duplicatas: Lista de dicts com {data_vencimento, valor} para pagamento a prazo
        
        Returns:
            dict: Resultado da emissão
        """
        from fiscal.models import (
            NotaFiscal, ItemNotaFiscal, PagamentoNotaFiscal,
            DuplicataNotaFiscal, ConfiguracaoFiscal
        )
        
        config = ConfiguracaoFiscal.get_config()
        if not config:
            return {"sucesso": False, "erro": "Configuração fiscal não encontrada"}
        
        cliente = venda.cliente
        if not cliente:
            return {"sucesso": False, "erro": "Venda sem cliente vinculado"}
        
        if not cliente.cpf_cnpj:
            return {"sucesso": False, "erro": "Cliente sem CPF/CNPJ cadastrado"}
        
        # Criar nota fiscal
        nota = NotaFiscal.objects.create(
            modelo="55",
            serie=config.serie_nfe,
            numero=config.get_proximo_numero_nfe(),
            natureza_operacao="VENDA DE MERCADORIA",
            tipo_operacao="1",
            finalidade="1",
            presenca="1",
            venda=venda,
            cliente=cliente,
            # Destinatário
            dest_cpf_cnpj=cliente.cpf_cnpj,
            dest_nome=cliente.nome,
            dest_ie=cliente.inscricao_estadual or "",
            dest_email=cliente.email or "",
            dest_telefone=cliente.telefone or "",
            dest_cep=cliente.cep or "",
            dest_logradouro=cliente.endereco or "",
            dest_numero=cliente.numero or "S/N",
            dest_complemento=cliente.complemento or "",
            dest_bairro=cliente.bairro or "",
            dest_cidade=cliente.cidade or "",
            dest_uf=cliente.uf or "",
            # Valores
            valor_produtos=venda.subtotal,
            valor_desconto=venda.desconto,
            valor_total=venda.total,
        )
        
        # Itens
        for idx, item_venda in enumerate(venda.itens.all(), 1):
            produto = item_venda.produto
            
            cfop = "5405" if produto.tem_st else "5102"
            csosn = "500" if produto.tem_st else "102"
            
            ItemNotaFiscal.objects.create(
                nota_fiscal=nota,
                produto=produto,
                numero_item=idx,
                codigo=produto.codigo,
                descricao=produto.descricao[:120],
                ncm=produto.ncm or "00000000",
                cfop=cfop,
                unidade=produto.unidade or "UN",
                quantidade=item_venda.quantidade,
                valor_unitario=item_venda.preco_unitario,
                valor_total=item_venda.total,
                valor_desconto=item_venda.desconto or 0,
                origem="0",
                csosn=csosn,
            )
        
        # Pagamento a prazo com duplicatas
        if duplicatas:
            PagamentoNotaFiscal.objects.create(
                nota_fiscal=nota,
                forma_pagamento="15",  # Boleto
                valor=venda.total,
            )
            
            for idx, dup in enumerate(duplicatas, 1):
                DuplicataNotaFiscal.objects.create(
                    nota_fiscal=nota,
                    numero=f"{nota.numero}-{idx}",
                    data_vencimento=dup["data_vencimento"],
                    valor=dup["valor"],
                )
        else:
            # Pagamento à vista
            forma_pagamento_map = {
                "DI": "01",
                "PI": "17",
                "CD": "04",
                "CC": "03",
            }
            forma = forma_pagamento_map.get(venda.forma_pagamento, "99")
            
            PagamentoNotaFiscal.objects.create(
                nota_fiscal=nota,
                forma_pagamento=forma,
                valor=venda.total,
            )
        
        # Emitir
        resultado = self.webmania.emitir_nfe(nota)
        
        return resultado
    
    def enviar_nota_por_email(self, nota_fiscal, email=None):
        """
        Envia a nota fiscal por email
        
        Args:
            nota_fiscal: Instância de NotaFiscal
            email: Email de destino (usa o email do cliente se não informado)
        
        Returns:
            bool: True se enviou com sucesso
        """
        from django.core.mail import EmailMessage
        
        email_destino = email or nota_fiscal.dest_email
        if not email_destino:
            return False
        
        config = ConfiguracaoFiscal.get_config()
        modelo_nome = "NFC-e" if nota_fiscal.modelo == "65" else "NF-e"
        
        assunto = f"{modelo_nome} Nº {nota_fiscal.numero} - {config.nome_fantasia}"
        
        corpo = f"""
Prezado(a) {nota_fiscal.dest_nome or 'Cliente'},

Segue em anexo a {modelo_nome} referente à sua compra.

Número: {nota_fiscal.numero}
Chave de Acesso: {nota_fiscal.chave_acesso}
Valor Total: R$ {nota_fiscal.valor_total}
Data: {nota_fiscal.data_emissao.strftime('%d/%m/%Y %H:%M')}

Atenciosamente,
{config.nome_fantasia}
        """
        
        try:
            email_msg = EmailMessage(
                subject=assunto,
                body=corpo,
                from_email=config.email,
                to=[email_destino],
            )
            
            # Anexar DANFE se disponível
            if nota_fiscal.pdf_danfe:
                email_msg.attach_file(nota_fiscal.pdf_danfe.path)
            
            email_msg.send()
            return True
        
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
