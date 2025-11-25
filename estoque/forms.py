# ============================================
# ESTOQUE/FORMS.PY - CORRIGIDO
# ✅ Apenas DESCRIÇÃO é obrigatória
# ✅ Código gerado automaticamente se vazio
# ============================================

from django import forms
from decimal import Decimal
from estoque.models import Produto, Categoria, Subcategoria, Fabricante, Fornecedor


class ProdutoForm(forms.ModelForm):
    """
    Formulário completo para cadastro de produtos
    ✅ CORRIGIDO: Apenas 'descricao' é obrigatória
    ✅ Todos os outros campos são opcionais
    """
    
    class Meta:
        model = Produto
        fields = [
            # Identificação
            'codigo', 'codigo_sku', 'codigo_barras', 'referencia_fabricante',
            'descricao', 'descricao_detalhada',
            
            # Categorização
            'categoria', 'subcategoria', 'fabricante', 'fornecedor_principal',
            
            # Localização
            'loja', 'setor', 'prateleira', 'divisao_prateleira',
            
            # Preços
            'preco_custo', 'preco_venda_dinheiro', 'preco_venda_debito',
            'preco_venda_credito', 'preco_atacado', 'quantidade_minima_atacado',
            
            # Estoque
            'estoque_atual', 'estoque_minimo', 'estoque_maximo',
            
            # Aplicação
            'aplicacao_generica',
            
            # Características
            'peso', 'comprimento', 'largura', 'altura',
            
            # Comercial
            'ncm', 'unidade_medida', 'garantia_meses',
            
            # Status
            'ativo', 'destaque', 'promocao', 'preco_promocional',
            
            # Imagem
            'imagem',
            
            # Observações
            'observacoes',
        ]
        
        widgets = {
            # ========== IDENTIFICAÇÃO ==========
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gerado automaticamente se vazio',
            }),
            'codigo_sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU do produto (opcional)',
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EAN / Código de barras (opcional)',
            }),
            'referencia_fabricante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código original (opcional)',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto *OBRIGATÓRIO*',
                'required': True,
            }),
            'descricao_detalhada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição completa (opcional)',
            }),
            
            # ========== CATEGORIZAÇÃO ==========
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'subcategoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fabricante': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fornecedor_principal': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            # ========== LOCALIZAÇÃO ==========
            'loja': forms.Select(attrs={
                'class': 'form-select',
            }),
            'setor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Motor, Suspensão (opcional)',
            }),
            'prateleira': forms.Select(attrs={
                'class': 'form-select',
            }),
            'divisao_prateleira': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: A1, B2, C3 (opcional)',
            }),
            
            # ========== PREÇOS ==========
            'preco_custo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'preco_venda_dinheiro': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'preco_venda_debito': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'preco_venda_credito': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'preco_atacado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'quantidade_minima_atacado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10',
                'min': '1',
            }),
            'preco_promocional': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            
            # ========== ESTOQUE ==========
            'estoque_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            'estoque_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            'estoque_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            
            # ========== APLICAÇÃO ==========
            'aplicacao_generica': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ex: Universal, Linha VW, etc (opcional)',
            }),
            
            # ========== CARACTERÍSTICAS ==========
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.000',
                'step': '0.001',
                'min': '0',
            }),
            'comprimento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'largura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            
            # ========== COMERCIAL ==========
            'ncm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 8708.30.19 (opcional)',
            }),
            'unidade_medida': forms.Select(attrs={
                'class': 'form-select',
            }),
            'garantia_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            
            # ========== STATUS ==========
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'destaque': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'promocao': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            # ========== IMAGEM ==========
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            
            # ========== OBSERVAÇÕES ==========
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ IMPORTANTE: Tornar TODOS os campos opcionais EXCETO descrição
        for field_name, field in self.fields.items():
            if field_name == 'descricao':
                field.required = True  # Único obrigatório
            else:
                field.required = False  # Todos os outros são opcionais
        
        # Configurar querysets para campos de relacionamento
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        self.fields['categoria'].empty_label = "Selecione uma categoria (opcional)"
        
        self.fields['fabricante'].queryset = Fabricante.objects.filter(ativo=True).order_by('nome')
        self.fields['fabricante'].empty_label = "Selecione um fabricante (opcional)"
        
        self.fields['fornecedor_principal'].queryset = Fornecedor.objects.filter(ativo=True).order_by('nome_fantasia')
        self.fields['fornecedor_principal'].empty_label = "Selecione um fornecedor (opcional)"
        
        # Filtrar subcategorias pela categoria selecionada
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(
                    categoria_id=categoria_id,
                    ativo=True
                ).order_by('nome')
            except (ValueError, TypeError):
                self.fields['subcategoria'].queryset = Subcategoria.objects.none()
        elif self.instance.pk and self.instance.categoria:
            self.fields['subcategoria'].queryset = self.instance.categoria.subcategorias.filter(
                ativo=True
            ).order_by('nome')
        else:
            self.fields['subcategoria'].queryset = Subcategoria.objects.none()
        
        self.fields['subcategoria'].empty_label = "Selecione uma subcategoria (opcional)"
    
    def clean_descricao(self):
        """Validar descrição (único campo obrigatório)"""
        descricao = self.cleaned_data.get('descricao')
        
        if not descricao or not descricao.strip():
            raise forms.ValidationError('A descrição do produto é obrigatória!')
        
        return descricao.strip()
    
    def clean_codigo(self):
        """
        Validar código - gerar automaticamente se não informado
        """
        codigo = self.cleaned_data.get('codigo')
        
        # Se não informou código, retorna None (será gerado no save do model)
        if not codigo or not codigo.strip():
            return None
        
        codigo = codigo.strip().upper()
        
        # Verificar se já existe (exceto se estiver editando)
        if Produto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um produto com este código!')
        
        return codigo
    
    def clean_codigo_sku(self):
        """Validar SKU - pode ser vazio"""
        codigo_sku = self.cleaned_data.get('codigo_sku')
        
        if not codigo_sku or not codigo_sku.strip():
            return None
        
        codigo_sku = codigo_sku.strip().upper()
        
        # Verificar duplicidade
        if Produto.objects.filter(codigo_sku=codigo_sku).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um produto com este SKU!')
        
        return codigo_sku
    
    def clean_preco_custo(self):
        """Garantir valor default para preço de custo"""
        preco = self.cleaned_data.get('preco_custo')
        return preco if preco is not None else Decimal('0.00')
    
    def clean_preco_venda_dinheiro(self):
        """Garantir valor default para preço de venda"""
        preco = self.cleaned_data.get('preco_venda_dinheiro')
        return preco if preco is not None else Decimal('0.00')
    
    def clean_estoque_atual(self):
        """Garantir valor default para estoque"""
        estoque = self.cleaned_data.get('estoque_atual')
        return estoque if estoque is not None else 0
    
    def clean_estoque_minimo(self):
        """Garantir valor default para estoque mínimo"""
        estoque = self.cleaned_data.get('estoque_minimo')
        return estoque if estoque is not None else 0
    
    def clean_estoque_maximo(self):
        """Garantir valor default para estoque máximo"""
        estoque = self.cleaned_data.get('estoque_maximo')
        return estoque if estoque is not None else 0
    
    def clean(self):
        """Validações gerais do formulário"""
        cleaned_data = super().clean()
        
        # Validar preços (apenas se ambos forem informados)
        preco_custo = cleaned_data.get('preco_custo')
        preco_venda = cleaned_data.get('preco_venda_dinheiro')
        
        if preco_custo and preco_venda and preco_custo > 0 and preco_venda > 0:
            if preco_venda < preco_custo:
                self.add_error(
                    'preco_venda_dinheiro', 
                    'Aviso: O preço de venda está menor que o custo!'
                )
        
        # Validar estoque (apenas se ambos forem informados e > 0)
        estoque_min = cleaned_data.get('estoque_minimo') or 0
        estoque_max = cleaned_data.get('estoque_maximo') or 0
        
        if estoque_min > 0 and estoque_max > 0:
            if estoque_max < estoque_min:
                self.add_error(
                    'estoque_maximo', 
                    'Estoque máximo deve ser maior que o mínimo!'
                )
        
        return cleaned_data


# ============================================
# FORMULÁRIO SIMPLIFICADO PARA CADASTRO RÁPIDO
# ============================================

class ProdutoSimplificadoForm(forms.ModelForm):
    """
    Formulário simplificado para cadastro rápido de produtos
    Apenas campos essenciais
    """
    
    class Meta:
        model = Produto
        fields = [
            'descricao',
            'categoria',
            'preco_venda_dinheiro',
            'estoque_atual',
        ]
        
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nome do produto *',
                'required': True,
                'autofocus': True,
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'preco_venda_dinheiro': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
            'estoque_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apenas descrição é obrigatória
        self.fields['descricao'].required = True
        self.fields['categoria'].required = False
        self.fields['preco_venda_dinheiro'].required = False
        self.fields['estoque_atual'].required = False
        
        # Configurar categoria
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        self.fields['categoria'].empty_label = "Sem categoria"
    
    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if not descricao or not descricao.strip():
            raise forms.ValidationError('A descrição é obrigatória!')
        return descricao.strip()
    """
    Formulário completo para cadastro de produtos
    ✅ CORRIGIDO: Apenas 'descricao' é obrigatória
    """
    
    class Meta:
        model = Produto
        fields = [
            # Identificação
            'codigo', 'codigo_sku', 'codigo_barras', 'referencia_fabricante',
            'descricao', 'descricao_detalhada',
            
            # Categorização
            'categoria', 'subcategoria', 'fabricante', 'fornecedor_principal',
            
            # Localização
            'loja', 'setor', 'prateleira', 'divisao_prateleira',
            
            # Preços
            'preco_custo', 'preco_venda_dinheiro', 'preco_venda_debito',
            'preco_venda_credito', 'preco_atacado', 'quantidade_minima_atacado',
            
            # Estoque
            'estoque_atual', 'estoque_minimo', 'estoque_maximo',
            
            # Aplicação (será tratada via ManyToMany separadamente)
            'aplicacao_generica',
            
            # Características
            'peso', 'comprimento', 'largura', 'altura',
            
            # Comercial
            'ncm', 'unidade_medida', 'garantia_meses',
            
            # Status
            'ativo', 'destaque', 'promocao', 'preco_promocional',
            
            # Imagem
            'imagem',
            
            # Observações
            'observacoes',
        ]
        
        widgets = {
            # Identificação
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Será gerado automaticamente se vazio',
            }),
            'codigo_sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU do produto (opcional)',
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EAN / Código de barras (opcional)',
            }),
            'referencia_fabricante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código original (opcional)',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto *OBRIGATÓRIO*',
                'required': True,
            }),
            'descricao_detalhada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição completa (opcional)',
            }),
            
            # Categorização
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'subcategoria': forms.Select(attrs={'class': 'form-select'}),
            'fabricante': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor_principal': forms.Select(attrs={'class': 'form-select'}),
            
            # Localização
            'loja': forms.Select(attrs={'class': 'form-select'}),
            'setor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Motor, Suspensão (opcional)',
            }),
            'prateleira': forms.Select(attrs={'class': 'form-select'}),
            'divisao_prateleira': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: A1, B2, C3 (opcional)',
            }),
            
            # Preços
            'preco_custo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00',
            }),
            'preco_venda_dinheiro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00',
            }),
            'preco_venda_debito': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00',
            }),
            'preco_venda_credito': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00',
            }),
            'preco_atacado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00',
            }),
            'quantidade_minima_atacado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10',
                'value': '10',
            }),
            'preco_promocional': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
            }),
            
            # Estoque
            'estoque_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'value': '0',
            }),
            'estoque_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '5',
                'value': '5',
            }),
            'estoque_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100',
                'value': '100',
            }),
            
            # Aplicação
            'aplicacao_generica': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ex: VW Gol Voyage Fox 2008-2023 1.0 1.6 (opcional)',
            }),
            
            # Características
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'placeholder': '0.000 kg',
            }),
            'comprimento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00 cm',
            }),
            'largura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00 cm',
            }),
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00 cm',
            }),
            
            # Comercial
            'ncm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000.00.00 (opcional)',
            }),
            'unidade_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UN',
                'value': 'UN',
            }),
            'garantia_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3',
                'value': '3',
            }),
            
            # Status
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'checked': True}),
            'destaque': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'promocao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Imagem
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            
            # Observações
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ CORRIGIDO: Apenas 'descricao' é obrigatória
        # Todos os outros campos são opcionais
        for field_name, field in self.fields.items():
            if field_name != 'descricao':
                field.required = False
        
        # Garantir que descricao é obrigatória
        self.fields['descricao'].required = True
        
        # Filtrar subcategorias pela categoria selecionada
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(
                    categoria_id=categoria_id,
                    ativo=True
                ).order_by('nome')
            except (ValueError, TypeError):
                self.fields['subcategoria'].queryset = Subcategoria.objects.none()
        elif self.instance.pk and self.instance.categoria:
            self.fields['subcategoria'].queryset = self.instance.categoria.subcategorias.filter(
                ativo=True
            ).order_by('nome')
        else:
            self.fields['subcategoria'].queryset = Subcategoria.objects.none()
    
    def clean_descricao(self):
        """Validar descrição (único campo obrigatório)"""
        descricao = self.cleaned_data.get('descricao')
        
        if not descricao or not descricao.strip():
            raise forms.ValidationError('A descrição do produto é obrigatória!')
        
        return descricao.strip()
    
    def clean_codigo(self):
        """Gerar código automaticamente se não informado"""
        codigo = self.cleaned_data.get('codigo')
        
        # Se não informou código, gerar automaticamente
        if not codigo:
            # Pegar último código e incrementar
            ultimo_produto = Produto.objects.order_by('-id').first()
            if ultimo_produto and ultimo_produto.codigo.isdigit():
                proximo_numero = int(ultimo_produto.codigo) + 1
            else:
                proximo_numero = 1
            
            codigo = str(proximo_numero).zfill(6)  # Ex: 000001
        
        # Verificar se já existe (exceto se estiver editando)
        if Produto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um produto com este código!')
        
        return codigo.upper()
    
    def clean(self):
        """Validações gerais"""
        cleaned_data = super().clean()
        
        # Validar preços (se informados)
        preco_custo = cleaned_data.get('preco_custo') or 0
        preco_venda = cleaned_data.get('preco_venda_dinheiro') or 0
        
        if preco_custo > 0 and preco_venda > 0:
            if preco_venda <= preco_custo:
                self.add_error('preco_venda_dinheiro', 
                    'O preço de venda deve ser maior que o preço de custo!')
        
        # Validar estoque
        estoque_min = cleaned_data.get('estoque_minimo') or 0
        estoque_max = cleaned_data.get('estoque_maximo') or 0
        
        if estoque_max > 0 and estoque_min > 0:
            if estoque_max <= estoque_min:
                self.add_error('estoque_maximo',
                    'O estoque máximo deve ser maior que o estoque mínimo!')
        
        return cleaned_data