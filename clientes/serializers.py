from rest_framework import serializers
from .models import Cliente, Veiculo


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    veiculos = VeiculoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteListSerializer(serializers.ModelSerializer):
    total_veiculos = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf_cnpj', 'telefone', 'cidade', 'ativo', 'total_veiculos']
    
    def get_total_veiculos(self, obj):
        return obj.veiculos.count()
