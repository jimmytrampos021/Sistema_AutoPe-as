# ============================================
# ESTOQUE/ADMIN.PY - VERSÃO FINAL CORRIGIDA
# ============================================

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Categoria, Subcategoria, Aplicacao, Fabricante, Fornecedor,
    Produto, MovimentacaoEstoque, HistoricoPreco,
    Montadora, VeiculoModelo, VeiculoVersao
)

# Verificar se CotacaoFornecedor existe
try:
    from .models import CotacaoFornecedor
    COTACAO_EXISTS = True
except ImportError:
    COTACAO_EXISTS = False


# ==========================================
# ADMIN: MONTADORA
# ==========================================
@admin.register(Montadora)
class MontadoraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'pais_origem', 'ordem', 'ativa', 'qtd_modelos']
    list_filter = ['ativa', 'pais_origem']
    search_fields = ['nome']
    list_editable = ['ordem', 'ativa']
    ordering = ['ordem', 'nome']
    
    def qtd_modelos(self, obj):
        return obj.modelos.count()
    qtd_modelos.short_description = 'Modelos'


# ==========================================
# ADMIN: VERSÃO INLINE
# ==========================================
class VeiculoVersaoInline(admin.TabularInline):
    model = VeiculoVersao
    extra = 1
    fields = ['nome', 'ano_inicial', 'ano_final', 'motorizacoes', 'ativo']


# ==========================================
# ADMIN: MODELO DE VEÍCULO
# ==========================================
@admin.register(VeiculoModelo)
class VeiculoModeloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'montadora', 'tipo', 'popular', 'ativo', 'qtd_versoes']
    list_filter = ['ativo', 'popular', 'tipo', 'montadora']
    search_fields = ['nome', 'montadora__nome']
    list_editable = ['popular', 'ativo']
    ordering = ['montadora__nome', 'nome']
    inlines = [VeiculoVersaoInline]
    
    def qtd_versoes(self, obj):
        return obj.versoes.count()
    qtd_versoes.short_description = 'Versões'


# ==========================================
# ADMIN: VERSÃO DO VEÍCULO
# ==========================================
@admin.register(VeiculoVersao)
class VeiculoVersaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modelo', 'montadora_nome', 'ano_inicial', 'ano_final', 'motorizacoes', 'ativo']
    list_filter = ['ativo', 'modelo__montadora', 'modelo']
    search_fields = ['nome', 'modelo__nome', 'modelo__montadora__nome', 'motorizacoes']
    list_editable = ['ativo']
    ordering = ['modelo__montadora__nome', 'modelo__nome', '-ano_inicial']
    
    def montadora_nome(self, obj):
        return obj.modelo.montadora.nome
    montadora_nome.short_description = 'Montadora'


# ==========================================
# ADMIN: SUBCATEGORIA INLINE
# ==========================================
class SubcategoriaInline(admin.TabularInline):
    model = Subcategoria
    extra = 1
    fields = ['nome', 'descricao', 'ativo']


# ==========================================
# ADMIN: FABRICANTE
# ==========================================
@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'pais_origem', 'site', 'telefone', 'email', 'ativo']
    list_filter = ['ativo', 'pais_origem']
    search_fields = ['nome', 'pais_origem']
    list_editable = ['ativo']
    ordering = ['nome']


# ==========================================
# ADMIN: CATEGORIA
# ==========================================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'qtd_subcategorias', 'qtd_produtos', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']
    inlines = [SubcategoriaInline]
    
    def descricao_curta(self, obj):
        if obj.descricao:
            return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
        return '-'
    descricao_curta.short_description = 'Descrição'
    
    def qtd_subcategorias(self, obj):
        return obj.subcategorias.count()
    qtd_subcategorias.short_description = 'Subcategorias'
    
    def qtd_produtos(self, obj):
        return obj.produtos.count()
    qtd_produtos.short_description = 'Produtos'


# ==========================================
# ADMIN: SUBCATEGORIA
# ==========================================
@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'qtd_produtos', 'ativo']
    list_filter = ['ativo', 'categoria']
    search_fields = ['nome', 'categoria__nome']
    list_editable = ['ativo']
    ordering = ['categoria__nome', 'nome']
    
    def qtd_produtos(self, obj):
        return obj.produtos.count()
    qtd_produtos.short_description = 'Produtos'


# ==========================================
# ADMIN: APLICAÇÃO
# ==========================================
@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'ano_inicial', 'ano_final', 'motor']
    list_filter = ['marca', 'ano_inicial']
    search_fields = ['marca', 'modelo', 'motor']
    ordering = ['marca', 'modelo', 'ano_inicial']


# ==========================================
# ADMIN: FORNECEDOR
# ==========================================
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = [
        'nome_fantasia', 'razao_social', 'cnpj', 'telefone', 
        'cidade', 'estado', 'classificacao_display', 'ativo'
    ]
    list_filter = ['ativo', 'estado', 'classificacao']
    search_fields = ['nome_fantasia', 'razao_social', 'cnpj', 'email']
    list_editable = ['ativo']
    ordering = ['nome_fantasia']
    
    def classificacao_display(self, obj):
        estrelas = '⭐' * (obj.classificacao or 0)
        return estrelas if estrelas else '-'
    classificacao_display.short_description = 'Classificação'


# ==========================================
# ADMIN: HISTÓRICO DE PREÇOS (INLINE)
# ==========================================
class HistoricoPrecoInline(admin.TabularInline):
    model = HistoricoPreco
    extra = 0
    can_delete = False
    readonly_fields = ['data_alteracao', 'usuario', 'preco_custo_anterior', 
                      'preco_custo_novo', 'preco_venda_anterior', 'preco_venda_novo']
    
    def has_add_permission(self, request, obj=None):
        return False


# ==========================================
# ADMIN: PRODUTO
# ==========================================
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'descricao_curta', 'categoria', 'fabricante',
        'estoque_badge', 'preco_display', 'ativo'
    ]
    
    list_filter = [
        'ativo', 'destaque', 'promocao', 'loja', 'categoria', 
        'subcategoria', 'fabricante'
    ]
    
    search_fields = [
        'codigo', 'codigo_sku', 'codigo_barras', 'referencia_fabricante',
        'descricao', 'aplicacao_generica'
    ]
    
    list_editable = ['ativo']
    
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    # ✅ CORRIGIDO: Apenas os campos ManyToMany que existem
    filter_horizontal = ['fornecedores_alternativos', 'versoes_compativeis']
    
    inlines = [HistoricoPrecoInline]
    
    fieldsets = (
        ('🏷️ Identificação', {
            'fields': (
                ('codigo', 'codigo_sku'),
                ('codigo_barras', 'referencia_fabricante'),
                'descricao',
                'descricao_detalhada'
            )
        }),
        ('📂 Categorização', {
            'fields': (
                ('categoria', 'subcategoria'),
                ('fabricante', 'fornecedor_principal'),
                'fornecedores_alternativos'
            )
        }),
        ('📍 Localização', {
            'fields': (
                ('loja', 'setor'),
                ('prateleira', 'divisao_prateleira'),
            ),
            'classes': ('collapse',)
        }),
        ('💰 Preços', {
            'fields': (
                'preco_custo',
                'preco_venda_dinheiro',
                'preco_venda_debito',
                'preco_venda_credito',
                ('preco_atacado', 'quantidade_minima_atacado'),
            )
        }),
        ('📦 Estoque', {
            'fields': (
                ('estoque_atual', 'estoque_reservado'),
                ('estoque_minimo', 'estoque_maximo'),
            )
        }),
        ('🚗 Compatibilidade', {
            'fields': (
                'versoes_compativeis',
                'aplicacao_generica'
            ),
            'classes': ('collapse',)
        }),
        ('⭐ Status', {
            'fields': (
                ('ativo', 'destaque', 'promocao'),
                'preco_promocional',
            )
        }),
        ('🖼️ Imagem', {
            'fields': ('imagem',),
            'classes': ('collapse',)
        }),
        ('📝 Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('📅 Datas', {
            'fields': (('data_cadastro', 'data_atualizacao'),),
            'classes': ('collapse',)
        }),
    )
    
    def descricao_curta(self, obj):
        return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
    descricao_curta.short_description = 'Descrição'
    
    def estoque_badge(self, obj):
        estoque = obj.estoque_atual or 0
        minimo = obj.estoque_minimo or 0
        if estoque <= 0:
            cor = 'danger'
        elif estoque <= minimo:
            cor = 'warning'
        else:
            cor = 'success'
        return format_html('<span class="badge bg-{}">{}</span>', cor, estoque)
    estoque_badge.short_description = 'Estoque'
    
    def preco_display(self, obj):
        preco = obj.preco_venda_dinheiro or 0
        return format_html('<span style="color: green;">R$ {:.2f}</span>', preco)
    preco_display.short_description = 'Preço'
    
    actions = ['ativar_produtos', 'desativar_produtos']
    
    @admin.action(description='✅ Ativar selecionados')
    def ativar_produtos(self, request, queryset):
        queryset.update(ativo=True)
    
    @admin.action(description='❌ Desativar selecionados')
    def desativar_produtos(self, request, queryset):
        queryset.update(ativo=False)


# ==========================================
# ADMIN: MOVIMENTAÇÃO DE ESTOQUE
# ==========================================
@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['data_movimentacao', 'tipo', 'produto', 'quantidade', 'motivo_curto']
    list_filter = ['tipo', 'data_movimentacao']
    search_fields = ['produto__codigo', 'produto__descricao', 'motivo']
    date_hierarchy = 'data_movimentacao'
    ordering = ['-data_movimentacao']
    readonly_fields = ['data_movimentacao']
    
    def motivo_curto(self, obj):
        if obj.motivo:
            return obj.motivo[:50] + '...' if len(obj.motivo) > 50 else obj.motivo
        return '-'
    motivo_curto.short_description = 'Motivo'


# ==========================================
# ADMIN: COTAÇÃO DE FORNECEDOR (se existir)
# ==========================================
if COTACAO_EXISTS:
    @admin.register(CotacaoFornecedor)
    class CotacaoFornecedorAdmin(admin.ModelAdmin):
        list_display = ['produto', 'fornecedor', 'preco_unitario', 'prazo_display', 'data_cotacao', 'ativo']
        list_filter = ['ativo', 'fornecedor', 'data_cotacao']
        search_fields = ['produto__codigo', 'produto__descricao', 'fornecedor__nome_fantasia']
        list_editable = ['ativo']
        ordering = ['-data_cotacao']
        
        def prazo_display(self, obj):
            dias = obj.prazo_entrega_dias or 0
            if dias == 0:
                return 'Imediato'
            return f'{dias} dias'
        prazo_display.short_description = 'Prazo'


# ==========================================
# ADMIN: HISTÓRICO DE PREÇOS
# ==========================================
@admin.register(HistoricoPreco)
class HistoricoPrecoAdmin(admin.ModelAdmin):
    list_display = ['data_alteracao', 'produto', 'preco_custo_anterior', 'preco_custo_novo', 'preco_venda_anterior', 'preco_venda_novo']
    list_filter = ['data_alteracao']
    search_fields = ['produto__codigo', 'produto__descricao']
    ordering = ['-data_alteracao']
    readonly_fields = ['data_alteracao', 'usuario']