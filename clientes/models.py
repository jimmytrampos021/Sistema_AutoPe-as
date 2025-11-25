from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    ]
    
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='F')
    nome = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    rg_ie = models.CharField(max_length=20, blank=True, null=True)
    
    # Contato
    telefone = models.CharField(max_length=15)
    celular = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Endereço
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    # Informações comerciais
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    # Datas
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cpf_cnpj}"


class Veiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='veiculos'  # ← IMPORTANTE
    )
    placa = models.CharField(max_length=8)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    ano_fabricacao = models.IntegerField()
    ano_modelo = models.IntegerField()
    cor = models.CharField(max_length=30)
    chassi = models.CharField(max_length=17, blank=True, null=True)
    renavam = models.CharField(max_length=11, blank=True, null=True)
    km_atual = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)
    
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']
    
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
