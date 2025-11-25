from django.db import models
from clientes.models import Cliente, Veiculo
from django.db import models
from django.contrib.auth.models import User
from estoque.models import Produto, VeiculoModelo
from decimal import Decimal



class Venda(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aberta'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('DI', 'Dinheiro'),
        ('CD', 'Cartão de Débito'),
        ('CC', 'Cartão de Crédito'),
        ('PI', 'PIX'),
        ('BO', 'Boleto'),
        ('CR', 'Crediário'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, null=True, blank=True)
    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    forma_pagamento = models.CharField(max_length=2, choices=FORMA_PAGAMENTO_CHOICES)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    observacoes = models.TextField(blank=True, null=True)
    
    vendedor = models.CharField(max_length=100)
    data_venda = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']
    
    def __str__(self):
        return f"Venda {self.numero} - {self.cliente.nome}"
    
    def calcular_total(self):
        self.subtotal = sum(item.total for item in self.itens.all())
        self.total = self.subtotal - self.desconto
        self.save()


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'
    
    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade}"
    
    def save(self, *args, **kwargs):
        self.total = (self.valor_unitario * self.quantidade) - self.desconto
        super().save(*args, **kwargs)


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('AB', 'Aberta'),
        ('EA', 'Em Andamento'),
        ('AG', 'Aguardando Peças'),
        ('FI', 'Finalizada'),
        ('CA', 'Cancelada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AB')
    
    defeito_reclamado = models.TextField()
    defeito_constatado = models.TextField(blank=True, null=True)
    servicos_executados = models.TextField(blank=True, null=True)
    
    km_entrada = models.IntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_prevista = models.DateTimeField(null=True, blank=True)
    data_saida = models.DateTimeField(null=True, blank=True)
    
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_servicos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    mecanico = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f"OS {self.numero} - {self.cliente.nome}"
    
    def calcular_total(self):
        self.valor_pecas = sum(item.total for item in self.pecas.all())
        self.valor_servicos = sum(servico.valor for servico in self.servicos.all())
        self.total = self.valor_pecas + self.valor_servicos - self.desconto
        self.save()


class PecaOS(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='pecas')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Peça da OS'
        verbose_name_plural = 'Peças da OS'
    
    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade}"
    
    def save(self, *args, **kwargs):
        self.total = self.valor_unitario * self.quantidade
        super().save(*args, **kwargs)


class ServicoOS(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos')
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Serviço da OS'
        verbose_name_plural = 'Serviços da OS'
    
    def __str__(self):
        return self.descricao



class Orcamento(models.Model):
    """Orçamento de venda"""
    
    # Identificação
    numero = models.CharField(max_length=20, unique=True, verbose_name='Número do Orçamento')
    data_orcamento = models.DateTimeField(auto_now_add=True, verbose_name='Data do Orçamento')
    data_validade = models.DateField(verbose_name='Validade')
    
    # Cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, 
                               related_name='orcamentos', verbose_name='Cliente')
    
    # Veículo do cliente (opcional)
    veiculo_modelo = models.ForeignKey(VeiculoModelo, on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      verbose_name='Modelo do Veículo')
    veiculo_placa = models.CharField(max_length=10, blank=True, null=True, verbose_name='Placa')
    veiculo_ano = models.IntegerField(blank=True, null=True, verbose_name='Ano do Veículo')
    
    # Vendedor
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT,
                                related_name='orcamentos', verbose_name='Vendedor')
    
    # Status
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('ENVIADO', 'Enviado ao Cliente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('CONVERTIDO', 'Convertido em Venda'),
        ('EXPIRADO', 'Expirado'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, 
                             default='ABERTO', verbose_name='Status')
    
    # Forma de pagamento
    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro/PIX'),
        ('DEBITO', 'Cartão Débito'),
        ('CREDITO', 'Cartão Crédito'),
        ('ATACADO', 'Atacado'),
    ]
    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES,
                                      default='DINHEIRO', verbose_name='Forma de Pagamento')
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                   verbose_name='Subtotal')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                   verbose_name='Desconto')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                verbose_name='Total')
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    observacoes_internas = models.TextField(blank=True, null=True, 
                                           verbose_name='Observações Internas')
    
    # Controle
    data_aprovacao = models.DateTimeField(blank=True, null=True, verbose_name='Data de Aprovação')
    data_conversao = models.DateTimeField(blank=True, null=True, verbose_name='Data de Conversão')
    venda_gerada = models.ForeignKey('vendas.Venda', on_delete=models.SET_NULL,
                                    blank=True, null=True,
                                    verbose_name='Venda Gerada')
    
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-data_orcamento']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['status']),
            models.Index(fields=['cliente']),
            models.Index(fields=['-data_orcamento']),
        ]
    
    def __str__(self):
        return f"Orçamento {self.numero} - {self.cliente.nome}"
    
    def calcular_totais(self):
        """Recalcula subtotal e total"""
        self.subtotal = sum(item.total for item in self.itens.all())
        self.total = self.subtotal - self.desconto
        self.save()
    
    def pode_converter(self):
        """Verifica se o orçamento pode ser convertido em venda"""
        if self.status != 'APROVADO':
            return False, "Orçamento precisa estar aprovado"
        
        # Verificar estoque de todos os itens
        for item in self.itens.all():
            if item.produto.estoque_disponivel < item.quantidade:
                return False, f"Estoque insuficiente para {item.produto.descricao}"
        
        return True, "OK"
    
    def get_percentual_desconto(self):
        """Retorna o percentual de desconto"""
        if self.subtotal > 0:
            return (self.desconto / self.subtotal * 100)
        return 0


class ItemOrcamento(models.Model):
    """Item de um orçamento"""
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE,
                                 related_name='itens', verbose_name='Orçamento')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto')
    quantidade = models.IntegerField(default=1, verbose_name='Quantidade')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, 
                                        verbose_name='Preço Unitário')
    desconto_item = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                       verbose_name='Desconto no Item')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    
    # Controle de estoque
    estoque_disponivel = models.IntegerField(default=0, editable=False,
                                            verbose_name='Estoque Disponível')
    
    class Meta:
        verbose_name = 'Item do Orçamento'
        verbose_name_plural = 'Itens do Orçamento'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.produto.codigo} - {self.quantidade}un"
    
    def save(self, *args, **kwargs):
        # Calcular total do item
        self.total = (self.preco_unitario * self.quantidade) - self.desconto_item
        
        # Armazenar estoque disponível no momento
        self.estoque_disponivel = self.produto.estoque_disponivel
        
        super().save(*args, **kwargs)
        
        # Recalcular totais do orçamento
        self.orcamento.calcular_totais()
    
    def tem_estoque(self):
        """Verifica se tem estoque suficiente"""
        return self.produto.estoque_disponivel >= self.quantidade
    
    def get_status_estoque(self):
        """Retorna o status do estoque para este item"""
        if self.produto.estoque_disponivel >= self.quantidade:
            return 'OK'
        elif self.produto.estoque_disponivel > 0:
            return 'PARCIAL'
        else:
            return 'INDISPONIVEL'