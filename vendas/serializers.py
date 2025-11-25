from rest_framework import serializers
from .models import Venda, ItemVenda, OrdemServico, PecaOS, ServicoOS


class ItemVendaSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.CharField(source='produto.descricao', read_only=True)
    
    class Meta:
        model = ItemVenda
        fields = '__all__'


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Venda
        fields = '__all__'


class VendaListSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    total_itens = serializers.SerializerMethodField()
    
    class Meta:
        model = Venda
        fields = ['id', 'numero', 'cliente_nome', 'data_venda', 'status', 
                  'forma_pagamento', 'total', 'total_itens']
    
    def get_total_itens(self, obj):
        return obj.itens.count()


class PecaOSSerializer(serializers.ModelSerializer):
    produto_descricao = serializers.CharField(source='produto.descricao', read_only=True)
    
    class Meta:
        model = PecaOS
        fields = '__all__'


class ServicoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoOS
        fields = '__all__'


class OrdemServicoSerializer(serializers.ModelSerializer):
    pecas = PecaOSSerializer(many=True, read_only=True)
    servicos = ServicoOSSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = OrdemServico
        fields = '__all__'


class OrdemServicoListSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    dias_aberta = serializers.SerializerMethodField()
    
    class Meta:
        model = OrdemServico
        fields = ['id', 'numero', 'cliente_nome', 'veiculo_placa', 'status', 
                  'data_entrada', 'data_prevista', 'total', 'dias_aberta']
    
    def get_dias_aberta(self, obj):
        from django.utils import timezone
        if obj.data_saida:
            return (obj.data_saida - obj.data_entrada).days
        return (timezone.now() - obj.data_entrada).days
