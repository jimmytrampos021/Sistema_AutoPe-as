# ============================================================
# COMANDO DJANGO: POPULAR MODELOS DE VEÍCULOS
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos.py
#
# Para executar:
# python manage.py popular_modelos
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula os modelos e versões de veículos'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('POPULANDO MODELOS DE VEÍCULOS')
        self.stdout.write('=' * 60)

        # Estrutura: MONTADORA -> [modelos com versões]
        dados = {
            'VOLKSWAGEN': [
                {'nome': 'GOL', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'GOL G3 1.0 8V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.0 8V'},
                    {'nome': 'GOL G3 1.0 16V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.0 16V'},
                    {'nome': 'GOL G4 1.0', 'ano_inicial': 2005, 'ano_final': 2014, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'GOL G5 1.0', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'GOL G5 1.6', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'GOL G6 1.0', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'GOL G6 1.6', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.6 8V/16V Flex'},
                    {'nome': 'GOL G7 1.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'GOL G7 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'VOYAGE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'VOYAGE G5 1.0', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'VOYAGE G5 1.6', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'VOYAGE G6 1.0', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'VOYAGE G6 1.6', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'FOX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FOX 1.0', 'ano_inicial': 2003, 'ano_final': 2021, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'FOX 1.6', 'ano_inicial': 2003, 'ano_final': 2021, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'CROSSFOX 1.6', 'ano_inicial': 2005, 'ano_final': 2021, 'motorizacoes': '1.6 8V/16V Flex'},
                    {'nome': 'SPACEFOX 1.6', 'ano_inicial': 2006, 'ano_final': 2021, 'motorizacoes': '1.6 8V Flex'},
                ]},
                {'nome': 'POLO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'POLO CLASSIC 1.8', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.8 8V'},
                    {'nome': 'POLO 1.6', 'ano_inicial': 2002, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'POLO 200 TSI', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo'},
                    {'nome': 'VIRTUS 200 TSI', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo'},
                ]},
                {'nome': 'SAVEIRO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SAVEIRO G3 1.6', 'ano_inicial': 2000, 'ano_final': 2005, 'motorizacoes': '1.6 8V'},
                    {'nome': 'SAVEIRO G4 1.6', 'ano_inicial': 2005, 'ano_final': 2009, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'SAVEIRO G5 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'SAVEIRO G6 1.6', 'ano_inicial': 2013, 'ano_final': None, 'motorizacoes': '1.6 8V/16V Flex'},
                ]},
                {'nome': 'KOMBI', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KOMBI 1.4', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'KOMBI 1.6', 'ano_inicial': 1997, 'ano_final': 2005, 'motorizacoes': '1.6 8V'},
                ]},
                {'nome': 'AMAROK', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'AMAROK 2.0 TDI', 'ano_inicial': 2010, 'ano_final': None, 'motorizacoes': '2.0 TDI Diesel'},
                    {'nome': 'AMAROK V6 3.0', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '3.0 V6 TDI Diesel'},
                ]},
                {'nome': 'T-CROSS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'T-CROSS 200 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo'},
                    {'nome': 'T-CROSS 250 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo'},
                ]},
            ],
            'FIAT': [
                {'nome': 'PALIO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'PALIO 1.0 8V', 'ano_inicial': 1996, 'ano_final': 2017, 'motorizacoes': '1.0 8V Fire Flex'},
                    {'nome': 'PALIO 1.4', 'ano_inicial': 2007, 'ano_final': 2017, 'motorizacoes': '1.4 8V Fire Flex'},
                    {'nome': 'PALIO 1.6 16V', 'ano_inicial': 2010, 'ano_final': 2017, 'motorizacoes': '1.6 16V E-Torq'},
                    {'nome': 'PALIO 1.8 R', 'ano_inicial': 2003, 'ano_final': 2010, 'motorizacoes': '1.8 8V Flex'},
                ]},
                {'nome': 'SIENA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SIENA 1.0', 'ano_inicial': 1998, 'ano_final': 2012, 'motorizacoes': '1.0 8V Fire Flex'},
                    {'nome': 'SIENA 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                    {'nome': 'SIENA EL 1.4', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'GRAND SIENA 1.4', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'GRAND SIENA 1.6', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.6 16V E-Torq'},
                ]},
                {'nome': 'UNO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'UNO MILLE 1.0', 'ano_inicial': 1990, 'ano_final': 2013, 'motorizacoes': '1.0 8V Fire Flex'},
                    {'nome': 'UNO VIVACE 1.0', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.0 8V Evo Flex'},
                    {'nome': 'UNO WAY 1.0', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.0 8V Evo Flex'},
                    {'nome': 'UNO WAY 1.4', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.4 8V Evo Flex'},
                ]},
                {'nome': 'STRADA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'STRADA 1.4', 'ano_inicial': 2004, 'ano_final': 2020, 'motorizacoes': '1.4 8V Fire Flex'},
                    {'nome': 'STRADA 1.8', 'ano_inicial': 2004, 'ano_final': 2020, 'motorizacoes': '1.8 8V/16V Flex'},
                    {'nome': 'NOVA STRADA 1.3', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.3 Firefly Flex'},
                    {'nome': 'NOVA STRADA 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                ]},
                {'nome': 'MOBI', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'MOBI 1.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                    {'nome': 'MOBI LIKE 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                ]},
                {'nome': 'ARGO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'ARGO 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 6V Firefly Flex'},
                    {'nome': 'ARGO 1.3', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                    {'nome': 'ARGO 1.8', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
                ]},
                {'nome': 'CRONOS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CRONOS 1.3', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                    {'nome': 'CRONOS 1.8', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
                ]},
                {'nome': 'TORO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'TORO 1.8', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'TORO 2.0 DIESEL', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'TORO 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                ]},
                {'nome': 'FIORINO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FIORINO 1.4', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '1.4 8V Evo Flex'},
                ]},
            ],
            'CHEVROLET': [
                {'nome': 'CORSA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CORSA 1.0 8V', 'ano_inicial': 1994, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'CORSA 1.4', 'ano_inicial': 2002, 'ano_final': 2012, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'CORSA 1.8', 'ano_inicial': 2002, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                    {'nome': 'CORSA SEDAN 1.0', 'ano_inicial': 1998, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'CORSA SEDAN 1.8', 'ano_inicial': 2002, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                ]},
                {'nome': 'CLASSIC', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CLASSIC 1.0', 'ano_inicial': 2003, 'ano_final': 2016, 'motorizacoes': '1.0 8V VHC Flex'},
                ]},
                {'nome': 'CELTA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CELTA 1.0', 'ano_inicial': 2000, 'ano_final': 2015, 'motorizacoes': '1.0 8V VHC Flex'},
                    {'nome': 'CELTA 1.4', 'ano_inicial': 2003, 'ano_final': 2006, 'motorizacoes': '1.4 8V'},
                ]},
                {'nome': 'PRISMA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'PRISMA 1.0', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.0 8V VHC Flex'},
                    {'nome': 'PRISMA 1.4', 'ano_inicial': 2006, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'NOVO PRISMA 1.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'NOVO PRISMA 1.4', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                ]},
                {'nome': 'ONIX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'ONIX 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'ONIX 1.4', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'NOVO ONIX 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'NOVO ONIX 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'ONIX PLUS 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'ONIX PLUS 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                ]},
                {'nome': 'MONTANA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'MONTANA 1.4', 'ano_inicial': 2003, 'ano_final': 2021, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'NOVA MONTANA 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo'},
                ]},
                {'nome': 'S10', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'S10 2.4', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '2.4 8V Flex'},
                    {'nome': 'S10 2.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                    {'nome': 'S10 2.8 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                ]},
                {'nome': 'TRACKER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'TRACKER 1.4 TURBO', 'ano_inicial': 2017, 'ano_final': 2020, 'motorizacoes': '1.4 Turbo Flex'},
                    {'nome': 'NOVO TRACKER 1.0 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO TRACKER 1.2 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                ]},
                {'nome': 'SPIN', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SPIN 1.8', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.8 8V Flex'},
                ]},
            ],
            'FORD': [
                {'nome': 'KA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KA 1.0', 'ano_inicial': 1997, 'ano_final': 2021, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'KA 1.5', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 12V Flex'},
                    {'nome': 'KA SEDAN 1.0', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'KA SEDAN 1.5', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 12V Flex'},
                ]},
                {'nome': 'FIESTA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FIESTA 1.0', 'ano_inicial': 1996, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                    {'nome': 'FIESTA 1.6', 'ano_inicial': 2002, 'ano_final': 2019, 'motorizacoes': '1.6 8V/16V Flex'},
                    {'nome': 'NEW FIESTA 1.5', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.5 16V Flex'},
                    {'nome': 'NEW FIESTA 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'ECOSPORT', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'ECOSPORT 1.6', 'ano_inicial': 2003, 'ano_final': 2017, 'motorizacoes': '1.6 8V/16V Flex'},
                    {'nome': 'ECOSPORT 2.0', 'ano_inicial': 2003, 'ano_final': 2017, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'NOVO ECOSPORT 1.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.5 12V Flex'},
                    {'nome': 'NOVO ECOSPORT 2.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                ]},
                {'nome': 'RANGER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'RANGER 2.3', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '2.3 16V Flex'},
                    {'nome': 'RANGER 2.5', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                    {'nome': 'RANGER 3.2 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                ]},
            ],
            'HYUNDAI': [
                {'nome': 'HB20', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HB20 1.0', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20 1.6', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20S 1.0', 'ano_inicial': 2013, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20S 1.6', 'ano_inicial': 2013, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20X 1.6', 'ano_inicial': 2013, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'TUCSON', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'TUCSON 2.0', 'ano_inicial': 2004, 'ano_final': 2016, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'NOVO TUCSON 1.6 TURBO', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.6 Turbo'},
                ]},
                {'nome': 'CRETA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CRETA 1.6', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'CRETA 2.0', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'NOVO CRETA 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo'},
                ]},
            ],
            'TOYOTA': [
                {'nome': 'COROLLA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COROLLA 1.8', 'ano_inicial': 2003, 'ano_final': None, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'COROLLA 2.0', 'ano_inicial': 2008, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'COROLLA CROSS 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Flex/Híbrido'},
                ]},
                {'nome': 'ETIOS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'ETIOS 1.3', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.3 16V Flex'},
                    {'nome': 'ETIOS 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Flex'},
                    {'nome': 'ETIOS SEDAN 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Flex'},
                ]},
                {'nome': 'HILUX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HILUX 2.7', 'ano_inicial': 2005, 'ano_final': None, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'HILUX 3.0 DIESEL', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '3.0 Diesel'},
                    {'nome': 'HILUX 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                ]},
                {'nome': 'YARIS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'YARIS 1.3', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.3 16V Flex'},
                    {'nome': 'YARIS 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Flex'},
                    {'nome': 'YARIS SEDAN 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Flex'},
                ]},
            ],
            'HONDA': [
                {'nome': 'CIVIC', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CIVIC 1.8', 'ano_inicial': 2006, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'CIVIC 2.0', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'CIVIC 1.5 TURBO', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.5 Turbo'},
                ]},
                {'nome': 'FIT', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FIT 1.4', 'ano_inicial': 2003, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
                    {'nome': 'FIT 1.5', 'ano_inicial': 2009, 'ano_final': 2021, 'motorizacoes': '1.5 16V Flex'},
                    {'nome': 'WR-V 1.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.5 16V Flex'},
                ]},
                {'nome': 'CITY', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CITY 1.5', 'ano_inicial': 2009, 'ano_final': None, 'motorizacoes': '1.5 16V Flex'},
                ]},
                {'nome': 'HR-V', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HR-V 1.8', 'ano_inicial': 2015, 'ano_final': 2021, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'NOVO HR-V 1.5 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.5 Turbo'},
                ]},
            ],
            'RENAULT': [
                {'nome': 'SANDERO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SANDERO 1.0', 'ano_inicial': 2007, 'ano_final': None, 'motorizacoes': '1.0 8V/16V Flex'},
                    {'nome': 'SANDERO 1.6', 'ano_inicial': 2007, 'ano_final': None, 'motorizacoes': '1.6 8V/16V Flex'},
                    {'nome': 'SANDERO STEPWAY 1.6', 'ano_inicial': 2010, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'LOGAN', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'LOGAN 1.0', 'ano_inicial': 2007, 'ano_final': None, 'motorizacoes': '1.0 8V/16V Flex'},
                    {'nome': 'LOGAN 1.6', 'ano_inicial': 2007, 'ano_final': None, 'motorizacoes': '1.6 8V/16V Flex'},
                ]},
                {'nome': 'DUSTER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'DUSTER 1.6', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'DUSTER 2.0', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'DUSTER OROCH 1.6', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'DUSTER OROCH 2.0', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                ]},
                {'nome': 'KWID', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KWID 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                ]},
            ],
            'NISSAN': [
                {'nome': 'MARCH', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'MARCH 1.0', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '1.0 16V Flex'},
                    {'nome': 'MARCH 1.6', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'VERSA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'VERSA 1.0', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '1.0 16V Flex'},
                    {'nome': 'VERSA 1.6', 'ano_inicial': 2011, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'KICKS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KICKS 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                {'nome': 'FRONTIER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FRONTIER 2.3 DIESEL', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                ]},
            ],
            'JEEP': [
                {'nome': 'RENEGADE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'RENEGADE 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'RENEGADE 2.0 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'RENEGADE 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                ]},
                {'nome': 'COMPASS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COMPASS 2.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'COMPASS 2.0 DIESEL', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'COMPASS 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                ]},
                {'nome': 'COMMANDER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COMMANDER 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMMANDER 2.0 DIESEL', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                ]},
            ],
            # MOTOS
            'HONDA MOTOS': [
                {'nome': 'CG 125', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'CG 125 FAN', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '125cc'},
                    {'nome': 'CG 125 CARGO', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '125cc'},
                ]},
                {'nome': 'CG 150', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'CG 150 TITAN', 'ano_inicial': 2004, 'ano_final': 2015, 'motorizacoes': '150cc'},
                    {'nome': 'CG 150 FAN', 'ano_inicial': 2009, 'ano_final': 2015, 'motorizacoes': '150cc'},
                ]},
                {'nome': 'CG 160', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'CG 160 START', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '160cc'},
                    {'nome': 'CG 160 FAN', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '160cc'},
                    {'nome': 'CG 160 TITAN', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '160cc'},
                ]},
                {'nome': 'BIZ', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'BIZ 100', 'ano_inicial': 1998, 'ano_final': 2015, 'motorizacoes': '100cc'},
                    {'nome': 'BIZ 110i', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '110cc'},
                    {'nome': 'BIZ 125', 'ano_inicial': 2005, 'ano_final': None, 'motorizacoes': '125cc'},
                ]},
                {'nome': 'NXR BROS', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'NXR 125 BROS', 'ano_inicial': 2003, 'ano_final': 2005, 'motorizacoes': '125cc'},
                    {'nome': 'NXR 150 BROS', 'ano_inicial': 2003, 'ano_final': 2015, 'motorizacoes': '150cc'},
                    {'nome': 'NXR 160 BROS', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '160cc'},
                ]},
                {'nome': 'POP', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'POP 100', 'ano_inicial': 2007, 'ano_final': 2015, 'motorizacoes': '100cc'},
                    {'nome': 'POP 110i', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '110cc'},
                ]},
            ],
            'YAMAHA': [
                {'nome': 'YBR 125', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'YBR 125 FACTOR', 'ano_inicial': 2008, 'ano_final': 2016, 'motorizacoes': '125cc'},
                    {'nome': 'YBR 125 CARGO', 'ano_inicial': 2008, 'ano_final': 2016, 'motorizacoes': '125cc'},
                ]},
                {'nome': 'FAZER 150', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'FAZER 150 UBS', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '150cc'},
                    {'nome': 'FAZER 150 SED', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '150cc'},
                ]},
                {'nome': 'FACTOR 125', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'FACTOR 125i', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '125cc'},
                ]},
                {'nome': 'CROSSER 150', 'tipo': 'MOTO', 'popular': True, 'versoes': [
                    {'nome': 'CROSSER 150', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '150cc'},
                ]},
            ],
        }

        modelos_criados = 0
        versoes_criadas = 0

        for montadora_nome, modelos in dados.items():
            try:
                montadora = Montadora.objects.get(nome=montadora_nome)
            except Montadora.DoesNotExist:
                self.stdout.write(f'  ⚠️ Montadora não encontrada: {montadora_nome}')
                continue
            
            for modelo_data in modelos:
                modelo, created = VeiculoModelo.objects.get_or_create(
                    montadora=montadora,
                    nome=modelo_data['nome'],
                    defaults={
                        'tipo': modelo_data['tipo'],
                        'popular': modelo_data['popular'],
                        'ativo': True
                    }
                )
                
                if created:
                    modelos_criados += 1
                    self.stdout.write(f'  ✅ Modelo: {montadora.nome} {modelo.nome}')
                
                # Criar versões
                for versao_data in modelo_data['versoes']:
                    versao, v_created = VeiculoVersao.objects.get_or_create(
                        modelo=modelo,
                        nome=versao_data['nome'],
                        defaults={
                            'ano_inicial': versao_data['ano_inicial'],
                            'ano_final': versao_data['ano_final'],
                            'motorizacoes': versao_data['motorizacoes'],
                            'ativo': True
                        }
                    )
                    
                    if v_created:
                        versoes_criadas += 1

        self.stdout.write('')
        self.stdout.write(f'📊 Modelos criados: {modelos_criados}')
        self.stdout.write(f'📊 Versões criadas: {versoes_criadas}')
        self.stdout.write(f'📊 Total Modelos: {VeiculoModelo.objects.count()}')
        self.stdout.write(f'📊 Total Versões: {VeiculoVersao.objects.count()}')
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write('✅ PROCESSO CONCLUÍDO!')
        self.stdout.write('=' * 60)