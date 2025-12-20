"""
Admin do Módulo de Compras
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import NotaFiscalEntrada, ItemNotaEntrada, LogEntradaMercadoria


class ItemNotaEntradaInline(admin.TabularInline):
    model = ItemNotaEntrada
    extra = 0
    readonly_fields = ['valor_custo_unitario', 'conferido', 'divergencia']
    fields = [
        'numero_item', 'codigo_produto_fornecedor', 'descricao_nf',
        'quantidade', 'valor_unitario', 'valor_total',
        'produto', 'conferido', 'divergencia'
    ]
    raw_id_fields = ['produto']


class LogEntradaInline(admin.TabularInline):
    model = LogEntradaMercadoria
    extra = 0
    readonly_fields = ['acao', 'descricao', 'usuario', 'created_at']
    fields = ['acao', 'descricao', 'usuario', 'created_at']
    can_delete = False
    max_num = 0
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(NotaFiscalEntrada)
class NotaFiscalEntradaAdmin(admin.ModelAdmin):
    list_display = [
        'numero_nf', 'serie', 'fornecedor', 'data_entrada',
        'valor_total_display', 'status_display', 'tipo_entrada_display',
        'itens_info'
    ]
    list_filter = ['status', 'tipo_entrada', 'data_entrada', 'fornecedor']
    search_fields = ['numero_nf', 'chave_acesso', 'fornecedor__nome_fantasia']
    date_hierarchy = 'data_entrada'
    readonly_fields = [
        'chave_acesso', 'created_at', 'updated_at',
        'usuario_cadastro', 'usuario_conferencia', 'usuario_finalizacao',
        'data_conferencia', 'data_finalizacao'
    ]
    inlines = [ItemNotaEntradaInline, LogEntradaInline]
    raw_id_fields = ['fornecedor']
    
    fieldsets = (
        ('Dados da Nota', {
            'fields': (
                ('numero_nf', 'serie'),
                'chave_acesso',
                'natureza_operacao',
                ('data_emissao', 'data_entrada'),
                'fornecedor',
            )
        }),
        ('Valores', {
            'fields': (
                ('valor_produtos', 'valor_desconto'),
                ('valor_frete', 'valor_seguro'),
                ('valor_ipi', 'valor_icms_st'),
                'valor_outras_despesas',
                'valor_total',
            )
        }),
        ('Configurações de Entrada', {
            'fields': (
                ('atualizar_preco_custo', 'atualizar_preco_venda'),
                ('margem_padrao', 'ratear_frete'),
                'atualizar_cotacao',
            ),
            'classes': ('collapse',)
        }),
        ('Status e Controle', {
            'fields': (
                ('status', 'tipo_entrada'),
                'arquivo_xml',
                'observacoes',
            )
        }),
        ('Auditoria', {
            'fields': (
                ('usuario_cadastro', 'created_at'),
                ('usuario_conferencia', 'data_conferencia'),
                ('usuario_finalizacao', 'data_finalizacao'),
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def valor_total_display(self, obj):
        return f"R$ {obj.valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    valor_total_display.short_description = 'Valor Total'
    valor_total_display.admin_order_field = 'valor_total'
    
    def status_display(self, obj):
        colors = {
            'P': '#ffc107',  # Amarelo
            'E': '#17a2b8',  # Azul
            'C': '#28a745',  # Verde
            'F': '#6c757d',  # Cinza
            'X': '#dc3545',  # Vermelho
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def tipo_entrada_display(self, obj):
        icons = {
            'M': '✏️',
            'X': '📄',
            'A': '🔄',
        }
        return f"{icons.get(obj.tipo_entrada, '')} {obj.get_tipo_entrada_display()}"
    tipo_entrada_display.short_description = 'Tipo'
    
    def itens_info(self, obj):
        total = obj.total_itens
        vinculados = obj.itens_vinculados
        conferidos = obj.itens_conferidos
        
        if total == 0:
            return '-'
        
        return format_html(
            '<span title="Total: {}, Vinculados: {}, Conferidos: {}">'
            '{}/{}/{}</span>',
            total, vinculados, conferidos,
            total, vinculados, conferidos
        )
    itens_info.short_description = 'Itens (T/V/C)'


@admin.register(ItemNotaEntrada)
class ItemNotaEntradaAdmin(admin.ModelAdmin):
    list_display = [
        'nota', 'numero_item', 'descricao_nf', 'quantidade',
        'valor_unitario', 'produto', 'conferido_display'
    ]
    list_filter = ['conferido', 'divergencia', 'nota__status']
    search_fields = ['descricao_nf', 'codigo_produto_fornecedor', 'nota__numero_nf']
    raw_id_fields = ['nota', 'produto']
    
    def conferido_display(self, obj):
        if obj.conferido:
            if obj.divergencia:
                return format_html('<span style="color: orange;">✓ (divergência)</span>')
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    conferido_display.short_description = 'Conferido'


@admin.register(LogEntradaMercadoria)
class LogEntradaMercadoriaAdmin(admin.ModelAdmin):
    list_display = ['nota', 'acao', 'descricao_curta', 'usuario', 'created_at']
    list_filter = ['acao', 'created_at']
    search_fields = ['nota__numero_nf', 'descricao']
    readonly_fields = ['nota', 'item', 'acao', 'descricao', 'dados_json', 'usuario', 'created_at']
    
    def descricao_curta(self, obj):
        if len(obj.descricao) > 60:
            return obj.descricao[:60] + '...'
        return obj.descricao
    descricao_curta.short_description = 'Descrição'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
