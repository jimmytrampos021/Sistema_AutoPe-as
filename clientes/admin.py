from django.contrib import admin
from .models import Cliente, Veiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf_cnpj', 'tipo', 'telefone', 'cidade', 'ativo']
    list_filter = ['tipo', 'ativo', 'cidade', 'estado']
    search_fields = ['nome', 'cpf_cnpj', 'telefone', 'email']
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'nome', 'cpf_cnpj', 'rg_ie')
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Informações Comerciais', {
            'fields': ('limite_credito', 'observacoes', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'marca', 'modelo', 'ano_modelo', 'cliente', 'km_atual']
    list_filter = ['marca', 'ano_modelo']
    search_fields = ['placa', 'marca', 'modelo', 'chassi', 'cliente__nome']
    autocomplete_fields = ['cliente']
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('cliente', 'placa', 'marca', 'modelo', 'ano_fabricacao', 'ano_modelo', 'cor')
        }),
        ('Documentação', {
            'fields': ('chassi', 'renavam')
        }),
        ('Informações Adicionais', {
            'fields': ('km_atual', 'observacoes')
        }),
    )
