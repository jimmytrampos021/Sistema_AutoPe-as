from django.contrib import admin
from .models import (
    ConfiguracaoFiscal, NCM, CFOP, NotaFiscal, ItemNotaFiscal,
    PagamentoNotaFiscal, DuplicataNotaFiscal, EventoNotaFiscal,
    Boleto, InutilizacaoNumeracao
)


@admin.register(ConfiguracaoFiscal)
class ConfiguracaoFiscalAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'ambiente', 'ativo']
    fieldsets = (
        ('Dados da Empresa', {
            'fields': ('razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual', 'inscricao_municipal')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'codigo_municipio')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Configurações Fiscais', {
            'fields': ('regime_tributario', 'ambiente')
        }),
        ('Certificado Digital', {
            'fields': ('certificado_arquivo', 'certificado_senha', 'certificado_validade')
        }),
        ('API WebmaniaBR', {
            'fields': ('webmania_consumer_key', 'webmania_consumer_secret', 'webmania_access_token', 'webmania_access_token_secret'),
            'classes': ('collapse',)
        }),
        ('NFC-e', {
            'fields': ('csc_id', 'csc_token', 'serie_nfce', 'proximo_numero_nfce'),
            'classes': ('collapse',)
        }),
        ('NF-e', {
            'fields': ('serie_nfe', 'proximo_numero_nfe'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NCM)
class NCMAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'tem_substituicao_tributaria', 'ativo']
    search_fields = ['codigo', 'descricao']
    list_filter = ['tem_substituicao_tributaria', 'ativo']


@admin.register(CFOP)
class CFOPAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'entrada_saida', 'ativo']
    search_fields = ['codigo', 'descricao']
    list_filter = ['entrada_saida', 'ativo']


class ItemNotaFiscalInline(admin.TabularInline):
    model = ItemNotaFiscal
    extra = 0
    readonly_fields = ['numero_item', 'codigo', 'descricao', 'quantidade', 'valor_unitario', 'valor_total']


class PagamentoNotaFiscalInline(admin.TabularInline):
    model = PagamentoNotaFiscal
    extra = 0


class DuplicataNotaFiscalInline(admin.TabularInline):
    model = DuplicataNotaFiscal
    extra = 0


class EventoNotaFiscalInline(admin.TabularInline):
    model = EventoNotaFiscal
    extra = 0
    readonly_fields = ['tipo', 'data_evento', 'protocolo', 'status']


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['numero', 'modelo', 'serie', 'status', 'dest_nome', 'valor_total', 'data_emissao']
    list_filter = ['modelo', 'status', 'data_emissao']
    search_fields = ['numero', 'chave_acesso', 'dest_nome', 'dest_cpf_cnpj']
    readonly_fields = ['uuid', 'chave_acesso', 'protocolo', 'data_autorizacao']
    date_hierarchy = 'data_emissao'
    inlines = [ItemNotaFiscalInline, PagamentoNotaFiscalInline, DuplicataNotaFiscalInline, EventoNotaFiscalInline]


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ['nosso_numero', 'cliente', 'valor', 'data_vencimento', 'status']
    list_filter = ['status', 'banco', 'data_vencimento']
    search_fields = ['nosso_numero', 'pagador_nome', 'pagador_cpf_cnpj']
    date_hierarchy = 'data_vencimento'


@admin.register(InutilizacaoNumeracao)
class InutilizacaoNumeracaoAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'serie', 'numero_inicial', 'numero_final', 'status', 'data_cadastro']
    list_filter = ['modelo', 'status']
