from django.core.management.base import BaseCommand
from financeiro.models import TaxaCartao
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula as taxas de cartão de crédito e débito'

    def handle(self, *args, **options):
        # Taxas conforme informado
        taxas = [
            # PIX (sem taxa)
            {'tipo': 'PIX', 'parcelas': 1, 'taxa_percentual': Decimal('0.00')},
            
            # Débito
            {'tipo': 'DEBITO', 'parcelas': 1, 'taxa_percentual': Decimal('1.09')},
            
            # Crédito
            {'tipo': 'CREDITO', 'parcelas': 1, 'taxa_percentual': Decimal('3.45')},
            {'tipo': 'CREDITO', 'parcelas': 2, 'taxa_percentual': Decimal('5.18')},
            {'tipo': 'CREDITO', 'parcelas': 3, 'taxa_percentual': Decimal('6.37')},
            {'tipo': 'CREDITO', 'parcelas': 4, 'taxa_percentual': Decimal('7.56')},
            {'tipo': 'CREDITO', 'parcelas': 5, 'taxa_percentual': Decimal('8.75')},
            {'tipo': 'CREDITO', 'parcelas': 6, 'taxa_percentual': Decimal('9.94')},
            {'tipo': 'CREDITO', 'parcelas': 7, 'taxa_percentual': Decimal('11.13')},
            {'tipo': 'CREDITO', 'parcelas': 8, 'taxa_percentual': Decimal('12.32')},
            {'tipo': 'CREDITO', 'parcelas': 9, 'taxa_percentual': Decimal('13.51')},
            {'tipo': 'CREDITO', 'parcelas': 10, 'taxa_percentual': Decimal('14.70')},
            {'tipo': 'CREDITO', 'parcelas': 11, 'taxa_percentual': Decimal('15.89')},
            {'tipo': 'CREDITO', 'parcelas': 12, 'taxa_percentual': Decimal('17.08')},
        ]

        criadas = 0
        atualizadas = 0

        for taxa_data in taxas:
            taxa, created = TaxaCartao.objects.update_or_create(
                tipo=taxa_data['tipo'],
                parcelas=taxa_data['parcelas'],
                defaults={
                    'taxa_percentual': taxa_data['taxa_percentual'],
                    'ativo': True
                }
            )
            if created:
                criadas += 1
                self.stdout.write(self.style.SUCCESS(
                    f"✓ Criada: {taxa}"
                ))
            else:
                atualizadas += 1
                self.stdout.write(self.style.WARNING(
                    f"↻ Atualizada: {taxa}"
                ))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Concluído! {criadas} taxas criadas, {atualizadas} atualizadas.'
        ))