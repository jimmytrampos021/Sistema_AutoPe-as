from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from datetime import date, timedelta
import uuid


# ==========================================
# CONFIGURAÇÃO FISCAL DA EMPRESA
# ==========================================
class ConfiguracaoFiscal(models.Model):
    """Configurações fiscais da empresa"""
    
    AMBIENTE_CHOICES = [
        ('1', 'Produção'),
        ('2', 'Homologação (Teste)'),
    ]
    
    REGIME_CHOICES = [
        ('1', 'Simples Nacional'),
        ('2', 'Simples Nacional - Excesso'),
        ('3', 'Regime Normal'),
    ]
    
    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    # Dados da Empresa
    razao_social = models.CharField(max_length=200, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=200, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    inscricao_estadual = models.CharField(max_length=20, verbose_name='Inscrição Estadual')
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True, 
                                           verbose_name='Inscrição Municipal')
    
    # Endereço
    cep = models.CharField(max_length=9, verbose_name='CEP')
    logradouro = models.CharField(max_length=200, verbose_name='Logradouro')
    numero = models.CharField(max_length=20, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    uf = models.CharField(max_length=2, choices=UF_CHOICES, verbose_name='UF')
    codigo_municipio = models.CharField(max_length=7, verbose_name='Código IBGE Município')
    
    # Contato
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')
    email = models.EmailField(verbose_name='Email para envio de notas')
    
    # Configurações Fiscais
    regime_tributario = models.CharField(max_length=1, choices=REGIME_CHOICES, 
                                         default='1', verbose_name='Regime Tributário')
    ambiente = models.CharField(max_length=1, choices=AMBIENTE_CHOICES, 
                               default='2', verbose_name='Ambiente')
    
    # Certificado Digital
    certificado_arquivo = models.FileField(upload_to='certificados/', blank=True, null=True,
                                           verbose_name='Certificado Digital A1 (.pfx)')
    certificado_senha = models.CharField(max_length=100, blank=True, null=True,
                                         verbose_name='Senha do Certificado')
    certificado_validade = models.DateField(blank=True, null=True, 
                                            verbose_name='Validade do Certificado')
    
    # API WebmaniaBR
    webmania_consumer_key = models.CharField(max_length=100, blank=True, null=True,
                                             verbose_name='Consumer Key')
    webmania_consumer_secret = models.CharField(max_length=100, blank=True, null=True,
                                                verbose_name='Consumer Secret')
    webmania_access_token = models.CharField(max_length=100, blank=True, null=True,
                                             verbose_name='Access Token')
    webmania_access_token_secret = models.CharField(max_length=100, blank=True, null=True,
                                                    verbose_name='Access Token Secret')
    
    # NFC-e
    csc_id = models.CharField(max_length=10, blank=True, null=True,
                              verbose_name='ID do CSC (NFC-e)')
    csc_token = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name='Token CSC (NFC-e)')
    
    # Séries
    serie_nfe = models.IntegerField(default=1, verbose_name='Série NF-e')
    serie_nfce = models.IntegerField(default=1, verbose_name='Série NFC-e')
    proximo_numero_nfe = models.IntegerField(default=1, verbose_name='Próximo Número NF-e')
    proximo_numero_nfce = models.IntegerField(default=1, verbose_name='Próximo Número NFC-e')
    
    # Controle
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração Fiscal'
        verbose_name_plural = 'Configurações Fiscais'
    
    def __str__(self):
        return f"{self.razao_social} - {self.cnpj}"
    
    @classmethod
    def get_config(cls):
        """Retorna a configuração ativa"""
        return cls.objects.filter(ativo=True).first()
    
    def get_proximo_numero_nfe(self):
        """Retorna e incrementa o próximo número de NF-e"""
        numero = self.proximo_numero_nfe
        self.proximo_numero_nfe += 1
        self.save(update_fields=['proximo_numero_nfe'])
        return numero
    
    def get_proximo_numero_nfce(self):
        """Retorna e incrementa o próximo número de NFC-e"""
        numero = self.proximo_numero_nfce
        self.proximo_numero_nfce += 1
        self.save(update_fields=['proximo_numero_nfce'])
        return numero


# ==========================================
# NCM - NOMENCLATURA COMUM DO MERCOSUL
# ==========================================
class NCM(models.Model):
    """Cadastro de NCMs"""
    codigo = models.CharField(max_length=8, unique=True, verbose_name='Código NCM')
    descricao = models.CharField(max_length=500, verbose_name='Descrição')
    aliquota_ipi = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                       verbose_name='Alíquota IPI (%)')
    tem_substituicao_tributaria = models.BooleanField(default=False, 
                                                       verbose_name='Tem ST?')
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'NCM'
        verbose_name_plural = 'NCMs'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao[:50]}"


# ==========================================
# CFOP - CÓDIGO FISCAL DE OPERAÇÕES
# ==========================================
class CFOP(models.Model):
    """Cadastro de CFOPs"""
    codigo = models.CharField(max_length=4, unique=True, verbose_name='Código CFOP')
    descricao = models.CharField(max_length=300, verbose_name='Descrição')
    aplicacao = models.TextField(blank=True, null=True, verbose_name='Aplicação')
    entrada_saida = models.CharField(max_length=1, choices=[('E', 'Entrada'), ('S', 'Saída')],
                                     verbose_name='Tipo')
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'CFOP'
        verbose_name_plural = 'CFOPs'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao[:50]}"


# ==========================================
# NOTA FISCAL ELETRÔNICA
# ==========================================
class NotaFiscal(models.Model):
    """Nota Fiscal Eletrônica (NF-e e NFC-e)"""
    
    MODELO_CHOICES = [
        ('55', 'NF-e (Modelo 55)'),
        ('65', 'NFC-e (Modelo 65)'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('AUTORIZADA', 'Autorizada'),
        ('REJEITADA', 'Rejeitada'),
        ('CANCELADA', 'Cancelada'),
        ('DENEGADA', 'Denegada'),
        ('INUTILIZADA', 'Inutilizada'),
    ]
    
    FINALIDADE_CHOICES = [
        ('1', 'NF-e Normal'),
        ('2', 'NF-e Complementar'),
        ('3', 'NF-e de Ajuste'),
        ('4', 'Devolução de Mercadoria'),
    ]
    
    TIPO_CHOICES = [
        ('0', 'Entrada'),
        ('1', 'Saída'),
    ]
    
    PRESENCA_CHOICES = [
        ('0', 'Não se aplica'),
        ('1', 'Operação presencial'),
        ('2', 'Operação não presencial, Internet'),
        ('3', 'Operação não presencial, Teleatendimento'),
        ('4', 'NFC-e em operação com entrega a domicílio'),
        ('5', 'Operação presencial, fora do estabelecimento'),
        ('9', 'Operação não presencial, outros'),
    ]
    
    # Identificação
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    modelo = models.CharField(max_length=2, choices=MODELO_CHOICES, default='65',
                              verbose_name='Modelo')
    serie = models.IntegerField(default=1, verbose_name='Série')
    numero = models.IntegerField(verbose_name='Número')
    
    # Chave e Protocolo
    chave_acesso = models.CharField(max_length=44, blank=True, null=True,
                                    verbose_name='Chave de Acesso')
    protocolo = models.CharField(max_length=20, blank=True, null=True,
                                 verbose_name='Protocolo de Autorização')
    data_autorizacao = models.DateTimeField(blank=True, null=True,
                                            verbose_name='Data/Hora Autorização')
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE',
                              verbose_name='Status')
    motivo_rejeicao = models.TextField(blank=True, null=True, verbose_name='Motivo Rejeição')
    codigo_status_sefaz = models.CharField(max_length=10, blank=True, null=True,
                                           verbose_name='Código Status SEFAZ')
    
    # Dados da Nota
    natureza_operacao = models.CharField(max_length=100, default='VENDA DE MERCADORIA',
                                         verbose_name='Natureza da Operação')
    tipo_operacao = models.CharField(max_length=1, choices=TIPO_CHOICES, default='1',
                                     verbose_name='Tipo')
    finalidade = models.CharField(max_length=1, choices=FINALIDADE_CHOICES, default='1',
                                  verbose_name='Finalidade')
    presenca = models.CharField(max_length=1, choices=PRESENCA_CHOICES, default='1',
                                verbose_name='Presença do Comprador')
    
    # Datas
    data_emissao = models.DateTimeField(default=timezone.now, verbose_name='Data Emissão')
    data_saida = models.DateTimeField(blank=True, null=True, verbose_name='Data Saída')
    
    # Destinatário
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT,
                                blank=True, null=True, verbose_name='Cliente',
                                related_name='notas_fiscais')
    dest_cpf_cnpj = models.CharField(max_length=18, blank=True, null=True,
                                     verbose_name='CPF/CNPJ Destinatário')
    dest_nome = models.CharField(max_length=200, blank=True, null=True,
                                 verbose_name='Nome/Razão Social')
    dest_ie = models.CharField(max_length=20, blank=True, null=True,
                               verbose_name='Inscrição Estadual')
    dest_email = models.EmailField(blank=True, null=True, verbose_name='Email')
    dest_telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')
    
    # Endereço Destinatário
    dest_cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP')
    dest_logradouro = models.CharField(max_length=200, blank=True, null=True, verbose_name='Logradouro')
    dest_numero = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número')
    dest_complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    dest_bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    dest_cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    dest_uf = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF')
    dest_codigo_municipio = models.CharField(max_length=7, blank=True, null=True,
                                             verbose_name='Código Município')
    
    # Totais
    valor_produtos = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                         verbose_name='Valor dos Produtos')
    valor_frete = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                      verbose_name='Valor do Frete')
    valor_seguro = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       verbose_name='Valor do Seguro')
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                         verbose_name='Valor do Desconto')
    valor_outras_despesas = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                                verbose_name='Outras Despesas')
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                      verbose_name='Valor Total da Nota')
    
    # Impostos
    base_calculo_icms = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                            verbose_name='Base Cálculo ICMS')
    valor_icms = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name='Valor ICMS')
    valor_icms_st = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                        verbose_name='Valor ICMS ST')
    valor_ipi = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    verbose_name='Valor IPI')
    valor_pis = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    verbose_name='Valor PIS')
    valor_cofins = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       verbose_name='Valor COFINS')
    
    # Informações Adicionais
    informacoes_complementares = models.TextField(blank=True, null=True,
                                                  verbose_name='Informações Complementares')
    informacoes_fisco = models.TextField(blank=True, null=True,
                                         verbose_name='Informações ao Fisco')
    
    # Vínculo com Venda
    venda = models.ForeignKey('vendas.Venda', on_delete=models.SET_NULL,
                              blank=True, null=True, verbose_name='Venda',
                              related_name='notas_fiscais')
    
    # Arquivos
    xml_envio = models.TextField(blank=True, null=True, verbose_name='XML de Envio')
    xml_retorno = models.TextField(blank=True, null=True, verbose_name='XML de Retorno')
    xml_autorizado = models.TextField(blank=True, null=True, verbose_name='XML Autorizado')
    pdf_danfe = models.FileField(upload_to='notas_fiscais/danfe/%Y/%m/', blank=True, null=True,
                                 verbose_name='DANFE (PDF)')
    
    # Controle
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Usuário')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-data_emissao']
        unique_together = ['modelo', 'serie', 'numero']
    
    def __str__(self):
        modelo_nome = 'NFC-e' if self.modelo == '65' else 'NF-e'
        return f"{modelo_nome} {self.numero} - {self.get_status_display()}"
    
    @property
    def is_nfce(self):
        return self.modelo == '65'
    
    @property
    def is_nfe(self):
        return self.modelo == '55'
    
    @property
    def pode_cancelar(self):
        """NF-e/NFC-e pode ser cancelada em até 24h (NFC-e) ou 168h (NF-e)"""
        if self.status != 'AUTORIZADA':
            return False
        
        horas_limite = 24 if self.is_nfce else 168
        tempo_decorrido = timezone.now() - self.data_autorizacao
        return tempo_decorrido.total_seconds() / 3600 <= horas_limite


# ==========================================
# ITEM DA NOTA FISCAL
# ==========================================
class ItemNotaFiscal(models.Model):
    """Itens da Nota Fiscal"""
    
    ORIGEM_CHOICES = [
        ('0', 'Nacional'),
        ('1', 'Estrangeira - Importação direta'),
        ('2', 'Estrangeira - Adquirida no mercado interno'),
        ('3', 'Nacional - Conteúdo de importação > 40%'),
        ('4', 'Nacional - Produção conforme processos básicos'),
        ('5', 'Nacional - Conteúdo de importação <= 40%'),
        ('6', 'Estrangeira - Importação direta, sem similar nacional'),
        ('7', 'Estrangeira - Adquirida no mercado interno, sem similar nacional'),
        ('8', 'Nacional - Conteúdo de importação > 70%'),
    ]
    
    # Códigos CSOSN para Simples Nacional
    CSOSN_CHOICES = [
        ('101', '101 - Tributada com permissão de crédito'),
        ('102', '102 - Tributada sem permissão de crédito'),
        ('103', '103 - Isenção do ICMS para faixa de receita bruta'),
        ('201', '201 - Tributada com permissão de crédito e com cobrança de ST'),
        ('202', '202 - Tributada sem permissão de crédito e com cobrança de ST'),
        ('203', '203 - Isenção do ICMS para faixa de receita bruta e com cobrança de ST'),
        ('300', '300 - Imune'),
        ('400', '400 - Não tributada'),
        ('500', '500 - ICMS cobrado anteriormente por ST'),
        ('900', '900 - Outros'),
    ]
    
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                    related_name='itens', verbose_name='Nota Fiscal')
    
    # Produto
    produto = models.ForeignKey('estoque.Produto', on_delete=models.PROTECT,
                                verbose_name='Produto')
    numero_item = models.IntegerField(verbose_name='Nº Item')
    
    # Dados do Produto
    codigo = models.CharField(max_length=60, verbose_name='Código')
    descricao = models.CharField(max_length=120, verbose_name='Descrição')
    ncm = models.CharField(max_length=8, verbose_name='NCM')
    cfop = models.CharField(max_length=4, verbose_name='CFOP')
    unidade = models.CharField(max_length=6, default='UN', verbose_name='Unidade')
    
    # Valores
    quantidade = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Quantidade')
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor Unitário')
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor Total')
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                         verbose_name='Desconto')
    
    # Tributos
    origem = models.CharField(max_length=1, choices=ORIGEM_CHOICES, default='0',
                              verbose_name='Origem')
    csosn = models.CharField(max_length=3, choices=CSOSN_CHOICES, default='102',
                             verbose_name='CSOSN')
    
    # ICMS
    base_calculo_icms = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                            verbose_name='Base Cálculo ICMS')
    aliquota_icms = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                        verbose_name='Alíquota ICMS')
    valor_icms = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name='Valor ICMS')
    
    # ICMS ST
    base_calculo_icms_st = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                               verbose_name='Base Cálculo ICMS ST')
    aliquota_icms_st = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                           verbose_name='Alíquota ICMS ST')
    valor_icms_st = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                        verbose_name='Valor ICMS ST')
    
    # PIS
    aliquota_pis = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                       verbose_name='Alíquota PIS')
    valor_pis = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    verbose_name='Valor PIS')
    
    # COFINS
    aliquota_cofins = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                          verbose_name='Alíquota COFINS')
    valor_cofins = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       verbose_name='Valor COFINS')
    
    # IPI
    aliquota_ipi = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                       verbose_name='Alíquota IPI')
    valor_ipi = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    verbose_name='Valor IPI')
    
    class Meta:
        verbose_name = 'Item da Nota Fiscal'
        verbose_name_plural = 'Itens da Nota Fiscal'
        ordering = ['numero_item']
    
    def __str__(self):
        return f"{self.numero_item} - {self.descricao}"
    
    def save(self, *args, **kwargs):
        if not self.valor_total:
            self.valor_total = self.quantidade * self.valor_unitario - self.valor_desconto
        super().save(*args, **kwargs)


# ==========================================
# PAGAMENTO DA NOTA FISCAL
# ==========================================
class PagamentoNotaFiscal(models.Model):
    """Formas de Pagamento da Nota Fiscal"""
    
    FORMA_CHOICES = [
        ('01', 'Dinheiro'),
        ('02', 'Cheque'),
        ('03', 'Cartão de Crédito'),
        ('04', 'Cartão de Débito'),
        ('05', 'Crédito Loja'),
        ('10', 'Vale Alimentação'),
        ('11', 'Vale Refeição'),
        ('12', 'Vale Presente'),
        ('13', 'Vale Combustível'),
        ('15', 'Boleto Bancário'),
        ('16', 'Depósito Bancário'),
        ('17', 'PIX'),
        ('18', 'Transferência'),
        ('19', 'Programa de Fidelidade'),
        ('90', 'Sem Pagamento'),
        ('99', 'Outros'),
    ]
    
    BANDEIRA_CHOICES = [
        ('01', 'Visa'),
        ('02', 'Mastercard'),
        ('03', 'American Express'),
        ('04', 'Sorocred'),
        ('05', 'Diners Club'),
        ('06', 'Elo'),
        ('07', 'Hipercard'),
        ('08', 'Aura'),
        ('09', 'Cabal'),
        ('99', 'Outros'),
    ]
    
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                    related_name='pagamentos', verbose_name='Nota Fiscal')
    forma_pagamento = models.CharField(max_length=2, choices=FORMA_CHOICES,
                                       verbose_name='Forma de Pagamento')
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')
    
    # Para cartões
    bandeira = models.CharField(max_length=2, choices=BANDEIRA_CHOICES, blank=True, null=True,
                                verbose_name='Bandeira')
    autorizacao = models.CharField(max_length=20, blank=True, null=True,
                                   verbose_name='Código Autorização')
    cnpj_credenciadora = models.CharField(max_length=18, blank=True, null=True,
                                          verbose_name='CNPJ Credenciadora')
    
    class Meta:
        verbose_name = 'Pagamento da Nota Fiscal'
        verbose_name_plural = 'Pagamentos da Nota Fiscal'
    
    def __str__(self):
        return f"{self.get_forma_pagamento_display()} - R$ {self.valor}"


# ==========================================
# DUPLICATA/COBRANÇA DA NOTA FISCAL
# ==========================================
class DuplicataNotaFiscal(models.Model):
    """Duplicatas para NF-e com pagamento a prazo"""
    
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                    related_name='duplicatas', verbose_name='Nota Fiscal')
    numero = models.CharField(max_length=60, verbose_name='Número da Duplicata')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')
    
    # Vinculo com boleto (se houver)
    boleto = models.ForeignKey('Boleto', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='duplicatas', verbose_name='Boleto')
    
    # Vinculo com conta a receber
    conta_receber = models.ForeignKey('financeiro.ContaReceber', on_delete=models.SET_NULL,
                                      blank=True, null=True, related_name='duplicatas_nf',
                                      verbose_name='Conta a Receber')
    
    class Meta:
        verbose_name = 'Duplicata'
        verbose_name_plural = 'Duplicatas'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"Dup. {self.numero} - Venc: {self.data_vencimento} - R$ {self.valor}"


# ==========================================
# EVENTO DA NOTA FISCAL
# ==========================================
class EventoNotaFiscal(models.Model):
    """Eventos da Nota Fiscal (cancelamento, carta de correção, etc.)"""
    
    TIPO_CHOICES = [
        ('CANCELAMENTO', 'Cancelamento'),
        ('CARTA_CORRECAO', 'Carta de Correção'),
        ('CIENCIA', 'Ciência da Operação'),
        ('CONFIRMACAO', 'Confirmação da Operação'),
        ('DESCONHECIMENTO', 'Desconhecimento da Operação'),
        ('NAO_REALIZADA', 'Operação não Realizada'),
    ]
    
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                    related_name='eventos', verbose_name='Nota Fiscal')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Evento')
    sequencia = models.IntegerField(default=1, verbose_name='Sequência')
    
    # Dados do Evento
    protocolo = models.CharField(max_length=20, blank=True, null=True,
                                 verbose_name='Protocolo')
    data_evento = models.DateTimeField(default=timezone.now, verbose_name='Data do Evento')
    justificativa = models.TextField(blank=True, null=True, verbose_name='Justificativa')
    
    # Para Carta de Correção
    correcao = models.TextField(blank=True, null=True, verbose_name='Texto da Correção')
    
    # Status
    status = models.CharField(max_length=15, default='PENDENTE', verbose_name='Status')
    motivo = models.TextField(blank=True, null=True, verbose_name='Motivo/Retorno')
    
    # XML
    xml_evento = models.TextField(blank=True, null=True, verbose_name='XML do Evento')
    xml_retorno = models.TextField(blank=True, null=True, verbose_name='XML de Retorno')
    
    # Controle
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evento da Nota Fiscal'
        verbose_name_plural = 'Eventos da Nota Fiscal'
        ordering = ['-data_evento']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - NF {self.nota_fiscal.numero}"


# ==========================================
# BOLETO BANCÁRIO
# ==========================================
class Boleto(models.Model):
    """Boletos Bancários"""
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('REGISTRADO', 'Registrado'),
        ('PAGO', 'Pago'),
        ('VENCIDO', 'Vencido'),
        ('CANCELADO', 'Cancelado'),
        ('PROTESTADO', 'Protestado'),
    ]
    
    BANCO_CHOICES = [
        ('001', 'Banco do Brasil'),
        ('033', 'Santander'),
        ('104', 'Caixa Econômica'),
        ('237', 'Bradesco'),
        ('341', 'Itaú'),
        ('077', 'Banco Inter'),
        ('756', 'Sicoob'),
        ('748', 'Sicredi'),
        ('asaas', 'Asaas'),
        ('paghiper', 'PagHiper'),
    ]
    
    # Identificação
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nosso_numero = models.CharField(max_length=20, blank=True, null=True,
                                    verbose_name='Nosso Número')
    linha_digitavel = models.CharField(max_length=60, blank=True, null=True,
                                       verbose_name='Linha Digitável')
    codigo_barras = models.CharField(max_length=50, blank=True, null=True,
                                     verbose_name='Código de Barras')
    
    # Banco
    banco = models.CharField(max_length=10, choices=BANCO_CHOICES, verbose_name='Banco')
    
    # Pagador
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT,
                                verbose_name='Cliente', related_name='boletos')
    pagador_cpf_cnpj = models.CharField(max_length=18, verbose_name='CPF/CNPJ')
    pagador_nome = models.CharField(max_length=200, verbose_name='Nome')
    pagador_endereco = models.CharField(max_length=300, blank=True, null=True,
                                        verbose_name='Endereço')
    
    # Valores
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     verbose_name='Valor Pago')
    
    # Datas
    data_emissao = models.DateField(default=date.today, verbose_name='Data Emissão')
    data_vencimento = models.DateField(verbose_name='Data Vencimento')
    data_pagamento = models.DateField(blank=True, null=True, verbose_name='Data Pagamento')
    
    # Juros e Multa
    juros_ao_dia = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                       verbose_name='Juros ao Dia (%)')
    multa = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                verbose_name='Multa (%)')
    desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                   verbose_name='Desconto')
    
    # Instruções
    instrucao_1 = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='Instrução 1')
    instrucao_2 = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='Instrução 2')
    instrucao_3 = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='Instrução 3')
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE',
                              verbose_name='Status')
    
    # Vínculo com Nota Fiscal
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.SET_NULL,
                                    blank=True, null=True, related_name='boletos',
                                    verbose_name='Nota Fiscal')
    
    # Vínculo com Conta a Receber
    conta_receber = models.ForeignKey('financeiro.ContaReceber', on_delete=models.SET_NULL,
                                      blank=True, null=True, related_name='boletos',
                                      verbose_name='Conta a Receber')
    
    # API
    id_externo = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name='ID na API')
    url_boleto = models.URLField(blank=True, null=True, verbose_name='URL do Boleto')
    pdf_boleto = models.FileField(upload_to='boletos/%Y/%m/', blank=True, null=True,
                                  verbose_name='PDF do Boleto')
    
    # Controle
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Boleto'
        verbose_name_plural = 'Boletos'
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"Boleto {self.nosso_numero or self.id} - {self.cliente.nome} - R$ {self.valor}"
    
    @property
    def esta_vencido(self):
        return self.status == 'PENDENTE' and self.data_vencimento < date.today()
    
    @property
    def dias_atraso(self):
        if self.esta_vencido:
            return (date.today() - self.data_vencimento).days
        return 0


# ==========================================
# INUTILIZAÇÃO DE NUMERAÇÃO
# ==========================================
class InutilizacaoNumeracao(models.Model):
    """Inutilização de numeração de NF-e/NFC-e"""
    
    MODELO_CHOICES = [
        ('55', 'NF-e'),
        ('65', 'NFC-e'),
    ]
    
    modelo = models.CharField(max_length=2, choices=MODELO_CHOICES, verbose_name='Modelo')
    serie = models.IntegerField(verbose_name='Série')
    numero_inicial = models.IntegerField(verbose_name='Número Inicial')
    numero_final = models.IntegerField(verbose_name='Número Final')
    justificativa = models.TextField(verbose_name='Justificativa',
                                     help_text='Mínimo 15 caracteres')
    
    # Retorno
    protocolo = models.CharField(max_length=20, blank=True, null=True, verbose_name='Protocolo')
    status = models.CharField(max_length=15, default='PENDENTE', verbose_name='Status')
    data_inutilizacao = models.DateTimeField(blank=True, null=True)
    
    # XML
    xml_envio = models.TextField(blank=True, null=True)
    xml_retorno = models.TextField(blank=True, null=True)
    
    # Controle
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inutilização de Numeração'
        verbose_name_plural = 'Inutilizações de Numeração'
    
    def __str__(self):
        return f"{self.get_modelo_display()} - {self.numero_inicial} a {self.numero_final}"
