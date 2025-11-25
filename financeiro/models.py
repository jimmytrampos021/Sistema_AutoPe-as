from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# ==========================================
# MODELO: CONFIGURAÇÃO DE TAXAS DE CARTÃO
# ==========================================
class TaxaCartao(models.Model):
    """Configuração das taxas de cartão de crédito/débito"""
    TIPO_CHOICES = [
        ('DEBITO', 'Débito'),
        ('CREDITO', 'Crédito'),
        ('PIX', 'PIX'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    parcelas = models.IntegerField(default=1, verbose_name='Parcelas',
                                   help_text='1 para débito, PIX ou crédito à vista')
    taxa_percentual = models.DecimalField(max_digits=5, decimal_places=2,
                                          verbose_name='Taxa (%)',
                                          help_text='Taxa cobrada pela operadora')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Taxa de Cartão'
        verbose_name_plural = 'Taxas de Cartão'
        ordering = ['tipo', 'parcelas']
        unique_together = ['tipo', 'parcelas']

    def __str__(self):
        if self.tipo == 'DEBITO':
            return f"Débito - {self.taxa_percentual}%"
        elif self.tipo == 'PIX':
            return f"PIX - {self.taxa_percentual}%"
        return f"Crédito {self.parcelas}x - {self.taxa_percentual}%"

    @classmethod
    def get_taxa(cls, tipo, parcelas=1):
        """Retorna a taxa para um tipo e número de parcelas"""
        try:
            taxa = cls.objects.get(tipo=tipo, parcelas=parcelas, ativo=True)
            return taxa.taxa_percentual
        except cls.DoesNotExist:
            return Decimal('0.00')

    @classmethod
    def get_todas_taxas(cls):
        """Retorna todas as taxas ativas organizadas"""
        taxas = cls.objects.filter(ativo=True).order_by('tipo', 'parcelas')
        return {
            'pix': taxas.filter(tipo='PIX').first(),
            'debito': taxas.filter(tipo='DEBITO').first(),
            'credito': list(taxas.filter(tipo='CREDITO'))
        }

    @classmethod
    def calcular_financeiro(cls, preco_venda, preco_custo, tipo='PIX', parcelas=1):
        """Calcula todos os indicadores financeiros"""
        preco_venda = Decimal(str(preco_venda)) if preco_venda else Decimal('0')
        preco_custo = Decimal(str(preco_custo)) if preco_custo else Decimal('0')

        taxa = cls.get_taxa(tipo, parcelas)
        valor_taxa = preco_venda * (taxa / Decimal('100'))
        lucro_bruto = preco_venda - preco_custo
        lucro_liquido = lucro_bruto - valor_taxa

        margem_liquida = (lucro_liquido / preco_venda * 100) if preco_venda > 0 else Decimal('0')
        margem_bruta = (lucro_bruto / preco_venda * 100) if preco_venda > 0 else Decimal('0')
        markup = (lucro_bruto / preco_custo * 100) if preco_custo > 0 else Decimal('0')

        return {
            'preco_venda': preco_venda,
            'preco_custo': preco_custo,
            'taxa_percentual': taxa,
            'valor_taxa': valor_taxa,
            'lucro_bruto': lucro_bruto,
            'lucro_liquido': lucro_liquido,
            'margem_bruta': margem_bruta,
            'margem_liquida': margem_liquida,
            'markup': markup,
        }


# ==========================================
# MODELO: CONFIGURAÇÃO DO SIMPLES NACIONAL
# ==========================================
class ConfiguracaoTributo(models.Model):
    """Configuração do tributo Simples Nacional"""
    nome = models.CharField(max_length=100, default='Simples Nacional', verbose_name='Nome')
    aliquota = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('4.00'),
                                   verbose_name='Alíquota (%)')
    dia_vencimento = models.IntegerField(default=20, verbose_name='Dia de Vencimento',
                                         help_text='Dia do mês seguinte para pagamento')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração de Tributo'
        verbose_name_plural = 'Configurações de Tributos'

    def __str__(self):
        return f"{self.nome} - {self.aliquota}%"

    @classmethod
    def get_configuracao_ativa(cls):
        """Retorna a configuração ativa ou cria uma padrão"""
        config = cls.objects.filter(ativo=True).first()
        if not config:
            config = cls.objects.create(
                nome='Simples Nacional',
                aliquota=Decimal('4.00'),
                dia_vencimento=20
            )
        return config


# ==========================================
# MODELO: CATEGORIA DE DESPESA
# ==========================================
class CategoriaDespesa(models.Model):
    """Categorias para organizar despesas"""
    TIPO_CHOICES = [
        ('FIXA', 'Despesa Fixa'),
        ('VARIAVEL', 'Despesa Variável'),
        ('AMBOS', 'Ambos'),
    ]

    nome = models.CharField(max_length=100, verbose_name='Nome')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='AMBOS', verbose_name='Tipo')
    icone = models.CharField(max_length=50, default='bi-folder', verbose_name='Ícone',
                             help_text='Classe do ícone Bootstrap (ex: bi-house)')
    cor = models.CharField(max_length=20, default='#6c757d', verbose_name='Cor',
                           help_text='Cor em hexadecimal')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')

    class Meta:
        verbose_name = 'Categoria de Despesa'
        verbose_name_plural = 'Categorias de Despesas'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


# ==========================================
# MODELO: FORMA DE PAGAMENTO
# ==========================================
class FormaPagamento(models.Model):
    """Formas de pagamento para despesas"""
    nome = models.CharField(max_length=50, verbose_name='Nome')
    icone = models.CharField(max_length=50, default='bi-wallet', verbose_name='Ícone')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ==========================================
# MODELO: DESPESA FIXA (RECORRENTE)
# ==========================================
class DespesaFixa(models.Model):
    """Despesas fixas mensais recorrentes"""
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.PROTECT,
                                  verbose_name='Categoria')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    dia_vencimento = models.IntegerField(verbose_name='Dia de Vencimento',
                                         help_text='Dia do mês para vencimento')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_inicio = models.DateField(default=date.today, verbose_name='Data de Início')
    data_fim = models.DateField(blank=True, null=True, verbose_name='Data de Término',
                                help_text='Deixe em branco para despesa sem prazo')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Despesa Fixa'
        verbose_name_plural = 'Despesas Fixas'
        ordering = ['dia_vencimento', 'descricao']

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} (dia {self.dia_vencimento})"

    def gerar_conta_mes(self, mes, ano):
        """Gera uma conta a pagar para o mês/ano especificado"""
        from calendar import monthrange
        
        # Verificar se a despesa está ativa no período
        data_vencimento = date(ano, mes, min(self.dia_vencimento, monthrange(ano, mes)[1]))
        
        if self.data_inicio and data_vencimento < self.data_inicio:
            return None
        if self.data_fim and data_vencimento > self.data_fim:
            return None
        if not self.ativo:
            return None

        # Verificar se já existe conta para este mês
        conta_existente = ContaPagar.objects.filter(
            despesa_fixa=self,
            data_vencimento__year=ano,
            data_vencimento__month=mes
        ).first()

        if conta_existente:
            return conta_existente

        # Criar nova conta
        conta = ContaPagar.objects.create(
            descricao=self.descricao,
            categoria=self.categoria,
            valor=self.valor,
            data_vencimento=data_vencimento,
            despesa_fixa=self,
            tipo='FIXA',
            observacoes=self.observacoes
        )
        return conta


# ==========================================
# MODELO: CONTA A PAGAR
# ==========================================
class ContaPagar(models.Model):
    """Contas a pagar (despesas fixas e variáveis)"""
    TIPO_CHOICES = [
        ('FIXA', 'Despesa Fixa'),
        ('VARIAVEL', 'Despesa Variável'),
        ('TRIBUTO', 'Tributo'),
        ('PARCELADO', 'Parcelado'),
    ]

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.PROTECT,
                                  verbose_name='Categoria')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='VARIAVEL',
                            verbose_name='Tipo')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    data_pagamento = models.DateField(blank=True, null=True, verbose_name='Data de Pagamento')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE',
                              verbose_name='Status')
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL,
                                        blank=True, null=True, verbose_name='Forma de Pagamento')
    despesa_fixa = models.ForeignKey(DespesaFixa, on_delete=models.SET_NULL,
                                     blank=True, null=True, verbose_name='Despesa Fixa Origem')
    
    # Campos para parcelamento
    parcela_atual = models.IntegerField(default=1, verbose_name='Parcela Atual')
    total_parcelas = models.IntegerField(default=1, verbose_name='Total de Parcelas')
    compra_parcelada = models.ForeignKey('CompraParcelada', on_delete=models.CASCADE,
                                         blank=True, null=True, related_name='parcelas')
    
    # Campos para tributo
    faturamento_referencia = models.ForeignKey('FaturamentoMensal', on_delete=models.SET_NULL,
                                               blank=True, null=True, related_name='tributos')
    
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    comprovante = models.FileField(upload_to='comprovantes/%Y/%m/', blank=True, null=True,
                                   verbose_name='Comprovante')
    
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='contas_cadastradas')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['data_vencimento', 'descricao']

    def __str__(self):
        parcela_str = f" ({self.parcela_atual}/{self.total_parcelas})" if self.total_parcelas > 1 else ""
        return f"{self.descricao}{parcela_str} - R$ {self.valor}"

    def save(self, *args, **kwargs):
        # Atualizar status automaticamente
        if self.status == 'PENDENTE' and self.data_vencimento < date.today():
            self.status = 'ATRASADO'
        if self.data_pagamento and self.status != 'CANCELADO':
            self.status = 'PAGO'
        super().save(*args, **kwargs)

    @property
    def esta_atrasado(self):
        return self.status == 'PENDENTE' and self.data_vencimento < date.today()

    @property
    def dias_atraso(self):
        if self.esta_atrasado:
            return (date.today() - self.data_vencimento).days
        return 0


# ==========================================
# MODELO: COMPRA PARCELADA
# ==========================================
class CompraParcelada(models.Model):
    """Agrupa parcelas de uma compra parcelada"""
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.PROTECT,
                                  verbose_name='Categoria')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total')
    numero_parcelas = models.IntegerField(verbose_name='Número de Parcelas')
    data_primeira_parcela = models.DateField(verbose_name='Data da Primeira Parcela')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Compra Parcelada'
        verbose_name_plural = 'Compras Parceladas'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.descricao} - {self.numero_parcelas}x de R$ {self.valor_parcela}"

    @property
    def valor_parcela(self):
        return self.valor_total / self.numero_parcelas

    @property
    def total_pago(self):
        return self.parcelas.filter(status='PAGO').aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')

    @property
    def total_pendente(self):
        return self.valor_total - self.total_pago

    def gerar_parcelas(self):
        """Gera todas as parcelas da compra"""
        valor_parcela = self.valor_total / self.numero_parcelas
        
        for i in range(self.numero_parcelas):
            data_venc = self.data_primeira_parcela + relativedelta(months=i)
            ContaPagar.objects.create(
                descricao=self.descricao,
                categoria=self.categoria,
                tipo='PARCELADO',
                valor=valor_parcela,
                data_vencimento=data_venc,
                parcela_atual=i + 1,
                total_parcelas=self.numero_parcelas,
                compra_parcelada=self,
                observacoes=self.observacoes
            )


# ==========================================
# MODELO: FATURAMENTO MENSAL
# ==========================================
class FaturamentoMensal(models.Model):
    """Registro de faturamento mensal para cálculo de tributos"""
    mes = models.IntegerField(verbose_name='Mês')
    ano = models.IntegerField(verbose_name='Ano')
    valor_faturamento = models.DecimalField(max_digits=12, decimal_places=2,
                                            verbose_name='Valor do Faturamento')
    valor_tributo = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name='Valor do Tributo', editable=False)
    aliquota_aplicada = models.DecimalField(max_digits=5, decimal_places=2,
                                            verbose_name='Alíquota Aplicada (%)', editable=False)
    data_vencimento_tributo = models.DateField(verbose_name='Data Vencimento Tributo')
    tributo_gerado = models.BooleanField(default=False, verbose_name='Tributo Gerado')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    calculado_automaticamente = models.BooleanField(default=True, 
                                                     verbose_name='Calculado Automaticamente')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Faturamento Mensal'
        verbose_name_plural = 'Faturamentos Mensais'
        ordering = ['-ano', '-mes']
        unique_together = ['mes', 'ano']

    def __str__(self):
        return f"{self.mes:02d}/{self.ano} - R$ {self.valor_faturamento}"

    def save(self, *args, **kwargs):
        # Calcular tributo
        config = ConfiguracaoTributo.get_configuracao_ativa()
        self.aliquota_aplicada = config.aliquota
        self.valor_tributo = self.valor_faturamento * (config.aliquota / Decimal('100'))
        
        # Calcular data de vencimento (mês seguinte)
        if self.mes == 12:
            mes_venc = 1
            ano_venc = self.ano + 1
        else:
            mes_venc = self.mes + 1
            ano_venc = self.ano
        
        from calendar import monthrange
        dia_venc = min(config.dia_vencimento, monthrange(ano_venc, mes_venc)[1])
        self.data_vencimento_tributo = date(ano_venc, mes_venc, dia_venc)
        
        super().save(*args, **kwargs)

    def gerar_tributo(self):
        """Gera a conta a pagar do tributo"""
        if self.tributo_gerado:
            return None

        # Buscar ou criar categoria de tributos
        categoria, _ = CategoriaDespesa.objects.get_or_create(
            nome='Tributos',
            defaults={
                'tipo': 'VARIAVEL',
                'icone': 'bi-bank',
                'cor': '#dc3545'
            }
        )

        conta = ContaPagar.objects.create(
            descricao=f"Simples Nacional - {self.mes:02d}/{self.ano}",
            categoria=categoria,
            tipo='TRIBUTO',
            valor=self.valor_tributo,
            data_vencimento=self.data_vencimento_tributo,
            faturamento_referencia=self,
            observacoes=f"Faturamento: R$ {self.valor_faturamento} | Alíquota: {self.aliquota_aplicada}%"
        )

        self.tributo_gerado = True
        self.save()
        return conta

    @classmethod
    def calcular_faturamento_vendas(cls, mes, ano):
        """Calcula o faturamento baseado nas vendas do sistema"""
        from vendas.models import Venda
        
        total = Venda.objects.filter(
            data_venda__month=mes,
            data_venda__year=ano,
            status='F'  # Finalizada
        ).aggregate(total=models.Sum('total'))['total'] or Decimal('0')
        
        return total


# ==========================================
# FUNÇÃO AUXILIAR PARA CÁLCULOS RÁPIDOS
# ==========================================
def calcular_indicadores_produto(produto):
    """Calcula todos os indicadores financeiros para um produto"""
    resultados = {
        'dinheiro': None,
        'pix': None,
        'debito': None,
        'credito': {}
    }

    custo = produto.preco_custo or Decimal('0')

    if produto.preco_venda_dinheiro:
        preco = produto.preco_venda_dinheiro
        lucro = preco - custo
        resultados['dinheiro'] = {
            'preco': preco,
            'lucro_bruto': lucro,
            'lucro_liquido': lucro,
            'margem_bruta': (lucro / preco * 100) if preco > 0 else Decimal('0'),
            'margem_liquida': (lucro / preco * 100) if preco > 0 else Decimal('0'),
            'markup': (lucro / custo * 100) if custo > 0 else Decimal('0'),
            'taxa': Decimal('0'),
            'valor_taxa': Decimal('0'),
        }

    if produto.preco_venda_dinheiro:
        resultados['pix'] = TaxaCartao.calcular_financeiro(
            produto.preco_venda_dinheiro, custo, 'PIX', 1
        )

    if produto.preco_venda_debito:
        resultados['debito'] = TaxaCartao.calcular_financeiro(
            produto.preco_venda_debito, custo, 'DEBITO', 1
        )

    if produto.preco_venda_credito:
        for parcela in range(1, 13):
            resultados['credito'][parcela] = TaxaCartao.calcular_financeiro(
                produto.preco_venda_credito, custo, 'CREDITO', parcela
            )

    return resultados