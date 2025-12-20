"""
Forms do Módulo de Compras
"""

from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal

from .models import NotaFiscalEntrada, ItemNotaEntrada


class ImportarXMLForm(forms.Form):
    """Formulário para importação de XML de NF-e"""
    
    arquivo_xml = forms.FileField(
        label='Arquivo XML',
        help_text='Selecione o arquivo XML da NF-e',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xml'
        })
    )
    
    atualizar_preco_custo = forms.BooleanField(
        label='Atualizar preço de custo dos produtos',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    atualizar_preco_venda = forms.BooleanField(
        label='Recalcular preço de venda (baseado na margem)',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    margem_padrao = forms.DecimalField(
        label='Margem de lucro (%)',
        required=False,
        initial=Decimal('50.00'),
        min_value=Decimal('0'),
        max_value=Decimal('500'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'style': 'width: 120px;'
        })
    )
    
    ratear_frete = forms.BooleanField(
        label='Ratear frete no custo dos produtos',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    atualizar_cotacao = forms.BooleanField(
        label='Atualizar cotação do fornecedor',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_arquivo_xml(self):
        arquivo = self.cleaned_data.get('arquivo_xml')
        
        if arquivo:
            # Verifica extensão
            if not arquivo.name.lower().endswith('.xml'):
                raise ValidationError('O arquivo deve ter extensão .xml')
            
            # Verifica tamanho (máximo 5MB)
            if arquivo.size > 5 * 1024 * 1024:
                raise ValidationError('O arquivo não pode exceder 5MB')
        
        return arquivo


class ImportarPDFForm(forms.Form):
    """Formulário para importação de PDF de pedido"""
    
    arquivo_pdf = forms.FileField(
        label='Arquivo PDF',
        help_text='Selecione o PDF do pedido do fornecedor',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        })
    )
    
    atualizar_preco_custo = forms.BooleanField(
        label='Atualizar preço de custo dos produtos',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    atualizar_preco_venda = forms.BooleanField(
        label='Recalcular preço de venda (baseado na margem)',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    margem_padrao = forms.DecimalField(
        label='Margem de lucro (%)',
        required=False,
        initial=Decimal('50.00'),
        min_value=Decimal('0'),
        max_value=Decimal('500'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'style': 'width: 120px;'
        })
    )
    
    ratear_frete = forms.BooleanField(
        label='Ratear frete no custo dos produtos',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    atualizar_cotacao = forms.BooleanField(
        label='Atualizar cotação do fornecedor',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_arquivo_pdf(self):
        arquivo = self.cleaned_data.get('arquivo_pdf')
        
        if arquivo:
            # Verifica extensão
            if not arquivo.name.lower().endswith('.pdf'):
                raise ValidationError('O arquivo deve ter extensão .pdf')
            
            # Verifica tamanho (máximo 10MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise ValidationError('O arquivo não pode exceder 10MB')
        
        return arquivo


class NotaFiscalEntradaManualForm(forms.ModelForm):
    """Formulário para entrada manual de nota fiscal"""
    
    class Meta:
        model = NotaFiscalEntrada
        fields = [
            'numero_nf', 'serie', 'chave_acesso', 'natureza_operacao',
            'data_emissao', 'data_entrada', 'fornecedor',
            'valor_produtos', 'valor_frete', 'valor_seguro',
            'valor_desconto', 'valor_outras_despesas',
            'valor_ipi', 'valor_icms_st', 'valor_total',
            'atualizar_preco_custo', 'atualizar_preco_venda',
            'margem_padrao', 'ratear_frete', 'atualizar_cotacao',
            'observacoes'
        ]
        widgets = {
            'numero_nf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da NF'
            }),
            'serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'style': 'width: 80px;'
            }),
            'chave_acesso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '44 dígitos da chave de acesso',
                'maxlength': '44'
            }),
            'natureza_operacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'COMPRA PARA REVENDA'
            }),
            'data_emissao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_entrada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'valor_produtos': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_frete': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_seguro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_desconto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_outras_despesas': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_ipi': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_icms_st': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'atualizar_preco_custo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'atualizar_preco_venda': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'margem_padrao': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'width: 120px;'
            }),
            'ratear_frete': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'atualizar_cotacao': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class ItemNotaEntradaForm(forms.ModelForm):
    """Formulário para adicionar item manualmente"""
    
    class Meta:
        model = ItemNotaEntrada
        fields = [
            'codigo_produto_fornecedor', 'codigo_barras_nf', 'descricao_nf',
            'ncm', 'cfop', 'unidade', 'quantidade', 'valor_unitario',
            'valor_desconto', 'valor_ipi', 'valor_icms_st'
        ]
        widgets = {
            'codigo_produto_fornecedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código do fornecedor'
            }),
            'codigo_barras_nf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EAN/GTIN'
            }),
            'descricao_nf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do produto'
            }),
            'ncm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NCM',
                'style': 'width: 120px;'
            }),
            'cfop': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CFOP',
                'style': 'width: 80px;'
            }),
            'unidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UN',
                'style': 'width: 80px;'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'style': 'width: 120px;'
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'style': 'width: 120px;'
            }),
            'valor_desconto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'width: 100px;'
            }),
            'valor_ipi': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'width: 100px;'
            }),
            'valor_icms_st': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'width: 100px;'
            }),
        }


class ConferirItemForm(forms.Form):
    """Formulário para conferência de item"""
    
    quantidade_conferida = forms.DecimalField(
        label='Quantidade Conferida',
        min_value=Decimal('0'),
        decimal_places=4,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.0001',
            'autofocus': True
        })
    )
    
    observacao = forms.CharField(
        label='Observação',
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Observação da conferência'
        })
    )


class VincularProdutoForm(forms.Form):
    """Formulário para vincular produto ao item"""
    
    produto_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    
    termo_busca = forms.CharField(
        label='Buscar Produto',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite código, código de barras ou descrição...',
            'autocomplete': 'off'
        })
    )


class CadastrarProdutoForm(forms.Form):
    """Formulário para cadastrar novo produto a partir do item"""
    
    from estoque.models import Categoria, Fabricante
    
    categoria_id = forms.ChoiceField(
        label='Categoria',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fabricante_id = forms.ChoiceField(
        label='Fabricante',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    preco_venda = forms.DecimalField(
        label='Preço de Venda',
        min_value=Decimal('0'),
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    estoque_minimo = forms.IntegerField(
        label='Estoque Mínimo',
        initial=1,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 100px;'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from estoque.models import Categoria, Fabricante
        
        self.fields['categoria_id'].choices = [
            (c.id, c.nome) for c in Categoria.objects.all().order_by('nome')
        ]
        self.fields['fabricante_id'].choices = [
            (f.id, f.nome) for f in Fabricante.objects.all().order_by('nome')
        ]


class FiltroEntradasForm(forms.Form):
    """Formulário para filtrar listagem de entradas"""
    
    STATUS_CHOICES = [
        ('', 'Todos'),
        ('P', 'Pendente'),
        ('E', 'Em Conferência'),
        ('C', 'Conferida'),
        ('F', 'Finalizada'),
        ('X', 'Cancelada'),
    ]
    
    TIPO_CHOICES = [
        ('', 'Todos'),
        ('M', 'Manual'),
        ('X', 'XML'),
        ('A', 'Automático'),
    ]
    
    data_inicio = forms.DateField(
        label='Data Início',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    data_fim = forms.DateField(
        label='Data Fim',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    status = forms.ChoiceField(
        label='Status',
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo_entrada = forms.ChoiceField(
        label='Tipo',
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fornecedor = forms.CharField(
        label='Fornecedor',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do fornecedor'
        })
    )
    
    numero_nf = forms.CharField(
        label='Número NF',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número da NF'
        })
    )
