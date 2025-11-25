from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TaxaCartao, ConfiguracaoTributo, CategoriaDespesa, 
    FormaPagamento, DespesaFixa, ContaPagar, CompraParcelada, 
    FaturamentoMensal
)


@admin.register(TaxaCartao)
class TaxaCartaoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'parcelas', 'taxa_percentual', 'ativo', 'data_atualizacao']
    list_filter = ['tipo', 'ativo']
    list_editable = ['taxa_percentual', 'ativo']
    ordering = ['tipo', 'parcelas']


@admin.register(ConfiguracaoTributo)
class ConfiguracaoTributoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'aliquota', 'dia_vencimento', 'ativo']
    list_editable = ['aliquota', 'dia_vencimento', 'ativo']


@admin.register(CategoriaDespesa)
class CategoriaDespesaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'icone_preview', 'cor_preview', 'ativo', 'ordem']
    list_filter = ['tipo', 'ativo']
    list_editable = ['tipo', 'ativo', 'ordem']
    search_fields = ['nome']
    ordering = ['ordem', 'nome']

    def icone_preview(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icone, obj.icone)
    icone_preview.short_description = 'Ícone'

    def cor_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 2px 10px; border-radius: 4px;">&nbsp;</span> {}',
            obj.cor, obj.cor
        )
    cor_preview.short_description = 'Cor'


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'ativo']
    list_editable = ['ativo']


@admin.register(DespesaFixa)
class DespesaFixaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'valor_formatado', 'dia_vencimento', 'ativo']
    list_filter = ['categoria', 'ativo']
    list_editable = ['ativo']
    search_fields = ['descricao']
    ordering = ['dia_vencimento']

    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}"
    valor_formatado.short_description = 'Valor'


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'tipo', 'valor_formatado', 
                    'data_vencimento', 'status_badge', 'parcela_info']
    list_filter = ['status', 'tipo', 'categoria', 'data_vencimento']
    search_fields = ['descricao']
    date_hierarchy = 'data_vencimento'
    ordering = ['data_vencimento']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('descricao', 'categoria', 'tipo', 'valor')
        }),
        ('Vencimento e Pagamento', {
            'fields': ('data_vencimento', 'data_pagamento', 'status', 'forma_pagamento')
        }),
        ('Parcelamento', {
            'fields': ('parcela_atual', 'total_parcelas'),
            'classes': ('collapse',)
        }),
        ('Observações e Anexos', {
            'fields': ('observacoes', 'comprovante'),
            'classes': ('collapse',)
        }),
    )

    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}"
    valor_formatado.short_description = 'Valor'

    def status_badge(self, obj):
        cores = {
            'PENDENTE': '#ffc107',
            'PAGO': '#28a745',
            'ATRASADO': '#dc3545',
            'CANCELADO': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px;">{}</span>',
            cores.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def parcela_info(self, obj):
        if obj.total_parcelas > 1:
            return f"{obj.parcela_atual}/{obj.total_parcelas}"
        return "-"
    parcela_info.short_description = 'Parcela'


@admin.register(CompraParcelada)
class CompraParceladaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'valor_total_formatado', 
                    'numero_parcelas', 'valor_parcela_formatado', 'progresso']
    list_filter = ['categoria']
    search_fields = ['descricao']

    def valor_total_formatado(self, obj):
        return f"R$ {obj.valor_total:,.2f}"
    valor_total_formatado.short_description = 'Valor Total'

    def valor_parcela_formatado(self, obj):
        return f"R$ {obj.valor_parcela:,.2f}"
    valor_parcela_formatado.short_description = 'Valor Parcela'

    def progresso(self, obj):
        pagas = obj.parcelas.filter(status='PAGO').count()
        total = obj.numero_parcelas
        percent = (pagas / total * 100) if total > 0 else 0
        return format_html(
            '<div style="width:100px; background:#e9ecef; border-radius:4px;">'
            '<div style="width:{}%; background:#28a745; height:20px; border-radius:4px; text-align:center; color:white; font-size:11px; line-height:20px;">'
            '{}/{}</div></div>',
            percent, pagas, total
        )
    progresso.short_description = 'Progresso'


@admin.register(FaturamentoMensal)
class FaturamentoMensalAdmin(admin.ModelAdmin):
    list_display = ['periodo', 'valor_faturamento_formatado', 'aliquota_aplicada',
                    'valor_tributo_formatado', 'data_vencimento_tributo', 'tributo_status']
    list_filter = ['ano', 'tributo_gerado']
    ordering = ['-ano', '-mes']

    def periodo(self, obj):
        meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return f"{meses[obj.mes]}/{obj.ano}"
    periodo.short_description = 'Período'

    def valor_faturamento_formatado(self, obj):
        return f"R$ {obj.valor_faturamento:,.2f}"
    valor_faturamento_formatado.short_description = 'Faturamento'

    def valor_tributo_formatado(self, obj):
        return f"R$ {obj.valor_tributo:,.2f}"
    valor_tributo_formatado.short_description = 'Tributo'

    def tributo_status(self, obj):
        if obj.tributo_gerado:
            return format_html('<span style="color: #28a745;">✓ Gerado</span>')
        return format_html('<span style="color: #ffc107;">⏳ Pendente</span>')
    tributo_status.short_description = 'Status Tributo'