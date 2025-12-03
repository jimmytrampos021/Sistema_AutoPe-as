# ============================================================
# COMANDO DJANGO: POPULAR MODELOS - PARTE 4 (FORD, HYUNDAI, HONDA)
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos_ford_hyundai_honda.py
#
# Para executar:
# python manage.py popular_modelos_ford_hyundai_honda
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula modelos FORD, HYUNDAI e HONDA'

    def handle(self, *args, **options):
        
        todas_montadoras = {
            # ============================================================
            # FORD
            # ============================================================
            'FORD': [
                # KA
                {'nome': 'KA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Ka Antigo
                    {'nome': 'KA 1.0 ZETEC ROCAM', 'ano_inicial': 1997, 'ano_final': 2007, 'motorizacoes': '1.0 8V Zetec Rocam'},
                    {'nome': 'KA 1.0 ZETEC ROCAM FLEX', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.0 8V Zetec Rocam Flex'},
                    {'nome': 'KA 1.6 ZETEC ROCAM', 'ano_inicial': 2007, 'ano_final': 2014, 'motorizacoes': '1.6 8V Zetec Rocam Flex'},
                    {'nome': 'KA GL 1.0', 'ano_inicial': 1997, 'ano_final': 2007, 'motorizacoes': '1.0 8V Zetec Rocam'},
                    {'nome': 'KA XR 1.6', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.6 8V'},
                    # Novo Ka
                    {'nome': 'NOVO KA 1.0 SE', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Ti-VCT Flex'},
                    {'nome': 'NOVO KA 1.0 SEL', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Ti-VCT Flex'},
                    {'nome': 'NOVO KA 1.5 SE', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'NOVO KA 1.5 SEL', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'KA+ SEDAN 1.0', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Ti-VCT Flex'},
                    {'nome': 'KA+ SEDAN 1.5', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'KA FREESTYLE 1.5', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                ]},
                
                # FIESTA
                {'nome': 'FIESTA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Fiesta Antigo
                    {'nome': 'FIESTA 1.0 ZETEC', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.0 8V Zetec'},
                    {'nome': 'FIESTA 1.0 ZETEC ROCAM', 'ano_inicial': 2002, 'ano_final': 2013, 'motorizacoes': '1.0 8V Zetec Rocam Flex'},
                    {'nome': 'FIESTA 1.6 ZETEC', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.6 8V Zetec'},
                    {'nome': 'FIESTA 1.6 ZETEC ROCAM', 'ano_inicial': 2002, 'ano_final': 2013, 'motorizacoes': '1.6 8V Zetec Rocam Flex'},
                    {'nome': 'FIESTA STREET 1.0', 'ano_inicial': 2002, 'ano_final': 2007, 'motorizacoes': '1.0 8V Zetec Rocam'},
                    {'nome': 'FIESTA STREET 1.6', 'ano_inicial': 2002, 'ano_final': 2007, 'motorizacoes': '1.6 8V Zetec Rocam'},
                    {'nome': 'FIESTA SUPERCHARGER 1.0', 'ano_inicial': 2003, 'ano_final': 2006, 'motorizacoes': '1.0 8V Supercharger'},
                    {'nome': 'FIESTA CLASS 1.6', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.6 8V Zetec Rocam Flex'},
                    {'nome': 'FIESTA SEDAN 1.0', 'ano_inicial': 2004, 'ano_final': 2013, 'motorizacoes': '1.0 8V Zetec Rocam Flex'},
                    {'nome': 'FIESTA SEDAN 1.6', 'ano_inicial': 2004, 'ano_final': 2013, 'motorizacoes': '1.6 8V Zetec Rocam Flex'},
                    {'nome': 'FIESTA TRAIL 1.6', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                    # New Fiesta
                    {'nome': 'NEW FIESTA 1.5', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.5 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA SE 1.5', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.5 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA SE 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA SEL 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA TITANIUM 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'NEW FIESTA SEDAN 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Sigma Flex'},
                ]},
                
                # FOCUS
                {'nome': 'FOCUS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Focus 1ª geração
                    {'nome': 'FOCUS 1.6', 'ano_inicial': 2000, 'ano_final': 2008, 'motorizacoes': '1.6 8V Zetec'},
                    {'nome': 'FOCUS 1.8', 'ano_inicial': 2000, 'ano_final': 2008, 'motorizacoes': '1.8 16V Zetec'},
                    {'nome': 'FOCUS 2.0', 'ano_inicial': 2000, 'ano_final': 2008, 'motorizacoes': '2.0 16V Duratec'},
                    {'nome': 'FOCUS HATCH 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'FOCUS HATCH 2.0', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '2.0 16V Duratec Flex'},
                    {'nome': 'FOCUS SEDAN 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 16V Sigma Flex'},
                    {'nome': 'FOCUS SEDAN 2.0', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '2.0 16V Duratec Flex'},
                    {'nome': 'FOCUS GLX 1.6', 'ano_inicial': 2000, 'ano_final': 2008, 'motorizacoes': '1.6 8V Zetec'},
                    # Novo Focus
                    {'nome': 'NOVO FOCUS SE 1.6', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '1.6 16V Ti-VCT Flex'},
                    {'nome': 'NOVO FOCUS SE 2.0', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '2.0 16V Ti-VCT Flex'},
                    {'nome': 'NOVO FOCUS TITANIUM 2.0', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '2.0 16V Ti-VCT Flex'},
                    {'nome': 'NOVO FOCUS FASTBACK SE 2.0', 'ano_inicial': 2016, 'ano_final': 2019, 'motorizacoes': '2.0 16V Ti-VCT Flex'},
                ]},
                
                # ECOSPORT
                {'nome': 'ECOSPORT', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # EcoSport 1ª geração
                    {'nome': 'ECOSPORT 1.0 SUPERCHARGER', 'ano_inicial': 2003, 'ano_final': 2007, 'motorizacoes': '1.0 8V Supercharger'},
                    {'nome': 'ECOSPORT 1.6 8V', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'ECOSPORT 2.0 16V', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '2.0 16V Duratec Flex'},
                    {'nome': 'ECOSPORT XLS 1.6', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                    {'nome': 'ECOSPORT XLT 2.0', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '2.0 16V Duratec Flex'},
                    {'nome': 'ECOSPORT FREESTYLE 1.6', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                    # Nova EcoSport
                    {'nome': 'NOVA ECOSPORT SE 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'NOVA ECOSPORT SE 2.0', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '2.0 16V Duratec Flex'},
                    {'nome': 'NOVA ECOSPORT SEL 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'NOVA ECOSPORT TITANIUM 2.0', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '2.0 16V Ti-VCT Flex'},
                    {'nome': 'NOVA ECOSPORT FREESTYLE 1.5', 'ano_inicial': 2012, 'ano_final': 2021, 'motorizacoes': '1.5 12V Ti-VCT Flex'},
                    {'nome': 'NOVA ECOSPORT STORM 2.0 4WD', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '2.0 16V Ti-VCT Flex 4WD'},
                ]},
                
                # RANGER
                {'nome': 'RANGER', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Ranger Antiga
                    {'nome': 'RANGER 2.3 16V', 'ano_inicial': 1995, 'ano_final': 2012, 'motorizacoes': '2.3 16V Duratec Flex'},
                    {'nome': 'RANGER 2.5 DIESEL', 'ano_inicial': 1998, 'ano_final': 2006, 'motorizacoes': '2.5 Diesel'},
                    {'nome': 'RANGER 2.8 DIESEL', 'ano_inicial': 2001, 'ano_final': 2005, 'motorizacoes': '2.8 Diesel'},
                    {'nome': 'RANGER 3.0 DIESEL', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '3.0 Diesel'},
                    {'nome': 'RANGER 4.0 V6', 'ano_inicial': 1995, 'ano_final': 2001, 'motorizacoes': '4.0 V6'},
                    {'nome': 'RANGER XL 2.3', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '2.3 16V Flex'},
                    {'nome': 'RANGER XLS 2.3', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '2.3 16V Flex'},
                    {'nome': 'RANGER XLT 3.0 DIESEL', 'ano_inicial': 2005, 'ano_final': 2012, 'motorizacoes': '3.0 Diesel'},
                    # Nova Ranger
                    {'nome': 'NOVA RANGER 2.5 FLEX', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.5 16V Flex'},
                    {'nome': 'NOVA RANGER 2.2 DIESEL', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '2.2 Diesel'},
                    {'nome': 'NOVA RANGER 3.2 DIESEL', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                    {'nome': 'RANGER XL 2.2', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.2 Diesel'},
                    {'nome': 'RANGER XLS 2.2', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '2.2 Diesel'},
                    {'nome': 'RANGER XLT 3.2', 'ano_inicial': 2012, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                    {'nome': 'RANGER LIMITED 3.2', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                    {'nome': 'RANGER BLACK 3.2', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                    {'nome': 'RANGER STORM 3.2', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '3.2 Diesel'},
                ]},
                
                # FUSION
                {'nome': 'FUSION', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'FUSION 2.3', 'ano_inicial': 2006, 'ano_final': 2009, 'motorizacoes': '2.3 16V'},
                    {'nome': 'FUSION SEL 2.3', 'ano_inicial': 2006, 'ano_final': 2009, 'motorizacoes': '2.3 16V'},
                    {'nome': 'FUSION 2.5', 'ano_inicial': 2010, 'ano_final': 2012, 'motorizacoes': '2.5 16V'},
                    {'nome': 'FUSION 3.0 V6', 'ano_inicial': 2006, 'ano_final': 2009, 'motorizacoes': '3.0 V6'},
                    {'nome': 'NOVO FUSION 2.0 ECOBOOST', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '2.0 Ecoboost Turbo'},
                    {'nome': 'NOVO FUSION 2.5', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '2.5 16V'},
                    {'nome': 'NOVO FUSION TITANIUM 2.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '2.0 Ecoboost Turbo'},
                    {'nome': 'NOVO FUSION HYBRID 2.0', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '2.0 Híbrido'},
                ]},
                
                # TERRITORY
                {'nome': 'TERRITORY', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'TERRITORY SEL 1.5 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.5 Turbo'},
                    {'nome': 'TERRITORY TITANIUM 1.5 TURBO', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.5 Turbo'},
                ]},
                
                # Clássicos Ford
                {'nome': 'ESCORT', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'ESCORT 1.6', 'ano_inicial': 1983, 'ano_final': 2002, 'motorizacoes': '1.6 8V AP'},
                    {'nome': 'ESCORT 1.8', 'ano_inicial': 1992, 'ano_final': 2002, 'motorizacoes': '1.8 16V Zetec'},
                    {'nome': 'ESCORT 2.0', 'ano_inicial': 1992, 'ano_final': 2002, 'motorizacoes': '2.0 16V Zetec'},
                    {'nome': 'ESCORT XR3 1.6', 'ano_inicial': 1984, 'ano_final': 1992, 'motorizacoes': '1.6 8V AP'},
                    {'nome': 'ESCORT XR3 1.8', 'ano_inicial': 1992, 'ano_final': 1995, 'motorizacoes': '1.8 16V Zetec'},
                    {'nome': 'ESCORT XR3 2.0', 'ano_inicial': 1992, 'ano_final': 1995, 'motorizacoes': '2.0 16V Zetec'},
                    {'nome': 'ESCORT HOBBY 1.0', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.0 8V'},
                    {'nome': 'ESCORT HOBBY 1.6', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.6 8V AP'},
                    {'nome': 'ESCORT SW 1.8', 'ano_inicial': 1997, 'ano_final': 2002, 'motorizacoes': '1.8 16V Zetec'},
                    {'nome': 'ESCORT ZETEC 1.8', 'ano_inicial': 1997, 'ano_final': 2002, 'motorizacoes': '1.8 16V Zetec'},
                ]},
                
                {'nome': 'VERSAILLES / ROYALE', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'VERSAILLES 1.8', 'ano_inicial': 1991, 'ano_final': 1996, 'motorizacoes': '1.8 8V AP'},
                    {'nome': 'VERSAILLES 2.0', 'ano_inicial': 1991, 'ano_final': 1996, 'motorizacoes': '2.0 8V AP'},
                    {'nome': 'VERSAILLES GHIA 2.0', 'ano_inicial': 1991, 'ano_final': 1996, 'motorizacoes': '2.0 8V AP'},
                    {'nome': 'ROYALE 1.8', 'ano_inicial': 1992, 'ano_final': 1996, 'motorizacoes': '1.8 8V AP'},
                    {'nome': 'ROYALE 2.0', 'ano_inicial': 1992, 'ano_final': 1996, 'motorizacoes': '2.0 8V AP'},
                    {'nome': 'ROYALE GHIA 2.0', 'ano_inicial': 1992, 'ano_final': 1996, 'motorizacoes': '2.0 8V AP'},
                ]},
                
                {'nome': 'DEL REY', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'DEL REY 1.6', 'ano_inicial': 1981, 'ano_final': 1991, 'motorizacoes': '1.6 8V CHT'},
                    {'nome': 'DEL REY BELINA 1.6', 'ano_inicial': 1981, 'ano_final': 1991, 'motorizacoes': '1.6 8V CHT'},
                    {'nome': 'DEL REY PAMPA 1.6', 'ano_inicial': 1982, 'ano_final': 1997, 'motorizacoes': '1.6/1.8 8V'},
                ]},
                
                {'nome': 'COURIER', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'COURIER 1.3', 'ano_inicial': 1997, 'ano_final': 2001, 'motorizacoes': '1.3 8V Endura'},
                    {'nome': 'COURIER 1.4', 'ano_inicial': 1999, 'ano_final': 2013, 'motorizacoes': '1.4 16V Zetec'},
                    {'nome': 'COURIER 1.6', 'ano_inicial': 2000, 'ano_final': 2013, 'motorizacoes': '1.6 8V Zetec Rocam Flex'},
                ]},
            ],
            
            # ============================================================
            # HYUNDAI
            # ============================================================
            'HYUNDAI': [
                # HB20
                {'nome': 'HB20', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # HB20 1ª geração
                    {'nome': 'HB20 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20 1.6', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20 COMFORT 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20 COMFORT PLUS 1.0', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20 COMFORT PLUS 1.6', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20 PREMIUM 1.6', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20 SPICY 1.6', 'ano_inicial': 2015, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20 R-SPEC 1.6', 'ano_inicial': 2016, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    # Novo HB20
                    {'nome': 'NOVO HB20 SENSE 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'NOVO HB20 VISION 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'NOVO HB20 EVOLUTION 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO HB20 LAUNCH EDITION 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': 2020, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO HB20 DIAMOND 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO HB20 PLATINUM 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                ]},
                
                # HB20S
                {'nome': 'HB20S', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HB20S 1.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20S 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20S COMFORT PLUS 1.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'HB20S COMFORT PLUS 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20S PREMIUM 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    # Novo HB20S
                    {'nome': 'NOVO HB20S VISION 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                    {'nome': 'NOVO HB20S EVOLUTION 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO HB20S DIAMOND 1.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO HB20S PLATINUM 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                ]},
                
                # HB20X
                {'nome': 'HB20X', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HB20X 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20X STYLE 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'HB20X PREMIUM 1.6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'NOVO HB20X VISION 1.6', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'NOVO HB20X EVOLUTION 1.6', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'NOVO HB20X DIAMOND 1.6', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.6 16V Flex'},
                ]},
                
                # CRETA
                {'nome': 'CRETA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CRETA ATTITUDE 1.6', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'CRETA SMART 1.6', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'CRETA PULSE 1.6', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.6 16V Flex'},
                    {'nome': 'CRETA PULSE PLUS 2.0', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'CRETA PRESTIGE 2.0', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'CRETA SPORT 2.0', 'ano_inicial': 2019, 'ano_final': 2021, 'motorizacoes': '2.0 16V Flex'},
                    # Novo Creta
                    {'nome': 'NOVO CRETA ACTION 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO CRETA COMFORT 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO CRETA LIMITED 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO CRETA PLATINUM 1.0 TURBO', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                    {'nome': 'NOVO CRETA ULTIMATE 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'NOVO CRETA N LINE 1.0 TURBO', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.0 Turbo Flex'},
                ]},
                
                # TUCSON
                {'nome': 'TUCSON', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'TUCSON 2.0', 'ano_inicial': 2004, 'ano_final': 2016, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'TUCSON GLS 2.0', 'ano_inicial': 2006, 'ano_final': 2016, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'TUCSON GL 2.0', 'ano_inicial': 2004, 'ano_final': 2012, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'TUCSON 2.7 V6', 'ano_inicial': 2006, 'ano_final': 2009, 'motorizacoes': '2.7 V6'},
                    # Novo Tucson
                    {'nome': 'NOVO TUCSON GLS 1.6 TURBO', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.6 Turbo'},
                    {'nome': 'NOVO TUCSON GL 1.6 TURBO', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '1.6 Turbo'},
                ]},
                
                # i30
                {'nome': 'I30', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'I30 2.0', 'ano_inicial': 2009, 'ano_final': 2017, 'motorizacoes': '2.0 16V'},
                    {'nome': 'I30 GLS 2.0', 'ano_inicial': 2009, 'ano_final': 2017, 'motorizacoes': '2.0 16V'},
                    {'nome': 'I30 CW 2.0', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '2.0 16V'},
                ]},
                
                # AZERA
                {'nome': 'AZERA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'AZERA 3.3 V6', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '3.3 V6'},
                    {'nome': 'AZERA 3.0 V6', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '3.0 V6'},
                ]},
                
                # SANTA FE
                {'nome': 'SANTA FE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'SANTA FE 2.7 V6', 'ano_inicial': 2006, 'ano_final': 2010, 'motorizacoes': '2.7 V6'},
                    {'nome': 'SANTA FE 3.5 V6', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '3.5 V6'},
                    {'nome': 'SANTA FE GLS 3.5', 'ano_inicial': 2011, 'ano_final': 2019, 'motorizacoes': '3.5 V6'},
                ]},
                
                # IX35
                {'nome': 'IX35', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'IX35 2.0', 'ano_inicial': 2010, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'IX35 GLS 2.0', 'ano_inicial': 2010, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'IX35 GL 2.0', 'ano_inicial': 2010, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'IX35 LAUNCHING EDITION 2.0', 'ano_inicial': 2015, 'ano_final': 2016, 'motorizacoes': '2.0 16V Flex'},
                ]},
                
                # VELOSTER
                {'nome': 'VELOSTER', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'VELOSTER 1.6', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '1.6 16V'},
                ]},
                
                # ELANTRA
                {'nome': 'ELANTRA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'ELANTRA 1.8', 'ano_inicial': 2011, 'ano_final': 2015, 'motorizacoes': '1.8 16V'},
                    {'nome': 'ELANTRA 2.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'ELANTRA GLS 2.0', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                ]},
            ],
            
            # ============================================================
            # HONDA
            # ============================================================
            'HONDA': [
                # CIVIC
                {'nome': 'CIVIC', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Civic Antigos
                    {'nome': 'CIVIC 1.6 16V', 'ano_inicial': 1992, 'ano_final': 2000, 'motorizacoes': '1.6 16V'},
                    {'nome': 'CIVIC EX 1.6', 'ano_inicial': 1996, 'ano_final': 2000, 'motorizacoes': '1.6 16V VTEC'},
                    {'nome': 'CIVIC LX 1.6', 'ano_inicial': 1996, 'ano_final': 2000, 'motorizacoes': '1.6 16V'},
                    # Civic 7ª geração
                    {'nome': 'CIVIC 1.7 16V', 'ano_inicial': 2001, 'ano_final': 2006, 'motorizacoes': '1.7 16V'},
                    {'nome': 'CIVIC EX 1.7', 'ano_inicial': 2001, 'ano_final': 2006, 'motorizacoes': '1.7 16V'},
                    {'nome': 'CIVIC LX 1.7', 'ano_inicial': 2001, 'ano_final': 2006, 'motorizacoes': '1.7 16V'},
                    {'nome': 'CIVIC LXB 1.7', 'ano_inicial': 2003, 'ano_final': 2006, 'motorizacoes': '1.7 16V'},
                    # New Civic
                    {'nome': 'NEW CIVIC 1.8', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'NEW CIVIC LXL 1.8', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'NEW CIVIC LXS 1.8', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'NEW CIVIC EXS 1.8', 'ano_inicial': 2006, 'ano_final': 2011, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'NEW CIVIC SI 2.0', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.0 16V i-VTEC'},
                    # Civic 9ª geração
                    {'nome': 'CIVIC 1.8 FLEX', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'CIVIC 2.0 FLEX', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'CIVIC LXL 1.8', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'CIVIC LXR 2.0', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'CIVIC LXS 1.8', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'CIVIC EXR 2.0', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    # Civic 10ª geração
                    {'nome': 'CIVIC EX 2.0', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'CIVIC EXL 2.0', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'CIVIC SPORT 2.0', 'ano_inicial': 2017, 'ano_final': 2021, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'CIVIC TOURING 1.5 TURBO', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.5 Turbo'},
                    {'nome': 'CIVIC SI 1.5 TURBO', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '1.5 Turbo'},
                    # Novo Civic 11ª geração
                    {'nome': 'NOVO CIVIC LX 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'NOVO CIVIC EX 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'NOVO CIVIC EXL 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                    {'nome': 'NOVO CIVIC TOURING 2.0', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '2.0 16V i-VTEC Flex'},
                ]},
                
                # FIT
                {'nome': 'FIT', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # Fit 1ª geração
                    {'nome': 'FIT 1.4', 'ano_inicial': 2003, 'ano_final': 2008, 'motorizacoes': '1.4 8V i-DSI'},
                    {'nome': 'FIT LX 1.4', 'ano_inicial': 2003, 'ano_final': 2008, 'motorizacoes': '1.4 8V i-DSI Flex'},
                    {'nome': 'FIT LXL 1.4', 'ano_inicial': 2003, 'ano_final': 2008, 'motorizacoes': '1.4 8V i-DSI Flex'},
                    {'nome': 'FIT EX 1.5', 'ano_inicial': 2006, 'ano_final': 2008, 'motorizacoes': '1.5 16V i-VTEC'},
                    # Fit 2ª geração
                    {'nome': 'FIT 1.4 FLEX', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.4 16V Flex'},
                    {'nome': 'FIT 1.5 FLEX', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT LX 1.4', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.4 16V Flex'},
                    {'nome': 'FIT LX 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT EX 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT EXL 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT TWIST 1.5', 'ano_inicial': 2012, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    # Fit 3ª geração
                    {'nome': 'FIT LX 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT EX 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT EXL 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'FIT PERSONAL 1.5', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                ]},
                
                # CITY
                {'nome': 'CITY', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    # City 1ª geração
                    {'nome': 'CITY 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY DX 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY LX 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY EX 1.5', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    # City 2ª geração
                    {'nome': 'CITY LX 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY EX 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY EXL 1.5 CVT', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY PERSONAL 1.5', 'ano_inicial': 2017, 'ano_final': 2019, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    # Novo City 3ª geração
                    {'nome': 'NOVO CITY LX 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO CITY EX 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO CITY EXL 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO CITY TOURING 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY HATCHBACK LX 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'CITY HATCHBACK EXL 1.5', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                ]},
                
                # HR-V
                {'nome': 'HR-V', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'HR-V LX 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'HR-V EX 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'HR-V EXL 1.8', 'ano_inicial': 2015, 'ano_final': 2022, 'motorizacoes': '1.8 16V i-VTEC Flex'},
                    {'nome': 'HR-V TOURING 1.5 TURBO', 'ano_inicial': 2019, 'ano_final': 2022, 'motorizacoes': '1.5 Turbo'},
                    # Novo HR-V
                    {'nome': 'NOVO HR-V EX 1.5', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO HR-V EXL 1.5', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO HR-V ADVANCE 1.5', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'NOVO HR-V TOURING 1.5', 'ano_inicial': 2022, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                ]},
                
                # WR-V
                {'nome': 'WR-V', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'WR-V LX 1.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'WR-V EX 1.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'WR-V EXL 1.5', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                    {'nome': 'WR-V TOURING 1.5', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.5 16V i-VTEC Flex'},
                ]},
                
                # CR-V
                {'nome': 'CR-V', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                    {'nome': 'CR-V 2.0', 'ano_inicial': 2000, 'ano_final': 2011, 'motorizacoes': '2.0 16V'},
                    {'nome': 'CR-V LX 2.0', 'ano_inicial': 2000, 'ano_final': 2011, 'motorizacoes': '2.0 16V'},
                    {'nome': 'CR-V EX 2.0', 'ano_inicial': 2007, 'ano_final': 2011, 'motorizacoes': '2.0 16V'},
                    {'nome': 'CR-V EXL 2.0', 'ano_inicial': 2007, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'CR-V LX 2.0 FLEX', 'ano_inicial': 2012, 'ano_final': 2019, 'motorizacoes': '2.0 16V Flex'},
                    {'nome': 'CR-V TOURING 1.5 TURBO', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.5 Turbo'},
                ]},
                
                # ACCORD
                {'nome': 'ACCORD', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                    {'nome': 'ACCORD 2.0', 'ano_inicial': 1994, 'ano_final': 2002, 'motorizacoes': '2.0 16V'},
                    {'nome': 'ACCORD 2.3', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '2.3 16V VTEC'},
                    {'nome': 'ACCORD 2.4', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '2.4 16V i-VTEC'},
                    {'nome': 'ACCORD 3.0 V6', 'ano_inicial': 2003, 'ano_final': 2012, 'motorizacoes': '3.0 V6'},
                    {'nome': 'ACCORD 3.5 V6', 'ano_inicial': 2013, 'ano_final': 2019, 'motorizacoes': '3.5 V6'},
                    {'nome': 'ACCORD 2.0 TURBO', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 Turbo'},
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
        self.stdout.write(self.style.SUCCESS('FORD, HYUNDAI e HONDA concluídos!'))
