from django.core.management.base import BaseCommand
from decimal import Decimal
from estoque.models import AmperagemBateria, EstoqueCasco


class Command(BaseCommand):
    help = 'Popula as amperagens de bateria padrão'

    def handle(self, *args, **options):
        amperagens = [
            {
                'amperagem': '40Ah',
                'nome_tecnico': 'NS40 / B19',
                'peso_kg': Decimal('10.00'),
                'valor_casco_troca': Decimal('0.00'),  # Definir depois
                'valor_casco_compra': Decimal('0.00'),  # Definir depois
                'aplicacao': 'Honda City, Honda Fit',
                'ordem': 1,
            },
            {
                'amperagem': '45Ah',
                'nome_tecnico': 'NS60 / B24',
                'peso_kg': Decimal('12.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Veículos compactos',
                'ordem': 2,
            },
            {
                'amperagem': '50Ah',
                'nome_tecnico': 'NS60L / 24',
                'peso_kg': Decimal('12.50'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Honda Civic, veículos compactos',
                'ordem': 3,
            },
            {
                'amperagem': '60Ah',
                'nome_tecnico': '22F / 60DD',
                'peso_kg': Decimal('13.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Veículos médios',
                'ordem': 4,
            },
            {
                'amperagem': '70Ah',
                'nome_tecnico': '24ST',
                'peso_kg': Decimal('16.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'SUVs, Sedãs médios',
                'ordem': 5,
            },
            {
                'amperagem': '90Ah Caixa Alta',
                'nome_tecnico': '30H / E41',
                'peso_kg': Decimal('22.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'SUVs, Pickups',
                'ordem': 6,
            },
            {
                'amperagem': '95Ah Caixa Baixa',
                'nome_tecnico': '27',
                'peso_kg': Decimal('23.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Pickups, Vans',
                'ordem': 7,
            },
            {
                'amperagem': '100Ah',
                'nome_tecnico': '31',
                'peso_kg': Decimal('24.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Veículos pesados',
                'ordem': 8,
            },
            {
                'amperagem': '150Ah',
                'nome_tecnico': '4D / N150',
                'peso_kg': Decimal('40.00'),
                'valor_casco_troca': Decimal('0.00'),
                'valor_casco_compra': Decimal('0.00'),
                'aplicacao': 'Caminhões, Diesel',
                'ordem': 9,
            },
        ]

        self.stdout.write('Populando amperagens de bateria...\n')

        for dados in amperagens:
            amperagem, created = AmperagemBateria.objects.update_or_create(
                amperagem=dados['amperagem'],
                defaults=dados
            )
            
            # Criar estoque de casco se não existir
            EstoqueCasco.objects.get_or_create(
                amperagem=amperagem,
                defaults={'quantidade': 0}
            )
            
            status = 'Criada' if created else 'Atualizada'
            self.stdout.write(f'  {status}: {amperagem.amperagem}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(amperagens)} amperagens processadas!'))
        self.stdout.write('\n⚠️  Lembre-se de definir os valores de casco no admin!')