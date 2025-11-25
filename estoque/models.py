from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone


# ==========================================
# MODELO: FABRICANTE
# ==========================================
class Fabricante(models.Model):
    """Fabricante de peças automotivas"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    pais_origem = models.CharField(max_length=50, blank=True, null=True, verbose_name='País de Origem')
    site = models.URLField(blank=True, null=True, verbose_name='Website')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ==========================================
# MODELO: CATEGORIA E SUBCATEGORIA
# ==========================================
class Categoria(models.Model):
    """Categoria de produtos"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    icone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ícone',
                             help_text='Nome do ícone (ex: gear, car-front)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Subcategoria(models.Model):
    """Subcategoria de produtos"""
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias', verbose_name='Categoria', blank=True, null=True)
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['categoria__nome', 'nome']
        unique_together = ['categoria', 'nome']

    def __str__(self):
        return f"{self.categoria.nome} > {self.nome}"


# ==========================================
# MODELO: APLICACAO (COMPATIBILIDADE)
# ==========================================
class Aplicacao(models.Model):
    """Aplicação/Compatibilidade do produto (veículos compatíveis)"""
    marca = models.CharField(max_length=50, verbose_name='Marca do Veículo')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    ano_inicial = models.IntegerField(verbose_name='Ano Inicial')
    ano_final = models.IntegerField(verbose_name='Ano Final', blank=True, null=True,
                                    help_text='Deixe em branco se ainda está em fabricação')
    motor = models.CharField(max_length=50, blank=True, null=True, verbose_name='Motor')
    observacoes = models.CharField(max_length=200, blank=True, null=True, verbose_name='Observações')

    class Meta:
        verbose_name = 'Aplicação'
        verbose_name_plural = 'Aplicações'
        ordering = ['marca', 'modelo', 'ano_inicial']

    def __str__(self):
        ano_str = f"{self.ano_inicial}"
        if self.ano_final:
            ano_str += f" a {self.ano_final}"
        else:
            ano_str += " em diante"

        motor_str = f" - {self.motor}" if self.motor else ""
        return f"{self.marca} {self.modelo} ({ano_str}){motor_str}"


# ==========================================
# MODELO: FORNECEDOR (COMPLETO)
# ==========================================
class Fornecedor(models.Model):
    """Fornecedor de produtos - versão completa"""
    nome_fantasia = models.CharField(max_length=100, verbose_name='Nome Fantasia')
    razao_social = models.CharField(max_length=200, blank=True, null=True, verbose_name='Razão Social')
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name='CNPJ')
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True, verbose_name='Inscrição Estadual')

    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name='Celular')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    site = models.URLField(blank=True, null=True, verbose_name='Site')
    contato_principal = models.CharField(max_length=100, blank=True, null=True, verbose_name='Contato Principal')

    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP')
    logradouro = models.CharField(max_length=200, blank=True, null=True, verbose_name='Logradouro')
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estado')

    # Condições comerciais
    FORMA_PAGAMENTO_CHOICES = [
        ('AVISTA', 'À Vista'),
        ('7DD', '7 Dias'),
        ('14DD', '14 Dias'),
        ('21DD', '21 Dias'),
        ('28DD', '28 Dias'),
        ('30DD', '30 Dias'),
        ('60DD', '60 Dias'),
        ('90DD', '90 Dias'),
        ('OUTROS', 'Outros'),
    ]

    forma_pagamento_padrao = models.CharField(
        max_length=10,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='30DD',
        verbose_name='Forma Pagamento Padrão'
    )

    prazo_entrega_dias = models.IntegerField(default=0, verbose_name='Prazo de Entrega (dias)')
    pedido_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Pedido Mínimo')
    frete_gratis_acima = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name='Frete Grátis Acima de'
    )

    # Dados bancários
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Banco')
    agencia = models.CharField(max_length=20, blank=True, null=True, verbose_name='Agência')
    conta = models.CharField(max_length=20, blank=True, null=True, verbose_name='Conta')
    pix = models.CharField(max_length=100, blank=True, null=True, verbose_name='Chave PIX')

    # Avaliação
    CLASSIFICACAO_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ Excelente'),
        (4, '⭐⭐⭐⭐ Muito Bom'),
        (3, '⭐⭐⭐ Bom'),
        (2, '⭐⭐ Regular'),
        (1, '⭐ Ruim'),
    ]
    classificacao = models.IntegerField(
        choices=CLASSIFICACAO_CHOICES,
        default=3,
        verbose_name='Classificação'
    )

    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    # Controle
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome_fantasia']

    def __str__(self):
        return self.nome_fantasia

    def get_classificacao_display_stars(self):
        return '⭐' * (self.classificacao or 0)


# ==========================================
# MODELO: PRODUTO (COMPLETO)
# ==========================================
# ==========================================
# MODELO: PRODUTO (CORRIGIDO)
# ✅ APENAS 'descricao' É OBRIGATÓRIO
# ✅ Todos os outros campos são opcionais com valores default
# ==========================================
# ==========================================
# MODELO: PRODUTO (CORRIGIDO)
# ✅ APENAS 'descricao' É OBRIGATÓRIO
# ✅ Todos os outros campos são opcionais com valores default
# ==========================================
class Produto(models.Model):
    """
    Produto de autopeças com informações completas
    ✅ CORRIGIDO: Apenas 'descricao' é obrigatório
    ✅ Todos os outros campos têm blank=True, null=True ou default
    """

    # ========== IDENTIFICAÇÃO ==========
    # ✅ Código: opcional, será gerado automaticamente se vazio
    codigo = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,  # ✅ Permite vazio no form
        verbose_name='Código Interno'
    )
    
    codigo_sku = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        null=True,  # ✅ Permite NULL no banco
        verbose_name='Código SKU'
    )
    
    codigo_barras = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='Código de Barras/EAN'
    )
    
    referencia_fabricante = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Referência do Fabricante'
    )

    # ========== DESCRIÇÃO ==========
    # ⚠️ ÚNICO CAMPO OBRIGATÓRIO
    descricao = models.CharField(
        max_length=200, 
        verbose_name='Descrição'
        # Sem blank=True, null=True = OBRIGATÓRIO
    )
    
    descricao_detalhada = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Descrição Detalhada'
    )

    # ========== CATEGORIZAÇÃO ==========
    # ✅ Todos opcionais com SET_NULL
    categoria = models.ForeignKey(
        'Categoria', 
        on_delete=models.SET_NULL,  # ✅ Mudado de PROTECT para SET_NULL
        blank=True,
        null=True,
        related_name='produtos', 
        verbose_name='Categoria'
    )
    
    subcategoria = models.ForeignKey(
        'Subcategoria', 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name='produtos', 
        verbose_name='Subcategoria'
    )

    # ========== RELACIONAMENTOS ==========
    fabricante = models.ForeignKey(
        'Fabricante', 
        on_delete=models.SET_NULL,  # ✅ Mudado de PROTECT para SET_NULL
        blank=True,
        null=True,
        related_name='produtos', 
        verbose_name='Fabricante'
    )
    
    fornecedor_principal = models.ForeignKey(
        'Fornecedor', 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name='produtos_principal',
        verbose_name='Fornecedor Principal',
        help_text='Fornecedor com melhor preço atual'
    )
    
    fornecedores_alternativos = models.ManyToManyField(
        'Fornecedor', 
        blank=True,
        related_name='produtos_alternativos',
        verbose_name='Fornecedores Alternativos'
    )

    # ========== LOCALIZAÇÃO NO ESTOQUE ==========
    LOJA_CHOICES = [
        ('1', 'Loja 1'),
        ('2', 'Loja 2'),
    ]
    loja = models.CharField(
        max_length=1, 
        choices=LOJA_CHOICES, 
        default='1',  # ✅ Valor default
        blank=True,
        verbose_name='Loja'
    )
    
    setor = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        default='',  # ✅ Valor default vazio
        verbose_name='Setor'
    )
    
    PRATELEIRA_CHOICES = [
        ('', 'Não definida'),
        ('A', 'Prateleira A'),
        ('B', 'Prateleira B'),
        ('C', 'Prateleira C'),
        ('D', 'Prateleira D'),
        ('E', 'Prateleira E'),
        ('F', 'Prateleira F'),
        ('G', 'Prateleira G'),
        ('H', 'Prateleira H'),
    ]
    prateleira = models.CharField(
        max_length=1, 
        choices=PRATELEIRA_CHOICES, 
        blank=True, 
        null=True,
        default='',
        verbose_name='Prateleira'
    )
    
    divisao_prateleira = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        default='',
        verbose_name='Divisão/Gaveta'
    )

    # ========== PREÇOS ==========
    # ✅ Todos com default=0
    preco_custo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),  # ✅ Default 0
        blank=True,
        null=True,
        verbose_name='Preço de Custo'
    )
    
    preco_venda_dinheiro = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        blank=True,
        null=True,
        verbose_name='Preço à Vista (Dinheiro)'
    )
    
    preco_venda_debito = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Preço no Débito'
    )
    
    preco_venda_credito = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Preço no Crédito'
    )
    
    preco_atacado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Preço Atacado'
    )
    
    quantidade_minima_atacado = models.IntegerField(
        default=10,
        blank=True,
        null=True,
        verbose_name='Qtd Mínima p/ Atacado'
    )
    
    preco_promocional = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Preço Promocional'
    )

    # ========== ESTOQUE ==========
    # ✅ Todos com default=0
    estoque_atual = models.IntegerField(
        default=0,  # ✅ Default 0
        blank=True,
        verbose_name='Estoque Atual'
    )
    
    estoque_reservado = models.IntegerField(
        default=0,
        blank=True,
        verbose_name='Estoque Reservado'
    )
    
    estoque_minimo = models.IntegerField(
        default=0,
        blank=True,
        verbose_name='Estoque Mínimo'
    )
    
    estoque_maximo = models.IntegerField(
        default=0,
        blank=True,
        verbose_name='Estoque Máximo'
    )
    
    quantidade_reposicao = models.IntegerField(
        default=0,
        blank=True,
        verbose_name='Qtd Sugerida para Reposição'
    )

    # ========== APLICAÇÃO/COMPATIBILIDADE (NOVO SISTEMA) ==========
    # ✅ ManyToMany para versões de veículos - opcional
    versoes_compativeis = models.ManyToManyField(
        'VeiculoVersao',
        blank=True,
        related_name='produtos',
        verbose_name='Versões Compatíveis',
        help_text='Selecione todas as versões de veículos compatíveis'
    )
    
    # Campo texto livre para aplicação genérica
    aplicacao_generica = models.TextField(
        blank=True, 
        null=True,
        default='',
        verbose_name='Aplicação Genérica',
        help_text='Texto livre para descrever compatibilidade'
    )

    # ========== CARACTERÍSTICAS FÍSICAS ==========
    # ✅ Todos opcionais com default
    peso = models.DecimalField(
        max_digits=8, 
        decimal_places=3, 
        blank=True, 
        null=True,
        default=Decimal('0.000'),
        verbose_name='Peso (kg)'
    )
    
    comprimento = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Comprimento (cm)'
    )
    
    largura = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Largura (cm)'
    )
    
    altura = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        default=Decimal('0.00'),
        verbose_name='Altura (cm)'
    )

    # ========== INFORMAÇÕES COMERCIAIS ==========
    ncm = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        default='',
        verbose_name='NCM'
    )
    
    UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('PC', 'Peça'),
        ('CJ', 'Conjunto'),
        ('KIT', 'Kit'),
        ('PAR', 'Par'),
        ('JG', 'Jogo'),
        ('CX', 'Caixa'),
        ('MT', 'Metro'),
        ('LT', 'Litro'),
        ('KG', 'Quilograma'),
    ]
    unidade_medida = models.CharField(
        max_length=5, 
        choices=UNIDADE_CHOICES, 
        default='UN',
        blank=True,
        verbose_name='Unidade de Medida'
    )
    
    garantia_meses = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='Garantia (meses)'
    )

    # ========== STATUS E PROMOÇÕES ==========
    ativo = models.BooleanField(
        default=True,  # ✅ Default True
        verbose_name='Produto Ativo'
    )
    
    destaque = models.BooleanField(
        default=False,
        verbose_name='Em Destaque'
    )
    
    promocao = models.BooleanField(
        default=False,
        verbose_name='Em Promoção'
    )

    # ========== MÍDIA ==========
    imagem = models.ImageField(
        upload_to='produtos/', 
        blank=True, 
        null=True,
        verbose_name='Imagem Principal'
    )


    # ========== CONFIGURAÇÃO DE IMPOSTOS E PREÇOS CUSTOMIZADOS ==========
    aplicar_imposto_4 = models.BooleanField(
        default=False,
        verbose_name='Aplicar Imposto 4% (Simples Nacional)',
        help_text='Marca se este produto deve ter 4% de imposto incluído no preço final'
    )

    preco_customizado_cartao = models.BooleanField(
        default=False,
        verbose_name='Usar Preços Customizados no Cartão',
        help_text='Se marcado, você define preços manualmente por parcela. Se desmarcado, usa taxa automática.'
    )

    # Preços customizados para cartão de crédito parcelado
    preco_credito_2x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 2x',
        help_text='Preço customizado para 2 parcelas'
    )

    preco_credito_3x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 3x'
    )

    preco_credito_4x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 4x'
    )

    preco_credito_5x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 5x'
    )

    preco_credito_6x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 6x'
    )

    preco_credito_7x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 7x'
    )

    preco_credito_8x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 8x'
    )

    preco_credito_9x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 9x'
    )

    preco_credito_10x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 10x'
    )

    preco_credito_11x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 11x'
    )

    preco_credito_12x = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Crédito 12x'
    )

    # ========== OBSERVAÇÕES ==========
    observacoes = models.TextField(
        blank=True, 
        null=True,
        default='',
        verbose_name='Observações'
    )

    # ========== CONTROLE ==========
    data_cadastro = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Data de Cadastro'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True, 
        verbose_name='Última Atualização'
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['codigo_sku']),
            models.Index(fields=['codigo_barras']),
            models.Index(fields=['categoria', 'subcategoria']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.descricao}" if self.codigo else self.descricao

    def save(self, *args, **kwargs):
        """
        Override save para:
        1. Gerar código automaticamente se vazio
        2. Garantir valores default para campos numéricos
        """
        # Gerar código se não informado
        if not self.codigo:
            ultimo_produto = Produto.objects.order_by('-id').first()
            if ultimo_produto:
                try:
                    # Tenta extrair número do último código
                    ultimo_num = int(''.join(filter(str.isdigit, ultimo_produto.codigo or '0')))
                    self.codigo = str(ultimo_num + 1).zfill(6)
                except ValueError:
                    self.codigo = str(Produto.objects.count() + 1).zfill(6)
            else:
                self.codigo = '000001'
        
        # Garantir valores default para campos numéricos
        if self.preco_custo is None:
            self.preco_custo = Decimal('0.00')
        if self.preco_venda_dinheiro is None:
            self.preco_venda_dinheiro = Decimal('0.00')
        if self.estoque_atual is None:
            self.estoque_atual = 0
        if self.estoque_minimo is None:
            self.estoque_minimo = 0
        if self.estoque_maximo is None:
            self.estoque_maximo = 0
        
        super().save(*args, **kwargs)

    # ========== PROPRIEDADES CALCULADAS ==========
    @property
    def estoque_disponivel(self):
        """Estoque disponível para venda"""
        return max(0, (self.estoque_atual or 0) - (self.estoque_reservado or 0))
    
    @property
    def margem_lucro_dinheiro(self):
        """Margem de lucro à vista"""
        if self.preco_custo and self.preco_custo > 0 and self.preco_venda_dinheiro:
            return round(((self.preco_venda_dinheiro - self.preco_custo) / self.preco_custo) * 100, 2)
        return 0
    
    @property
    def margem_lucro_credito(self):
        """Margem de lucro no crédito"""
        if self.preco_custo and self.preco_custo > 0 and self.preco_venda_credito:
            return round(((self.preco_venda_credito - self.preco_custo) / self.preco_custo) * 100, 2)
        return 0
    
    @property
    def situacao_estoque(self):
        """Retorna situação do estoque"""
        if (self.estoque_atual or 0) <= 0:
            return 'zerado'
        elif (self.estoque_atual or 0) <= (self.estoque_minimo or 0):
            return 'critico'
        elif (self.estoque_atual or 0) <= ((self.estoque_minimo or 0) * 2):
            return 'baixo'
        else:
            return 'normal'
    
    @property
    def localizacao_completa(self):
        """Retorna localização formatada"""
        partes = []
        if self.loja:
            partes.append(f"Loja {self.loja}")
        if self.setor:
            partes.append(self.setor)
        if self.prateleira:
            partes.append(f"Prat. {self.prateleira}")
        if self.divisao_prateleira:
            partes.append(self.divisao_prateleira)
        return ' / '.join(partes) if partes else 'Não definida'
    
    def get_preco_cartao(self, tipo='CREDITO', parcelas=1):
        """
        Retorna o preço para venda no cartão considerando:
        - Preços customizados (se configurado)
        - Taxas automáticas da tabela TaxaCartao
        - Imposto de 4% (se aplicável)
        """
        from financeiro.models import TaxaCartao
        
        # Se for PIX, retorna preço dinheiro (sem taxa)
        if tipo == 'PIX':
            preco_base = self.preco_venda_dinheiro or Decimal('0.00')
            if self.aplicar_imposto_4:
                preco_base = preco_base * Decimal('1.04')
            return preco_base
        
        # Se for DÉBITO
        if tipo == 'DEBITO':
            if self.preco_venda_debito and self.preco_venda_debito > 0:
                preco_base = self.preco_venda_debito
            else:
                preco_base = self.preco_venda_dinheiro or Decimal('0.00')
                taxa = TaxaCartao.get_taxa('DEBITO', 1)
                preco_base = preco_base * (Decimal('1') + (taxa / Decimal('100')))
            
            if self.aplicar_imposto_4:
                preco_base = preco_base * Decimal('1.04')
            
            return preco_base
        
        # Se for CRÉDITO
        if tipo == 'CREDITO':
            # Verifica se tem preço customizado
            if self.preco_customizado_cartao and parcelas >= 2:
                campo_preco = f'preco_credito_{parcelas}x'
                preco_customizado = getattr(self, campo_preco, None)
                
                if preco_customizado and preco_customizado > 0:
                    preco_base = preco_customizado
                    if self.aplicar_imposto_4:
                        preco_base = preco_base * Decimal('1.04')
                    return preco_base
            
            # Calcula automaticamente
            if parcelas == 1:
                if self.preco_venda_credito and self.preco_venda_credito > 0:
                    preco_base = self.preco_venda_credito
                else:
                    preco_base = self.preco_venda_dinheiro or Decimal('0.00')
                    taxa = TaxaCartao.get_taxa('CREDITO', 1)
                    preco_base = preco_base * (Decimal('1') + (taxa / Decimal('100')))
            else:
                preco_base = self.preco_venda_dinheiro or Decimal('0.00')
                taxa = TaxaCartao.get_taxa('CREDITO', parcelas)
                preco_base = preco_base * (Decimal('1') + (taxa / Decimal('100')))
            
            if self.aplicar_imposto_4:
                preco_base = preco_base * Decimal('1.04')
            
            return preco_base
        
        return Decimal('0.00')


    def get_todos_precos_cartao(self):
        """
        Retorna dicionário com todos os preços possíveis
        """
        return {
            'pix': self.get_preco_cartao('PIX', 1),
            'dinheiro': self.preco_venda_dinheiro or Decimal('0.00'),
            'debito': self.get_preco_cartao('DEBITO', 1),
            'credito': {
                parcela: self.get_preco_cartao('CREDITO', parcela)
                for parcela in range(1, 13)
            }
        }


    def calcular_lucro_liquido(self, preco_venda, tipo_pagamento='PIX', parcelas=1):
        """
        Calcula lucro líquido considerando taxas e imposto
        """
        from financeiro.models import TaxaCartao
        
        preco_venda = Decimal(str(preco_venda))
        preco_custo = self.preco_custo or Decimal('0.00')
        
        taxa_cartao_percentual = Decimal('0.00')
        valor_taxa_cartao = Decimal('0.00')
        imposto_4_percentual = Decimal('4.00') if self.aplicar_imposto_4 else Decimal('0.00')
        valor_imposto_4 = Decimal('0.00')
        
        # Taxa do cartão
        if tipo_pagamento in ['DEBITO', 'CREDITO']:
            taxa_cartao_percentual = TaxaCartao.get_taxa(tipo_pagamento, parcelas)
            valor_taxa_cartao = preco_venda * (taxa_cartao_percentual / Decimal('100'))
        
        # Imposto 4%
        if self.aplicar_imposto_4:
            base_imposto = preco_venda - valor_taxa_cartao
            valor_imposto_4 = base_imposto * Decimal('0.04')
        
        # Lucros
        lucro_bruto = preco_venda - preco_custo
        lucro_liquido = preco_venda - preco_custo - valor_taxa_cartao - valor_imposto_4
        
        margem_liquida = Decimal('0.00')
        if preco_custo > 0:
            margem_liquida = (lucro_liquido / preco_custo) * Decimal('100')
        
        return {
            'preco_venda': preco_venda,
            'preco_custo': preco_custo,
            'taxa_cartao_percentual': taxa_cartao_percentual,
            'valor_taxa_cartao': valor_taxa_cartao,
            'imposto_4_percentual': imposto_4_percentual,
            'valor_imposto_4': valor_imposto_4,
            'lucro_bruto': lucro_bruto,
            'lucro_liquido': lucro_liquido,
            'margem_liquida': margem_liquida
        }


    def preencher_precos_automaticos(self):
        """
        Preenche automaticamente preços de débito e crédito
        """
        from financeiro.models import TaxaCartao
        
        if not self.preco_venda_dinheiro or self.preco_venda_dinheiro <= 0:
            return
        
        taxa_debito = TaxaCartao.get_taxa('DEBITO', 1)
        self.preco_venda_debito = self.preco_venda_dinheiro * (Decimal('1') + (taxa_debito / Decimal('100')))
        
        taxa_credito_1x = TaxaCartao.get_taxa('CREDITO', 1)
        self.preco_venda_credito = self.preco_venda_dinheiro * (Decimal('1') + (taxa_credito_1x / Decimal('100')))
        
        if not self.preco_customizado_cartao:
            for parcela in range(2, 13):
                setattr(self, f'preco_credito_{parcela}x', None)
        
        
    def get_aplicacoes_formatadas(self):
        """Retorna lista de aplicações formatadas"""
        aplicacoes = []
        for versao in self.versoes_compativeis.all().select_related('modelo__montadora'):
            aplicacoes.append(str(versao))
        return aplicacoes
    

# ==========================================
# MODELO: COTAÇÃO DE FORNECEDOR
# ==========================================
class CotacaoFornecedor(models.Model):
    """Modelo para armazenar cotações de preços de fornecedores"""

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='cotacoes',
        verbose_name='Produto'
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        related_name='cotacoes',
        verbose_name='Fornecedor'
    )

    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')
    quantidade_minima = models.IntegerField(default=1, verbose_name='Quantidade Mínima')

    FORMA_PAGAMENTO_CHOICES = [
        ('AVISTA', 'À Vista'),
        ('7DD', '7 Dias'),
        ('14DD', '14 Dias'),
        ('21DD', '21 Dias'),
        ('28DD', '28 Dias'),
        ('30DD', '30 Dias'),
        ('60DD', '60 Dias'),
        ('90DD', '90 Dias'),
        ('OUTROS', 'Outros'),
    ]

    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES, default='30DD', verbose_name='Forma de Pagamento')
    prazo_entrega_dias = models.IntegerField(default=0, verbose_name='Prazo de Entrega (dias)')
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor do Frete')

    desconto_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True, verbose_name='Desconto (%)')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    numero_cotacao = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nº Cotação do Fornecedor')

    data_cotacao = models.DateField(default=timezone.now, verbose_name='Data da Cotação')
    validade_dias = models.IntegerField(default=30, verbose_name='Validade (dias)')
    ativo = models.BooleanField(default=True, verbose_name='Cotação Ativa')

    usuario_cadastro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Usuário')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Cotação de Fornecedor'
        verbose_name_plural = 'Cotações de Fornecedores'
        ordering = ['-data_cotacao', 'preco_unitario']
        unique_together = ['produto', 'fornecedor', 'data_cotacao']

    def __str__(self):
        return f"{self.produto.descricao} - {self.fornecedor.nome_fantasia} - R$ {self.preco_unitario}"

    def get_preco_total(self):
        """Calcula o preço total incluindo frete"""
        return self.preco_unitario + self.valor_frete

    def get_economia_percentual(self):
        """Calcula economia em relação ao preço de venda atual"""
        if self.produto.preco_venda_dinheiro and self.produto.preco_venda_dinheiro > Decimal('0.00'):
            economia = ((self.produto.preco_venda_dinheiro - self.preco_unitario) / self.produto.preco_venda_dinheiro) * 100
            return max(Decimal('0.00'), economia)
        return Decimal('0.00')

    def esta_valida(self):
        """Verifica se a cotação ainda está dentro do prazo de validade"""
        from datetime import timedelta
        data_validade = self.data_cotacao + timedelta(days=self.validade_dias)
        return timezone.now().date() <= data_validade and self.ativo

    def get_data_validade(self):
        """Retorna a data de validade da cotação"""
        from datetime import timedelta
        return self.data_cotacao + timedelta(days=self.validade_dias)


# ==========================================
# MODELO: MOVIMENTAÇÃO DE ESTOQUE
# ==========================================
class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('A', 'Ajuste'),
        ('D', 'Devolução'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes')
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)

    documento = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    usuario = models.CharField(max_length=100)
    data_movimentacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.descricao} - {self.quantidade}"


# ==========================================
# MODELO: HISTÓRICO DE PREÇOS
# ==========================================
class HistoricoPreco(models.Model):
    """Histórico de alterações de preço"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='historico_precos')
    preco_custo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo_novo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda_novo = models.DecimalField(max_digits=10, decimal_places=2)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    motivo = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Preço'
        verbose_name_plural = 'Históricos de Preços'
        ordering = ['-data_alteracao']

    def __str__(self):
        return f"{self.produto.codigo} - {self.data_alteracao.strftime('%d/%m/%Y %H:%M')}"


# ==========================================
# SISTEMA HIERÁRQUICO DE VEÍCULOS
# Montadora → Modelo → Versão
# ==========================================

class Montadora(models.Model):
    """Montadoras que operam no Brasil"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Montadora')
    pais_origem = models.CharField(max_length=50, verbose_name='País de Origem')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    logo = models.ImageField(upload_to='montadoras/', blank=True, null=True, verbose_name='Logo')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Montadora'
        verbose_name_plural = 'Montadoras'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class VeiculoModelo(models.Model):
    """Modelo de veículo (ex: Gol, Onix, Uno)"""
    montadora = models.ForeignKey(Montadora, on_delete=models.CASCADE, 
                                  related_name='modelos', verbose_name='Montadora')
    nome = models.CharField(max_length=100, verbose_name='Modelo')
    
    TIPO_CHOICES = [
        ('HATCH', 'Hatchback'),
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV/Crossover'),
        ('PICKUP', 'Picape'),
        ('VAN', 'Van/Utilitário'),
        ('WAGON', 'Station Wagon'),
        ('SPORT', 'Esportivo'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='HATCH', verbose_name='Tipo')
    
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    popular = models.BooleanField(default=False, verbose_name='Modelo Popular')
    imagem = models.ImageField(upload_to='veiculos/', blank=True, null=True, verbose_name='Imagem')
    
    class Meta:
        verbose_name = 'Modelo de Veículo'
        verbose_name_plural = 'Modelos de Veículos'
        ordering = ['montadora__nome', 'nome']
        unique_together = ['montadora', 'nome']
    
    def __str__(self):
        return f"{self.montadora.nome} {self.nome}"


class VeiculoVersao(models.Model):
    """Versão específica de um modelo (ex: Gol G5, Gol G6)"""
    modelo = models.ForeignKey(VeiculoModelo, on_delete=models.CASCADE,
                              related_name='versoes', verbose_name='Modelo')
    nome = models.CharField(max_length=100, verbose_name='Versão')
    ano_inicial = models.IntegerField(verbose_name='Ano Inicial')
    ano_final = models.IntegerField(blank=True, null=True, verbose_name='Ano Final')
    motorizacoes = models.CharField(max_length=200, verbose_name='Motorizações')
    codigo_fipe = models.CharField(max_length=20, blank=True, null=True, verbose_name='Código FIPE')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Versão do Veículo'
        verbose_name_plural = 'Versões dos Veículos'
        ordering = ['modelo__montadora__nome', 'modelo__nome', '-ano_inicial', 'nome']
        unique_together = ['modelo', 'nome', 'ano_inicial']
    
    def __str__(self):
        ano_str = f"{self.ano_inicial}"
        if self.ano_final:
            ano_str += f"-{self.ano_final}"
        else:
            ano_str += "+"
        return f"{self.modelo.montadora.nome} {self.modelo.nome} {self.nome} ({ano_str})"
    
    def get_anos_range(self):
        """Retorna o range de anos formatado"""
        if self.ano_final:
            return f"{self.ano_inicial}-{self.ano_final}"
        else:
            return f"{self.ano_inicial}+"
    
    def get_descricao_completa(self):
        """Retorna descrição completa formatada"""
        ano = f"{self.ano_inicial}"
        if self.ano_final:
            ano += f"-{self.ano_final}"
        else:
            ano += " em diante"
        return f"{self.nome} ({ano}) - {self.motorizacoes}"


# ==========================================
# COLE ESTE CÓDIGO NO FINAL DE estoque/models.py
# ==========================================

# DADOS DAS MONTADORAS
MONTADORAS_BRASIL = [
    ('Volkswagen', 'Alemanha', 1),
    ('Chevrolet', 'EUA', 2),
    ('Fiat', 'Itália', 3),
    ('Ford', 'EUA', 4),
    ('Renault', 'França', 5),
    ('Toyota', 'Japão', 6),
    ('Honda', 'Japão', 7),
    ('Hyundai', 'Coreia do Sul', 8),
    ('Nissan', 'Japão', 9),
    ('Peugeot', 'França', 10),
]

# DADOS DOS VEÍCULOS - Estrutura: Montadora → {(Modelo, Tipo, Popular): [Versões]}
VEICULOS_DETALHADOS_BRASIL = {
    'Volkswagen': {
        ('Gol', 'HATCH', True): [
            ('G4', 2006, 2008, '1.0, 1.6 Power'),
            ('G5', 2008, 2012, '1.0, 1.6 Power'),
            ('G6', 2013, 2016, '1.0, 1.6'),
            ('G7', 2017, 2023, '1.0, 1.6 MSI'),
            ('G8', 2023, None, '1.0 TSI'),
        ],
        ('Voyage', 'SEDAN', True): [
            ('G5', 2008, 2012, '1.0, 1.6 Power'),
            ('G6', 2013, 2016, '1.0, 1.6'),
            ('G7', 2017, 2023, '1.0, 1.6 MSI'),
        ],
        ('Polo', 'HATCH', True): [
            ('Classic', 2002, 2014, '1.6, 2.0'),
            ('MPI', 2018, 2021, '1.6 MSI'),
            ('TSI', 2018, None, '1.0 TSI, 1.4 TSI'),
        ],
        ('Virtus', 'SEDAN', True): [
            ('Comfortline', 2018, None, '1.0 TSI, 1.6 MSI'),
            ('Highline', 2018, None, '1.0 TSI, 1.6 MSI'),
        ],
        ('Fox', 'HATCH', True): [
            ('1ª Geração', 2003, 2009, '1.0, 1.6'),
            ('2ª Geração', 2010, 2014, '1.0, 1.6'),
            ('3ª Geração', 2015, 2021, '1.0, 1.6'),
        ],
        ('Up!', 'HATCH', True): [
            ('MPI', 2014, 2017, '1.0 MPI'),
            ('TSI', 2018, None, '1.0 TSI'),
        ],
        ('T-Cross', 'SUV', True): [
            ('1ª Geração', 2019, 2023, '1.0 TSI, 1.4 TSI'),
            ('2ª Geração', 2024, None, '1.0 TSI 116cv'),
        ],
        ('Saveiro', 'PICKUP', True): [
            ('G5', 2009, 2013, '1.6'),
            ('G6', 2014, 2016, '1.6'),
            ('G7', 2017, 2023, '1.6 MSI'),
        ],
        ('Amarok', 'PICKUP', False): [
            ('1ª Geração', 2011, 2016, '2.0 TDI'),
            ('V6', 2017, 2022, '3.0 V6 TDI'),
        ],
    },
    
    'Chevrolet': {
        ('Onix', 'HATCH', True): [
            ('Joy', 2012, 2015, '1.0, 1.4'),
            ('1ª Geração', 2016, 2019, '1.0, 1.4'),
            ('2ª Geração', 2020, None, '1.0, 1.0 Turbo'),
        ],
        ('Onix Plus', 'SEDAN', True): [
            ('LT', 2020, None, '1.0, 1.0 Turbo'),
            ('Premier', 2020, None, '1.0 Turbo'),
        ],
        ('Prisma', 'SEDAN', True): [
            ('1ª Geração', 2006, 2012, '1.0, 1.4'),
            ('2ª Geração', 2013, 2019, '1.0, 1.4'),
        ],
        ('Celta', 'HATCH', True): [
            ('1ª Geração', 2000, 2006, '1.0, 1.4'),
            ('2ª Geração', 2007, 2015, '1.0, 1.4'),
        ],
        ('Cruze', 'SEDAN', False): [
            ('1ª Geração', 2011, 2016, '1.8'),
            ('2ª Geração', 2017, None, '1.4 Turbo'),
        ],
        ('Tracker', 'SUV', True): [
            ('1ª Geração', 2013, 2019, '1.8'),
            ('2ª Geração', 2020, None, '1.0 Turbo, 1.2 Turbo'),
        ],
        ('S10', 'PICKUP', False): [
            ('2ª Geração', 2012, 2023, '2.4, 2.8 Diesel'),
            ('3ª Geração', 2024, None, '2.8 Diesel'),
        ],
        ('Montana', 'PICKUP', True): [
            ('1ª Geração', 2011, 2020, '1.4'),
            ('2ª Geração', 2023, None, '1.2 Turbo'),
        ],
    },
    
    'Fiat': {
        ('Uno', 'HATCH', True): [
            ('Vivace', 2010, 2013, '1.0, 1.4'),
            ('Way', 2011, 2021, '1.0, 1.4'),
            ('Drive', 2016, 2021, '1.0, 1.3'),
        ],
        ('Palio', 'HATCH', True): [
            ('Fire', 1996, 2017, '1.0, 1.4'),
        ],
        ('Strada', 'PICKUP', True): [
            ('Working', 1998, 2020, '1.4'),
            ('Freedom', 2021, None, '1.3'),
        ],
        ('Argo', 'HATCH', True): [
            ('Drive', 2017, None, '1.0, 1.3'),
            ('Trekking', 2018, None, '1.3, 1.8'),
        ],
        ('Cronos', 'SEDAN', True): [
            ('Drive', 2018, None, '1.3'),
            ('Precision', 2018, None, '1.8'),
        ],
        ('Toro', 'PICKUP', False): [
            ('Freedom', 2016, None, '1.8, 2.0 Diesel'),
            ('Volcano', 2016, None, '2.0 Diesel'),
        ],
        ('Mobi', 'HATCH', True): [
            ('Easy', 2016, None, '1.0'),
            ('Like', 2016, None, '1.0'),
        ],
    },
    
    'Ford': {
        ('Ka', 'HATCH', True): [
            ('SE', 2014, 2021, '1.0, 1.5'),
            ('SEL', 2014, 2021, '1.5'),
        ],
        ('Ka Sedan', 'SEDAN', True): [
            ('SE', 2014, 2021, '1.0, 1.5'),
        ],
        ('EcoSport', 'SUV', True): [
            ('1ª Geração', 2003, 2012, '1.6, 2.0'),
            ('2ª Geração', 2013, 2022, '1.6, 2.0'),
        ],
        ('Ranger', 'PICKUP', False): [
            ('3ª Geração', 2013, 2022, '2.2 Diesel, 3.2 Diesel'),
            ('4ª Geração', 2023, None, '2.0 Bi-Turbo'),
        ],
    },
    
    'Renault': {
        ('Sandero', 'HATCH', True): [
            ('1ª Geração', 2007, 2014, '1.0, 1.6'),
            ('2ª Geração', 2015, 2021, '1.0, 1.6'),
        ],
        ('Logan', 'SEDAN', True): [
            ('1ª Geração', 2007, 2013, '1.0, 1.6'),
            ('2ª Geração', 2014, 2021, '1.0, 1.6'),
        ],
        ('Kwid', 'HATCH', True): [
            ('Zen', 2017, None, '1.0'),
            ('Intense', 2017, None, '1.0'),
        ],
        ('Duster', 'SUV', True): [
            ('1ª Geração', 2011, 2021, '1.6, 2.0'),
            ('2ª Geração', 2022, None, '1.6 CVT'),
        ],
        ('Captur', 'SUV', False): [
            ('1ª Geração', 2017, 2021, '1.6, 2.0'),
            ('2ª Geração', 2022, None, '1.6 CVT'),
        ],
    },
    
    'Toyota': {
        ('Corolla', 'SEDAN', False): [
            ('11ª Geração', 2015, 2019, '1.8, 2.0'),
            ('12ª Geração', 2020, None, '1.8 Hybrid, 2.0'),
        ],
        ('Yaris', 'HATCH', True): [
            ('XL', 2018, None, '1.3, 1.5'),
            ('XS', 2018, None, '1.5'),
        ],
        ('Etios', 'HATCH', True): [
            ('X', 2012, 2021, '1.3'),
            ('XS', 2012, 2021, '1.5'),
        ],
        ('Hilux', 'PICKUP', False): [
            ('7ª Geração', 2005, 2015, '3.0 Diesel'),
            ('8ª Geração', 2016, None, '2.8 Diesel'),
        ],
    },
    
    'Honda': {
        ('Civic', 'SEDAN', False): [
            ('9ª Geração', 2012, 2016, '2.0'),
            ('10ª Geração', 2017, 2021, '1.5 Turbo, 2.0'),
            ('11ª Geração', 2022, None, '2.0'),
        ],
        ('City', 'SEDAN', True): [
            ('5ª Geração', 2009, 2014, '1.5'),
            ('6ª Geração', 2015, 2020, '1.5'),
        ],
        ('Fit', 'HATCH', True): [
            ('2ª Geração', 2009, 2014, '1.4, 1.5'),
            ('3ª Geração', 2015, 2020, '1.5'),
        ],
        ('HR-V', 'SUV', True): [
            ('1ª Geração', 2015, 2021, '1.8'),
            ('2ª Geração', 2022, None, '1.5 Turbo'),
        ],
    },
    
    'Hyundai': {
        ('HB20', 'HATCH', True): [
            ('1ª Geração', 2012, 2019, '1.0, 1.6'),
            ('2ª Geração', 2020, None, '1.0, 1.0 Turbo'),
        ],
        ('HB20S', 'SEDAN', True): [
            ('1ª Geração', 2012, 2019, '1.0, 1.6'),
            ('2ª Geração', 2020, None, '1.0 Turbo'),
        ],
        ('Creta', 'SUV', True): [
            ('1ª Geração', 2017, 2021, '1.6, 2.0'),
            ('2ª Geração', 2022, None, '1.0 Turbo, 2.0'),
        ],
        ('Tucson', 'SUV', False): [
            ('3ª Geração', 2017, 2021, '1.6 Turbo'),
            ('4ª Geração', 2022, None, '1.6 Turbo, 2.0'),
        ],
    },
    
    'Nissan': {
        ('March', 'HATCH', True): [
            ('1ª Geração', 2011, 2018, '1.0, 1.6'),
        ],
        ('Versa', 'SEDAN', True): [
            ('1ª Geração', 2011, 2014, '1.6'),
            ('2ª Geração', 2015, None, '1.0, 1.6'),
        ],
        ('Kicks', 'SUV', True): [
            ('1ª Geração', 2016, None, '1.6'),
        ],
        ('Sentra', 'SEDAN', False): [
            ('7ª Geração', 2014, 2019, '2.0'),
            ('8ª Geração', 2020, None, '2.0 CVT'),
        ],
        ('Frontier', 'PICKUP', False): [
            ('2ª Geração', 2008, 2016, '2.5 Diesel'),
            ('3ª Geração', 2017, None, '2.3 Diesel'),
        ],
    },
    
    'Peugeot': {
        ('208', 'HATCH', True): [
            ('1ª Geração', 2013, 2019, '1.5, 1.6'),
            ('2ª Geração', 2020, None, '1.6'),
        ],
        ('2008', 'SUV', True): [
            ('1ª Geração', 2015, 2019, '1.6'),
            ('2ª Geração', 2020, None, '1.6 Turbo'),
        ],
        ('3008', 'SUV', False): [
            ('2ª Geração', 2018, None, '1.6 Turbo'),
        ],
    },
}


def popular_veiculos_expandidos():
    """
    Popula banco de dados com estrutura hierárquica completa
    Montadora → Modelo → Versões
    
    Execute no shell:
    >>> from estoque.models import popular_veiculos_expandidos
    >>> popular_veiculos_expandidos()
    """
    from django.db import transaction
    
    print("🚗 Iniciando população hierárquica de veículos...")
    print("   Estrutura: Montadora → Modelo → Versão\n")
    
    stats = {
        'montadoras': 0,
        'modelos': 0,
        'versoes': 0,
    }
    
    with transaction.atomic():
        # 1. Criar montadoras
        print("📋 Criando montadoras...")
        montadoras_dict = {}
        for nome, pais, ordem in MONTADORAS_BRASIL:
            montadora, created = Montadora.objects.get_or_create(
                nome=nome,
                defaults={'pais_origem': pais, 'ordem': ordem, 'ativa': True}
            )
            montadoras_dict[nome] = montadora
            if created:
                stats['montadoras'] += 1
                print(f"  ✓ {nome}")
        
        # 2. Criar modelos e versões
        print("\n🚙 Criando modelos e versões...")
        for montadora_nome, modelos_dict in VEICULOS_DETALHADOS_BRASIL.items():
            if montadora_nome not in montadoras_dict:
                continue
            
            montadora = montadoras_dict[montadora_nome]
            print(f"\n  {montadora_nome}:")
            
            for (modelo_nome, tipo, popular), versoes in modelos_dict.items():
                # Criar modelo
                modelo, created = VeiculoModelo.objects.get_or_create(
                    montadora=montadora,
                    nome=modelo_nome,
                    defaults={
                        'tipo': tipo,
                        'popular': popular,
                        'ativo': True
                    }
                )
                
                if created:
                    stats['modelos'] += 1
                    print(f"    ✓ {modelo_nome} ({len(versoes)} versões)")
                
                # Criar versões deste modelo
                for versao_nome, ano_ini, ano_fim, motores in versoes:
                    versao, created = VeiculoVersao.objects.get_or_create(
                        modelo=modelo,
                        nome=versao_nome,
                        ano_inicial=ano_ini,
                        defaults={
                            'ano_final': ano_fim,
                            'motorizacoes': motores,
                            'ativo': True
                        }
                    )
                    
                    if created:
                        stats['versoes'] += 1
    
    print(f"\n✅ Concluído!")
    print(f"   Montadoras criadas: {stats['montadoras']}")
    print(f"   Modelos criados: {stats['modelos']}")
    print(f"   Versões criadas: {stats['versoes']}")
    print(f"\n💡 Agora você pode associar produtos às versões específicas!")
    
    return stats