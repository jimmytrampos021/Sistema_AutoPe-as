from django.core.management.base import BaseCommand
from financeiro.models import ContaFinanceira


class Command(BaseCommand):
    help = 'Popula as contas financeiras iniciais (Santander e Dinheiro em Mãos)'

    def handle(self, *args, **options):
        contas = [
            {
                'nome': 'Santander',
                'tipo': 'BANCO',
                'saldo_inicial': 0,
                'saldo_atual': 0,
                'icone': 'bi-bank',
                'cor': '#EC0000',  # Vermelho Santander
                'ativo': True,
            },
            {
                'nome': 'Dinheiro em Mãos',
                'tipo': 'DINHEIRO',
                'saldo_inicial': 0,
                'saldo_atual': 0,
                'icone': 'bi-cash-stack',
                'cor': '#198754',  # Verde
                'ativo': True,
            },
        ]

        criadas = 0
        existentes = 0

        for conta_data in contas:
            conta, created = ContaFinanceira.objects.get_or_create(
                nome=conta_data['nome'],
                defaults=conta_data
            )
            
            if created:
                criadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Conta "{conta.nome}" criada com sucesso!')
                )
            else:
                existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'→ Conta "{conta.nome}" já existe.')
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'Resumo: {criadas} conta(s) criada(s), {existentes} já existente(s).')
        )