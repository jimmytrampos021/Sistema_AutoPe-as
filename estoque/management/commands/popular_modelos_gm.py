# ============================================================
# COMANDO DJANGO: POPULAR MODELOS - PARTE 3 (CHEVROLET)
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos_gm.py
#
# Para executar:
# python manage.py popular_modelos_gm
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula modelos CHEVROLET'

    def handle(self, *args, **options):
        self.stdout.write('Populando CHEVROLET...')
        
        try:
            montadora = Montadora.objects.get(nome='CHEVROLET')
        except Montadora.DoesNotExist:
            self.stdout.write(self.style.ERROR('Montadora CHEVROLET não encontrada!'))
            return

        modelos_data = [
            # CORSA
            {'nome': 'CORSA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CORSA WIND 1.0', 'ano_inicial': 1994, 'ano_final': 2002, 'motorizacoes': '1.0 8V MPFI'},
                {'nome': 'CORSA SUPER 1.0', 'ano_inicial': 1996, 'ano_final': 1999, 'motorizacoes': '1.0 8V MPFI'},
                {'nome': 'CORSA GL 1.6', 'ano_inicial': 1996, 'ano_final': 1999, 'motorizacoes': '1.6 8V MPFI'},
                {'nome': 'CORSA 1.0 16V', 'ano_inicial': 1999, 'ano_final': 2002, 'motorizacoes': '1.0 16V'},
                {'nome': 'CORSA 1.4 ECOPOWER', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'CORSA 1.6 16V', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.6 16V'},
                {'nome': 'CORSA 1.8 8V', 'ano_inicial': 2002, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'CORSA SEDAN 1.0', 'ano_inicial': 1998, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CORSA SEDAN 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'CORSA SEDAN 1.8', 'ano_inicial': 2002, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'CORSA GSI 1.6 16V', 'ano_inicial': 1996, 'ano_final': 1998, 'motorizacoes': '1.6 16V'},
                {'nome': 'CORSA PICKUP 1.6', 'ano_inicial': 1995, 'ano_final': 2003, 'motorizacoes': '1.6 8V'},
                {'nome': 'CORSA WAGON 1.6', 'ano_inicial': 1997, 'ano_final': 2002, 'motorizacoes': '1.6 8V/16V'},
                {'nome': 'CORSA JOY 1.0', 'ano_inicial': 2005, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CORSA JOY 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'CORSA MAXX 1.0', 'ano_inicial': 2005, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CORSA MAXX 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'CORSA PREMIUM 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'CORSA SS 1.8', 'ano_inicial': 2005, 'ano_final': 2009, 'motorizacoes': '1.8 8V Flex'},
            ]},
            
            # CLASSIC
            {'nome': 'CLASSIC', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CLASSIC 1.0 VHC', 'ano_inicial': 2003, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CLASSIC 1.0 VHCE', 'ano_inicial': 2010, 'ano_final': 2016, 'motorizacoes': '1.0 8V VHCE Flex'},
                {'nome': 'CLASSIC LIFE 1.0', 'ano_inicial': 2005, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CLASSIC SPIRIT 1.0', 'ano_inicial': 2005, 'ano_final': 2010, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CLASSIC LS 1.0', 'ano_inicial': 2010, 'ano_final': 2016, 'motorizacoes': '1.0 8V VHCE Flex'},
            ]},
            
            # CELTA
            {'nome': 'CELTA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CELTA 1.0 VHC', 'ano_inicial': 2000, 'ano_final': 2006, 'motorizacoes': '1.0 8V VHC'},
                {'nome': 'CELTA 1.0 VHCE', 'ano_inicial': 2006, 'ano_final': 2015, 'motorizacoes': '1.0 8V VHCE Flex'},
                {'nome': 'CELTA 1.4 VHC', 'ano_inicial': 2003, 'ano_final': 2006, 'motorizacoes': '1.4 8V VHC'},
                {'nome': 'CELTA LIFE 1.0', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CELTA SPIRIT 1.0', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'CELTA LT 1.0', 'ano_inicial': 2012, 'ano_final': 2015, 'motorizacoes': '1.0 8V VHCE Flex'},
                {'nome': 'CELTA LS 1.0', 'ano_inicial': 2012, 'ano_final': 2015, 'motorizacoes': '1.0 8V VHCE Flex'},
            ]},
            
            # PRISMA
            {'nome': 'PRISMA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'PRISMA 1.0 VHC', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'PRISMA 1.4 VHC', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'PRISMA JOY 1.0', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.0 8V VHC Flex'},
                {'nome': 'PRISMA JOY 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'PRISMA MAXX 1.4', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'NOVO PRISMA LT 1.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'NOVO PRISMA LT 1.4', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'NOVO PRISMA LTZ 1.4', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'NOVO PRISMA ACTIV 1.4', 'ano_inicial': 2016, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'PRISMA JOY 1.0 SPE4', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
            ]},
            
            # ONIX
            {'nome': 'ONIX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'ONIX 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'ONIX 1.4', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'ONIX JOY 1.0', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'ONIX LT 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'ONIX LT 1.4', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'ONIX LTZ 1.4', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'ONIX ACTIV 1.4', 'ano_inicial': 2016, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'ONIX EFFECT 1.4', 'ano_inicial': 2015, 'ano_final': 2017, 'motorizacoes': '1.4 8V Flex'},
                # Novo Onix
                {'nome': 'NOVO ONIX 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'NOVO ONIX 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO ONIX LT 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'NOVO ONIX LT 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO ONIX LTZ 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO ONIX PREMIER 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO ONIX RS 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                # Onix Plus (Sedan)
                {'nome': 'ONIX PLUS 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'ONIX PLUS 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'ONIX PLUS LT 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'ONIX PLUS LT 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'ONIX PLUS LTZ 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'ONIX PLUS PREMIER 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
            ]},
            
            # MONTANA
            {'nome': 'MONTANA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'MONTANA 1.4', 'ano_inicial': 2003, 'ano_final': 2010, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'MONTANA 1.8', 'ano_inicial': 2003, 'ano_final': 2010, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'MONTANA CONQUEST 1.4', 'ano_inicial': 2008, 'ano_final': 2021, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'MONTANA SPORT 1.4', 'ano_inicial': 2010, 'ano_final': 2015, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'MONTANA LS 1.4', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.4 8V Ecopower Flex'},
                # Nova Montana
                {'nome': 'NOVA MONTANA 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                {'nome': 'NOVA MONTANA LS 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                {'nome': 'NOVA MONTANA LT 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                {'nome': 'NOVA MONTANA LTZ 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                {'nome': 'NOVA MONTANA PREMIER 1.2 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
            ]},
            
            # MERIVA
            {'nome': 'MERIVA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'MERIVA 1.4', 'ano_inicial': 2003, 'ano_final': 2008, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'MERIVA 1.8', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'MERIVA JOY 1.4', 'ano_inicial': 2006, 'ano_final': 2008, 'motorizacoes': '1.4 8V VHC Flex'},
                {'nome': 'MERIVA JOY 1.8', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'MERIVA MAXX 1.4', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.4 8V Ecopower Flex'},
                {'nome': 'MERIVA MAXX 1.8', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'MERIVA PREMIUM 1.8', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'MERIVA SS 1.8', 'ano_inicial': 2005, 'ano_final': 2008, 'motorizacoes': '1.8 8V Flex'},
            ]},
            
            # VECTRA
            {'nome': 'VECTRA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'VECTRA 2.0 8V', 'ano_inicial': 1994, 'ano_final': 2005, 'motorizacoes': '2.0 8V'},
                {'nome': 'VECTRA 2.0 16V', 'ano_inicial': 1994, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'VECTRA 2.2 16V', 'ano_inicial': 1997, 'ano_final': 2005, 'motorizacoes': '2.2 16V'},
                {'nome': 'VECTRA CD 2.0', 'ano_inicial': 1997, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'VECTRA GLS 2.0', 'ano_inicial': 1997, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'VECTRA CHALLENGE 2.2', 'ano_inicial': 2000, 'ano_final': 2002, 'motorizacoes': '2.2 16V'},
                # Novo Vectra
                {'nome': 'VECTRA 2.0 FLEX', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'VECTRA 2.4 16V', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.4 16V Flex'},
                {'nome': 'VECTRA ELEGANCE 2.0', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'VECTRA EXPRESSION 2.0', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'VECTRA ELITE 2.4', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.4 16V Flex'},
                {'nome': 'VECTRA GT 2.0', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'VECTRA GTX 2.4', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.4 16V Flex'},
                {'nome': 'VECTRA COLLECTION 2.0', 'ano_inicial': 2010, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
            ]},
            
            # ASTRA
            {'nome': 'ASTRA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'ASTRA 1.8', 'ano_inicial': 1995, 'ano_final': 1997, 'motorizacoes': '1.8 8V'},
                {'nome': 'ASTRA 2.0 8V', 'ano_inicial': 1995, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ASTRA 2.0 16V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'ASTRA GL 1.8', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '1.8 8V'},
                {'nome': 'ASTRA GLS 2.0', 'ano_inicial': 1998, 'ano_final': 2005, 'motorizacoes': '2.0 8V/16V'},
                {'nome': 'ASTRA CD 2.0', 'ano_inicial': 1998, 'ano_final': 2005, 'motorizacoes': '2.0 8V/16V'},
                {'nome': 'ASTRA ADVANTAGE 2.0', 'ano_inicial': 2005, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ASTRA ELEGANCE 2.0', 'ano_inicial': 2004, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ASTRA SEDAN 2.0', 'ano_inicial': 1999, 'ano_final': 2011, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ASTRA GSI 2.0 16V', 'ano_inicial': 1999, 'ano_final': 2004, 'motorizacoes': '2.0 16V'},
                {'nome': 'ASTRA SS 2.0', 'ano_inicial': 2003, 'ano_final': 2005, 'motorizacoes': '2.0 8V Flex'},
            ]},
            
            # ZAFIRA
            {'nome': 'ZAFIRA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'ZAFIRA 2.0 8V', 'ano_inicial': 2001, 'ano_final': 2012, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ZAFIRA 2.0 16V', 'ano_inicial': 2001, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'ZAFIRA CD 2.0', 'ano_inicial': 2001, 'ano_final': 2005, 'motorizacoes': '2.0 16V'},
                {'nome': 'ZAFIRA ELEGANCE 2.0', 'ano_inicial': 2004, 'ano_final': 2012, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ZAFIRA ELITE 2.0', 'ano_inicial': 2004, 'ano_final': 2012, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'ZAFIRA COLLECTION 2.0', 'ano_inicial': 2011, 'ano_final': 2012, 'motorizacoes': '2.0 8V Flex'},
            ]},
            
            # CRUZE
            {'nome': 'CRUZE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CRUZE LT 1.8', 'ano_inicial': 2011, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                {'nome': 'CRUZE LTZ 1.8', 'ano_inicial': 2011, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                {'nome': 'CRUZE SPORT6 LT 1.8', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                {'nome': 'CRUZE SPORT6 LTZ 1.8', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                # Novo Cruze
                {'nome': 'NOVO CRUZE LT 1.4 TURBO', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.4 Turbo Flex'},
                {'nome': 'NOVO CRUZE LTZ 1.4 TURBO', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.4 Turbo Flex'},
                {'nome': 'NOVO CRUZE PREMIER 1.4 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.4 Turbo Flex'},
                {'nome': 'CRUZE SPORT6 LT 1.4 TURBO', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.4 Turbo Flex'},
                {'nome': 'CRUZE SPORT6 LTZ 1.4 TURBO', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.4 Turbo Flex'},
            ]},
            
            # TRACKER
            {'nome': 'TRACKER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'TRACKER LTZ 1.8', 'ano_inicial': 2013, 'ano_final': 2016, 'motorizacoes': '1.8 16V Flex'},
                {'nome': 'TRACKER PREMIER 1.4 TURBO', 'ano_inicial': 2017, 'ano_final': 2020, 'motorizacoes': '1.4 Turbo Flex'},
                {'nome': 'TRACKER LT 1.4 TURBO', 'ano_inicial': 2017, 'ano_final': 2020, 'motorizacoes': '1.4 Turbo Flex'},
                # Novo Tracker
                {'nome': 'NOVO TRACKER 1.0 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO TRACKER 1.2 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
                {'nome': 'NOVO TRACKER LT 1.0 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO TRACKER LTZ 1.0 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                {'nome': 'NOVO TRACKER PREMIER 1.2 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.2 Turbo Flex'},
            ]},
            
            # SPIN
            {'nome': 'SPIN', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'SPIN LT 1.8', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'SPIN LTZ 1.8', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'SPIN ACTIV 1.8', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'SPIN PREMIER 1.8', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.8 8V Flex'},
            ]},
            
            # COBALT
            {'nome': 'COBALT', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'COBALT LT 1.4', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'COBALT LT 1.8', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'COBALT LTZ 1.4', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'COBALT LTZ 1.8', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'COBALT ELITE 1.8', 'ano_inicial': 2016, 'ano_final': 2019, 'motorizacoes': '1.8 8V Flex'},
            ]},
            
            # S10
            {'nome': 'S10', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                # S10 Antiga
                {'nome': 'S10 2.2', 'ano_inicial': 1995, 'ano_final': 2000, 'motorizacoes': '2.2 8V'},
                {'nome': 'S10 2.4', 'ano_inicial': 2001, 'ano_final': 2011, 'motorizacoes': '2.4 8V Flex'},
                {'nome': 'S10 2.8 DIESEL', 'ano_inicial': 1997, 'ano_final': 2011, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'S10 4.3 V6', 'ano_inicial': 1998, 'ano_final': 2004, 'motorizacoes': '4.3 V6'},
                # Nova S10
                {'nome': 'NOVA S10 2.4 FLEX', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '2.4 8V Flex'},
                {'nome': 'NOVA S10 2.5 FLEX', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                {'nome': 'NOVA S10 2.8 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'S10 LT 2.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                {'nome': 'S10 LTZ 2.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                {'nome': 'S10 LT 2.8 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'S10 LTZ 2.8 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'S10 HIGH COUNTRY 2.8', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
            ]},
            
            # TRAILBLAZER
            {'nome': 'TRAILBLAZER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'TRAILBLAZER LT 2.8', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'TRAILBLAZER LTZ 2.8', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                {'nome': 'TRAILBLAZER PREMIER 2.8', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
            ]},
            
            # KADETT / MONZA / OMEGA (Clássicos)
            {'nome': 'KADETT', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'KADETT 1.8', 'ano_inicial': 1989, 'ano_final': 1998, 'motorizacoes': '1.8 8V'},
                {'nome': 'KADETT 2.0', 'ano_inicial': 1989, 'ano_final': 1998, 'motorizacoes': '2.0 8V'},
                {'nome': 'KADETT GSI 2.0', 'ano_inicial': 1992, 'ano_final': 1995, 'motorizacoes': '2.0 8V'},
                {'nome': 'KADETT IPANEMA 1.8', 'ano_inicial': 1989, 'ano_final': 1998, 'motorizacoes': '1.8 8V'},
                {'nome': 'KADETT IPANEMA 2.0', 'ano_inicial': 1989, 'ano_final': 1998, 'motorizacoes': '2.0 8V'},
            ]},
            
            {'nome': 'MONZA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'MONZA 1.8', 'ano_inicial': 1982, 'ano_final': 1996, 'motorizacoes': '1.8 8V'},
                {'nome': 'MONZA 2.0', 'ano_inicial': 1987, 'ano_final': 1996, 'motorizacoes': '2.0 8V'},
                {'nome': 'MONZA CLASSIC 2.0', 'ano_inicial': 1990, 'ano_final': 1996, 'motorizacoes': '2.0 8V'},
                {'nome': 'MONZA GLS 2.0', 'ano_inicial': 1991, 'ano_final': 1996, 'motorizacoes': '2.0 8V'},
            ]},
            
            {'nome': 'OMEGA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'OMEGA 2.0', 'ano_inicial': 1992, 'ano_final': 1998, 'motorizacoes': '2.0 8V'},
                {'nome': 'OMEGA 2.2', 'ano_inicial': 1995, 'ano_final': 1998, 'motorizacoes': '2.2 8V'},
                {'nome': 'OMEGA 3.0', 'ano_inicial': 1992, 'ano_final': 1998, 'motorizacoes': '3.0 12V'},
                {'nome': 'OMEGA 4.1', 'ano_inicial': 1994, 'ano_final': 1998, 'motorizacoes': '4.1 12V'},
                {'nome': 'OMEGA GLS 2.2', 'ano_inicial': 1995, 'ano_final': 1998, 'motorizacoes': '2.2 8V'},
                {'nome': 'OMEGA CD 4.1', 'ano_inicial': 1994, 'ano_final': 1998, 'motorizacoes': '4.1 12V'},
                # Omega Australiano
                {'nome': 'OMEGA 3.6 V6', 'ano_inicial': 2005, 'ano_final': 2011, 'motorizacoes': '3.6 V6'},
                {'nome': 'OMEGA CD 3.6', 'ano_inicial': 2005, 'ano_final': 2011, 'motorizacoes': '3.6 V6'},
            ]},
            
            {'nome': 'CHEVETTE', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'CHEVETTE 1.4', 'ano_inicial': 1973, 'ano_final': 1993, 'motorizacoes': '1.4 8V'},
                {'nome': 'CHEVETTE 1.6', 'ano_inicial': 1978, 'ano_final': 1993, 'motorizacoes': '1.6 8V'},
                {'nome': 'CHEVETTE SL 1.6', 'ano_inicial': 1983, 'ano_final': 1993, 'motorizacoes': '1.6 8V'},
                {'nome': 'CHEVETTE SE 1.6', 'ano_inicial': 1987, 'ano_final': 1993, 'motorizacoes': '1.6 8V'},
                {'nome': 'CHEVETTE DL 1.6', 'ano_inicial': 1991, 'ano_final': 1993, 'motorizacoes': '1.6 8V'},
                {'nome': 'CHEVY 500 1.6', 'ano_inicial': 1983, 'ano_final': 1995, 'motorizacoes': '1.6 8V'},
                {'nome': 'MARAJÓ 1.6', 'ano_inicial': 1980, 'ano_final': 1989, 'motorizacoes': '1.6 8V'},
            ]},
            
            {'nome': 'OPALA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'OPALA 2.5', 'ano_inicial': 1969, 'ano_final': 1992, 'motorizacoes': '2.5 6 cilindros'},
                {'nome': 'OPALA 4.1', 'ano_inicial': 1975, 'ano_final': 1992, 'motorizacoes': '4.1 6 cilindros'},
                {'nome': 'OPALA COMODORO 2.5', 'ano_inicial': 1975, 'ano_final': 1992, 'motorizacoes': '2.5 6 cilindros'},
                {'nome': 'OPALA COMODORO 4.1', 'ano_inicial': 1975, 'ano_final': 1992, 'motorizacoes': '4.1 6 cilindros'},
                {'nome': 'OPALA DIPLOMATA 4.1', 'ano_inicial': 1979, 'ano_final': 1992, 'motorizacoes': '4.1 6 cilindros'},
                {'nome': 'CARAVAN 2.5', 'ano_inicial': 1975, 'ano_final': 1992, 'motorizacoes': '2.5 6 cilindros'},
                {'nome': 'CARAVAN 4.1', 'ano_inicial': 1975, 'ano_final': 1992, 'motorizacoes': '4.1 6 cilindros'},
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
        self.stdout.write(self.style.SUCCESS('CHEVROLET concluído!'))
