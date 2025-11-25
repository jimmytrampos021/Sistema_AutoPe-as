from django.core.management.base import BaseCommand
from financeiro.models import CategoriaDespesa, FormaPagamento, ConfiguracaoTributo
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula os dados iniciais do módulo financeiro'

    def handle(self, *args, **options):
        self.stdout.write('Populando dados do módulo financeiro...\n')
        
        # ==========================================
        # CATEGORIAS DE DESPESA
        # ==========================================
        categorias = [
            # Infraestrutura
            {'nome': 'Aluguel', 'tipo': 'FIXA', 'icone': 'bi-house', 'cor': '#6f42c1', 'ordem': 1},
            {'nome': 'Prestação Imóvel', 'tipo': 'FIXA', 'icone': 'bi-building', 'cor': '#6f42c1', 'ordem': 2},
            {'nome': 'Energia Elétrica', 'tipo': 'FIXA', 'icone': 'bi-lightning', 'cor': '#ffc107', 'ordem': 3},
            {'nome': 'Água', 'tipo': 'FIXA', 'icone': 'bi-droplet', 'cor': '#0dcaf0', 'ordem': 4},
            {'nome': 'Internet', 'tipo': 'FIXA', 'icone': 'bi-wifi', 'cor': '#0d6efd', 'ordem': 5},
            {'nome': 'Telefone', 'tipo': 'FIXA', 'icone': 'bi-telephone', 'cor': '#0d6efd', 'ordem': 6},
            
            # Pessoal
            {'nome': 'Salários', 'tipo': 'FIXA', 'icone': 'bi-people', 'cor': '#198754', 'ordem': 10},
            {'nome': 'Vale Transporte', 'tipo': 'FIXA', 'icone': 'bi-bus-front', 'cor': '#198754', 'ordem': 11},
            {'nome': 'Vale Alimentação', 'tipo': 'FIXA', 'icone': 'bi-cup-hot', 'cor': '#198754', 'ordem': 12},
            {'nome': 'FGTS', 'tipo': 'FIXA', 'icone': 'bi-bank', 'cor': '#198754', 'ordem': 13},
            {'nome': 'INSS', 'tipo': 'FIXA', 'icone': 'bi-shield-check', 'cor': '#198754', 'ordem': 14},
            
            # Operacional
            {'nome': 'Compra de Mercadoria', 'tipo': 'VARIAVEL', 'icone': 'bi-box-seam', 'cor': '#fd7e14', 'ordem': 20},
            {'nome': 'Embalagens', 'tipo': 'VARIAVEL', 'icone': 'bi-bag', 'cor': '#fd7e14', 'ordem': 21},
            {'nome': 'Material de Escritório', 'tipo': 'VARIAVEL', 'icone': 'bi-pencil', 'cor': '#fd7e14', 'ordem': 22},
            {'nome': 'Material de Limpeza', 'tipo': 'VARIAVEL', 'icone': 'bi-droplet-half', 'cor': '#fd7e14', 'ordem': 23},
            
            # Veículos
            {'nome': 'Combustível', 'tipo': 'VARIAVEL', 'icone': 'bi-fuel-pump', 'cor': '#dc3545', 'ordem': 30},
            {'nome': 'Manutenção Veículos', 'tipo': 'VARIAVEL', 'icone': 'bi-tools', 'cor': '#dc3545', 'ordem': 31},
            {'nome': 'Seguro Veículos', 'tipo': 'FIXA', 'icone': 'bi-shield', 'cor': '#dc3545', 'ordem': 32},
            {'nome': 'IPVA', 'tipo': 'VARIAVEL', 'icone': 'bi-car-front', 'cor': '#dc3545', 'ordem': 33},
            
            # Serviços
            {'nome': 'Contador', 'tipo': 'FIXA', 'icone': 'bi-calculator', 'cor': '#20c997', 'ordem': 40},
            {'nome': 'Advocacia', 'tipo': 'VARIAVEL', 'icone': 'bi-briefcase', 'cor': '#20c997', 'ordem': 41},
            {'nome': 'Marketing', 'tipo': 'VARIAVEL', 'icone': 'bi-megaphone', 'cor': '#e91e8c', 'ordem': 42},
            {'nome': 'Software/Sistemas', 'tipo': 'FIXA', 'icone': 'bi-pc-display', 'cor': '#0d6efd', 'ordem': 43},
            
            # Tributos
            {'nome': 'Tributos', 'tipo': 'VARIAVEL', 'icone': 'bi-bank', 'cor': '#dc3545', 'ordem': 50},
            {'nome': 'Taxas e Licenças', 'tipo': 'VARIAVEL', 'icone': 'bi-file-earmark-text', 'cor': '#dc3545', 'ordem': 51},
            
            # Manutenção
            {'nome': 'Manutenção Loja', 'tipo': 'VARIAVEL', 'icone': 'bi-wrench', 'cor': '#6c757d', 'ordem': 60},
            {'nome': 'Equipamentos', 'tipo': 'VARIAVEL', 'icone': 'bi-gear', 'cor': '#6c757d', 'ordem': 61},
            
            # Outros
            {'nome': 'Outros', 'tipo': 'AMBOS', 'icone': 'bi-three-dots', 'cor': '#6c757d', 'ordem': 99},
        ]

        for cat_data in categorias:
            cat, created = CategoriaDespesa.objects.update_or_create(
                nome=cat_data['nome'],
                defaults=cat_data
            )
            status = '✓ Criada' if created else '↻ Atualizada'
            self.stdout.write(f"  {status}: {cat.nome}")

        self.stdout.write(self.style.SUCCESS(f'\n✓ {len(categorias)} categorias processadas'))

        # ==========================================
        # FORMAS DE PAGAMENTO
        # ==========================================
        formas = [
            {'nome': 'Dinheiro', 'icone': 'bi-cash'},
            {'nome': 'PIX', 'icone': 'bi-qr-code'},
            {'nome': 'Cartão de Débito', 'icone': 'bi-credit-card'},
            {'nome': 'Cartão de Crédito', 'icone': 'bi-credit-card-2-front'},
            {'nome': 'Boleto', 'icone': 'bi-upc-scan'},
            {'nome': 'Transferência Bancária', 'icone': 'bi-bank'},
            {'nome': 'Cheque', 'icone': 'bi-card-text'},
        ]

        for forma_data in formas:
            forma, created = FormaPagamento.objects.update_or_create(
                nome=forma_data['nome'],
                defaults=forma_data
            )
            status = '✓ Criada' if created else '↻ Atualizada'
            self.stdout.write(f"  {status}: {forma.nome}")

        self.stdout.write(self.style.SUCCESS(f'\n✓ {len(formas)} formas de pagamento processadas'))

        # ==========================================
        # CONFIGURAÇÃO DO TRIBUTO
        # ==========================================
        config, created = ConfiguracaoTributo.objects.update_or_create(
            nome='Simples Nacional',
            defaults={
                'aliquota': Decimal('4.00'),
                'dia_vencimento': 20,
                'ativo': True
            }
        )
        status = '✓ Criada' if created else '↻ Atualizada'
        self.stdout.write(f"\n  {status}: Configuração Simples Nacional - {config.aliquota}%")

        self.stdout.write(self.style.SUCCESS('\n✅ Módulo financeiro populado com sucesso!'))