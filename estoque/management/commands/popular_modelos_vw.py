# ============================================================
# COMANDO DJANGO: POPULAR MODELOS - PARTE 1 (VOLKSWAGEN)
# ============================================================
# Arquivo: estoque/management/commands/popular_modelos_vw.py
#
# Para executar:
# python manage.py popular_modelos_vw
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Montadora, VeiculoModelo, VeiculoVersao


class Command(BaseCommand):
    help = 'Popula modelos VOLKSWAGEN'

    def handle(self, *args, **options):
        self.stdout.write('Populando VOLKSWAGEN...')
        
        try:
            montadora = Montadora.objects.get(nome='VOLKSWAGEN')
        except Montadora.DoesNotExist:
            self.stdout.write(self.style.ERROR('Montadora VOLKSWAGEN não encontrada!'))
            return

        modelos_data = [
            # GOL - Todas as gerações
            {'nome': 'GOL', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                # Quadrado
                {'nome': 'GOL QUADRADO 1.0', 'ano_inicial': 1980, 'ano_final': 1994, 'motorizacoes': '1.0 8V'},
                {'nome': 'GOL QUADRADO 1.6', 'ano_inicial': 1980, 'ano_final': 1994, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'GOL QUADRADO 1.8', 'ano_inicial': 1984, 'ano_final': 1994, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'GOL QUADRADO 2.0', 'ano_inicial': 1988, 'ano_final': 1994, 'motorizacoes': '2.0 8V AP GTI'},
                # Bola (G2)
                {'nome': 'GOL BOLA 1.0 8V', 'ano_inicial': 1994, 'ano_final': 1999, 'motorizacoes': '1.0 8V MI'},
                {'nome': 'GOL BOLA 1.0 16V', 'ano_inicial': 1997, 'ano_final': 1999, 'motorizacoes': '1.0 16V Turbo'},
                {'nome': 'GOL BOLA 1.6', 'ano_inicial': 1994, 'ano_final': 1999, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'GOL BOLA 1.8', 'ano_inicial': 1994, 'ano_final': 1999, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'GOL BOLA 2.0', 'ano_inicial': 1994, 'ano_final': 1999, 'motorizacoes': '2.0 8V/16V GTI'},
                # G3
                {'nome': 'GOL G3 1.0 8V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.0 8V MI'},
                {'nome': 'GOL G3 1.0 16V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.0 16V Power'},
                {'nome': 'GOL G3 1.0 16V TURBO', 'ano_inicial': 2000, 'ano_final': 2003, 'motorizacoes': '1.0 16V Turbo'},
                {'nome': 'GOL G3 1.6 8V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'GOL G3 1.6 16V', 'ano_inicial': 2003, 'ano_final': 2005, 'motorizacoes': '1.6 16V Power'},
                {'nome': 'GOL G3 1.8', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'GOL G3 2.0', 'ano_inicial': 1999, 'ano_final': 2003, 'motorizacoes': '2.0 8V/16V GTI'},
                # G4
                {'nome': 'GOL G4 1.0 8V FLEX', 'ano_inicial': 2005, 'ano_final': 2014, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'GOL G4 1.0 ECOMOTION', 'ano_inicial': 2008, 'ano_final': 2014, 'motorizacoes': '1.0 8V Ecomotion'},
                {'nome': 'GOL G4 1.6 8V FLEX', 'ano_inicial': 2005, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'GOL G4 1.6 POWER', 'ano_inicial': 2005, 'ano_final': 2009, 'motorizacoes': '1.6 8V Power Flex'},
                # G5
                {'nome': 'GOL G5 1.0 TREND', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'GOL G5 1.6 POWER', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'GOL G5 1.6 RALLYE', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                # G6
                {'nome': 'GOL G6 1.0 TRENDLINE', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'GOL G6 1.0 COMFORTLINE', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'GOL G6 1.6 HIGHLINE', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'GOL G6 1.6 MSI', 'ano_inicial': 2014, 'ano_final': 2016, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'GOL G6 1.6 RALLYE', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.6 16V Flex'},
                # G7
                {'nome': 'GOL G7 1.0 12V', 'ano_inicial': 2016, 'ano_final': 2023, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'GOL G7 1.6 MSI', 'ano_inicial': 2016, 'ano_final': 2023, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'GOL G7 1.0 TSI', 'ano_inicial': 2018, 'ano_final': 2023, 'motorizacoes': '1.0 TSI Turbo'},
            ]},
            
            # VOYAGE
            {'nome': 'VOYAGE', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'VOYAGE QUADRADO 1.6', 'ano_inicial': 1981, 'ano_final': 1994, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'VOYAGE QUADRADO 1.8', 'ano_inicial': 1984, 'ano_final': 1994, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'VOYAGE QUADRADO 2.0', 'ano_inicial': 1988, 'ano_final': 1994, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'VOYAGE G5 1.0', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'VOYAGE G5 1.6', 'ano_inicial': 2008, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'VOYAGE G6 1.0', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'VOYAGE G6 1.6', 'ano_inicial': 2012, 'ano_final': 2016, 'motorizacoes': '1.6 16V Flex'},
                {'nome': 'VOYAGE G7 1.0', 'ano_inicial': 2016, 'ano_final': 2023, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'VOYAGE G7 1.6', 'ano_inicial': 2016, 'ano_final': 2023, 'motorizacoes': '1.6 16V MSI Flex'},
            ]},
            
            # PARATI
            {'nome': 'PARATI', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'PARATI QUADRADA 1.6', 'ano_inicial': 1982, 'ano_final': 1995, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'PARATI QUADRADA 1.8', 'ano_inicial': 1984, 'ano_final': 1995, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'PARATI BOLA 1.6', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'PARATI BOLA 1.8', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'PARATI BOLA 2.0', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'PARATI G3 1.0 16V', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.0 16V Turbo'},
                {'nome': 'PARATI G3 1.6', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'PARATI G3 1.8', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'PARATI G3 2.0', 'ano_inicial': 1999, 'ano_final': 2005, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'PARATI G4 1.6', 'ano_inicial': 2005, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'PARATI G4 1.8', 'ano_inicial': 2005, 'ano_final': 2013, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'PARATI SURF 1.6', 'ano_inicial': 2007, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'PARATI TRACK FIELD 1.6', 'ano_inicial': 2006, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
            ]},
            
            # SAVEIRO
            {'nome': 'SAVEIRO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'SAVEIRO QUADRADA 1.6', 'ano_inicial': 1982, 'ano_final': 1995, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'SAVEIRO QUADRADA 1.8', 'ano_inicial': 1984, 'ano_final': 1995, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'SAVEIRO BOLA 1.6', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'SAVEIRO BOLA 1.8', 'ano_inicial': 1995, 'ano_final': 1999, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'SAVEIRO BOLA 2.0', 'ano_inicial': 1997, 'ano_final': 1999, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'SAVEIRO G3 1.6', 'ano_inicial': 2000, 'ano_final': 2005, 'motorizacoes': '1.6 8V AP'},
                {'nome': 'SAVEIRO G3 1.8', 'ano_inicial': 2000, 'ano_final': 2005, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'SAVEIRO G3 2.0', 'ano_inicial': 2000, 'ano_final': 2005, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'SAVEIRO G4 1.6', 'ano_inicial': 2005, 'ano_final': 2009, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SAVEIRO G4 1.8', 'ano_inicial': 2005, 'ano_final': 2009, 'motorizacoes': '1.8 8V Flex'},
                {'nome': 'SAVEIRO G5 1.6', 'ano_inicial': 2009, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SAVEIRO G5 CROSS 1.6', 'ano_inicial': 2010, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SAVEIRO G5 TROOPER 1.6', 'ano_inicial': 2010, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SAVEIRO G6 1.6', 'ano_inicial': 2013, 'ano_final': 2016, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SAVEIRO G6 1.6 MSI', 'ano_inicial': 2014, 'ano_final': 2016, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'SAVEIRO G6 CROSS 1.6', 'ano_inicial': 2013, 'ano_final': 2016, 'motorizacoes': '1.6 16V Flex'},
                {'nome': 'SAVEIRO G7 1.6 MSI', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'SAVEIRO G7 CROSS 1.6', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'SAVEIRO G7 PEPPER 1.6', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'SAVEIRO G7 ROBUST 1.6', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.6 16V MSI Flex'},
            ]},
            
            # SANTANA / QUANTUM
            {'nome': 'SANTANA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'SANTANA 1.8', 'ano_inicial': 1984, 'ano_final': 2006, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'SANTANA 2.0', 'ano_inicial': 1984, 'ano_final': 2006, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'SANTANA 2.0 MI', 'ano_inicial': 1996, 'ano_final': 2006, 'motorizacoes': '2.0 8V MI'},
                {'nome': 'SANTANA EVIDENCE 2.0', 'ano_inicial': 1998, 'ano_final': 2006, 'motorizacoes': '2.0 8V MI'},
                {'nome': 'SANTANA EXCLUSIV 2.0', 'ano_inicial': 1998, 'ano_final': 2006, 'motorizacoes': '2.0 8V MI'},
            ]},
            
            {'nome': 'QUANTUM', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'QUANTUM 1.8', 'ano_inicial': 1985, 'ano_final': 2002, 'motorizacoes': '1.8 8V AP'},
                {'nome': 'QUANTUM 2.0', 'ano_inicial': 1985, 'ano_final': 2002, 'motorizacoes': '2.0 8V AP'},
                {'nome': 'QUANTUM 2.0 MI', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '2.0 8V MI'},
                {'nome': 'QUANTUM EVIDENCE 2.0', 'ano_inicial': 1998, 'ano_final': 2002, 'motorizacoes': '2.0 8V MI'},
            ]},
            
            # FOX / CROSSFOX / SPACEFOX
            {'nome': 'FOX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'FOX 1.0 8V', 'ano_inicial': 2003, 'ano_final': 2014, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'FOX 1.0 BLUEMOTION', 'ano_inicial': 2012, 'ano_final': 2014, 'motorizacoes': '1.0 8V Flex'},
                {'nome': 'FOX 1.6 8V', 'ano_inicial': 2003, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'FOX 1.6 MSI', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'FOX PRIME 1.6', 'ano_inicial': 2009, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'FOX HIGHLINE 1.6', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'FOX PEPPER 1.6', 'ano_inicial': 2015, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'FOX XTREME 1.6', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'FOX CONNECT 1.6', 'ano_inicial': 2019, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
            ]},
            
            {'nome': 'CROSSFOX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'CROSSFOX 1.6 8V', 'ano_inicial': 2005, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'CROSSFOX 1.6 MSI', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
            ]},
            
            {'nome': 'SPACEFOX', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'SPACEFOX 1.6 8V', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'SPACEFOX 1.6 MSI', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'SPACEFOX HIGHLINE 1.6', 'ano_inicial': 2015, 'ano_final': 2021, 'motorizacoes': '1.6 16V MSI Flex'},
            ]},
            
            # POLO
            {'nome': 'POLO', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'POLO CLASSIC 1.8', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '1.8 8V MI'},
                {'nome': 'POLO CLASSIC 2.0', 'ano_inicial': 1996, 'ano_final': 2002, 'motorizacoes': '2.0 8V MI'},
                {'nome': 'POLO HATCH 1.6', 'ano_inicial': 2002, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'POLO HATCH 2.0', 'ano_inicial': 2002, 'ano_final': 2006, 'motorizacoes': '2.0 8V'},
                {'nome': 'POLO SEDAN 1.6', 'ano_inicial': 2002, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'POLO SEDAN 2.0', 'ano_inicial': 2002, 'ano_final': 2006, 'motorizacoes': '2.0 8V'},
                {'nome': 'POLO SPORTLINE 1.6', 'ano_inicial': 2007, 'ano_final': 2012, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'POLO BLUEMOTION 1.6', 'ano_inicial': 2012, 'ano_final': 2014, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'NOVO POLO 1.0', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'NOVO POLO 1.0 TSI', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'NOVO POLO 1.4 TSI', 'ano_inicial': 2017, 'ano_final': 2020, 'motorizacoes': '1.4 TSI Turbo Flex'},
                {'nome': 'POLO GTS 1.4 TSI', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
                {'nome': 'POLO TRACK 1.0', 'ano_inicial': 2023, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
            ]},
            
            # VIRTUS
            {'nome': 'VIRTUS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'VIRTUS 1.0 TSI', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'VIRTUS 1.6 MSI', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.6 16V MSI Flex'},
                {'nome': 'VIRTUS HIGHLINE 1.0 TSI', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'VIRTUS GTS 1.4 TSI', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
            ]},
            
            # GOLF
            {'nome': 'GOLF', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'GOLF 1.6', 'ano_inicial': 1999, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'GOLF 2.0', 'ano_inicial': 1999, 'ano_final': 2013, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'GOLF GTI 1.8 TURBO', 'ano_inicial': 1999, 'ano_final': 2006, 'motorizacoes': '1.8 20V Turbo'},
                {'nome': 'GOLF SPORTLINE 1.6', 'ano_inicial': 2008, 'ano_final': 2013, 'motorizacoes': '1.6 8V Flex'},
                {'nome': 'GOLF COMFORTLINE 1.4 TSI', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '1.4 TSI Turbo'},
                {'nome': 'GOLF HIGHLINE 1.4 TSI', 'ano_inicial': 2014, 'ano_final': 2019, 'motorizacoes': '1.4 TSI Turbo'},
                {'nome': 'GOLF GTI 2.0 TSI', 'ano_inicial': 2014, 'ano_final': None, 'motorizacoes': '2.0 TSI Turbo'},
            ]},
            
            # JETTA
            {'nome': 'JETTA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'JETTA 2.0', 'ano_inicial': 2005, 'ano_final': 2010, 'motorizacoes': '2.0 8V Flex'},
                {'nome': 'JETTA 2.5', 'ano_inicial': 2005, 'ano_final': 2014, 'motorizacoes': '2.5 20V'},
                {'nome': 'JETTA TSI 2.0', 'ano_inicial': 2011, 'ano_final': 2018, 'motorizacoes': '2.0 TSI Turbo'},
                {'nome': 'JETTA 1.4 TSI', 'ano_inicial': 2016, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
                {'nome': 'JETTA GLI 2.0 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '2.0 TSI Turbo'},
            ]},
            
            # FUSCA
            {'nome': 'FUSCA', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'FUSCA 1300', 'ano_inicial': 1967, 'ano_final': 1986, 'motorizacoes': '1.3 8V Ar'},
                {'nome': 'FUSCA 1500', 'ano_inicial': 1970, 'ano_final': 1986, 'motorizacoes': '1.5 8V Ar'},
                {'nome': 'FUSCA 1600', 'ano_inicial': 1974, 'ano_final': 1996, 'motorizacoes': '1.6 8V Ar'},
                {'nome': 'FUSCA ITAMAR 1600', 'ano_inicial': 1993, 'ano_final': 1996, 'motorizacoes': '1.6 8V Ar Inj'},
            ]},
            
            # KOMBI
            {'nome': 'KOMBI', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'KOMBI 1.4 FLEX', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'KOMBI 1.6', 'ano_inicial': 1975, 'ano_final': 2005, 'motorizacoes': '1.6 8V Ar'},
                {'nome': 'KOMBI 1.6 MI', 'ano_inicial': 1997, 'ano_final': 2005, 'motorizacoes': '1.6 8V MI'},
                {'nome': 'KOMBI FURGAO 1.4', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'KOMBI ESCOLAR 1.4', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
                {'nome': 'KOMBI LOTACAO 1.4', 'ano_inicial': 2006, 'ano_final': 2014, 'motorizacoes': '1.4 8V Flex'},
            ]},
            
            # BRASILIA
            {'nome': 'BRASILIA', 'tipo': 'CARRO', 'popular': False, 'versoes': [
                {'nome': 'BRASILIA 1600', 'ano_inicial': 1973, 'ano_final': 1982, 'motorizacoes': '1.6 8V Ar'},
            ]},
            
            # UP
            {'nome': 'UP', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'UP 1.0 TAKE', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'UP 1.0 MOVE', 'ano_inicial': 2014, 'ano_final': 2021, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'UP 1.0 TSI MOVE', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'UP 1.0 TSI CONNECT', 'ano_inicial': 2018, 'ano_final': 2021, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'CROSS UP 1.0 TSI', 'ano_inicial': 2016, 'ano_final': 2021, 'motorizacoes': '1.0 TSI Turbo Flex'},
            ]},
            
            # T-CROSS
            {'nome': 'T-CROSS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'T-CROSS SENSE 1.0', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 12V Flex'},
                {'nome': 'T-CROSS 200 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'T-CROSS COMFORTLINE 200 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'T-CROSS HIGHLINE 250 TSI', 'ano_inicial': 2019, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
            ]},
            
            # NIVUS
            {'nome': 'NIVUS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'NIVUS 200 TSI', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'NIVUS COMFORTLINE 200 TSI', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
                {'nome': 'NIVUS HIGHLINE 200 TSI', 'ano_inicial': 2020, 'ano_final': None, 'motorizacoes': '1.0 TSI Turbo Flex'},
            ]},
            
            # TAOS
            {'nome': 'TAOS', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'TAOS COMFORTLINE 250 TSI', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
                {'nome': 'TAOS HIGHLINE 250 TSI', 'ano_inicial': 2021, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
            ]},
            
            # TIGUAN
            {'nome': 'TIGUAN', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'TIGUAN 2.0 TSI', 'ano_inicial': 2009, 'ano_final': 2016, 'motorizacoes': '2.0 TSI Turbo'},
                {'nome': 'TIGUAN ALLSPACE 250 TSI', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '1.4 TSI Turbo Flex'},
                {'nome': 'TIGUAN ALLSPACE 350 TSI', 'ano_inicial': 2017, 'ano_final': None, 'motorizacoes': '2.0 TSI Turbo'},
            ]},
            
            # AMAROK
            {'nome': 'AMAROK', 'tipo': 'CARRO', 'popular': True, 'versoes': [
                {'nome': 'AMAROK 2.0 TDI', 'ano_inicial': 2010, 'ano_final': None, 'motorizacoes': '2.0 TDI Diesel Bi-Turbo'},
                {'nome': 'AMAROK V6 3.0 TDI', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '3.0 V6 TDI Diesel'},
                {'nome': 'AMAROK HIGHLINE 2.0 TDI', 'ano_inicial': 2010, 'ano_final': None, 'motorizacoes': '2.0 TDI Diesel'},
                {'nome': 'AMAROK EXTREME V6', 'ano_inicial': 2018, 'ano_final': None, 'motorizacoes': '3.0 V6 TDI Diesel'},
                {'nome': 'AMAROK TRENDLINE 2.0 TDI', 'ano_inicial': 2010, 'ano_final': None, 'motorizacoes': '2.0 TDI Diesel'},
                {'nome': 'AMAROK SE 2.0 TDI', 'ano_inicial': 2012, 'ano_final': 2017, 'motorizacoes': '2.0 TDI Diesel'},
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
        self.stdout.write(self.style.SUCCESS('VOLKSWAGEN concluído!'))
