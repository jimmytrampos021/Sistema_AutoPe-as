# ============================================================
# COMANDO DJANGO: POPULAR MODELOS - PARTE 5 (TOYOTA, RENAULT, NISSAN, JEEP)
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos_toyota_renault_nissan_jeep.py
#
# Para executar:
# python manage.py popular_modelos_toyota_renault_nissan_jeep
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula modelos TOYOTA, RENAULT, NISSAN e JEEP'

    def handle(self, *args, **options):
        
        todas_montadoras = {
            # ============================================================
            # TOYOTA
            # ============================================================
            'TOYOTA': [
                # COROLLA
                {'nome': 'COROLLA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Corolla Antigos
                    {'nome': 'COROLLA 1.6 16V', 'ano_inicial': 1992, 'ano_final': 2002, 'motorizacoes': '1.6 16V'},
                    {'nome': 'COROLLA 1.8 16V', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '1.8 16V VVT-i'},
                    {'nome': 'COROLLA XLI 1.6', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '1.6 16V'},
                    {'nome': 'COROLLA XEI 1.8', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '1.8 16V VVT-i'},
                    {'nome': 'COROLLA SE-G 1.8', 'ano_inicial': 2000, 'ano_final': 2002, 'motorizacoes': '1.8 16V VVT-i'},
                    # Corolla 2003-2007
                    {'nome': 'COROLLA XLI 1.6', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.6 16V VVT-i'},
                    {'nome': 'COROLLA XLI 1.8', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.8 16V VVT-i'},
                    {'nome': 'COROLLA XEI 1.8', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.8 16V VVT-i'},
                    {'nome': 'COROLLA SE-G 1.8', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.8 16V VVT-i'},
                    # Corolla 2008-2014
                    {'nome': 'COROLLA GLI 1.8', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.8 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA XLI 1.8', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.8 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA XEI 1.8', 'ano_inicial': 2008, 'ano_final': 2011, 'motorizacoes': '1.8 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA XEI 2.0', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '2.0 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA ALTIS 2.0', 'ano_inicial': 2010, 'ano_final': 2014, 'motorizacoes': '2.0 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA SE-G 1.8', 'ano_inicial': 2008, 'ano_final': 2011, 'motorizacoes': '1.8 16V Dual VVT-i Flex'},
                    # Corolla 2015-2019
                    {'nome': 'COROLLA GLI 1.8', 'ano_inicial': 2015, 'ano_final': 2019, 'motorizacoes': '1.8 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA XEI 2.0', 'ano_inicial': 2015, 'ano_final': 2019, 'motorizacoes': '2.0 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA ALTIS 2.0', 'ano_inicial': 2015, 'ano_final': 2019, 'motorizacoes': '2.0 16V Dual VVT-i Flex'},
                    {'nome': 'COROLLA DYNAMIC 2.0', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '2.0 16V Dual VVT-i Flex'},
                    # Novo Corolla
                    {'nome': 'COROLLA GLI 2.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA XEI 2.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA ALTIS 2.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA ALTIS PREMIUM 2.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA ALTIS HYBRID', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.8 Híbrido'},
                    {'nome': 'COROLLA GR-S 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                ]},
                
                # COROLLA CROSS
                {'nome': 'COROLLA CROSS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COROLLA CROSS XR 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA CROSS XRE 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA CROSS XRX 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                    {'nome': 'COROLLA CROSS XRV HYBRID', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.8 Híbrido'},
                    {'nome': 'COROLLA CROSS GR-S 2.0', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '2.0 16V Dynamic Force Flex'},
                ]},
                
                # ETIOS
                {'nome': 'ETIOS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Etios Hatch
                    {'nome': 'ETIOS X 1.3', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.3 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS XS 1.3', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.3 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS XS 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS XLS 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS CROSS 1.5', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS READY 1.5', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS PLATINUM 1.5', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    # Etios Sedan
                    {'nome': 'ETIOS SEDAN X 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS SEDAN XS 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS SEDAN XLS 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'ETIOS SEDAN PLATINUM 1.5', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                ]},
                
                # YARIS
                {'nome': 'YARIS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Yaris Hatch
                    {'nome': 'YARIS XL 1.3', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.3 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS XL 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS XS 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS XLS 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS S 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    # Yaris Sedan
                    {'nome': 'YARIS SEDAN XL 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS SEDAN XS 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                    {'nome': 'YARIS SEDAN XLS 1.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 16V Dual VVT-i Flex'},
                ]},
                
                # HILUX
                {'nome': 'HILUX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Hilux Antiga
                    {'nome': 'HILUX 2.5 DIESEL', 'ano_inicial': 2005, 'ano_final': 2011, 'motorizacoes': '2.5 Diesel'},
                    {'nome': 'HILUX 3.0 DIESEL', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '3.0 Diesel'},
                    {'nome': 'HILUX 2.7 FLEX', 'ano_inicial': 2005, 'ano_final': None, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'HILUX SR 2.7', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'HILUX SR 3.0', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '3.0 Diesel'},
                    {'nome': 'HILUX SRV 3.0', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '3.0 Diesel'},
                    # Nova Hilux
                    {'nome': 'HILUX STD 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'HILUX SR 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'HILUX SRV 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'HILUX SRX 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'HILUX SR 2.7 FLEX', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'HILUX SRV 2.7 FLEX', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'HILUX GR-S 2.8 DIESEL', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                ]},
                
                # HILUX SW4
                {'nome': 'HILUX SW4', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SW4 SR 2.7', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'SW4 SRV 3.0', 'ano_inicial': 2005, 'ano_final': 2015, 'motorizacoes': '3.0 Diesel'},
                    {'nome': 'SW4 SR 2.7 FLEX', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.7 16V Flex'},
                    {'nome': 'SW4 SRX 2.8 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'SW4 SRX DIAMOND 2.8', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'SW4 GR-S 2.8 DIESEL', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.8 Diesel'},
                ]},
                
                # RAV4
                {'nome': 'RAV4', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'RAV4 2.0', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '2.0 16V'},
                    {'nome': 'RAV4 2.4', 'ano_inicial': 2009, 'ano_final': 2012, 'motorizacoes': '2.4 16V'},
                    {'nome': 'RAV4 2.0', 'ano_inicial': 2013, 'ano_final': 2018, 'motorizacoes': '2.0 16V'},
                    {'nome': 'RAV4 2.5', 'ano_inicial': 2013, 'ano_final': 2018, 'motorizacoes': '2.5 16V'},
                    {'nome': 'RAV4 HYBRID 2.5', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.5 Híbrido'},
                    {'nome': 'RAV4 SX HYBRID 2.5', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.5 Híbrido'},
                ]},
                
                # CAMRY
                {'nome': 'CAMRY', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'CAMRY 2.4', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.4 16V'},
                    {'nome': 'CAMRY 3.5 V6', 'ano_inicial': 2007, 'ano_final': 2017, 'motorizacoes': '3.5 V6'},
                    {'nome': 'CAMRY XLE 3.5', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '3.5 V6'},
                    {'nome': 'CAMRY HYBRID 2.5', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '2.5 Híbrido'},
                ]},
            ],
            
            # ============================================================
            # RENAULT
            # ============================================================
            'RENAULT': [
                # SANDERO
                {'nome': 'SANDERO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SANDERO 1.0 16V', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'SANDERO 1.6 8V', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 8V Hi-Flex'},
                    {'nome': 'SANDERO 1.6 16V', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'SANDERO EXPRESSION 1.0', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'SANDERO EXPRESSION 1.6', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 8V Hi-Flex'},
                    {'nome': 'SANDERO PRIVILEGE 1.6', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'SANDERO GT LINE 1.6', 'ano_inicial': 2012, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    # Novo Sandero
                    {'nome': 'NOVO SANDERO AUTHENTIQUE 1.0', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO SANDERO EXPRESSION 1.0', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO SANDERO EXPRESSION 1.6', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.6 8V SCe Flex'},
                    {'nome': 'NOVO SANDERO DYNAMIQUE 1.6', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.6 8V/16V SCe Flex'},
                    {'nome': 'NOVO SANDERO ZEN 1.0', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO SANDERO INTENSE 1.6', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'SANDERO RS 2.0', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '2.0 16V'},
                ]},
                
                # SANDERO STEPWAY
                {'nome': 'SANDERO STEPWAY', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SANDERO STEPWAY 1.6 8V', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.6 8V Hi-Flex'},
                    {'nome': 'SANDERO STEPWAY 1.6 16V', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'NOVO SANDERO STEPWAY 1.6', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.6 8V/16V SCe Flex'},
                    {'nome': 'NOVO SANDERO STEPWAY ZEN 1.6', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'NOVO SANDERO STEPWAY ICONIC 1.6', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.6 16V SCe Flex'},
                ]},
                
                # LOGAN
                {'nome': 'LOGAN', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'LOGAN 1.0 16V', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'LOGAN 1.6 8V', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 8V Hi-Flex'},
                    {'nome': 'LOGAN 1.6 16V', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'LOGAN EXPRESSION 1.0', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'LOGAN EXPRESSION 1.6', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 8V Hi-Flex'},
                    {'nome': 'LOGAN PRIVILEGE 1.6', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 16V Hi-Flex'},
                    # Novo Logan
                    {'nome': 'NOVO LOGAN AUTHENTIQUE 1.0', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO LOGAN EXPRESSION 1.0', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO LOGAN EXPRESSION 1.6', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.6 8V SCe Flex'},
                    {'nome': 'NOVO LOGAN DYNAMIQUE 1.6', 'ano_inicial': 2014, 'ano_final': 2022, 'motorizacoes': '1.6 8V/16V SCe Flex'},
                    {'nome': 'NOVO LOGAN ZEN 1.0', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.0 12V SCe Flex'},
                    {'nome': 'NOVO LOGAN INTENSE 1.6', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.6 16V SCe Flex'},
                ]},
                
                # DUSTER
                {'nome': 'DUSTER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'DUSTER 1.6 16V', 'ano_inicial': 2011, 'ano_final': 2020, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'DUSTER 2.0 16V', 'ano_inicial': 2011, 'ano_final': 2020, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'DUSTER EXPRESSION 1.6', 'ano_inicial': 2011, 'ano_final': 2020, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'DUSTER DYNAMIQUE 1.6', 'ano_inicial': 2011, 'ano_final': 2020, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'DUSTER DYNAMIQUE 2.0', 'ano_inicial': 2011, 'ano_final': 2020, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'DUSTER TECH ROAD 1.6', 'ano_inicial': 2014, 'ano_final': 2020, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'DUSTER TECH ROAD 2.0', 'ano_inicial': 2014, 'ano_final': 2020, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'DUSTER OROCH 1.6', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'DUSTER OROCH 2.0', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'DUSTER OROCH OUTSIDER 2.0', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '2.0 16V Hi-Flex'},
                    # Novo Duster
                    {'nome': 'NOVO DUSTER ZEN 1.6', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'NOVO DUSTER INTENSE 1.6', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'NOVO DUSTER ICONIC 1.6', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'NOVO DUSTER 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo'},
                ]},
                
                # KWID
                {'nome': 'KWID', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KWID ZEN 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 12V SCe'},
                    {'nome': 'KWID INTENSE 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 12V SCe'},
                    {'nome': 'KWID OUTSIDER 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V SCe'},
                ]},
                
                # CLIO
                {'nome': 'CLIO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CLIO 1.0 16V', 'ano_inicial': 1999, 'ano_final': 2015, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'CLIO 1.6 16V', 'ano_inicial': 1999, 'ano_final': 2015, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'CLIO AUTHENTIQUE 1.0', 'ano_inicial': 2003, 'ano_final': 2015, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'CLIO EXPRESSION 1.0', 'ano_inicial': 2003, 'ano_final': 2015, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'CLIO CAMPUS 1.0', 'ano_inicial': 2006, 'ano_final': 2015, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'CLIO SEDAN 1.0', 'ano_inicial': 2000, 'ano_final': 2009, 'motorizacoes': '1.0 16V Hi-Flex'},
                    {'nome': 'CLIO SEDAN 1.6', 'ano_inicial': 2000, 'ano_final': 2009, 'motorizacoes': '1.6 16V Hi-Flex'},
                ]},
                
                # SYMBOL
                {'nome': 'SYMBOL', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'SYMBOL 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'SYMBOL EXPRESSION 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'SYMBOL PRIVILEGE 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 16V Hi-Flex'},
                ]},
                
                # MEGANE
                {'nome': 'MEGANE', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'MEGANE 1.6 16V', 'ano_inicial': 1998, 'ano_final': 2011, 'motorizacoes': '1.6 16V'},
                    {'nome': 'MEGANE 2.0 16V', 'ano_inicial': 1998, 'ano_final': 2011, 'motorizacoes': '2.0 16V'},
                    {'nome': 'MEGANE DYNAMIQUE 1.6', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'MEGANE DYNAMIQUE 2.0', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'MEGANE GRAND TOUR 1.6', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'MEGANE GRAND TOUR 2.0', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.0 16V Hi-Flex'},
                ]},
                
                # SCENIC
                {'nome': 'SCENIC', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'SCENIC 1.6 16V', 'ano_inicial': 1999, 'ano_final': 2011, 'motorizacoes': '1.6 16V'},
                    {'nome': 'SCENIC 2.0 16V', 'ano_inicial': 1999, 'ano_final': 2011, 'motorizacoes': '2.0 16V'},
                    {'nome': 'SCENIC EXPRESSION 1.6', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.6 16V Hi-Flex'},
                    {'nome': 'SCENIC PRIVILEGE 2.0', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '2.0 16V Hi-Flex'},
                ]},
                
                # FLUENCE
                {'nome': 'FLUENCE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FLUENCE 2.0 16V', 'ano_inicial': 2011, 'ano_final': 2017, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'FLUENCE EXPRESSION 2.0', 'ano_inicial': 2011, 'ano_final': 2017, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'FLUENCE DYNAMIQUE 2.0', 'ano_inicial': 2011, 'ano_final': 2017, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'FLUENCE PRIVILEGE 2.0', 'ano_inicial': 2011, 'ano_final': 2017, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'FLUENCE GT LINE 2.0', 'ano_inicial': 2013, 'ano_final': 2017, 'motorizacoes': '2.0 16V Hi-Flex'},
                ]},
                
                # CAPTUR
                {'nome': 'CAPTUR', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CAPTUR ZEN 1.6', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'CAPTUR INTENSE 1.6', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                    {'nome': 'CAPTUR INTENSE 2.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.0 16V Hi-Flex'},
                    {'nome': 'CAPTUR BOSE 1.6', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.6 16V SCe Flex'},
                ]},
            ],
            
            # ============================================================
            # NISSAN
            # ============================================================
            'NISSAN': [
                # MARCH
                {'nome': 'MARCH', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'MARCH 1.0 12V', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'MARCH 1.6 16V', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'MARCH S 1.0', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'MARCH SV 1.0', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'MARCH SV 1.6', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'MARCH SL 1.6', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'MARCH RIO 1.0', 'ano_inicial': 2015, 'ano_final': 2017, 'motorizacoes': '1.0 12V Flex'},
                ]},
                
                # VERSA
                {'nome': 'VERSA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'VERSA 1.0 12V', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'VERSA 1.6 16V', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'VERSA S 1.0', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'VERSA SV 1.0', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'VERSA SV 1.6', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'VERSA SL 1.6', 'ano_inicial': 2011, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'VERSA UNIQUE 1.6', 'ano_inicial': 2015, 'ano_final': 2018, 'motorizacoes': '1.6 16V Flex'},
                    # Novo Versa
                    {'nome': 'NOVO VERSA SENSE 1.6', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'NOVO VERSA ADVANCE 1.6', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'NOVO VERSA EXCLUSIVE 1.6', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                
                # KICKS
                {'nome': 'KICKS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'KICKS S 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'KICKS SV 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'KICKS SL 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'KICKS ADVANCE 1.6', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'KICKS EXCLUSIVE 1.6', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'KICKS RIO 1.6', 'ano_inicial': 2016, 'ano_final': 2017, 'motorizacoes': '1.6 16V Flex'},
                ]},
                
                # FRONTIER
                {'nome': 'FRONTIER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FRONTIER 2.5 DIESEL', 'ano_inicial': 2002, 'ano_final': 2016, 'motorizacoes': '2.5 Diesel'},
                    {'nome': 'FRONTIER XE 2.5', 'ano_inicial': 2008, 'ano_final': 2016, 'motorizacoes': '2.5 Diesel'},
                    {'nome': 'FRONTIER SE 2.5', 'ano_inicial': 2008, 'ano_final': 2016, 'motorizacoes': '2.5 Diesel'},
                    {'nome': 'FRONTIER LE 2.5', 'ano_inicial': 2008, 'ano_final': 2016, 'motorizacoes': '2.5 Diesel'},
                    # Nova Frontier
                    {'nome': 'NOVA FRONTIER S 2.3', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                    {'nome': 'NOVA FRONTIER SE 2.3', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                    {'nome': 'NOVA FRONTIER LE 2.3', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                    {'nome': 'NOVA FRONTIER XE 2.3', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                    {'nome': 'NOVA FRONTIER ATTACK 2.3', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.3 Diesel'},
                ]},
                
                # SENTRA
                {'nome': 'SENTRA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SENTRA 2.0', 'ano_inicial': 2007, 'ano_final': 2013, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'SENTRA S 2.0', 'ano_inicial': 2007, 'ano_final': 2013, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'SENTRA SV 2.0', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'SENTRA SL 2.0', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'SENTRA UNIQUE 2.0', 'ano_inicial': 2015, 'ano_final': 2017, 'motorizacoes': '2.0 16V Flex'},
                ]},
                
                # LIVINA
                {'nome': 'LIVINA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'LIVINA 1.6 16V', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'LIVINA 1.8 16V', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'LIVINA S 1.6', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'LIVINA SL 1.8', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'GRAND LIVINA 1.8', 'ano_inicial': 2010, 'ano_final': 2014, 'motorizacoes': '1.8 16V Flex'},
                ]},
                
                # TIIDA
                {'nome': 'TIIDA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'TIIDA 1.8 16V', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'TIIDA S 1.8', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'TIIDA SL 1.8', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'TIIDA SEDAN 1.8', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.8 16V Flex'},
                ]},
            ],
            
            # ============================================================
            # JEEP
            # ============================================================
            'JEEP': [
                # RENEGADE
                {'nome': 'RENEGADE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'RENEGADE SPORT 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'RENEGADE LONGITUDE 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'RENEGADE LIMITED 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V Flex'},
                    {'nome': 'RENEGADE TRAILHAWK 2.0 DIESEL', 'ano_inicial': 2015, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'RENEGADE SPORT 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'RENEGADE LONGITUDE 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'RENEGADE LIMITED 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'RENEGADE SERIE S 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'RENEGADE 80 ANOS 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': 2022, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'RENEGADE MOAB 2.0 DIESEL', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                ]},
                
                # COMPASS
                {'nome': 'COMPASS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COMPASS SPORT 2.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'COMPASS LONGITUDE 2.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'COMPASS LIMITED 2.0', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'COMPASS TRAILHAWK 2.0 DIESEL', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'COMPASS S 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMPASS LONGITUDE 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMPASS LIMITED 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMPASS SERIE S 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMPASS 80 ANOS 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': 2022, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMPASS OVERLAND 2.0 DIESEL', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                ]},
                
                # COMMANDER
                {'nome': 'COMMANDER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'COMMANDER LIMITED 1.3 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                    {'nome': 'COMMANDER OVERLAND 2.0 DIESEL', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 Diesel'},
                    {'nome': 'COMMANDER SERIE S 1.3 TURBO', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.3 Turbo Flex'},
                ]},
                
                # WRANGLER
                {'nome': 'WRANGLER', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'WRANGLER SPORT 3.6 V6', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.6 V6'},
                    {'nome': 'WRANGLER SAHARA 3.6 V6', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.6 V6'},
                    {'nome': 'WRANGLER RUBICON 3.6 V6', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '3.6 V6'},
                    {'nome': 'WRANGLER UNLIMITED 3.6 V6', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.6 V6'},
                ]},
            ],
        }
        
        total_modelos = 0
        total_versoes = 0
        
        for montadora_nome, modelos_data in todas_montadoras.items():
            self.stdout.write(f'\nPopulando {montadora_nome}...')
            
            try:
                montadora = Montadora.objects.get(nome=montadora_nome)
            except Montadora.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Montadora {montadora_nome} não encontrada!'))
                continue
            
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
            
            self.stdout.write(f'  Modelos: {modelos_criados} | Versões: {versoes_criadas}')
            total_modelos += modelos_criados
            total_versoes += versoes_criadas

        self.stdout.write('')
        self.stdout.write(f'TOTAL - Modelos: {total_modelos} | Versões: {total_versoes}')
        self.stdout.write(self.style.SUCCESS('TOYOTA, RENAULT, NISSAN e JEEP concluídos!'))
