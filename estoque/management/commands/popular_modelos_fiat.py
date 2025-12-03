# ============================================================
# COMANDO DJANGO: POPULAR MODELOS - PARTE 2 (FIAT)
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos_fiat.py
#
# Para executar:
# python manage.py popular_modelos_fiat
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula modelos FIAT'

    def handle(self, *args, **options):
        self.stdout.write('Populando FIAT...')
        
        try:
            montadora = Montadora.objects.get(nome='FIAT')
        except Montadora.DoesNotExist:
            self.stdout.write(self.style.ERROR('Montadora FIAT não encontrada!'))
            return

        modelos_data = [
            # UNO
            {'nome': 'UNO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                # Uno Antigo
                {'nome': 'UNO MILLE 1.0', 'ano_inicial': 1990, 'ano_final': 2013, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'UNO MILLE EP', 'ano_inicial': 1994, 'ano_final': 2002, 'motorizacoes': '1.0 8V'},
                {'nome': 'UNO MILLE SX', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.0 8V'},
                {'nome': 'UNO MILLE SMART', 'ano_inicial': 1999, 'ano_final': 2002, 'motorizacoes': '1.0 8V'},
                {'nome': 'UNO MILLE FIRE', 'ano_inicial': 2002, 'ano_final': 2013, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'UNO MILLE WAY', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'UNO MILLE ECONOMY', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'UNO 1.3 SPS', 'ano_inicial': 1994, 'ano_final': 1996, 'motorizacoes': '1.3 8V'},
                {'nome': 'UNO 1.5R', 'ano_inicial': 1990, 'ano_final': 1995, 'motorizacoes': '1.5 8V'},
                {'nome': 'UNO 1.6R', 'ano_inicial': 1990, 'ano_final': 1995, 'motorizacoes': '1.6 8V'},
                {'nome': 'UNO TURBO 1.4', 'ano_inicial': 1994, 'ano_final': 1996, 'motorizacoes': '1.4 8V Turbo'},
                {'nome': 'UNO FURGONETA', 'ano_inicial': 1988, 'ano_final': 2013, 'motorizacoes': '1.0/1.3/1.5 8V'},
                # Novo Uno
                {'nome': 'NOVO UNO VIVACE 1.0', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.0 8V Evo Flex'},
                {'nome': 'NOVO UNO WAY 1.0', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.0 8V Evo Flex'},
                {'nome': 'NOVO UNO WAY 1.4', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO UNO ATTRACTIVE 1.0', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.0 8V Evo Flex'},
                {'nome': 'NOVO UNO ATTRACTIVE 1.4', 'ano_inicial': 2010, 'ano_final': 2021, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO UNO SPORTING 1.4', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO UNO DRIVE 1.0', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.0 6V Firefly Flex'},
            ]},
            
            # PALIO
            {'nome': 'PALIO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                # Palio G1
                {'nome': 'PALIO 1.0 EX', 'ano_inicial': 1996, 'ano_final': 2000, 'motorizacoes': '1.0 8V Fire'},
                {'nome': 'PALIO 1.0 ED', 'ano_inicial': 1996, 'ano_final': 2000, 'motorizacoes': '1.0 8V Fire'},
                {'nome': 'PALIO 1.0 EDX', 'ano_inicial': 1996, 'ano_final': 2000, 'motorizacoes': '1.0 8V Fire'},
                {'nome': 'PALIO 1.0 YOUNG', 'ano_inicial': 2000, 'ano_final': 2003, 'motorizacoes': '1.0 8V Fire'},
                {'nome': 'PALIO 1.5', 'ano_inicial': 1996, 'ano_final': 2001, 'motorizacoes': '1.5 8V'},
                {'nome': 'PALIO 1.6 16V', 'ano_inicial': 1996, 'ano_final': 2001, 'motorizacoes': '1.6 16V'},
                # Palio G2 (Fire)
                {'nome': 'PALIO FIRE 1.0 8V', 'ano_inicial': 2001, 'ano_final': 2017, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'PALIO FIRE ECONOMY 1.0', 'ano_inicial': 2007, 'ano_final': 2017, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'PALIO 1.3 8V FIRE', 'ano_inicial': 2003, 'ano_final': 2005, 'motorizacoes': '1.3 8V Fire'},
                # Palio G3/G4
                {'nome': 'PALIO ELX 1.0', 'ano_inicial': 2004, 'ano_final': 2012, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'PALIO ELX 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PALIO HLX 1.8', 'ano_inicial': 2004, 'ano_final': 2008, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'PALIO ATTRACTIVE 1.0', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'PALIO ATTRACTIVE 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PALIO ESSENCE 1.6', 'ano_inicial': 2010, 'ano_final': 2012, 'motorizacoes': '1.6 16V E-Torq Flex'},
                # Novo Palio
                {'nome': 'NOVO PALIO ATTRACTIVE 1.0', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.0 8V Evo Flex'},
                {'nome': 'NOVO PALIO ATTRACTIVE 1.4', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO PALIO ESSENCE 1.6', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'NOVO PALIO SPORTING 1.6', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.6 16V E-Torq Flex'},
            ]},
            
            # PALIO WEEKEND
            {'nome': 'PALIO WEEKEND', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'PALIO WEEKEND 1.5', 'ano_inicial': 1997, 'ano_final': 2001, 'motorizacoes': '1.5 8V'},
                {'nome': 'PALIO WEEKEND 1.6 16V', 'ano_inicial': 1997, 'ano_final': 2001, 'motorizacoes': '1.6 16V'},
                {'nome': 'PALIO WEEKEND 1.0 16V', 'ano_inicial': 2001, 'ano_final': 2004, 'motorizacoes': '1.0 16V Fire'},
                {'nome': 'PALIO WEEKEND 1.3 8V', 'ano_inicial': 2003, 'ano_final': 2004, 'motorizacoes': '1.3 8V Fire'},
                {'nome': 'PALIO WEEKEND ELX 1.4', 'ano_inicial': 2004, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PALIO WEEKEND ADVENTURE 1.8', 'ano_inicial': 1999, 'ano_final': 2012, 'motorizacoes': '1.8 8V/16V Flex'},
                {'nome': 'PALIO WEEKEND TREKKING 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PALIO WEEKEND TREKKING 1.6', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'PALIO WEEKEND ATTRACTIVE 1.4', 'ano_inicial': 2013, 'ano_final': 2018, 'motorizacoes': '1.4 8V Evo Flex'},
            ]},
            
            # SIENA
            {'nome': 'SIENA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'SIENA 1.0 8V FIRE', 'ano_inicial': 1998, 'ano_final': 2010, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'SIENA 1.3 8V FIRE', 'ano_inicial': 2003, 'ano_final': 2005, 'motorizacoes': '1.3 8V Fire'},
                {'nome': 'SIENA 1.5', 'ano_inicial': 1998, 'ano_final': 2001, 'motorizacoes': '1.5 8V'},
                {'nome': 'SIENA 1.6 16V', 'ano_inicial': 1998, 'ano_final': 2001, 'motorizacoes': '1.6 16V'},
                {'nome': 'SIENA EL 1.0', 'ano_inicial': 2010, 'ano_final': 2014, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'SIENA EL 1.4', 'ano_inicial': 2010, 'ano_final': 2014, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'SIENA ELX 1.0', 'ano_inicial': 2004, 'ano_final': 2010, 'motorizacoes': '1.0 8V Fire Flex'},
                {'nome': 'SIENA ELX 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'SIENA ESSENCE 1.6', 'ano_inicial': 2011, 'ano_final': 2014, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'SIENA HLX 1.8', 'ano_inicial': 2004, 'ano_final': 2010, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'SIENA TETRAFUEL 1.4', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.4 8V Tetrafuel'},
            ]},
            
            # GRAND SIENA
            {'nome': 'GRAND SIENA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'GRAND SIENA ATTRACTIVE 1.4', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'GRAND SIENA ESSENCE 1.6', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'GRAND SIENA TETRAFUEL 1.4', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.4 8V Tetrafuel'},
                {'nome': 'GRAND SIENA SUBLIME 1.6', 'ano_inicial': 2015, 'ano_final': 2021, 'motorizacoes': '1.6 16V E-Torq Flex'},
            ]},
            
            # STRADA
            {'nome': 'STRADA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'STRADA 1.5', 'ano_inicial': 1998, 'ano_final': 2003, 'motorizacoes': '1.5 8V'},
                {'nome': 'STRADA 1.6 16V', 'ano_inicial': 1998, 'ano_final': 2003, 'motorizacoes': '1.6 16V'},
                {'nome': 'STRADA FIRE 1.4', 'ano_inicial': 2004, 'ano_final': 2020, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'STRADA WORKING 1.4', 'ano_inicial': 2013, 'ano_final': 2020, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'STRADA HARD WORKING 1.4', 'ano_inicial': 2017, 'ano_final': 2020, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'STRADA ADVENTURE 1.8', 'ano_inicial': 2004, 'ano_final': 2020, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'STRADA TREKKING 1.4', 'ano_inicial': 2009, 'ano_final': 2020, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'STRADA TREKKING 1.6', 'ano_inicial': 2013, 'ano_final': 2020, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'STRADA CABINE DUPLA 1.4', 'ano_inicial': 2010, 'ano_final': 2020, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'STRADA CABINE DUPLA 1.6', 'ano_inicial': 2013, 'ano_final': 2020, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'STRADA CABINE DUPLA 1.8', 'ano_inicial': 2010, 'ano_final': 2020, 'motorizacoes': '1.8 16V E-Torq Flex'},
                # Nova Strada
                {'nome': 'NOVA STRADA ENDURANCE 1.4', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.4 8V Firefly Flex'},
                {'nome': 'NOVA STRADA FREEDOM 1.3', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'NOVA STRADA VOLCANO 1.3', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'NOVA STRADA RANCH 1.3', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'NOVA STRADA ULTRA 1.3 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
            ]},
            
            # FIORINO
            {'nome': 'FIORINO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'FIORINO 1.0', 'ano_inicial': 1988, 'ano_final': 2004, 'motorizacoes': '1.0 8V Fire'},
                {'nome': 'FIORINO 1.3', 'ano_inicial': 1988, 'ano_final': 2004, 'motorizacoes': '1.3 8V Fire'},
                {'nome': 'FIORINO 1.5', 'ano_inicial': 1991, 'ano_final': 2004, 'motorizacoes': '1.5 8V'},
                {'nome': 'NOVO FIORINO 1.4 EVO', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO FIORINO HARD WORKING 1.4', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'NOVO FIORINO ENDURANCE 1.4', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.4 8V Evo Flex'},
            ]},
            
            # DOBLO
            {'nome': 'DOBLO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'DOBLO 1.3 16V', 'ano_inicial': 2002, 'ano_final': 2006, 'motorizacoes': '1.3 16V Fire'},
                {'nome': 'DOBLO 1.4', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'DOBLO 1.8', 'ano_inicial': 2003, 'ano_final': 2017, 'motorizacoes': '1.8 8V/16V Flex'},
                {'nome': 'DOBLO ADVENTURE 1.8', 'ano_inicial': 2003, 'ano_final': 2017, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'DOBLO ESSENCE 1.8', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'DOBLO CARGO 1.4', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'DOBLO CARGO 1.8', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # MOBI
            {'nome': 'MOBI', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'MOBI EASY 1.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                {'nome': 'MOBI LIKE 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                {'nome': 'MOBI WAY 1.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                {'nome': 'MOBI DRIVE 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
                {'nome': 'MOBI TREKKING 1.0', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 8V Firefly Flex'},
            ]},
            
            # ARGO
            {'nome': 'ARGO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'ARGO 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 6V Firefly Flex'},
                {'nome': 'ARGO DRIVE 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 6V Firefly Flex'},
                {'nome': 'ARGO DRIVE 1.3', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'ARGO TREKKING 1.3', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'ARGO PRECISION 1.8', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'ARGO HGT 1.8', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # CRONOS
            {'nome': 'CRONOS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CRONOS DRIVE 1.3', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'CRONOS PRECISION 1.8', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'CRONOS HGT 1.8', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # PUNTO
            {'nome': 'PUNTO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'PUNTO 1.4', 'ano_inicial': 2007, 'ano_final': 2017, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PUNTO ELX 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'PUNTO ATTRACTIVE 1.4', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'PUNTO ESSENCE 1.6', 'ano_inicial': 2010, 'ano_final': 2017, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'PUNTO SPORTING 1.8', 'ano_inicial': 2007, 'ano_final': 2017, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'PUNTO T-JET 1.4 TURBO', 'ano_inicial': 2008, 'ano_final': 2017, 'motorizacoes': '1.4 16V T-Jet Turbo'},
                {'nome': 'PUNTO BLACKMOTION 1.8', 'ano_inicial': 2014, 'ano_final': 2017, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # LINEA
            {'nome': 'LINEA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'LINEA 1.8', 'ano_inicial': 2009, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'LINEA 1.9', 'ano_inicial': 2009, 'ano_final': 2012, 'motorizacoes': '1.9 16V'},
                {'nome': 'LINEA ESSENCE 1.8', 'ano_inicial': 2009, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'LINEA ABSOLUTE 1.8', 'ano_inicial': 2009, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex Dualogic'},
                {'nome': 'LINEA T-JET 1.4 TURBO', 'ano_inicial': 2009, 'ano_final': 2016, 'motorizacoes': '1.4 16V T-Jet Turbo'},
            ]},
            
            # BRAVO
            {'nome': 'BRAVO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'BRAVO ESSENCE 1.8', 'ano_inicial': 2011, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'BRAVO ABSOLUTE 1.8', 'ano_inicial': 2011, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
                {'nome': 'BRAVO T-JET 1.4 TURBO', 'ano_inicial': 2011, 'ano_final': 2016, 'motorizacoes': '1.4 16V T-Jet Turbo'},
                {'nome': 'BRAVO SPORTING 1.8', 'ano_inicial': 2014, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # IDEA
            {'nome': 'IDEA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'IDEA 1.4', 'ano_inicial': 2006, 'ano_final': 2016, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'IDEA ELX 1.4', 'ano_inicial': 2006, 'ano_final': 2010, 'motorizacoes': '1.4 8V Fire Flex'},
                {'nome': 'IDEA ATTRACTIVE 1.4', 'ano_inicial': 2010, 'ano_final': 2016, 'motorizacoes': '1.4 8V Evo Flex'},
                {'nome': 'IDEA ESSENCE 1.6', 'ano_inicial': 2010, 'ano_final': 2016, 'motorizacoes': '1.6 16V E-Torq Flex'},
                {'nome': 'IDEA HLX 1.8', 'ano_inicial': 2006, 'ano_final': 2010, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'IDEA ADVENTURE 1.8', 'ano_inicial': 2007, 'ano_final': 2016, 'motorizacoes': '1.8 16V E-Torq Flex'},
            ]},
            
            # TORO
            {'nome': 'TORO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'TORO FREEDOM 1.8', 'ano_inicial': 2016, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex AT6'},
                {'nome': 'TORO ENDURANCE 1.8', 'ano_inicial': 2018, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex AT6'},
                {'nome': 'TORO OPENING EDITION 1.8', 'ano_inicial': 2016, 'ano_final': 2017, 'motorizacoes': '1.8 16V Flex'},
                {'nome': 'TORO VOLCANO 2.0 DIESEL', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 Diesel AT9'},
                {'nome': 'TORO RANCH 2.0 DIESEL', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 Diesel AT9'},
                {'nome': 'TORO ULTRA 2.0 DIESEL', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '2.0 Diesel AT9'},
                {'nome': 'TORO FREEDOM 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex AT6'},
                {'nome': 'TORO VOLCANO 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex AT6'},
                {'nome': 'TORO RANCH 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex AT6'},
                {'nome': 'TORO ULTRA 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex AT6'},
            ]},
            
            # PULSE
            {'nome': 'PULSE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'PULSE DRIVE 1.3', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 8V Firefly Flex'},
                {'nome': 'PULSE AUDACE 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'PULSE IMPETUS 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'PULSE ABARTH 1.3 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
            ]},
            
            # FASTBACK
            {'nome': 'FASTBACK', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'FASTBACK AUDACE 1.0 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'FASTBACK IMPETUS 1.0 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'FASTBACK ABARTH 1.3 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
            ]},
            
            # 147
            {'nome': '147', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': '147 1.0', 'ano_inicial': 1976, 'ano_final': 1986, 'motorizacoes': '1.0 8V'},
                {'nome': '147 1.3', 'ano_inicial': 1976, 'ano_final': 1986, 'motorizacoes': '1.3 8V'},
                {'nome': '147 1.5', 'ano_inicial': 1981, 'ano_final': 1986, 'motorizacoes': '1.5 8V'},
                {'nome': 'PANORAMA 147', 'ano_inicial': 1980, 'ano_final': 1986, 'motorizacoes': '1.3/1.5 8V'},
                {'nome': 'SPAZIO', 'ano_inicial': 1983, 'ano_final': 1986, 'motorizacoes': '1.0/1.3 8V'},
            ]},
            
            # TEMPRA
            {'nome': 'TEMPRA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'TEMPRA 2.0 8V', 'ano_inicial': 1992, 'ano_final': 1999, 'motorizacoes': '2.0 8V'},
                {'nome': 'TEMPRA 2.0 16V', 'ano_inicial': 1993, 'ano_final': 1999, 'motorizacoes': '2.0 16V'},
                {'nome': 'TEMPRA TURBO', 'ano_inicial': 1994, 'ano_final': 1998, 'motorizacoes': '2.0 8V Turbo'},
                {'nome': 'TEMPRA STILE 2.0', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '2.0 16V'},
                {'nome': 'TEMPRA OURO 2.0', 'ano_inicial': 1997, 'ano_final': 1999, 'motorizacoes': '2.0 16V'},
                {'nome': 'TEMPRA SW 2.0', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '2.0 16V'},
            ]},
            
            # TIPO
            {'nome': 'TIPO', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'TIPO 1.6', 'ano_inicial': 1993, 'ano_final': 1997, 'motorizacoes': '1.6 8V IE'},
                {'nome': 'TIPO 2.0', 'ano_inicial': 1993, 'ano_final': 1997, 'motorizacoes': '2.0 8V'},
                {'nome': 'TIPO 2.0 16V SEDICIVALVOLE', 'ano_inicial': 1994, 'ano_final': 1995, 'motorizacoes': '2.0 16V'},
            ]},
            
            # PREMIO / ELBA
            {'nome': 'PREMIO', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'PREMIO 1.3', 'ano_inicial': 1985, 'ano_final': 1996, 'motorizacoes': '1.3 8V'},
                {'nome': 'PREMIO 1.5', 'ano_inicial': 1985, 'ano_final': 1996, 'motorizacoes': '1.5 8V'},
                {'nome': 'PREMIO 1.6', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.6 8V'},
                {'nome': 'PREMIO CSL 1.6', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.6 8V IE'},
            ]},
            
            {'nome': 'ELBA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'ELBA 1.3', 'ano_inicial': 1986, 'ano_final': 1996, 'motorizacoes': '1.3 8V'},
                {'nome': 'ELBA 1.5', 'ano_inicial': 1986, 'ano_final': 1996, 'motorizacoes': '1.5 8V'},
                {'nome': 'ELBA 1.6', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.6 8V IE'},
                {'nome': 'ELBA WEEKEND 1.6', 'ano_inicial': 1992, 'ano_final': 1996, 'motorizacoes': '1.6 8V'},
            ]},
        ]

        # Criar modelos e versões
        modelos_criados = 0
        versoes_criadas = 0
        
        for modelo_data in modelos_data:
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
                self.stdout.write(f"  + Modelo: {modelo.nome}")
            
            for versao_data in modelo_data['versoes']:
                versao, v_created = VeiculoVersao.objects.get_or_create(
                    modelo=modelo,
                    nome=versao_data['nome'],
                    defaults={
                        'ano_inicial': versao_data['ano_inicial'],
                        'ano_final': versao_data.get('ano_final'),
                        'motorizacoes': versao_data['motorizacoes'],
                        'ativo': True
                    }
                )
                if v_created:
                    versoes_criadas += 1

        self.stdout.write('')
        self.stdout.write(f'Modelos criados: {modelos_criados}')
        self.stdout.write(f'Versões criadas: {versoes_criadas}')
        self.stdout.write(self.style.SUCCESS('FIAT concluído!'))
