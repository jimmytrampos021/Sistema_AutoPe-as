from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from decimal import Decimal
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
     # ADICIONE ESTA LINHA:
    change_form_template = 'admin/estoque/produto/change_form.html'
    list_display = [
        'codigo', 'descricao_curta', 'categoria', 'fabricante',
        'estoque_badge', 'preco_display', 'tem_customizacao', 'ativo'
    ]
    
    list_filter = [
        'ativo', 'destaque', 'promocao', 'loja', 'categoria', 
        'subcategoria', 'fabricante', 'aplicar_imposto_4', 'preco_customizado_cartao'
    ]
    
    search_fields = [
        'codigo', 'codigo_sku', 'codigo_barras', 'referencia_fabricante',
        'descricao', 'aplicacao_generica'
    ]
    
    list_editable = ['ativo']
    
    readonly_fields = ['data_cadastro', 'data_atualizacao', 'preview_precos_cartao']
    
    filter_horizontal = ['fornecedores_alternativos', 'versoes_compativeis']
    
    inlines = [HistoricoPrecoInline]
    
    # Ações personalizadas
    actions = ['gerar_precos_automaticos', 'ativar_imposto_4', 'desativar_imposto_4']
    
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
        ('💰 Preços Base', {
            'fields': (
                'preco_custo',
                'preco_venda_dinheiro',
                'preco_venda_debito',
                'preco_venda_credito',
                ('preco_atacado', 'quantidade_minima_atacado'),
            ),
            'description': 'Preços básicos do produto. O preço à vista é usado como base para cálculos.'
        }),
        ('💳 Configuração de Cartão e Impostos', {
            'fields': (
                'aplicar_imposto_4',
                'preco_customizado_cartao',
            ),
            'description': mark_safe(
                '<strong>Imposto 4%:</strong> Marca se este produto tem imposto de Simples Nacional embutido.<br>'
                '<strong>Preços Customizados:</strong> Se marcado, você define preços manualmente por parcela. '
                'Se desmarcado, o sistema calcula automaticamente usando as taxas da tabela.'
            )
        }),
        ('💳 Preços Customizados no Crédito (2x a 12x)', {
            'fields': (
                ('preco_credito_2x', 'preco_credito_3x', 'preco_credito_4x'),
                ('preco_credito_5x', 'preco_credito_6x', 'preco_credito_7x'),
                ('preco_credito_8x', 'preco_credito_9x', 'preco_credito_10x'),
                ('preco_credito_11x', 'preco_credito_12x'),
            ),
            'classes': ('collapse',),
            'description': mark_safe(
                '⚠️ <strong>Estes campos só são usados se "Preços Customizados" estiver marcado.</strong><br>'
                'Deixe em branco para usar cálculo automático com as taxas da tabela.<br>'
                'Exemplo: Se você quer vender em 3x por R$ 120,00, preencha apenas o campo "3x" com 120.00'
            )
        }),
        ('📊 Visualização de Preços', {
            'fields': ('preview_precos_cartao',),
            'classes': ('collapse',),
            'description': 'Visualize todos os preços calculados para este produto.'
        }),
        ('📦 Estoque', {
            'fields': (
                ('estoque_atual', 'estoque_reservado'),
                ('estoque_minimo', 'estoque_maximo'),
                'quantidade_reposicao',
            )
        }),
        ('🚗 Aplicação/Compatibilidade', {
            'fields': (
                'versoes_compativeis',
                'aplicacao_generica',
            ),
            'classes': ('collapse',)
        }),
        ('📏 Características Físicas', {
            'fields': (
                ('peso', 'unidade_medida'),
                ('comprimento', 'largura', 'altura'),
            ),
            'classes': ('collapse',)
        }),
        ('📄 Informações Comerciais', {
            'fields': (
                ('ncm', 'garantia_meses'),
            ),
            'classes': ('collapse',)
        }),
        ('⭐ Status e Promoções', {
            'fields': (
                ('ativo', 'destaque', 'promocao'),
                'preco_promocional',
            )
        }),
        ('🖼️ Mídia', {
            'fields': ('imagem',),
            'classes': ('collapse',)
        }),
        ('📝 Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('📅 Controle', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    # ========== MÉTODOS PERSONALIZADOS ==========
    
    def descricao_curta(self, obj):
        """Trunca descrição para exibição"""
        if len(obj.descricao) > 50:
            return obj.descricao[:50] + '...'
        return obj.descricao
    descricao_curta.short_description = 'Descrição'
    
    def estoque_badge(self, obj):
        """Badge colorido do estoque"""
        situacao = obj.situacao_estoque
        
        if situacao == 'zerado':
            badge_class = 'danger'
            icon = '❌'
            texto = 'ZERADO'
        elif situacao == 'critico':
            badge_class = 'warning'
            icon = '⚠️'
            texto = 'CRÍTICO'
        elif situacao == 'baixo':
            badge_class = 'info'
            icon = '📦'
            texto = 'BAIXO'
        else:
            badge_class = 'success'
            icon = '✅'
            texto = 'OK'
        
        return format_html(
            '<span class="badge badge-{}" style="background-color: var(--bs-{});">{} {} ({} un)</span>',
            badge_class,
            badge_class,
            icon,
            texto,
            obj.estoque_atual or 0
        )
    estoque_badge.short_description = 'Estoque'
    
    def preco_display(self, obj):
        """Exibe preço à vista formatado"""
        if obj.preco_venda_dinheiro:
            return format_html(
                '<strong style="color: #28a745;">R$ {}</strong>',
                obj.preco_venda_dinheiro
            )
        return '-'
    preco_display.short_description = 'Preço À Vista'
    
    def tem_customizacao(self, obj):
        """Indica se tem preços customizados ou imposto"""
        badges = []
        
        if obj.preco_customizado_cartao:
            badges.append('<span style="background: #0d6efd; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem;">💳 Custom</span>')
        
        if obj.aplicar_imposto_4:
            badges.append('<span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem;">📊 4%</span>')
        
        return mark_safe(' '.join(badges)) if badges else '-'
    tem_customizacao.short_description = 'Config'
    
    def preview_precos_cartao(self, obj):
        """
        Mostra preview de todos os preços de cartão calculados
        """
        if not obj.pk or not obj.preco_venda_dinheiro:
            return mark_safe('<p style="color: #6c757d;">Salve o produto com um preço à vista para ver os cálculos.</p>')
        
        try:
            precos = obj.get_todos_precos_cartao()
            
            html = '<div style="font-family: monospace; background: #f8f9fa; padding: 15px; border-radius: 8px;">'
            html += '<h4 style="margin-top: 0;">💳 Todos os Preços Calculados</h4>'
            
            # Tabela de preços
            html += '<table style="width: 100%; border-collapse: collapse;">'
            html += '<thead><tr style="background: #e9ecef;">'
            html += '<th style="padding: 8px; text-align: left;">Forma de Pagamento</th>'
            html += '<th style="padding: 8px; text-align: right;">Preço Final</th>'
            html += '<th style="padding: 8px; text-align: center;">Tipo</th>'
            html += '</tr></thead><tbody>'
            
            # PIX
            html += '<tr style="border-bottom: 1px solid #dee2e6;">'
            html += f'<td style="padding: 8px;">💰 PIX</td>'
            html += f'<td style="padding: 8px; text-align: right; font-weight: bold; color: #28a745;">R$ {precos["pix"]:.2f}</td>'
            html += '<td style="padding: 8px; text-align: center;"><span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem;">Sem taxa</span></td>'
            html += '</tr>'
            
            # Dinheiro
            html += '<tr style="border-bottom: 1px solid #dee2e6;">'
            html += f'<td style="padding: 8px;">💵 Dinheiro</td>'
            html += f'<td style="padding: 8px; text-align: right; font-weight: bold; color: #28a745;">R$ {precos["dinheiro"]:.2f}</td>'
            html += '<td style="padding: 8px; text-align: center;"><span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem;">Sem taxa</span></td>'
            html += '</tr>'
            
            # Débito
            html += '<tr style="border-bottom: 1px solid #dee2e6;">'
            html += f'<td style="padding: 8px;">💳 Débito</td>'
            html += f'<td style="padding: 8px; text-align: right; font-weight: bold; color: #0d6efd;">R$ {precos["debito"]:.2f}</td>'
            html += '<td style="padding: 8px; text-align: center;"><span style="background: #0d6efd; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem;">Auto</span></td>'
            html += '</tr>'
            
            # Crédito (todas as parcelas)
            for parcela, preco in precos['credito'].items():
                # Verifica se é customizado
                campo_custom = f'preco_credito_{parcela}x'
                tem_custom = obj.preco_customizado_cartao and getattr(obj, campo_custom, None) and getattr(obj, campo_custom) > 0
                
                badge_tipo = 'Custom' if tem_custom else 'Auto'
                badge_color = '#6f42c1' if tem_custom else '#0d6efd'
                
                html += '<tr style="border-bottom: 1px solid #dee2e6;">'
                html += f'<td style="padding: 8px;">💳 Crédito {parcela}x</td>'
                html += f'<td style="padding: 8px; text-align: right; font-weight: bold; color: {badge_color};">R$ {preco:.2f}</td>'
                html += f'<td style="padding: 8px; text-align: center;"><span style="background: {badge_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem;">{badge_tipo}</span></td>'
                html += '</tr>'
            
            html += '</tbody></table>'
            
            # Legenda
            html += '<div style="margin-top: 15px; padding: 10px; background: #fff3cd; border-radius: 5px;">'
            html += '<strong>📌 Legenda:</strong><br>'
            html += '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem; margin-right: 5px;">Sem taxa</span> PIX e Dinheiro<br>'
            html += '<span style="background: #0d6efd; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem; margin-right: 5px;">Auto</span> Calculado automaticamente com taxa da tabela<br>'
            html += '<span style="background: #6f42c1; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem; margin-right: 5px;">Custom</span> Preço customizado definido manualmente'
            
            if obj.aplicar_imposto_4:
                html += '<br><br><strong style="color: #dc3545;">⚠️ Imposto 4% ESTÁ ATIVO:</strong> Todos os preços acima já incluem o imposto de 4%.'
            
            html += '</div>'
            
            html += '</div>'
            
            return mark_safe(html)
            
        except Exception as e:
            return mark_safe(f'<p style="color: #dc3545;">Erro ao calcular preços: {str(e)}</p>')
    
    preview_precos_cartao.short_description = 'Preview de Preços'
    
    # ========== AÇÕES EM LOTE ==========
    
    def gerar_precos_automaticos(self, request, queryset):
        """Gera preços automáticos de débito e crédito para produtos selecionados"""
        count = 0
        for produto in queryset:
            if produto.preco_venda_dinheiro and produto.preco_venda_dinheiro > 0:
                produto.preencher_precos_automaticos()
                produto.save()
                count += 1
        
        self.message_user(
            request,
            f'{count} produto(s) tiveram seus preços de débito e crédito calculados automaticamente!'
        )
    gerar_precos_automaticos.short_description = ' Gerar preços automáticos de cartão'
    
    def ativar_imposto_4(self, request, queryset):
        """Ativa imposto de 4% nos produtos selecionados"""
        count = queryset.update(aplicar_imposto_4=True)
        self.message_user(
            request,
            f'Imposto de 4% ATIVADO em {count} produto(s)!'
        )
    ativar_imposto_4.short_description = ' Ativar imposto 4%%'
    
    def desativar_imposto_4(self, request, queryset):
        """Desativa imposto de 4% nos produtos selecionados"""
        count = queryset.update(aplicar_imposto_4=False)
        self.message_user(
            request,
            f'Imposto de 4% DESATIVADO em {count} produto(s)!'
        )
    desativar_imposto_4.short_description = ' Desativar imposto 4%%'
    
    # ========== CONFIGURAÇÕES ADICIONAIS ==========
    
    class Media:
        css = {
            'all': ('admin/css/precos_customizados.css',)
        }
        js = ('admin/js/precos_customizados.js',)
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