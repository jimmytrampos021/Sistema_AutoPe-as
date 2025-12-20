"""
Services do Módulo de Compras

Contém a lógica de negócio para:
- Importação de XML
- Vinculação de produtos
- Finalização de entrada
- Atualização de estoque e preços
"""

from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from django.db import transaction, models
from django.utils import timezone
from django.contrib.auth.models import User

from .models import NotaFiscalEntrada, ItemNotaEntrada, LogEntradaMercadoria
from .utils.xml_parser import NFEXMLParser
from .utils.pdf_parser import PDFPedidoParser


class EntradaMercadoriaService:
    """
    Service principal para operações de entrada de mercadoria
    """
    
    def __init__(self, usuario: User = None):
        self.usuario = usuario
        self.errors = []
        self.warnings = []
    
    @transaction.atomic
    def importar_xml(self, xml_file, config: Dict = None) -> Tuple[bool, Optional[NotaFiscalEntrada], List[str]]:
        """
        Importa nota fiscal a partir de arquivo XML
        
        Args:
            xml_file: Arquivo XML
            config: Configurações de importação
            
        Returns:
            Tuple (success, nota_fiscal, errors)
        """
        self.errors = []
        self.warnings = []
        
        config = config or {}
        
        # Parse do XML
        parser = NFEXMLParser(xml_file=xml_file)
        dados = parser.get_all_data()
        
        if not dados.get('success'):
            return False, None, dados.get('errors', ['Erro ao processar XML'])
        
        # Extrai dados
        dados_nota = dados.get('nota', {})
        dados_emitente = dados.get('emitente', {})
        itens = dados.get('itens', [])
        totais = dados.get('totais', {})
        
        # Validações básicas
        if not dados_nota.get('numero_nf'):
            self.errors.append("Número da NF não encontrado no XML")
            return False, None, self.errors
        
        if not dados_emitente.get('cnpj'):
            self.errors.append("CNPJ do emitente não encontrado no XML")
            return False, None, self.errors
        
        # Verifica se a nota já existe (ignora canceladas)
        chave_acesso = dados_nota.get('chave_acesso')
        numero_nf = dados_nota.get('numero_nf')
        serie = dados_nota.get('serie', '1')
        
        if chave_acesso:
            nota_existente = NotaFiscalEntrada.objects.filter(chave_acesso=chave_acesso).exclude(status='X').first()
            if nota_existente:
                self.errors.append(f"Nota fiscal já importada anteriormente (ID: {nota_existente.id}, Status: {nota_existente.get_status_display()})")
                return False, None, self.errors
            
            # Se existe uma cancelada com mesma chave, limpa a chave da cancelada
            nota_cancelada = NotaFiscalEntrada.objects.filter(chave_acesso=chave_acesso, status='X').first()
            if nota_cancelada:
                nota_cancelada.chave_acesso = f"{chave_acesso}-CANCELADA"
                nota_cancelada.save()
                self.warnings.append(f"Reimportação de NF cancelada. Chave anterior modificada.")
        
        # Busca ou cria fornecedor
        fornecedor = self._get_or_create_fornecedor(dados_emitente)
        if not fornecedor:
            return False, None, self.errors
        
        # Verifica se existe nota cancelada com mesmo número/série/fornecedor
        nota_cancelada_nf = NotaFiscalEntrada.objects.filter(
            numero_nf=numero_nf,
            serie=serie,
            fornecedor=fornecedor,
            status='X'
        ).first()
        
        if nota_cancelada_nf:
            # Modifica o número da nota cancelada para liberar
            import uuid
            nota_cancelada_nf.numero_nf = f"{numero_nf}-CANC-{str(uuid.uuid4())[:4].upper()}"
            nota_cancelada_nf.save()
            self.warnings.append(f"Nota cancelada renumerada para permitir reimportação.")
        
        # Cria a nota fiscal
        try:
            nota = NotaFiscalEntrada.objects.create(
                numero_nf=numero_nf,
                serie=serie,
                chave_acesso=chave_acesso,
                natureza_operacao=dados_nota.get('natureza_operacao', 'COMPRA'),
                data_emissao=dados_nota.get('data_emissao') or timezone.now().date(),
                data_entrada=timezone.now().date(),
                fornecedor=fornecedor,
                valor_produtos=totais.get('valor_produtos', Decimal('0.00')),
                valor_frete=totais.get('valor_frete', Decimal('0.00')),
                valor_seguro=totais.get('valor_seguro', Decimal('0.00')),
                valor_desconto=totais.get('valor_desconto', Decimal('0.00')),
                valor_outras_despesas=totais.get('valor_outras_despesas', Decimal('0.00')),
                valor_ipi=totais.get('valor_ipi', Decimal('0.00')),
                valor_icms_st=totais.get('valor_icms_st', Decimal('0.00')),
                valor_total=totais.get('valor_total', Decimal('0.00')),
                tipo_entrada='X',  # XML
                status='P',  # Pendente
                arquivo_xml=xml_file,
                atualizar_preco_custo=config.get('atualizar_preco_custo', True),
                atualizar_preco_venda=config.get('atualizar_preco_venda', False),
                margem_padrao=config.get('margem_padrao', Decimal('50.00')),
                ratear_frete=config.get('ratear_frete', True),
                atualizar_cotacao=config.get('atualizar_cotacao', True),
                usuario_cadastro=self.usuario,
            )
        except Exception as e:
            self.errors.append(f"Erro ao criar nota fiscal: {str(e)}")
            return False, None, self.errors
        
        # Cria os itens
        itens_criados = 0
        itens_vinculados = 0
        
        for item_data in itens:
            try:
                item = ItemNotaEntrada.objects.create(
                    nota=nota,
                    numero_item=item_data.get('numero_item', 1),
                    codigo_produto_fornecedor=item_data.get('codigo_produto_fornecedor', ''),
                    codigo_barras_nf=item_data.get('codigo_barras', ''),
                    descricao_nf=item_data.get('descricao', ''),
                    ncm=item_data.get('ncm', ''),
                    cest=item_data.get('cest', ''),
                    cfop=item_data.get('cfop', ''),
                    unidade=item_data.get('unidade', 'UN'),
                    quantidade=item_data.get('quantidade', Decimal('0')),
                    valor_unitario=item_data.get('valor_unitario', Decimal('0')),
                    valor_total=item_data.get('valor_total', Decimal('0')),
                    valor_desconto=item_data.get('valor_desconto', Decimal('0')),
                    valor_ipi=item_data.get('valor_ipi', Decimal('0')),
                    valor_icms_st=item_data.get('valor_icms_st', Decimal('0')),
                )
                
                itens_criados += 1
                
                # Tenta vincular automaticamente
                produto = item.vincular_produto_automatico()
                if produto:
                    itens_vinculados += 1
                
            except Exception as e:
                self.warnings.append(f"Erro ao criar item {item_data.get('numero_item')}: {str(e)}")
        
        # Log
        self._criar_log(
            nota=nota,
            acao='IMPORTAR_XML',
            descricao=f"XML importado com sucesso. {itens_criados} itens, {itens_vinculados} vinculados automaticamente.",
            dados={'itens_criados': itens_criados, 'itens_vinculados': itens_vinculados}
        )
        
        return True, nota, self.warnings
    
    @transaction.atomic
    def importar_pdf(self, pdf_file, config: Dict = None) -> Tuple[bool, Optional[NotaFiscalEntrada], List[str]]:
        """
        Importa pedido a partir de arquivo PDF
        
        Args:
            pdf_file: Arquivo PDF
            config: Configurações de importação
            
        Returns:
            Tuple (success, nota_fiscal, errors)
        """
        self.errors = []
        self.warnings = []
        
        config = config or {}
        
        # Parse do PDF
        parser = PDFPedidoParser()
        success, dados, warnings = parser.parse(pdf_file)
        
        if not success:
            return False, None, warnings
        
        self.warnings.extend(warnings)
        
        # Extrai dados
        itens = dados.get('itens', [])
        
        if not itens:
            self.errors.append("Nenhum item encontrado no PDF")
            return False, None, self.errors
        
        # Busca ou cria fornecedor
        fornecedor_nome = dados.get('fornecedor', '')
        if fornecedor_nome:
            fornecedor = self._get_or_create_fornecedor_por_nome(fornecedor_nome)
        else:
            self.errors.append("Fornecedor não identificado no PDF")
            return False, None, self.errors
        
        if not fornecedor:
            return False, None, self.errors
        
        # Gera número único para o pedido
        numero_pedido = dados.get('numero_pedido', '')
        if not numero_pedido:
            import uuid
            numero_pedido = f"PDF-{str(uuid.uuid4())[:8].upper()}"
        
        # Verifica duplicidade (ignora canceladas)
        nota_existente = NotaFiscalEntrada.objects.filter(
            numero_nf=numero_pedido,
            fornecedor=fornecedor
        ).exclude(status='X').first()
        
        if nota_existente:
            self.errors.append(f"Pedido {numero_pedido} já importado anteriormente (ID: {nota_existente.id}, Status: {nota_existente.get_status_display()})")
            return False, None, self.errors
        
        # Se existe uma cancelada com mesmo número, adiciona sufixo
        nota_cancelada = NotaFiscalEntrada.objects.filter(
            numero_nf=numero_pedido,
            fornecedor=fornecedor,
            status='X'
        ).first()
        
        if nota_cancelada:
            # Adiciona sufixo para evitar conflito de UNIQUE constraint
            import uuid
            numero_pedido = f"{numero_pedido}-R{str(uuid.uuid4())[:4].upper()}"
            self.warnings.append(f"Reimportação de pedido cancelado. Novo número: {numero_pedido}")
        
        # Calcula totais
        valor_produtos = sum(item.get('valor_total', Decimal('0')) for item in itens)
        valor_total = dados.get('total', valor_produtos)
        
        # Cria a nota fiscal (entrada de pedido)
        try:
            nota = NotaFiscalEntrada.objects.create(
                numero_nf=numero_pedido,
                serie='PDF',
                chave_acesso=None,
                natureza_operacao='ENTRADA VIA PEDIDO PDF',
                data_emissao=dados.get('data_emissao') or timezone.now().date(),
                data_entrada=timezone.now().date(),
                fornecedor=fornecedor,
                valor_produtos=valor_produtos,
                valor_frete=Decimal('0.00'),
                valor_seguro=Decimal('0.00'),
                valor_desconto=Decimal('0.00'),
                valor_outras_despesas=Decimal('0.00'),
                valor_ipi=dados.get('ipi', Decimal('0.00')),
                valor_icms_st=dados.get('icms_st', Decimal('0.00')),
                valor_total=valor_total,
                tipo_entrada='X',  # Usamos X para indicar arquivo importado
                status='P',  # Pendente
                atualizar_preco_custo=config.get('atualizar_preco_custo', True),
                atualizar_preco_venda=config.get('atualizar_preco_venda', False),
                margem_padrao=config.get('margem_padrao', Decimal('50.00')),
                ratear_frete=config.get('ratear_frete', True),
                atualizar_cotacao=config.get('atualizar_cotacao', True),
                usuario_cadastro=self.usuario,
                observacoes=f"Importado de PDF - Formato: {dados.get('formato_detectado', 'desconhecido')}",
            )
        except Exception as e:
            self.errors.append(f"Erro ao criar entrada: {str(e)}")
            return False, None, self.errors
        
        # Cria os itens
        itens_criados = 0
        itens_vinculados = 0
        
        for item_data in itens:
            try:
                item = ItemNotaEntrada.objects.create(
                    nota=nota,
                    numero_item=item_data.get('numero_item', itens_criados + 1),
                    codigo_produto_fornecedor=item_data.get('codigo', ''),
                    codigo_barras_nf=item_data.get('codigo_barras', ''),
                    descricao_nf=item_data.get('descricao', '')[:120],
                    ncm='',
                    cest='',
                    cfop='',
                    unidade=item_data.get('unidade', 'UN'),
                    quantidade=item_data.get('quantidade', Decimal('0')),
                    valor_unitario=item_data.get('valor_unitario', Decimal('0')),
                    valor_total=item_data.get('valor_total', Decimal('0')),
                    valor_desconto=Decimal('0.00'),
                    valor_ipi=Decimal('0.00'),
                    valor_icms_st=Decimal('0.00'),
                )
                
                itens_criados += 1
                
                # Tenta vincular automaticamente
                produto = item.vincular_produto_automatico()
                if produto:
                    itens_vinculados += 1
                
            except Exception as e:
                self.warnings.append(f"Erro ao criar item {item_data.get('numero_item')}: {str(e)}")
        
        # Log
        self._criar_log(
            nota=nota,
            acao='IMPORTAR_XML',
            descricao=f"PDF importado ({dados.get('formato_detectado')}). {itens_criados} itens, {itens_vinculados} vinculados.",
            dados={'itens_criados': itens_criados, 'itens_vinculados': itens_vinculados, 'formato': dados.get('formato_detectado')}
        )
        
        return True, nota, self.warnings
    
    def _get_or_create_fornecedor_por_nome(self, nome: str):
        """Busca ou cria fornecedor pelo nome"""
        from estoque.models import Fornecedor
        
        if not nome:
            self.errors.append("Nome do fornecedor não informado")
            return None
        
        # Limpa o nome
        nome = nome.strip()[:100]
        
        # Busca por nome fantasia ou razão social
        fornecedor = Fornecedor.objects.filter(
            models.Q(nome_fantasia__icontains=nome[:50]) |
            models.Q(razao_social__icontains=nome[:50])
        ).first()
        
        if not fornecedor:
            # Cria novo fornecedor
            try:
                fornecedor = Fornecedor.objects.create(
                    cnpj='',  # Sem CNPJ
                    razao_social=nome,
                    nome_fantasia=nome[:100],
                    ativo=True,
                )
                self.warnings.append(f"Fornecedor '{nome[:50]}' cadastrado automaticamente (sem CNPJ)")
            except Exception as e:
                self.errors.append(f"Erro ao cadastrar fornecedor: {str(e)}")
                return None
        
        return fornecedor
    
    def _gerar_proximo_codigo_produto(self) -> str:
        """
        Gera o próximo código de produto sequencial
        Baseado no maior código numérico existente + 1
        """
        from estoque.models import Produto
        from django.db.models import Max
        from django.db.models.functions import Cast
        from django.db.models import IntegerField
        
        try:
            # Busca o maior código numérico (6 dígitos)
            # Filtra apenas códigos que são puramente numéricos e têm 6 dígitos
            produtos_numericos = Produto.objects.filter(
                codigo__regex=r'^\d{6}$'
            )
            
            if produtos_numericos.exists():
                # Converte para inteiro e pega o máximo
                maior_codigo = 0
                for p in produtos_numericos.values_list('codigo', flat=True):
                    try:
                        cod_int = int(p)
                        if cod_int > maior_codigo:
                            maior_codigo = cod_int
                    except ValueError:
                        continue
                
                proximo = maior_codigo + 1
            else:
                # Se não há códigos de 6 dígitos, começa do 100001
                proximo = 100001
            
            # Formata com 6 dígitos
            codigo = str(proximo).zfill(6)
            
            # Garante que não existe (segurança extra)
            while Produto.objects.filter(codigo=codigo).exists():
                proximo += 1
                codigo = str(proximo).zfill(6)
            
            return codigo
            
        except Exception as e:
            # Fallback: gera código único com timestamp
            import uuid
            return f"{int(timezone.now().timestamp()) % 1000000:06d}"
    
    def _get_or_create_fornecedor(self, dados_emitente: Dict):
        """Busca ou cria fornecedor com dados do XML"""
        from estoque.models import Fornecedor
        
        cnpj = dados_emitente.get('cnpj', '')
        if not cnpj:
            self.errors.append("CNPJ do fornecedor não informado")
            return None
        
        # Busca por CNPJ
        fornecedor = Fornecedor.objects.filter(cnpj=cnpj).first()
        
        if not fornecedor:
            # Cria novo fornecedor
            try:
                fornecedor = Fornecedor.objects.create(
                    cnpj=cnpj,
                    razao_social=dados_emitente.get('razao_social', '')[:200],
                    nome_fantasia=dados_emitente.get('nome_fantasia', '')[:100] or dados_emitente.get('razao_social', '')[:100],
                    inscricao_estadual=dados_emitente.get('inscricao_estadual', '')[:20],
                    telefone=dados_emitente.get('telefone', '')[:20],
                    email=dados_emitente.get('email', '')[:254] if dados_emitente.get('email') else '',
                    cep=dados_emitente.get('cep', '')[:9],
                    logradouro=dados_emitente.get('logradouro', '')[:200],
                    numero=dados_emitente.get('numero', '')[:10],
                    complemento=dados_emitente.get('complemento', '')[:100],
                    bairro=dados_emitente.get('bairro', '')[:100],
                    cidade=dados_emitente.get('cidade', '')[:100],
                    estado=dados_emitente.get('uf', '')[:2],
                    ativo=True,
                )
                self.warnings.append(f"Fornecedor '{fornecedor.nome_fantasia}' cadastrado automaticamente")
            except Exception as e:
                self.errors.append(f"Erro ao cadastrar fornecedor: {str(e)}")
                return None
        
        return fornecedor
    
    @transaction.atomic
    def vincular_produto(self, item_id: int, produto_id: int) -> Tuple[bool, str]:
        """
        Vincula um item da nota a um produto do sistema
        
        Args:
            item_id: ID do ItemNotaEntrada
            produto_id: ID do Produto
            
        Returns:
            Tuple (success, message)
        """
        from estoque.models import Produto
        
        try:
            item = ItemNotaEntrada.objects.get(id=item_id)
            produto = Produto.objects.get(id=produto_id)
            
            item.produto = produto
            item.save()
            
            self._criar_log(
                nota=item.nota,
                item=item,
                acao='VINCULAR',
                descricao=f"Item '{item.descricao_nf[:50]}' vinculado ao produto '{produto.descricao[:50]}'",
                dados={'produto_id': produto_id, 'item_id': item_id}
            )
            
            return True, f"Produto vinculado com sucesso"
            
        except ItemNotaEntrada.DoesNotExist:
            return False, "Item não encontrado"
        except Produto.DoesNotExist:
            return False, "Produto não encontrado"
        except Exception as e:
            return False, f"Erro ao vincular: {str(e)}"
    
    @transaction.atomic
    def cadastrar_produto_do_item(self, item_id: int, dados_adicionais: Dict = None) -> Tuple[bool, Optional[int], str]:
        """
        Cadastra um novo produto a partir dos dados do item da NF
        
        Args:
            item_id: ID do ItemNotaEntrada
            dados_adicionais: Dados complementares (categoria, fabricante, etc.)
            
        Returns:
            Tuple (success, produto_id, message)
        """
        from estoque.models import Produto, Categoria, Fabricante, Subcategoria, Grupo, Subgrupo
        
        try:
            item = ItemNotaEntrada.objects.get(id=item_id)
            dados_adicionais = dados_adicionais or {}
            
            # Verifica se já está vinculado
            if item.produto:
                return False, item.produto.id, "Item já está vinculado a um produto"
            
            # Categoria
            categoria = None
            categoria_id = dados_adicionais.get('categoria_id')
            if categoria_id:
                try:
                    categoria = Categoria.objects.get(id=categoria_id)
                except Categoria.DoesNotExist:
                    pass
            
            # Subcategoria
            subcategoria = None
            subcategoria_id = dados_adicionais.get('subcategoria_id')
            if subcategoria_id:
                try:
                    subcategoria = Subcategoria.objects.get(id=subcategoria_id)
                except Subcategoria.DoesNotExist:
                    pass
            
            # Grupo
            grupo = None
            grupo_id = dados_adicionais.get('grupo_id')
            if grupo_id:
                try:
                    grupo = Grupo.objects.get(id=grupo_id)
                except Grupo.DoesNotExist:
                    pass
            
            # Subgrupo
            subgrupo = None
            subgrupo_id = dados_adicionais.get('subgrupo_id')
            if subgrupo_id:
                try:
                    subgrupo = Subgrupo.objects.get(id=subgrupo_id)
                except Subgrupo.DoesNotExist:
                    pass
            
            # Fabricante
            fabricante = None
            fabricante_id = dados_adicionais.get('fabricante_id')
            if fabricante_id:
                try:
                    fabricante = Fabricante.objects.get(id=fabricante_id)
                except Fabricante.DoesNotExist:
                    pass
            
            # Gera código automático do sistema (próximo sequencial)
            codigo_informado = dados_adicionais.get('codigo', '').strip()
            if codigo_informado:
                # Se usuário informou um código, usa ele
                codigo = codigo_informado
                # Garante código único
                codigo_original = codigo
                contador = 1
                while Produto.objects.filter(codigo=codigo).exists():
                    codigo = f"{codigo_original[:40]}-{contador}"
                    contador += 1
            else:
                # Gera código automático sequencial
                codigo = self._gerar_proximo_codigo_produto()
            
            # Referência do fabricante (código que veio da nota)
            referencia_fabricante = item.codigo_produto_fornecedor or dados_adicionais.get('referencia_fabricante', '') or ''
            
            # Preço de custo
            preco_custo = Decimal(str(dados_adicionais.get('preco_custo') or item.valor_custo_unitario or item.valor_unitario))
            
            # Calcula preço de venda com MARGEM (não markup)
            # Margem = (Preço Venda - Preço Custo) / Preço Venda * 100
            # Preço Venda = Preço Custo / (1 - Margem/100)
            preco_venda = dados_adicionais.get('preco_venda')
            if preco_venda:
                preco_venda = Decimal(str(preco_venda))
            else:
                margem = Decimal(str(dados_adicionais.get('margem', item.nota.margem_padrao or 30)))
                if margem >= 100:
                    margem = Decimal('30')  # Margem padrão se >= 100%
                preco_venda = preco_custo / (1 - margem / 100)
            
            # Arredonda para 2 casas
            preco_venda = preco_venda.quantize(Decimal('0.01'))
            
            # Descrição e outros campos
            descricao = dados_adicionais.get('descricao', item.descricao_nf) or item.descricao_nf
            codigo_barras = dados_adicionais.get('codigo_barras', item.codigo_barras_nf) or item.codigo_barras_nf or ''
            ncm = dados_adicionais.get('ncm', item.ncm) or item.ncm or ''
            unidade = dados_adicionais.get('unidade_medida', item.unidade) or item.unidade or 'UN'
            
            # Cria o produto
            produto = Produto.objects.create(
                codigo=codigo[:50],
                codigo_barras=codigo_barras[:50] if codigo_barras else None,
                referencia_fabricante=referencia_fabricante[:100] if referencia_fabricante else None,
                descricao=descricao[:200],
                ncm=ncm[:10] if ncm else None,
                unidade_medida=unidade[:5],
                preco_custo=preco_custo,
                preco_venda_dinheiro=preco_venda,
                preco_venda_debito=preco_venda,
                preco_venda_credito=preco_venda * Decimal('1.05'),  # +5% para crédito
                estoque_atual=0,  # Será atualizado na finalização
                estoque_minimo=int(dados_adicionais.get('estoque_minimo', 1)),
                estoque_maximo=int(dados_adicionais.get('estoque_maximo', 100)),
                quantidade_reposicao=int(dados_adicionais.get('quantidade_reposicao', 5)),
                categoria=categoria,
                subcategoria=subcategoria,
                grupo=grupo,
                subgrupo=subgrupo,
                fabricante=fabricante,
                fornecedor_principal=item.nota.fornecedor,
                loja=dados_adicionais.get('loja', 'A'),
                ativo=True,
            )
            
            # Vincula ao item
            item.produto = produto
            item.save()
            
            self._criar_log(
                nota=item.nota,
                item=item,
                acao='CADASTRAR_PRODUTO',
                descricao=f"Produto '{produto.descricao[:50]}' cadastrado e vinculado",
                dados={'produto_id': produto.id}
            )
            
            return True, produto.id, f"Produto '{produto.codigo}' cadastrado e vinculado com sucesso"
            
        except ItemNotaEntrada.DoesNotExist:
            return False, None, "Item não encontrado"
        except Exception as e:
            return False, None, f"Erro ao cadastrar produto: {str(e)}"
    
    @transaction.atomic
    def conferir_item(self, item_id: int, quantidade_conferida: Decimal, observacao: str = '') -> Tuple[bool, str]:
        """
        Marca um item como conferido
        
        Args:
            item_id: ID do ItemNotaEntrada
            quantidade_conferida: Quantidade física conferida
            observacao: Observação da conferência
            
        Returns:
            Tuple (success, message)
        """
        try:
            item = ItemNotaEntrada.objects.get(id=item_id)
            
            item.quantidade_conferida = quantidade_conferida
            item.conferido = True
            item.divergencia = (quantidade_conferida != item.quantidade)
            item.observacao = observacao
            item.save()
            
            # Calcula custo unitário
            item.calcular_custo_unitario()
            
            # Atualiza status da nota
            nota = item.nota
            if nota.itens.filter(conferido=False).count() == 0:
                nota.status = 'C'  # Conferida
                nota.data_conferencia = timezone.now()
                nota.usuario_conferencia = self.usuario
                nota.save()
            elif nota.status == 'P':
                nota.status = 'E'  # Em conferência
                nota.save()
            
            self._criar_log(
                nota=nota,
                item=item,
                acao='CONFERIR',
                descricao=f"Item conferido: {quantidade_conferida} {item.unidade}" + 
                         (f" (divergência: NF={item.quantidade})" if item.divergencia else ""),
                dados={'quantidade_conferida': str(quantidade_conferida), 'divergencia': item.divergencia}
            )
            
            return True, "Item conferido com sucesso"
            
        except ItemNotaEntrada.DoesNotExist:
            return False, "Item não encontrado"
        except Exception as e:
            return False, f"Erro ao conferir: {str(e)}"
    
    @transaction.atomic
    def finalizar_entrada(self, nota_id: int) -> Tuple[bool, str, Dict]:
        """
        Finaliza a entrada de mercadoria
        
        - Atualiza estoque dos produtos
        - Atualiza preço de custo
        - Recalcula preço de venda (se configurado)
        - Cria cotações do fornecedor (se configurado)
        - Gera movimentações de estoque
        
        Args:
            nota_id: ID da NotaFiscalEntrada
            
        Returns:
            Tuple (success, message, resumo)
        """
        from estoque.models import MovimentacaoEstoque, CotacaoFornecedor, HistoricoPreco
        
        resumo = {
            'estoque_atualizado': 0,
            'precos_atualizados': 0,
            'cotacoes_criadas': 0,
            'erros': []
        }
        
        try:
            nota = NotaFiscalEntrada.objects.get(id=nota_id)
            
            # Validações
            if nota.status == 'F':
                return False, "Nota já finalizada", resumo
            
            if nota.status == 'X':
                return False, "Nota cancelada", resumo
            
            if nota.itens_pendentes > 0:
                return False, f"Existem {nota.itens_pendentes} itens não vinculados", resumo
            
            # Processa cada item
            for item in nota.itens.filter(produto__isnull=False):
                produto = item.produto
                quantidade = int(item.quantidade_conferida or item.quantidade)
                
                try:
                    # 1. Atualiza estoque
                    estoque_anterior = produto.estoque_atual
                    produto.estoque_atual = (produto.estoque_atual or 0) + quantidade
                    
                    # 2. Atualiza preço de custo
                    custo_anterior = produto.preco_custo
                    if nota.atualizar_preco_custo:
                        produto.preco_custo = item.valor_custo_unitario or item.valor_unitario
                    
                    # 3. Recalcula preço de venda se configurado (usando MARGEM, não markup)
                    # Margem = (Venda - Custo) / Venda * 100
                    # Venda = Custo / (1 - Margem/100)
                    venda_anterior = produto.preco_venda_dinheiro
                    if nota.atualizar_preco_venda and produto.preco_custo:
                        margem = nota.margem_padrao / 100
                        if margem < 1:  # Se margem < 100%
                            produto.preco_venda_dinheiro = produto.preco_custo / (1 - margem)
                        else:
                            # Fallback para markup se margem >= 100%
                            produto.preco_venda_dinheiro = produto.preco_custo * Decimal('1.5')
                        
                        # Atualiza outros preços proporcionalmente se existirem
                        if produto.preco_venda_debito and venda_anterior and venda_anterior > 0:
                            fator = produto.preco_venda_dinheiro / venda_anterior
                            produto.preco_venda_debito = produto.preco_venda_debito * fator
                        
                        if produto.preco_venda_credito and venda_anterior and venda_anterior > 0:
                            fator = produto.preco_venda_dinheiro / venda_anterior
                            produto.preco_venda_credito = produto.preco_venda_credito * fator
                        
                        resumo['precos_atualizados'] += 1
                    
                    produto.save()
                    resumo['estoque_atualizado'] += 1
                    
                    # 4. Cria movimentação de estoque
                    MovimentacaoEstoque.objects.create(
                        produto=produto,
                        tipo='E',  # Entrada
                        quantidade=quantidade,
                        valor_unitario=item.valor_custo_unitario or item.valor_unitario,
                        valor_total=item.valor_total,
                        documento=f"NF {nota.numero_nf}/{nota.serie}",
                        observacoes=f"Entrada via NF {nota.numero_nf} - {nota.fornecedor.nome_fantasia}",
                        usuario=self.usuario.username if self.usuario else 'Sistema',
                    )
                    
                    # 5. Registra histórico de preço se mudou
                    if custo_anterior != produto.preco_custo or venda_anterior != produto.preco_venda_dinheiro:
                        HistoricoPreco.objects.create(
                            produto=produto,
                            preco_custo_anterior=custo_anterior or Decimal('0.00'),
                            preco_custo_novo=produto.preco_custo or Decimal('0.00'),
                            preco_venda_anterior=venda_anterior or Decimal('0.00'),
                            preco_venda_novo=produto.preco_venda_dinheiro or Decimal('0.00'),
                            usuario=self.usuario,
                            motivo=f"Entrada NF {nota.numero_nf}"
                        )
                    
                    # 6. Cria/atualiza cotação do fornecedor
                    if nota.atualizar_cotacao:
                        cotacao, created = CotacaoFornecedor.objects.update_or_create(
                            produto=produto,
                            fornecedor=nota.fornecedor,
                            defaults={
                                'preco': item.valor_unitario,
                                'prazo_entrega': nota.fornecedor.prazo_entrega_dias or 0,
                                'observacoes': f"Atualizado via NF {nota.numero_nf} em {timezone.now().strftime('%d/%m/%Y')}",
                                'ativo': True,
                            }
                        )
                        if created:
                            resumo['cotacoes_criadas'] += 1
                    
                    self._criar_log(
                        nota=nota,
                        item=item,
                        acao='ATUALIZAR_ESTOQUE',
                        descricao=f"Estoque atualizado: {estoque_anterior} → {produto.estoque_atual}",
                        dados={
                            'estoque_anterior': estoque_anterior,
                            'estoque_novo': produto.estoque_atual,
                            'custo_anterior': str(custo_anterior),
                            'custo_novo': str(produto.preco_custo)
                        }
                    )
                    
                except Exception as e:
                    resumo['erros'].append(f"Erro no item {item.numero_item}: {str(e)}")
            
            # Finaliza a nota
            nota.status = 'F'
            nota.data_finalizacao = timezone.now()
            nota.usuario_finalizacao = self.usuario
            nota.save()
            
            self._criar_log(
                nota=nota,
                acao='FINALIZAR',
                descricao=f"Entrada finalizada. Estoque: {resumo['estoque_atualizado']} itens, "
                         f"Preços: {resumo['precos_atualizados']}, Cotações: {resumo['cotacoes_criadas']}",
                dados=resumo
            )
            
            return True, "Entrada finalizada com sucesso", resumo
            
        except NotaFiscalEntrada.DoesNotExist:
            return False, "Nota fiscal não encontrada", resumo
        except Exception as e:
            return False, f"Erro ao finalizar: {str(e)}", resumo
    
    @transaction.atomic
    def cancelar_entrada(self, nota_id: int, motivo: str = '') -> Tuple[bool, str]:
        """
        Cancela uma entrada de mercadoria
        
        Args:
            nota_id: ID da NotaFiscalEntrada
            motivo: Motivo do cancelamento
            
        Returns:
            Tuple (success, message)
        """
        try:
            nota = NotaFiscalEntrada.objects.get(id=nota_id)
            
            if nota.status == 'F':
                return False, "Não é possível cancelar entrada já finalizada"
            
            if nota.status == 'X':
                return False, "Entrada já está cancelada"
            
            nota.status = 'X'
            nota.observacoes = f"{nota.observacoes}\n[CANCELADA] {motivo}".strip()
            nota.save()
            
            self._criar_log(
                nota=nota,
                acao='CANCELAR',
                descricao=f"Entrada cancelada. Motivo: {motivo}",
                dados={'motivo': motivo}
            )
            
            return True, "Entrada cancelada com sucesso"
            
        except NotaFiscalEntrada.DoesNotExist:
            return False, "Nota fiscal não encontrada"
        except Exception as e:
            return False, f"Erro ao cancelar: {str(e)}"
    
    def buscar_produtos_para_vincular(self, termo: str, limit: int = 10) -> List[Dict]:
        """
        Busca produtos para vincular a um item
        
        Args:
            termo: Termo de busca
            limit: Limite de resultados
            
        Returns:
            Lista de produtos encontrados
        """
        from estoque.models import Produto
        from django.db.models import Q
        
        if not termo or len(termo) < 2:
            return []
        
        produtos = Produto.objects.filter(
            Q(codigo__icontains=termo) |
            Q(codigo_barras__icontains=termo) |
            Q(descricao__icontains=termo) |
            Q(referencia_fabricante__icontains=termo),
            ativo=True
        )[:limit]
        
        return [
            {
                'id': p.id,
                'codigo': p.codigo,
                'codigo_barras': p.codigo_barras,
                'descricao': p.descricao,
                'estoque_atual': p.estoque_atual,
                'preco_custo': str(p.preco_custo or 0),
                'preco_venda': str(p.preco_venda_dinheiro or 0),
            }
            for p in produtos
        ]
    
    def _criar_log(self, nota: NotaFiscalEntrada, acao: str, descricao: str, 
                   item: ItemNotaEntrada = None, dados: Dict = None):
        """Cria registro de log"""
        LogEntradaMercadoria.objects.create(
            nota=nota,
            item=item,
            acao=acao,
            descricao=descricao,
            dados_json=dados,
            usuario=self.usuario,
        )
