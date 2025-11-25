from django.contrib import admin
from .models import Venda, ItemVenda, OrdemServico, PecaOS, ServicoOS


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    fields = ['produto', 'quantidade', 'valor_unitario', 'desconto', 'total']
    readonly_fields = ['total']


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'data_venda', 'status', 'forma_pagamento', 'total']
    list_filter = ['status', 'forma_pagamento', 'data_venda']
    search_fields = ['numero', 'cliente__nome']
    readonly_fields = ['data_venda', 'data_atualizacao', 'subtotal', 'total']
    inlines = [ItemVendaInline]
    date_hierarchy = 'data_venda'
    
    fieldsets = (
        ('Informações da Venda', {
            'fields': ('numero', 'cliente', 'veiculo', 'vendedor')
        }),
        ('Pagamento', {
            'fields': ('status', 'forma_pagamento')
        }),
        ('Valores', {
            'fields': ('subtotal', 'desconto', 'total')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Datas', {
            'fields': ('data_venda', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


class PecaOSInline(admin.TabularInline):
    model = PecaOS
    extra = 1
    fields = ['produto', 'quantidade', 'valor_unitario', 'total']
    readonly_fields = ['total']


class ServicoOSInline(admin.TabularInline):
    model = ServicoOS
    extra = 1
    fields = ['descricao', 'valor']


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'veiculo', 'status', 'data_entrada', 'mecanico', 'total']
    list_filter = ['status', 'data_entrada', 'mecanico']
    search_fields = ['numero', 'cliente__nome', 'veiculo__placa']
    readonly_fields = ['data_entrada', 'valor_pecas', 'valor_servicos', 'total']
    inlines = [PecaOSInline, ServicoOSInline]
    date_hierarchy = 'data_entrada'
    
    fieldsets = (
        ('Informações da OS', {
            'fields': ('numero', 'cliente', 'veiculo', 'status', 'mecanico')
        }),
        ('Veículo', {
            'fields': ('km_entrada',)
        }),
        ('Defeitos e Serviços', {
            'fields': ('defeito_reclamado', 'defeito_constatado', 'servicos_executados')
        }),
        ('Datas', {
            'fields': ('data_entrada', 'data_prevista', 'data_saida')
        }),
        ('Valores', {
            'fields': ('valor_pecas', 'valor_servicos', 'desconto', 'total')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
