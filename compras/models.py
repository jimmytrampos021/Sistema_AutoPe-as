"""
Módulo de Compras/Entrada de Mercadorias
Sistema AutoPeças

Models para controle de entrada de mercadorias via:
- Digitação manual
- Upload de XML de NF-e
- Integração com API SEFAZ (futuro)
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class NotaFiscalEntrada(models.Model):
    """
    Nota Fiscal de Entrada (Compra de Mercadorias)
    
    Representa uma nota fiscal de compra que pode ser:
    - Digitada manualmente
    - Importada via XML
    - Sincronizada via API SEFAZ
    """
    
    STATUS_CHOICES = [
        ('P', 'Pendente'),       # Aguardando conferência
        ('E', 'Em Conferência'), # Conferência em andamento
        ('C', 'Conferida'),      # Todos os itens conferidos
        ('F', 'Finalizada'),     # Estoque atualizado
        ('X', 'Cancelada'),      # Nota cancelada
    ]
    
    TIPO_ENTRADA_CHOICES = [
        ('M', 'Manual'),
        ('X', 'XML'),
        ('A', 'Automático (API)'),
    ]
    
    # ========== DADOS DA NOTA FISCAL ==========
    numero_nf = models.CharField(
        max_length=20,
        verbose_name='Número da NF'
    )
    serie = models.CharField(
        max_length=5,
        default='1',
        verbose_name='Série'
    )
    chave_acesso = models.CharField(
        max_length=44,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Chave de Acesso',
        help_text='44 dígitos da chave de acesso da NF-e'
    )
    natureza_operacao = models.CharField(
        max_length=100,
        blank=True,
        default='COMPRA PARA REVENDA',
        verbose_name='Natureza da Operação'
    )
    
    # ========== DATAS ==========
    data_emissao = models.DateField(
        verbose_name='Data de Emissão'
    )
    data_entrada = models.DateField(
        default=timezone.now,
        verbose_name='Data de Entrada'
    )
    data_conferencia = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data da Conferência'
    )
    data_finalizacao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data de Finalização'
    )
    
    # ========== FORNECEDOR ==========
    fornecedor = models.ForeignKey(
        'estoque.Fornecedor',
        on_delete=models.PROTECT,
        related_name='notas_entrada',
        verbose_name='Fornecedor'
    )
    
    # ========== VALORES ==========
    valor_produtos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor dos Produtos'
    )
    valor_frete = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor do Frete'
    )
    valor_seguro = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor do Seguro'
    )
    valor_desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor do Desconto'
    )
    valor_outras_despesas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Outras Despesas'
    )
    valor_ipi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor do IPI'
    )
    valor_icms_st = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor ICMS ST'
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Total da NF'
    )
    
    # ========== CONTROLE ==========
    tipo_entrada = models.CharField(
        max_length=1,
        choices=TIPO_ENTRADA_CHOICES,
        default='M',
        verbose_name='Tipo de Entrada'
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
        verbose_name='Status'
    )
    arquivo_xml = models.FileField(
        upload_to='nfe_entrada/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Arquivo XML'
    )
    
    # ========== CONFIGURAÇÕES DE ENTRADA ==========
    atualizar_preco_custo = models.BooleanField(
        default=True,
        verbose_name='Atualizar Preço de Custo',
        help_text='Atualiza o preço de custo dos produtos ao finalizar'
    )
    atualizar_preco_venda = models.BooleanField(
        default=False,
        verbose_name='Recalcular Preço de Venda',
        help_text='Recalcula o preço de venda baseado na margem ao finalizar'
    )
    margem_padrao = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('50.00'),
        verbose_name='Margem Padrão (%)',
        help_text='Margem de lucro para recalcular preço de venda'
    )
    ratear_frete = models.BooleanField(
        default=True,
        verbose_name='Ratear Frete no Custo',
        help_text='Inclui o frete proporcional no custo de cada item'
    )
    atualizar_cotacao = models.BooleanField(
        default=True,
        verbose_name='Atualizar Cotação do Fornecedor',
        help_text='Cria/atualiza cotação do fornecedor com os preços da NF'
    )
    
    # ========== AUDITORIA ==========
    usuario_cadastro = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='nf_entrada_cadastradas',
        verbose_name='Usuário Cadastro'
    )
    usuario_conferencia = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nf_entrada_conferidas',
        verbose_name='Usuário Conferência'
    )
    usuario_finalizacao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nf_entrada_finalizadas',
        verbose_name='Usuário Finalização'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota Fiscal de Entrada'
        verbose_name_plural = 'Notas Fiscais de Entrada'
        ordering = ['-data_entrada', '-created_at']
        unique_together = ['numero_nf', 'serie', 'fornecedor']
    
    def __str__(self):
        return f"NF {self.numero_nf}/{self.serie} - {self.fornecedor.nome_fantasia}"
    
    @property
    def total_itens(self):
        """Retorna o total de itens da nota"""
        return self.itens.count()
    
    @property
    def itens_conferidos(self):
        """Retorna quantidade de itens já conferidos"""
        return self.itens.filter(conferido=True).count()
    
    @property
    def itens_vinculados(self):
        """Retorna quantidade de itens vinculados a produtos"""
        return self.itens.filter(produto__isnull=False).count()
    
    @property
    def itens_pendentes(self):
        """Retorna quantidade de itens não vinculados"""
        return self.itens.filter(produto__isnull=True).count()
    
    @property
    def percentual_conferencia(self):
        """Retorna percentual de conferência"""
        total = self.total_itens
        if total == 0:
            return 0
        return round((self.itens_conferidos / total) * 100, 1)
    
    @property
    def pode_finalizar(self):
        """Verifica se a nota pode ser finalizada"""
        # Todos os itens devem estar conferidos e vinculados
        return (
            self.status in ['P', 'E', 'C'] and
            self.itens_pendentes == 0 and
            self.total_itens > 0
        )
    
    def calcular_totais(self):
        """Recalcula os totais da nota baseado nos itens"""
        from django.db.models import Sum
        
        totais = self.itens.aggregate(
            total_produtos=Sum('valor_total')
        )
        
        self.valor_produtos = totais['total_produtos'] or Decimal('0.00')
        self.valor_total = (
            self.valor_produtos +
            self.valor_frete +
            self.valor_seguro +
            self.valor_outras_despesas +
            self.valor_ipi +
            self.valor_icms_st -
            self.valor_desconto
        )
        self.save()


class ItemNotaEntrada(models.Model):
    """
    Item da Nota Fiscal de Entrada
    
    Cada item representa um produto da nota que pode:
    - Ser vinculado a um produto existente
    - Cadastrar um novo produto
    - Atualizar estoque e preços
    """
    
    nota = models.ForeignKey(
        NotaFiscalEntrada,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Nota Fiscal'
    )
    
    # ========== VÍNCULO COM PRODUTO DO SISTEMA ==========
    produto = models.ForeignKey(
        'estoque.Produto',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='entradas',
        verbose_name='Produto Vinculado',
        help_text='Produto do sistema vinculado a este item'
    )
    
    # ========== DADOS DO XML/NF ==========
    numero_item = models.IntegerField(
        default=1,
        verbose_name='Nº Item'
    )
    codigo_produto_fornecedor = models.CharField(
        max_length=60,
        verbose_name='Código do Fornecedor',
        help_text='Código do produto no fornecedor'
    )
    codigo_barras_nf = models.CharField(
        max_length=14,
        blank=True,
        default='',
        verbose_name='Código de Barras (NF)',
        help_text='EAN/GTIN da nota fiscal'
    )
    descricao_nf = models.CharField(
        max_length=120,
        verbose_name='Descrição na NF'
    )
    ncm = models.CharField(
        max_length=10,
        blank=True,
        default='',
        verbose_name='NCM'
    )
    cest = models.CharField(
        max_length=7,
        blank=True,
        default='',
        verbose_name='CEST'
    )
    cfop = models.CharField(
        max_length=4,
        blank=True,
        default='',
        verbose_name='CFOP'
    )
    unidade = models.CharField(
        max_length=6,
        default='UN',
        verbose_name='Unidade'
    )
    
    # ========== QUANTIDADES ==========
    quantidade = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))],
        verbose_name='Quantidade NF'
    )
    quantidade_conferida = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('0.0000'),
        verbose_name='Qtd Conferida'
    )
    
    # ========== VALORES ==========
    valor_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000'))],
        verbose_name='Valor Unitário'
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Total'
    )
    valor_desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Desconto'
    )
    
    # ========== IMPOSTOS ==========
    valor_ipi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='IPI'
    )
    valor_icms_st = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='ICMS ST'
    )
    
    # ========== CUSTO CALCULADO ==========
    valor_custo_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('0.0000'),
        verbose_name='Custo Unitário',
        help_text='Custo com rateio de frete/impostos'
    )
    
    # ========== STATUS DO ITEM ==========
    conferido = models.BooleanField(
        default=False,
        verbose_name='Conferido'
    )
    divergencia = models.BooleanField(
        default=False,
        verbose_name='Com Divergência',
        help_text='Quantidade conferida difere da NF'
    )
    observacao = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Observação'
    )
    
    # ========== AUDITORIA ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item da Nota de Entrada'
        verbose_name_plural = 'Itens da Nota de Entrada'
        ordering = ['numero_item']
    
    def __str__(self):
        return f"{self.numero_item} - {self.descricao_nf[:50]}"
    
    def save(self, *args, **kwargs):
        # Calcula valor total se não informado
        if not self.valor_total:
            self.valor_total = self.quantidade * self.valor_unitario - self.valor_desconto
        super().save(*args, **kwargs)
    
    def calcular_custo_unitario(self):
        """
        Calcula o custo unitário com rateio de frete e impostos
        """
        nota = self.nota
        
        # Valor base do item
        custo = self.valor_unitario
        
        # Adiciona impostos proporcionais
        custo += (self.valor_ipi / self.quantidade) if self.quantidade > 0 else 0
        custo += (self.valor_icms_st / self.quantidade) if self.quantidade > 0 else 0
        
        # Rateia frete se configurado
        if nota.ratear_frete and nota.valor_frete > 0 and nota.valor_produtos > 0:
            proporcao = self.valor_total / nota.valor_produtos
            frete_item = nota.valor_frete * proporcao
            custo += (frete_item / self.quantidade) if self.quantidade > 0 else 0
        
        self.valor_custo_unitario = Decimal(str(round(custo, 4)))
        self.save()
        
        return self.valor_custo_unitario
    
    def vincular_produto_automatico(self):
        """
        Tenta vincular automaticamente a um produto do sistema
        Busca por: código de barras, código, referência
        """
        from estoque.models import Produto
        
        # Já está vinculado
        if self.produto:
            return self.produto
        
        produto = None
        
        # 1. Busca por código de barras
        if self.codigo_barras_nf:
            produto = Produto.objects.filter(
                codigo_barras=self.codigo_barras_nf,
                ativo=True
            ).first()
        
        # 2. Busca por código do fornecedor (pode estar no código do produto)
        if not produto and self.codigo_produto_fornecedor:
            produto = Produto.objects.filter(
                codigo=self.codigo_produto_fornecedor,
                ativo=True
            ).first()
            
            # Tenta também pela referência do fabricante
            if not produto:
                produto = Produto.objects.filter(
                    referencia_fabricante=self.codigo_produto_fornecedor,
                    ativo=True
                ).first()
        
        # 3. Busca por descrição similar (último recurso)
        if not produto:
            # Remove caracteres especiais e busca
            descricao_limpa = ''.join(e for e in self.descricao_nf if e.isalnum() or e.isspace())
            palavras = descricao_limpa.split()[:3]  # Primeiras 3 palavras
            
            if palavras:
                from django.db.models import Q
                query = Q()
                for palavra in palavras:
                    if len(palavra) > 3:  # Ignora palavras muito curtas
                        query &= Q(descricao__icontains=palavra)
                
                if query:
                    produtos = Produto.objects.filter(query, ativo=True)[:5]
                    if produtos.count() == 1:
                        produto = produtos.first()
        
        if produto:
            self.produto = produto
            self.save()
        
        return produto


class LogEntradaMercadoria(models.Model):
    """
    Log de operações realizadas na entrada de mercadoria
    """
    
    ACAO_CHOICES = [
        ('CRIAR', 'Nota Criada'),
        ('IMPORTAR_XML', 'XML Importado'),
        ('VINCULAR', 'Produto Vinculado'),
        ('DESVINCULAR', 'Produto Desvinculado'),
        ('CONFERIR', 'Item Conferido'),
        ('CADASTRAR_PRODUTO', 'Produto Cadastrado'),
        ('FINALIZAR', 'Entrada Finalizada'),
        ('CANCELAR', 'Entrada Cancelada'),
        ('ATUALIZAR_ESTOQUE', 'Estoque Atualizado'),
        ('ATUALIZAR_PRECO', 'Preço Atualizado'),
        ('ATUALIZAR_COTACAO', 'Cotação Atualizada'),
    ]
    
    nota = models.ForeignKey(
        NotaFiscalEntrada,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='Nota Fiscal'
    )
    item = models.ForeignKey(
        ItemNotaEntrada,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Item'
    )
    acao = models.CharField(
        max_length=20,
        choices=ACAO_CHOICES,
        verbose_name='Ação'
    )
    descricao = models.TextField(
        verbose_name='Descrição'
    )
    dados_json = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Dados Adicionais'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Entrada'
        verbose_name_plural = 'Logs de Entrada'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_acao_display()} - {self.nota.numero_nf}"
