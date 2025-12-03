# ============================================================
# COMANDO DJANGO: POPULAR MONTADORAS
# ============================================================
# Arquivo: estoque/management/commands/popular_montadoras.py
#
# Para executar:
# python manage.py popular_montadoras
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora


class Command(BaseCommand):
    help = 'Popula as montadoras de veículos'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('POPULANDO MONTADORAS')
        self.stdout.write('=' * 60)

        # Lista de montadoras com ordem de exibição
        montadoras = [
            # Nacionais/Populares (aparecem primeiro)
            {'nome': 'VOLKSWAGEN', 'pais_origem': 'Alemanha', 'ordem': 1},
            {'nome': 'FIAT', 'pais_origem': 'Itália', 'ordem': 2},
            {'nome': 'CHEVROLET', 'pais_origem': 'EUA', 'ordem': 3},
            {'nome': 'FORD', 'pais_origem': 'EUA', 'ordem': 4},
            {'nome': 'HYUNDAI', 'pais_origem': 'Coreia do Sul', 'ordem': 5},
            {'nome': 'TOYOTA', 'pais_origem': 'Japão', 'ordem': 6},
            {'nome': 'HONDA', 'pais_origem': 'Japão', 'ordem': 7},
            {'nome': 'RENAULT', 'pais_origem': 'França', 'ordem': 8},
            {'nome': 'NISSAN', 'pais_origem': 'Japão', 'ordem': 9},
            {'nome': 'JEEP', 'pais_origem': 'EUA', 'ordem': 10},
            
            # Outras populares
            {'nome': 'PEUGEOT', 'pais_origem': 'França', 'ordem': 11},
            {'nome': 'CITROËN', 'pais_origem': 'França', 'ordem': 12},
            {'nome': 'MITSUBISHI', 'pais_origem': 'Japão', 'ordem': 13},
            {'nome': 'KIA', 'pais_origem': 'Coreia do Sul', 'ordem': 14},
            {'nome': 'SUZUKI', 'pais_origem': 'Japão', 'ordem': 15},
            {'nome': 'MERCEDES-BENZ', 'pais_origem': 'Alemanha', 'ordem': 16},
            {'nome': 'BMW', 'pais_origem': 'Alemanha', 'ordem': 17},
            {'nome': 'AUDI', 'pais_origem': 'Alemanha', 'ordem': 18},
            
            # Caminhões e Comerciais
            {'nome': 'SCANIA', 'pais_origem': 'Suécia', 'ordem': 20},
            {'nome': 'VOLVO', 'pais_origem': 'Suécia', 'ordem': 21},
            {'nome': 'IVECO', 'pais_origem': 'Itália', 'ordem': 22},
            {'nome': 'MAN', 'pais_origem': 'Alemanha', 'ordem': 23},
            {'nome': 'DAF', 'pais_origem': 'Holanda', 'ordem': 24},
            
            # Motos
            {'nome': 'YAMAHA', 'pais_origem': 'Japão', 'ordem': 30},
            {'nome': 'HONDA MOTOS', 'pais_origem': 'Japão', 'ordem': 31},
            {'nome': 'SUZUKI MOTOS', 'pais_origem': 'Japão', 'ordem': 32},
            {'nome': 'KAWASAKI', 'pais_origem': 'Japão', 'ordem': 33},
            {'nome': 'HARLEY-DAVIDSON', 'pais_origem': 'EUA', 'ordem': 34},
            {'nome': 'BMW MOTORRAD', 'pais_origem': 'Alemanha', 'ordem': 35},
            {'nome': 'DAFRA', 'pais_origem': 'Brasil', 'ordem': 36},
            {'nome': 'SHINERAY', 'pais_origem': 'China', 'ordem': 37},
            
            # Outras marcas
            {'nome': 'CHERY', 'pais_origem': 'China', 'ordem': 40},
            {'nome': 'JAC', 'pais_origem': 'China', 'ordem': 41},
            {'nome': 'LIFAN', 'pais_origem': 'China', 'ordem': 42},
            {'nome': 'CAOA CHERY', 'pais_origem': 'China', 'ordem': 43},
            {'nome': 'BYD', 'pais_origem': 'China', 'ordem': 44},
            {'nome': 'GWM', 'pais_origem': 'China', 'ordem': 45},
            
            # Premium/Luxo
            {'nome': 'LAND ROVER', 'pais_origem': 'Reino Unido', 'ordem': 50},
            {'nome': 'JAGUAR', 'pais_origem': 'Reino Unido', 'ordem': 51},
            {'nome': 'PORSCHE', 'pais_origem': 'Alemanha', 'ordem': 52},
            {'nome': 'LEXUS', 'pais_origem': 'Japão', 'ordem': 53},
            {'nome': 'INFINITI', 'pais_origem': 'Japão', 'ordem': 54},
            
            # Picapes/Utilitários
            {'nome': 'RAM', 'pais_origem': 'EUA', 'ordem': 60},
            {'nome': 'DODGE', 'pais_origem': 'EUA', 'ordem': 61},
            {'nome': 'TROLLER', 'pais_origem': 'Brasil', 'ordem': 62},
            
            # Genérico para universal
            {'nome': 'UNIVERSAL', 'pais_origem': 'N/A', 'ordem': 99},
        ]

        criadas = 0
        existentes = 0

        for dados in montadoras:
            montadora, created = Montadora.objects.get_or_create(
                nome=dados['nome'],
                defaults={
                    'pais_origem': dados['pais_origem'],
                    'ordem': dados['ordem'],
                    'ativa': True
                }
            )
            
            if created:
                criadas += 1
                self.stdout.write(f'  ✅ Criada: {dados["nome"]}')
            else:
                existentes += 1

        self.stdout.write('')
        self.stdout.write(f'📊 Montadoras criadas: {criadas}')
        self.stdout.write(f'📊 Já existentes: {existentes}')
        self.stdout.write(f'📊 Total no sistema: {Montadora.objects.count()}')
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write('✅ PROCESSO CONCLUÍDO!')
        self.stdout.write('=' * 60)