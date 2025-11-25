"""
Script para popular o banco de dados com dados de exemplo
Execute: python manage.py shell < populate_data.py
"""

from clientes.models import Cliente, Veiculo
from estoque.models import Categoria, Fornecedor, Produto
from vendas.models import Venda, ItemVenda, OrdemServico, PecaOS, ServicoOS
from django.utils import timezone
from decimal import Decimal

print("Iniciando população do banco de dados...")

# Criar Categorias
print("Criando categorias...")
categorias = [
    Categoria.objects.get_or_create(nome="Freios", descricao="Peças do sistema de freios")[0],
    Categoria.objects.get_or_create(nome="Suspensão", descricao="Peças de suspensão")[0],
    Categoria.objects.get_or_create(nome="Motor", descricao="Peças do motor")[0],
    Categoria.objects.get_or_create(nome="Elétrica", descricao="Sistema elétrico")[0],
    Categoria.objects.get_or_create(nome="Filtros", descricao="Filtros diversos")[0],
    Categoria.objects.get_or_create(nome="Óleos e Lubrificantes", descricao="Óleos e lubrificantes")[0],
]

# Criar Fornecedores
print("Criando fornecedores...")
fornecedores = [
    Fornecedor.objects.get_or_create(
        cnpj="12.345.678/0001-90",
        defaults={
            'razao_social': "Cofap SA",
            'nome_fantasia': "Cofap",
            'telefone': "(11) 3456-7890",
            'email': "vendas@cofap.com.br",
            'cep': "01234-000",
            'logradouro': "Av. Industrial",
            'numero': "1000",
            'bairro': "Distrito Industrial",
            'cidade': "São Paulo",
            'estado': "SP"
        }
    )[0],
    Fornecedor.objects.get_or_create(
        cnpj="98.765.432/0001-10",
        defaults={
            'razao_social': "NGK do Brasil Ltda",
            'nome_fantasia': "NGK",
            'telefone': "(11) 2345-6789",
            'email': "comercial@ngk.com.br",
            'cep': "09876-000",
            'logradouro': "Rua das Velas",
            'numero': "500",
            'bairro': "Centro",
            'cidade': "São Bernardo do Campo",
            'estado': "SP"
        }
    )[0],
]

# Criar Produtos
print("Criando produtos...")
produtos = [
    Produto.objects.get_or_create(
        codigo="PAST-001",
        defaults={
            'descricao': "Pastilha de Freio Dianteira",
            'categoria': categorias[0],
            'fornecedor': fornecedores[0],
            'marca_veiculo': "Chevrolet",
            'modelo_veiculo': "Onix",
            'ano_inicial': 2012,
            'ano_final': 2023,
            'unidade': 'PC',
            'preco_custo': Decimal('45.00'),
            'preco_venda': Decimal('89.90'),
            'estoque_atual': 25,
            'estoque_minimo': 10,
            'estoque_maximo': 50,
        }
    )[0],
    Produto.objects.get_or_create(
        codigo="AMOR-001",
        defaults={
            'descricao': "Amortecedor Dianteiro",
            'categoria': categorias[1],
            'fornecedor': fornecedores[0],
            'marca_veiculo': "Volkswagen",
            'modelo_veiculo': "Gol",
            'ano_inicial': 2008,
            'ano_final': 2023,
            'unidade': 'UN',
            'preco_custo': Decimal('120.00'),
            'preco_venda': Decimal('249.90'),
            'estoque_atual': 15,
            'estoque_minimo': 5,
            'estoque_maximo': 30,
        }
    )[0],
    Produto.objects.get_or_create(
        codigo="VELA-001",
        defaults={
            'descricao': "Vela de Ignição NGK",
            'categoria': categorias[3],
            'fornecedor': fornecedores[1],
            'unidade': 'UN',
            'preco_custo': Decimal('12.00'),
            'preco_venda': Decimal('24.90'),
            'estoque_atual': 80,
            'estoque_minimo': 40,
            'estoque_maximo': 150,
        }
    )[0],
    Produto.objects.get_or_create(
        codigo="FILT-001",
        defaults={
            'descricao': "Filtro de Óleo",
            'categoria': categorias[4],
            'fornecedor': fornecedores[0],
            'unidade': 'UN',
            'preco_custo': Decimal('18.00'),
            'preco_venda': Decimal('35.90'),
            'estoque_atual': 50,
            'estoque_minimo': 20,
            'estoque_maximo': 100,
        }
    )[0],
    Produto.objects.get_or_create(
        codigo="OLEO-001",
        defaults={
            'descricao': "Óleo Motor 5W30 Sintético 1L",
            'categoria': categorias[5],
            'fornecedor': fornecedores[1],
            'unidade': 'LT',
            'preco_custo': Decimal('28.00'),
            'preco_venda': Decimal('54.90'),
            'estoque_atual': 40,
            'estoque_minimo': 20,
            'estoque_maximo': 80,
        }
    )[0],
]

# Criar Clientes
print("Criando clientes...")
cliente1 = Cliente.objects.get_or_create(
    cpf_cnpj="123.456.789-00",
    defaults={
        'tipo': 'F',
        'nome': "João da Silva",
        'telefone': "(22) 98765-4321",
        'celular': "(22) 99876-5432",
        'email': "joao.silva@email.com",
        'cep': "28000-000",
        'logradouro': "Rua das Flores",
        'numero': "123",
        'complemento': "Casa",
        'bairro': "Centro",
        'cidade': "Campos dos Goytacazes",
        'estado': "RJ",
        'limite_credito': Decimal('5000.00'),
    }
)[0]

cliente2 = Cliente.objects.get_or_create(
    cpf_cnpj="987.654.321-00",
    defaults={
        'tipo': 'F',
        'nome': "Maria Santos",
        'telefone': "(22) 3333-4444",
        'email': "maria.santos@email.com",
        'cep': "28010-000",
        'logradouro': "Av. Principal",
        'numero': "456",
        'bairro': "Pelinca",
        'cidade': "Campos dos Goytacazes",
        'estado': "RJ",
        'limite_credito': Decimal('3000.00'),
    }
)[0]

# Criar Veículos
print("Criando veículos...")
veiculo1 = Veiculo.objects.get_or_create(
    placa="ABC-1234",
    defaults={
        'cliente': cliente1,
        'marca': "Chevrolet",
        'modelo': "Onix",
        'ano_fabricacao': 2019,
        'ano_modelo': 2020,
        'cor': "Branco",
        'km_atual': 45000,
    }
)[0]

veiculo2 = Veiculo.objects.get_or_create(
    placa="XYZ-9876",
    defaults={
        'cliente': cliente2,
        'marca': "Volkswagen",
        'modelo': "Gol",
        'ano_fabricacao': 2015,
        'ano_modelo': 2016,
        'cor': "Prata",
        'km_atual': 78000,
    }
)[0]

print("✓ Banco de dados populado com sucesso!")
print(f"- {len(categorias)} categorias")
print(f"- {len(fornecedores)} fornecedores")
print(f"- {len(produtos)} produtos")
print(f"- 2 clientes")
print(f"- 2 veículos")
print("\nAcesse o admin em: http://localhost:8000/admin")
