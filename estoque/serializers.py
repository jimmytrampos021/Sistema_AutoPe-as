from rest_framework import serializers
from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.nome_fantasia', read_only=True)
    estoque_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = '__all__'
    
    def get_estoque_status(self, obj):
        if obj.estoque_atual <= obj.estoque_minimo:
            return 'CRÍTICO'
        elif obj.estoque_atual <= obj.estoque_minimo * 1.5:
            return 'BAIXO'
        elif obj.estoque_atual >= obj.estoque_maximo:
            return 'EXCESSO'
        return 'NORMAL'


class ProdutoListSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    estoque_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = ['id', 'codigo', 'descricao', 'categoria_nome', 'preco_venda', 
                  'estoque_atual', 'estoque_status', 'ativo']
    
    def get_estoque_status(self, obj):
        if obj.estoque_atual <= obj.estoque_minimo:
            return 'CRÍTICO'
        elif obj.estoque_atual <= obj.estoque_minimo * 1.5:
            return 'BAIXO'
        return 'NORMAL'


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.CharField(source='produto.descricao', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoque
        fields = '__all__'
