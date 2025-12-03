# ============================================================
# COMANDO DJANGO: POPULAR CATEGORIAS E CLASSIFICAR PRODUTOS
# ============================================================
# Arquivo: estoque/management/commands/popular_categorias_completo.py
#
# Estrutura de pastas necessária:
# estoque/
#   management/
#     __init__.py
#     commands/
#       __init__.py
#       popular_categorias_completo.py
#
# Para executar:
# python manage.py popular_categorias_completo
# ============================================================

from django.core.management.base import BaseCommand
from estoque.models import Categoria, Subcategoria, Grupo, Subgrupo, Produto
import re


class Command(BaseCommand):
    help = 'Popula categorias, subcategorias, grupos, subgrupos e classifica produtos'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('POPULANDO CATEGORIAS E CLASSIFICANDO PRODUTOS')
        self.stdout.write('=' * 60)

        # ============================================================
        # PASSO 1: LIMPAR TUDO
        # ============================================================
        self.stdout.write('')
        self.stdout.write('🗑️  LIMPANDO DADOS ANTIGOS...')
        
        # Primeiro, remover referências dos produtos
        Produto.objects.all().update(
            categoria=None,
            subcategoria=None,
            grupo=None,
            subgrupo=None
        )
        self.stdout.write('  ✅ Referências dos produtos removidas')
        
        # Deletar na ordem correta (do mais específico para o mais geral)
        deleted_subgrupos = Subgrupo.objects.all().delete()[0]
        self.stdout.write(f'  ✅ {deleted_subgrupos} subgrupos deletados')
        
        deleted_grupos = Grupo.objects.all().delete()[0]
        self.stdout.write(f'  ✅ {deleted_grupos} grupos deletados')
        
        deleted_subcategorias = Subcategoria.objects.all().delete()[0]
        self.stdout.write(f'  ✅ {deleted_subcategorias} subcategorias deletadas')
        
        deleted_categorias = Categoria.objects.all().delete()[0]
        self.stdout.write(f'  ✅ {deleted_categorias} categorias deletadas')

        # ============================================================
        # ESTRUTURA COMPLETA
        # ============================================================
        
        estrutura = {
            'BATERIAS': {
                'subcategorias': {
                    'Bateria Automotiva': {
                        'grupos': {
                            'Bateria Convencional': {'subgrupos': ['Kraft', 'Omega', 'Pioneiro', 'Heliar', 'Onbat']},
                            'Bateria Start-Stop (AGM)': {'subgrupos': ['Heliar', 'Moura']},
                            'Bateria Start-Stop (EFB)': {'subgrupos': ['Heliar', 'Moura']},
                            'Bateria Selada (Livre de Manutenção)': {'subgrupos': ['Kraft', 'Omega', 'Pioneiro', 'Heliar', 'Onbat']},
                        }
                    },
                    'Bateria Moto': {
                        'grupos': {
                            'Bateria Convencional': {'subgrupos': ['Kraft']},
                            'Bateria Selada': {'subgrupos': ['Kraft']},
                            'Bateria Gel': {'subgrupos': ['Kraft']},
                        }
                    },
                    'Bateria Controle/Lítio': {
                        'grupos': {
                            'CR2032 (Disco)': {'subgrupos': ['Golden']},
                            'CR2025 (Disco)': {'subgrupos': ['Golden']},
                            'CR2016 (Disco)': {'subgrupos': ['Golden']},
                            'CR2450 (Disco)': {'subgrupos': ['Golden']},
                            'CR123A (Cilíndrica)': {'subgrupos': ['Golden']},
                            '23A 12V (Cilíndrica)': {'subgrupos': ['Golden']},
                            '27A 12V (Cilíndrica)': {'subgrupos': ['Golden']},
                            'LR44 (Botão)': {'subgrupos': ['Golden']},
                            'A76 (Botão)': {'subgrupos': ['Golden']},
                        }
                    },
                }
            },
            'PARTE ELÉTRICA': {
                'subcategorias': {
                    'Alternador': {
                        'grupos': {
                            'Rotor': {'subgrupos': ['Donati', 'Bosch', 'Indutec']},
                            'Estator': {'subgrupos': ['Donati']},
                            'Regulador Voltagem': {'subgrupos': ['Gauss', 'Bosch', 'Valeo']},
                            'Retificador': {'subgrupos': ['Gauss']},
                            'Rolamento': {'subgrupos': ['VTO', 'NSK', 'Gauss']},
                            'Escova': {'subgrupos': ['Schunk']},
                            'Polia': {'subgrupos': ['Zen']},
                            'Mancal': {'subgrupos': []},
                        }
                    },
                    'Motor Partida': {
                        'grupos': {
                            'Induzido': {'subgrupos': ['Donati', 'Bosch', 'Indutec']},
                            'Bendix': {'subgrupos': ['Zen', 'Fiorenzi', 'Bosch']},
                            'Automático': {'subgrupos': ['SDL', 'ZF']},
                            'Suporte Escova': {'subgrupos': ['Bosch', 'Valeo', 'SCA', 'UF', 'MYR']},
                            'Planetária': {'subgrupos': []},
                            'Bobina Campo': {'subgrupos': []},
                            'Garfo': {'subgrupos': []},
                            'Mancal': {'subgrupos': []},
                        }
                    },
                    'Ignição': {
                        'grupos': {
                            'Bobina Ignição': {'subgrupos': []},
                            'Vela': {'subgrupos': []},
                            'Cabo Vela': {'subgrupos': []},
                            'Tampa Distribuidor': {'subgrupos': []},
                            'Rotor Distribuidor': {'subgrupos': ['Bosch', 'Marflex']},
                            'Módulo Ignição': {'subgrupos': []},
                        }
                    },
                    'Sensores': {
                        'grupos': {
                            'Sensor Temperatura': {'subgrupos': []},
                            'Sensor Óleo': {'subgrupos': []},
                            'Sensor Ré': {'subgrupos': []},
                            'Interruptor Freio': {'subgrupos': ['Marflex']},
                            'Interruptor Embreagem': {'subgrupos': []},
                        }
                    },
                    'Iluminação': {
                        'grupos': {
                            'Farol': {'subgrupos': ['Arteb', 'Orgus', 'Cibie']},
                            'Lanterna Dianteira': {'subgrupos': ['Cibie', 'Arteb', 'JCV']},
                            'Lanterna Traseira': {'subgrupos': ['JCV', 'Cofran', 'HT', 'IAN', 'AMG', 'Arteb']},
                            'Lanterna Lateral': {'subgrupos': ['Sinalsul']},
                            'Lanterna Placa': {'subgrupos': ['DSC']},
                            'Lanterna Teto': {'subgrupos': []},
                            'Farol Milha': {'subgrupos': ['Orgus']},
                        }
                    },
                    'Lâmpadas': {
                        'grupos': {
                            'Farol (H1/H3/H4/H7/HB3/HB4)': {'subgrupos': ['Philips', 'Tiger', 'Eagleye', 'Neolux', 'Tesla', 'Gauss']},
                            'LED': {'subgrupos': ['BTR', 'Autopoli', 'Fenix']},
                            'Pisca/Seta': {'subgrupos': []},
                            'Painel': {'subgrupos': []},
                            'Torpedo': {'subgrupos': ['Philips']},
                        }
                    },
                    'Relés': {
                        'grupos': {
                            'Relé Auxiliar': {'subgrupos': ['DNI']},
                            'Relé Pisca': {'subgrupos': ['DNI']},
                            'Relé Temporizador': {'subgrupos': []},
                            'Relé Bomba Combustível': {'subgrupos': []},
                        }
                    },
                    'Fusíveis': {
                        'grupos': {
                            'Fusível Lamina': {'subgrupos': []},
                            'Fusível Mini': {'subgrupos': []},
                            'Fusível Maxi': {'subgrupos': []},
                            'Porta Fusível': {'subgrupos': []},
                        }
                    },
                    'Chicotes': {
                        'grupos': {
                            'Chicote Sensor': {'subgrupos': []},
                            'Chicote Farol': {'subgrupos': []},
                            'Chicote Bomba': {'subgrupos': []},
                            'Chicote Rádio': {'subgrupos': []},
                        }
                    },
                    'Soquetes': {
                        'grupos': {
                            'Soquete Farol': {'subgrupos': ['ETE']},
                            'Soquete Lanterna': {'subgrupos': ['ETE']},
                            'Soquete Painel': {'subgrupos': []},
                        }
                    },
                    'Chaves e Comutadores': {
                        'grupos': {
                            'Chave Seta': {'subgrupos': []},
                            'Chave Luz': {'subgrupos': []},
                            'Comutador Ignição': {'subgrupos': []},
                            'Cilindro Ignição': {'subgrupos': []},
                            'Chave Limpador': {'subgrupos': []},
                        }
                    },
                    'Botões': {
                        'grupos': {
                            'Botão Vidro Elétrico': {'subgrupos': []},
                            'Botão Pisca Alerta': {'subgrupos': []},
                            'Botão Trava Porta': {'subgrupos': []},
                            'Botão Partida': {'subgrupos': []},
                        }
                    },
                }
            },
            'CARROCERIA': {
                'subcategorias': {
                    'Retrovisores': {
                        'grupos': {
                            'Retrovisor Externo': {'subgrupos': ['Blawer', 'Retrovex', 'Cofran', 'Metagal', 'Ficosa']},
                            'Retrovisor Interno': {'subgrupos': []},
                            'Vidro Retrovisor': {'subgrupos': ['Blawer', 'Retroparts', 'Refix']},
                            'Capa Retrovisor': {'subgrupos': []},
                            'Aplique Retrovisor': {'subgrupos': []},
                        }
                    },
                    'Maçanetas': {
                        'grupos': {
                            'Maçaneta Externa': {'subgrupos': []},
                            'Maçaneta Interna': {'subgrupos': []},
                            'Gatilho': {'subgrupos': []},
                            'Cilindro Maçaneta': {'subgrupos': []},
                        }
                    },
                    'Fechaduras': {
                        'grupos': {
                            'Fechadura Porta': {'subgrupos': []},
                            'Fechadura Ignição': {'subgrupos': []},
                            'Fechadura Mala': {'subgrupos': []},
                        }
                    },
                    'Emblemas': {
                        'grupos': {
                            'Emblema VW': {'subgrupos': []},
                            'Emblema GM': {'subgrupos': []},
                            'Emblema Fiat': {'subgrupos': []},
                            'Emblema Ford': {'subgrupos': []},
                            'Emblema Toyota': {'subgrupos': []},
                            'Emblema Honda': {'subgrupos': []},
                        }
                    },
                    'Apliques': {
                        'grupos': {
                            'Aplique Cromado Maçaneta': {'subgrupos': []},
                            'Aplique Cromado Retrovisor': {'subgrupos': []},
                            'Aplique Tampa Combustível': {'subgrupos': []},
                        }
                    },
                    'Frisos': {
                        'grupos': {
                            'Friso Lateral': {'subgrupos': []},
                            'Friso Para-choque': {'subgrupos': []},
                        }
                    },
                    'Grades': {
                        'grupos': {
                            'Grade Radiador': {'subgrupos': []},
                            'Grade Para-choque': {'subgrupos': []},
                        }
                    },
                    'Borrachas': {
                        'grupos': {
                            'Borracha Porta': {'subgrupos': []},
                            'Borracha Porta-Malas': {'subgrupos': []},
                            'Borracha Vedação': {'subgrupos': []},
                        }
                    },
                }
            },
            'VIDROS E MÁQUINAS': {
                'subcategorias': {
                    'Máquina Vidro Manual': {
                        'grupos': {
                            'Máquina Dianteira': {'subgrupos': []},
                            'Máquina Traseira': {'subgrupos': []},
                        }
                    },
                    'Máquina Vidro Elétrico': {
                        'grupos': {
                            'Máquina Dianteira': {'subgrupos': []},
                            'Máquina Traseira': {'subgrupos': []},
                            'Motor Vidro': {'subgrupos': []},
                        }
                    },
                    'Componentes': {
                        'grupos': {
                            'Kit Reparo': {'subgrupos': []},
                            'Roldana': {'subgrupos': []},
                            'Arraste': {'subgrupos': []},
                            'Suporte Vidro': {'subgrupos': []},
                            'Cabo Máquina': {'subgrupos': []},
                        }
                    },
                    'Manivela': {
                        'grupos': {
                            'Manivela Vidro': {'subgrupos': []},
                        }
                    },
                }
            },
            'MOTOR': {
                'subcategorias': {
                    'Arrefecimento': {
                        'grupos': {
                            "Bomba D'água": {'subgrupos': []},
                            'Válvula Termostática': {'subgrupos': []},
                            'Cebolão Radiador': {'subgrupos': []},
                            'Mangueira Radiador': {'subgrupos': []},
                            'Reservatório Expansão': {'subgrupos': ['Gonel']},
                            'Tampa Radiador': {'subgrupos': []},
                            'Tampa Reservatório': {'subgrupos': []},
                        }
                    },
                    'Alimentação': {
                        'grupos': {
                            'Bomba Combustível': {'subgrupos': ['Marwal']},
                            'Bico Injetor': {'subgrupos': []},
                            'Regulador Pressão': {'subgrupos': []},
                        }
                    },
                    'Correias': {
                        'grupos': {
                            'Correia Dentada': {'subgrupos': []},
                            'Correia Poly V': {'subgrupos': ['Contitech', 'Gates']},
                            'Correia em V': {'subgrupos': ['Contitech', 'Dayco', 'Gates']},
                            'Tensor': {'subgrupos': []},
                        }
                    },
                    'Filtros': {
                        'grupos': {
                            'Filtro Ar': {'subgrupos': ['Tecfil', 'Mann', 'Redux32']},
                            'Filtro Óleo': {'subgrupos': ['Tecfil', 'Wega', 'Mann', 'Vox', 'Seineca']},
                            'Filtro Combustível': {'subgrupos': ['Tecfil', 'Mann']},
                            'Filtro Cabine': {'subgrupos': ['Tecfil', 'Redux32', 'Wega', 'Japanparts']},
                        }
                    },
                    'Tampas e Vedações': {
                        'grupos': {
                            'Tampa Óleo': {'subgrupos': []},
                            'Vareta Nível': {'subgrupos': []},
                            'Junta Cabeçote': {'subgrupos': []},
                            'Junta Carter': {'subgrupos': []},
                        }
                    },
                }
            },
            'INTERIOR': {
                'subcategorias': {
                    'Bancos': {
                        'grupos': {
                            'Capa Reclinável': {'subgrupos': []},
                            'Manopla Regulagem': {'subgrupos': []},
                            'Botão Trava Banco': {'subgrupos': ['VB']},
                            'Deslize Banco': {'subgrupos': []},
                            'Alça Banco': {'subgrupos': ['VB']},
                        }
                    },
                    'Câmbio': {
                        'grupos': {
                            'Bola Câmbio': {'subgrupos': []},
                            'Coifa Câmbio': {'subgrupos': []},
                            'Kit Trambulador': {'subgrupos': []},
                        }
                    },
                    'Painel': {
                        'grupos': {
                            'Difusor Ar': {'subgrupos': []},
                            'Moldura Painel': {'subgrupos': []},
                            'Cobertura Painel': {'subgrupos': []},
                        }
                    },
                    'Volante': {
                        'grupos': {
                            'Cubo Volante': {'subgrupos': []},
                            'Came Volante': {'subgrupos': ['DSC']},
                            'Cinta Airbag': {'subgrupos': []},
                        }
                    },
                    'Pedais': {
                        'grupos': {
                            'Kit Borracha Pedal': {'subgrupos': []},
                        }
                    },
                    'Portas': {
                        'grupos': {
                            'Puxador Porta': {'subgrupos': []},
                            'Pino Trava': {'subgrupos': []},
                            'Moldura Maçaneta': {'subgrupos': []},
                            'Botão Trava': {'subgrupos': []},
                        }
                    },
                    'Diversos': {
                        'grupos': {
                            'Quebra-Sol': {'subgrupos': []},
                            'Lanterna Teto': {'subgrupos': []},
                            'Tapete': {'subgrupos': []},
                        }
                    },
                }
            },
            'LIMPADOR PARA-BRISA': {
                'subcategorias': {
                    'Palhetas': {
                        'grupos': {
                            'Palheta Dianteira Comum': {'subgrupos': ['VTO']},
                            'Palheta Dianteira Específica': {'subgrupos': ['Redux32']},
                            'Palheta Silicone': {'subgrupos': ['Tiger', 'Code', 'Techone', 'BTR']},
                            'Palheta Traseira': {'subgrupos': ['Redux32']},
                        }
                    },
                    'Componentes': {
                        'grupos': {
                            'Bomba Limpador': {'subgrupos': []},
                            'Reservatório Água': {'subgrupos': ['Gonel']},
                            'Motor Limpador': {'subgrupos': []},
                            'Bico Ejetor': {'subgrupos': []},
                            'Conexão/Mangueira': {'subgrupos': []},
                        }
                    },
                }
            },
            'SOM E ACESSÓRIOS': {
                'subcategorias': {
                    'Alto-Falantes': {
                        'grupos': {
                            'Reparo Driver': {'subgrupos': ['JBL']},
                            'Reparo Tweeter': {'subgrupos': ['Scorpion']},
                            'Capacitor': {'subgrupos': ['Technoise']},
                            'Corneta': {'subgrupos': ['Permak']},
                        }
                    },
                    'Instalação': {
                        'grupos': {
                            'Chicote Rádio': {'subgrupos': ['Permak', 'Pioneer', 'Buster']},
                            'Antena': {'subgrupos': ['Permark']},
                            'Aro Adaptador Alto-Falante': {'subgrupos': []},
                        }
                    },
                    'Acessórios': {
                        'grupos': {
                            'Câmera Ré': {'subgrupos': ['Techone']},
                            'Sensor Estacionamento': {'subgrupos': []},
                        }
                    },
                }
            },
            'QUÍMICOS E LUBRIFICANTES': {
                'subcategorias': {
                    'Óleos Motor': {
                        'grupos': {
                            '5W30': {'subgrupos': ['Shell', 'Castrol', 'Petronas', 'Radnac', 'Texas']},
                            '10W40': {'subgrupos': ['Castrol', 'Petronas', 'Dulub', 'Panther', 'Radnac']},
                            '15W40': {'subgrupos': ['Lubrax', 'Petronas', 'Shell', 'Texas']},
                            '20W50': {'subgrupos': ['Lubrax', 'Castrol', 'Shell', 'Petronas', 'Bradock']},
                            '25W60': {'subgrupos': ['Lubrax', 'Castrol']},
                        }
                    },
                    'Óleos Transmissão': {
                        'grupos': {
                            'ATF': {'subgrupos': ['Lubrax', 'Castrol', 'Panther', 'Dulub', 'Petronas']},
                            'Hidráulico': {'subgrupos': ['Dulub']},
                            'Câmbio': {'subgrupos': ['Dulub', 'Lubrax']},
                        }
                    },
                    'Óleos Freio': {
                        'grupos': {
                            'DOT3': {'subgrupos': ['Varga', 'Radnaq']},
                            'DOT4': {'subgrupos': ['Radnaq']},
                            'DOT5': {'subgrupos': ['Tirreno']},
                        }
                    },
                    'Aditivos': {
                        'grupos': {
                            'Aditivo Radiador': {'subgrupos': ['Paraflu', 'Coolant', 'Tutela']},
                            'Aditivo Combustível': {'subgrupos': []},
                        }
                    },
                    'Limpeza': {
                        'grupos': {
                            'Limpa Contato': {'subgrupos': ['Tecbril']},
                            'Limpa Ar Condicionado': {'subgrupos': []},
                            'Shampoo': {'subgrupos': []},
                            'Limpa Para-brisa': {'subgrupos': ['Radnaq']},
                        }
                    },
                    'Lubrificantes': {
                        'grupos': {
                            'Silicone': {'subgrupos': ['Radnac', 'Tecbril', 'Orbi']},
                            'Graxa': {'subgrupos': ['Radnaq', 'Incollub']},
                            'WD40': {'subgrupos': ['WD40']},
                            'Vaselina': {'subgrupos': []},
                            'Descarbonizante': {'subgrupos': ['Tecbril']},
                        }
                    },
                    'Colas e Vedantes': {
                        'grupos': {
                            'Silicone Alta Temp': {'subgrupos': ['Orbi']},
                            'Cola Instantânea': {'subgrupos': ['Tekbond']},
                            'Veda Junta': {'subgrupos': ['Orbi']},
                        }
                    },
                }
            },
            'FIXAÇÃO E TERMINAIS': {
                'subcategorias': {
                    'Abraçadeiras': {
                        'grupos': {
                            'Abraçadeira Nylon': {'subgrupos': []},
                            'Abraçadeira Metal': {'subgrupos': []},
                            'Abraçadeira Mola': {'subgrupos': []},
                        }
                    },
                    'Terminais Bateria': {
                        'grupos': {
                            'Terminal Positivo/Negativo': {'subgrupos': []},
                            'Garra Bateria': {'subgrupos': ['ETE']},
                        }
                    },
                    'Terminais Elétricos': {
                        'grupos': {
                            'Terminal Olhal': {'subgrupos': ['ETE']},
                            'Terminal Encaixe': {'subgrupos': ['ETE']},
                            'Terminal Forquilha': {'subgrupos': []},
                        }
                    },
                }
            },
            'TRAVAS E ALARMES': {
                'subcategorias': {
                    'Trava Elétrica': {
                        'grupos': {
                            'Trava Porta': {'subgrupos': []},
                            'Centralina': {'subgrupos': ['Positron', 'Soft', 'Tury']},
                            'Motor Fechadura': {'subgrupos': []},
                            'Cabo Acionamento': {'subgrupos': []},
                        }
                    },
                    'Vidro Elétrico': {
                        'grupos': {
                            'Centralina Vidro': {'subgrupos': ['Soft', 'Tury']},
                            'Motor Vidro': {'subgrupos': []},
                        }
                    },
                    'Telecomando': {
                        'grupos': {
                            'Capa Telecomando': {'subgrupos': []},
                            'Botão Telecomando': {'subgrupos': []},
                        }
                    },
                }
            },
            'PARA-CHOQUE E EXTERNA': {
                'subcategorias': {
                    'Para-choque': {
                        'grupos': {
                            'Grade Para-choque': {'subgrupos': []},
                            'Ponteira': {'subgrupos': []},
                            'Refletor': {'subgrupos': []},
                        }
                    },
                    'Proteção': {
                        'grupos': {
                            'Calha Chuva': {'subgrupos': []},
                            'Protetor Porta': {'subgrupos': []},
                        }
                    },
                    'Engate Reboque': {
                        'grupos': {
                            'Engate': {'subgrupos': []},
                            'Tomada Reboque': {'subgrupos': []},
                            'Bola Engate': {'subgrupos': []},
                            'Capa Engate': {'subgrupos': []},
                        }
                    },
                    'Tampa Combustível': {
                        'grupos': {
                            'Tampa Tanque': {'subgrupos': []},
                        }
                    },
                }
            },
            'SUSPENSÃO E RODAS': {
                'subcategorias': {
                    'Amortecedores': {
                        'grupos': {
                            'Amortecedor Mala': {'subgrupos': []},
                            'Amortecedor Capô': {'subgrupos': []},
                        }
                    },
                    'Rolamentos': {
                        'grupos': {
                            'Rolamento Roda Dianteiro': {'subgrupos': []},
                            'Rolamento Roda Traseiro': {'subgrupos': []},
                        }
                    },
                    'Buchas': {
                        'grupos': {
                            'Bucha Suspensão': {'subgrupos': []},
                        }
                    },
                    'Rodas': {
                        'grupos': {
                            'Calota': {'subgrupos': []},
                            'Câmara de Ar': {'subgrupos': []},
                            'Parafuso Roda': {'subgrupos': []},
                            'Porca Roda': {'subgrupos': []},
                            'Prisioneiro': {'subgrupos': []},
                        }
                    },
                }
            },
            'MOTO': {
                'subcategorias': {
                    'Pneus': {
                        'grupos': {
                            'Pneu Dianteiro': {'subgrupos': []},
                            'Pneu Traseiro': {'subgrupos': []},
                        }
                    },
                    'Câmaras': {
                        'grupos': {
                            'Câmara Dianteira': {'subgrupos': []},
                            'Câmara Traseira': {'subgrupos': []},
                        }
                    },
                    'Elétrica': {
                        'grupos': {
                            'Lâmpada Moto': {'subgrupos': []},
                            'Vela Moto': {'subgrupos': []},
                        }
                    },
                }
            },
            'FERRAMENTAS': {
                'subcategorias': {
                    'Chaves': {
                        'grupos': {
                            'Chave Combinada': {'subgrupos': ['Tramontina']},
                            'Chave Canhão': {'subgrupos': ['Tramontina']},
                            'Chave Roda': {'subgrupos': []},
                        }
                    },
                    'Solda': {
                        'grupos': {
                            'Solda Tubo': {'subgrupos': []},
                        }
                    },
                    'Extintor': {
                        'grupos': {
                            'Extintor Incêndio': {'subgrupos': []},
                        }
                    },
                }
            },
        }

        # ============================================================
        # CRIAR CATEGORIAS, SUBCATEGORIAS, GRUPOS E SUBGRUPOS
        # ============================================================
        
        self.stdout.write('')
        self.stdout.write('📦 CRIANDO ESTRUTURA DE CATEGORIAS...')
        
        total_categorias = 0
        total_subcategorias = 0
        total_grupos = 0
        total_subgrupos = 0
        
        for cat_nome, cat_data in estrutura.items():
            # Criar categoria
            categoria = Categoria.objects.create(
                nome=cat_nome,
                ativo=True
            )
            total_categorias += 1
            self.stdout.write(f'  ✅ Categoria: {cat_nome}')
            
            for subcat_nome, subcat_data in cat_data['subcategorias'].items():
                # Criar subcategoria
                subcategoria = Subcategoria.objects.create(
                    nome=subcat_nome,
                    categoria=categoria,
                    ativo=True
                )
                total_subcategorias += 1
                
                for grupo_nome, grupo_data in subcat_data['grupos'].items():
                    # Criar grupo
                    grupo = Grupo.objects.create(
                        nome=grupo_nome,
                        subcategoria=subcategoria,
                        ativo=True
                    )
                    total_grupos += 1
                    
                    for subgrupo_nome in grupo_data['subgrupos']:
                        # Criar subgrupo
                        Subgrupo.objects.create(
                            nome=subgrupo_nome,
                            grupo=grupo,
                            ativo=True
                        )
                        total_subgrupos += 1

        self.stdout.write('')
        self.stdout.write(f'📊 Categorias criadas: {total_categorias}')
        self.stdout.write(f'📊 Subcategorias criadas: {total_subcategorias}')
        self.stdout.write(f'📊 Grupos criados: {total_grupos}')
        self.stdout.write(f'📊 Subgrupos criados: {total_subgrupos}')

        # ============================================================
        # CLASSIFICAR PRODUTOS
        # ============================================================
        
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write('CLASSIFICANDO PRODUTOS...')
        self.stdout.write('=' * 60)
        
        # Regras de classificação (palavra-chave -> (categoria, subcategoria, grupo))
        regras = [
            # BATERIAS
            (r'BATERIA.*(HELIAR|KRAFT|OMEGA|PIONEIRO|ONBAT).*(?:AH|MESES)', 'BATERIAS', 'Bateria Automotiva', 'Bateria Selada (Livre de Manutenção)'),
            (r'BATERIA.*MOTO', 'BATERIAS', 'Bateria Moto', 'Bateria Selada'),
            (r'BATERIA.*CONTROLE|BATERIA.*ALARME|BATERIA.*GOLDEN', 'BATERIAS', 'Bateria Controle/Lítio', 'CR2032 (Disco)'),
            
            # PARTE ELÉTRICA - Alternador
            (r'ROTOR ALT', 'PARTE ELÉTRICA', 'Alternador', 'Rotor'),
            (r'ESTATOR ALT', 'PARTE ELÉTRICA', 'Alternador', 'Estator'),
            (r'REGULADOR VOLT', 'PARTE ELÉTRICA', 'Alternador', 'Regulador Voltagem'),
            (r'RETIFICADOR ALT', 'PARTE ELÉTRICA', 'Alternador', 'Retificador'),
            (r'ROLAMENTO ALT', 'PARTE ELÉTRICA', 'Alternador', 'Rolamento'),
            (r'ESCOVA ALT', 'PARTE ELÉTRICA', 'Alternador', 'Escova'),
            (r'POLIA ALT', 'PARTE ELÉTRICA', 'Alternador', 'Polia'),
            (r'MANCAL ALT', 'PARTE ELÉTRICA', 'Alternador', 'Mancal'),
            
            # PARTE ELÉTRICA - Motor Partida
            (r'INDUZIDO', 'PARTE ELÉTRICA', 'Motor Partida', 'Induzido'),
            (r'BENDIX', 'PARTE ELÉTRICA', 'Motor Partida', 'Bendix'),
            (r'AUTOMATICO PART', 'PARTE ELÉTRICA', 'Motor Partida', 'Automático'),
            (r'SUPORTE ESC PART', 'PARTE ELÉTRICA', 'Motor Partida', 'Suporte Escova'),
            (r'PLANETARIA', 'PARTE ELÉTRICA', 'Motor Partida', 'Planetária'),
            (r'BOBINA CAMPO PART', 'PARTE ELÉTRICA', 'Motor Partida', 'Bobina Campo'),
            (r'GARFO ARRAN|GARFO PART', 'PARTE ELÉTRICA', 'Motor Partida', 'Garfo'),
            (r'MANCAL PART', 'PARTE ELÉTRICA', 'Motor Partida', 'Mancal'),
            
            # PARTE ELÉTRICA - Ignição
            (r'BOBINA IGN', 'PARTE ELÉTRICA', 'Ignição', 'Bobina Ignição'),
            (r'VELA IGN', 'PARTE ELÉTRICA', 'Ignição', 'Vela'),
            (r'CABO VELA', 'PARTE ELÉTRICA', 'Ignição', 'Cabo Vela'),
            (r'TAMPA DISTRIB', 'PARTE ELÉTRICA', 'Ignição', 'Tampa Distribuidor'),
            (r'ROTOR DISTRIB', 'PARTE ELÉTRICA', 'Ignição', 'Rotor Distribuidor'),
            (r'MODULO IGN', 'PARTE ELÉTRICA', 'Ignição', 'Módulo Ignição'),
            
            # PARTE ELÉTRICA - Sensores
            (r'SENSOR TEMP', 'PARTE ELÉTRICA', 'Sensores', 'Sensor Temperatura'),
            (r'INTERROPTOR OLEO|INTERRUPTOR OLEO|SENSOR OLEO', 'PARTE ELÉTRICA', 'Sensores', 'Sensor Óleo'),
            (r'INTERROPTOR RE|INTERRUPTOR RE|SENSOR RE', 'PARTE ELÉTRICA', 'Sensores', 'Sensor Ré'),
            (r'INTERROPTOR FREIO|INTERRUPTOR FREIO', 'PARTE ELÉTRICA', 'Sensores', 'Interruptor Freio'),
            (r'INTERROPTOR EMBREA|INTERRUPTOR EMBREA', 'PARTE ELÉTRICA', 'Sensores', 'Interruptor Embreagem'),
            
            # PARTE ELÉTRICA - Iluminação
            (r'^FAROL(?! MILHA)', 'PARTE ELÉTRICA', 'Iluminação', 'Farol'),
            (r'FAROL MILHA|FAROL AUX', 'PARTE ELÉTRICA', 'Iluminação', 'Farol Milha'),
            (r'LANT DNT|LANTERNA DIANT', 'PARTE ELÉTRICA', 'Iluminação', 'Lanterna Dianteira'),
            (r'LANT TRAS|LANTERNA TRAS', 'PARTE ELÉTRICA', 'Iluminação', 'Lanterna Traseira'),
            (r'LANT LATERAL|LANTERNA LATERAL', 'PARTE ELÉTRICA', 'Iluminação', 'Lanterna Lateral'),
            (r'LANT.*PLACA|LANTERNA PLACA', 'PARTE ELÉTRICA', 'Iluminação', 'Lanterna Placa'),
            (r'LANT.*TETO|LANTERNA TETO', 'PARTE ELÉTRICA', 'Iluminação', 'Lanterna Teto'),
            
            # PARTE ELÉTRICA - Lâmpadas
            (r'LAMPADA.*(H1|H3|H4|H7|H8|H9|H11|H16|H27|HB1|HB3|HB4)', 'PARTE ELÉTRICA', 'Lâmpadas', 'Farol (H1/H3/H4/H7/HB3/HB4)'),
            (r'LAMPADA.*LED', 'PARTE ELÉTRICA', 'Lâmpadas', 'LED'),
            (r'LAMPADA.*(PISCA|SETA|1 POLO|2 POLO|1POLO|2POLO)', 'PARTE ELÉTRICA', 'Lâmpadas', 'Pisca/Seta'),
            (r'LAMPADA.*PAINEL', 'PARTE ELÉTRICA', 'Lâmpadas', 'Painel'),
            (r'LAMPADA.*TORPEDO', 'PARTE ELÉTRICA', 'Lâmpadas', 'Torpedo'),
            
            # PARTE ELÉTRICA - Relés
            (r'RELE AUX', 'PARTE ELÉTRICA', 'Relés', 'Relé Auxiliar'),
            (r'RELE PISCA', 'PARTE ELÉTRICA', 'Relés', 'Relé Pisca'),
            (r'RELE TEMPO', 'PARTE ELÉTRICA', 'Relés', 'Relé Temporizador'),
            (r'RELE.*BOMBA|RELE COMB', 'PARTE ELÉTRICA', 'Relés', 'Relé Bomba Combustível'),
            
            # PARTE ELÉTRICA - Fusíveis
            (r'FUSIVEL LAMINA', 'PARTE ELÉTRICA', 'Fusíveis', 'Fusível Lamina'),
            (r'FUSIVEL MINI', 'PARTE ELÉTRICA', 'Fusíveis', 'Fusível Mini'),
            (r'FUSIVEL MAXI', 'PARTE ELÉTRICA', 'Fusíveis', 'Fusível Maxi'),
            (r'PORTA FUSIVEL', 'PARTE ELÉTRICA', 'Fusíveis', 'Porta Fusível'),
            
            # PARTE ELÉTRICA - Chicotes
            (r'CHICOTE.*SENSOR', 'PARTE ELÉTRICA', 'Chicotes', 'Chicote Sensor'),
            (r'CHICOTE.*FAROL', 'PARTE ELÉTRICA', 'Chicotes', 'Chicote Farol'),
            (r'CHICOTE.*BOMBA', 'PARTE ELÉTRICA', 'Chicotes', 'Chicote Bomba'),
            (r'CHICOTE.*RADIO', 'PARTE ELÉTRICA', 'Chicotes', 'Chicote Rádio'),
            (r'CHICOTE', 'PARTE ELÉTRICA', 'Chicotes', 'Chicote Sensor'),
            
            # PARTE ELÉTRICA - Soquetes
            (r'SOQUETE.*FAROL', 'PARTE ELÉTRICA', 'Soquetes', 'Soquete Farol'),
            (r'SOQUETE.*(LANT|PISCA)', 'PARTE ELÉTRICA', 'Soquetes', 'Soquete Lanterna'),
            (r'SOQUETE.*PAINEL', 'PARTE ELÉTRICA', 'Soquetes', 'Soquete Painel'),
            (r'SOQUETE', 'PARTE ELÉTRICA', 'Soquetes', 'Soquete Lanterna'),
            
            # PARTE ELÉTRICA - Chaves e Comutadores
            (r'CHAVE SETA', 'PARTE ELÉTRICA', 'Chaves e Comutadores', 'Chave Seta'),
            (r'CHAVE LUZ', 'PARTE ELÉTRICA', 'Chaves e Comutadores', 'Chave Luz'),
            (r'COMUTADOR IGN', 'PARTE ELÉTRICA', 'Chaves e Comutadores', 'Comutador Ignição'),
            (r'CIL IGN|CILINDRO IGN', 'PARTE ELÉTRICA', 'Chaves e Comutadores', 'Cilindro Ignição'),
            (r'CHAVE LIMP', 'PARTE ELÉTRICA', 'Chaves e Comutadores', 'Chave Limpador'),
            
            # PARTE ELÉTRICA - Botões
            (r'BOTAO VIDRO|INTERRUPTOR VIDRO', 'PARTE ELÉTRICA', 'Botões', 'Botão Vidro Elétrico'),
            (r'BOTAO PISCA|PISCA ALERTA', 'PARTE ELÉTRICA', 'Botões', 'Botão Pisca Alerta'),
            (r'BOTAO TRAVA', 'PARTE ELÉTRICA', 'Botões', 'Botão Trava Porta'),
            (r'BOTAO PART', 'PARTE ELÉTRICA', 'Botões', 'Botão Partida'),
            
            # CARROCERIA - Retrovisores
            (r'RETROV.*(LD|LE|DIR|ESQ)(?!.*VIDRO)', 'CARROCERIA', 'Retrovisores', 'Retrovisor Externo'),
            (r'RETROV.*INTER', 'CARROCERIA', 'Retrovisores', 'Retrovisor Interno'),
            (r'VIDRO RETROV', 'CARROCERIA', 'Retrovisores', 'Vidro Retrovisor'),
            (r'CAPA RETROV', 'CARROCERIA', 'Retrovisores', 'Capa Retrovisor'),
            (r'APLIQUE.*RETROV', 'CARROCERIA', 'Retrovisores', 'Aplique Retrovisor'),
            
            # CARROCERIA - Maçanetas
            (r'MACANETA.*EXT', 'CARROCERIA', 'Maçanetas', 'Maçaneta Externa'),
            (r'MACANETA.*INT', 'CARROCERIA', 'Maçanetas', 'Maçaneta Interna'),
            (r'GATILHO', 'CARROCERIA', 'Maçanetas', 'Gatilho'),
            (r'CIL.*MACANETA|CILINDRO MACANETA', 'CARROCERIA', 'Maçanetas', 'Cilindro Maçaneta'),
            
            # CARROCERIA - Fechaduras
            (r'FECHADURA.*PORTA', 'CARROCERIA', 'Fechaduras', 'Fechadura Porta'),
            (r'FECHADURA.*IGN', 'CARROCERIA', 'Fechaduras', 'Fechadura Ignição'),
            (r'FECHADURA.*(MALA|TAMPA)', 'CARROCERIA', 'Fechaduras', 'Fechadura Mala'),
            
            # CARROCERIA - Emblemas
            (r'EMBLEMA VW', 'CARROCERIA', 'Emblemas', 'Emblema VW'),
            (r'EMBLEMA GM', 'CARROCERIA', 'Emblemas', 'Emblema GM'),
            (r'EMBLEMA FIAT', 'CARROCERIA', 'Emblemas', 'Emblema Fiat'),
            (r'EMBLEMA FORD', 'CARROCERIA', 'Emblemas', 'Emblema Ford'),
            (r'EMBLEMA TOYOTA', 'CARROCERIA', 'Emblemas', 'Emblema Toyota'),
            (r'EMBLEMA HONDA', 'CARROCERIA', 'Emblemas', 'Emblema Honda'),
            (r'EMBLEMA', 'CARROCERIA', 'Emblemas', 'Emblema VW'),
            
            # CARROCERIA - Apliques
            (r'APLIQUE.*MACANETA', 'CARROCERIA', 'Apliques', 'Aplique Cromado Maçaneta'),
            (r'APLIQUE.*RETROV', 'CARROCERIA', 'Apliques', 'Aplique Cromado Retrovisor'),
            (r'APLIQUE.*TAMPA.*COMB', 'CARROCERIA', 'Apliques', 'Aplique Tampa Combustível'),
            
            # CARROCERIA - Frisos
            (r'FRISO LAT', 'CARROCERIA', 'Frisos', 'Friso Lateral'),
            (r'FRISO.*PARA.*CHOQUE', 'CARROCERIA', 'Frisos', 'Friso Para-choque'),
            
            # CARROCERIA - Grades
            (r'GRADE.*RADIADOR', 'CARROCERIA', 'Grades', 'Grade Radiador'),
            (r'GRADE.*PARA.*CHOQUE', 'CARROCERIA', 'Grades', 'Grade Para-choque'),
            
            # CARROCERIA - Borrachas
            (r'BORRACHA.*PORTA(?!.*MALA)', 'CARROCERIA', 'Borrachas', 'Borracha Porta'),
            (r'BORRACHA.*PORTA.*MALA', 'CARROCERIA', 'Borrachas', 'Borracha Porta-Malas'),
            (r'BORRACHA.*VEDACAO', 'CARROCERIA', 'Borrachas', 'Borracha Vedação'),
            
            # VIDROS E MÁQUINAS
            (r'MAQ.*VIDRO.*MANUAL.*DNT|MAQ.*VIDRO.*DNT.*MANUAL', 'VIDROS E MÁQUINAS', 'Máquina Vidro Manual', 'Máquina Dianteira'),
            (r'MAQ.*VIDRO.*MANUAL.*TRAS', 'VIDROS E MÁQUINAS', 'Máquina Vidro Manual', 'Máquina Traseira'),
            (r'MAQ.*VIDRO.*ELET.*DNT|MAQ.*VIDRO.*DNT.*ELET', 'VIDROS E MÁQUINAS', 'Máquina Vidro Elétrico', 'Máquina Dianteira'),
            (r'MAQ.*VIDRO.*ELET.*TRAS', 'VIDROS E MÁQUINAS', 'Máquina Vidro Elétrico', 'Máquina Traseira'),
            (r'MOTOR.*VIDRO', 'VIDROS E MÁQUINAS', 'Máquina Vidro Elétrico', 'Motor Vidro'),
            (r'KIT.*REPARO.*VIDRO', 'VIDROS E MÁQUINAS', 'Componentes', 'Kit Reparo'),
            (r'ROLDANA.*VIDRO', 'VIDROS E MÁQUINAS', 'Componentes', 'Roldana'),
            (r'ARRASTE.*VIDRO', 'VIDROS E MÁQUINAS', 'Componentes', 'Arraste'),
            (r'SUPORTE.*VIDRO', 'VIDROS E MÁQUINAS', 'Componentes', 'Suporte Vidro'),
            (r'CABO.*MAQ.*VIDRO', 'VIDROS E MÁQUINAS', 'Componentes', 'Cabo Máquina'),
            (r'MANIVELA', 'VIDROS E MÁQUINAS', 'Manivela', 'Manivela Vidro'),
            
            # MOTOR - Arrefecimento
            (r'BOMBA.*AGUA|BOMBA D.*AGUA', 'MOTOR', 'Arrefecimento', "Bomba D'água"),
            (r'VALVULA TERM', 'MOTOR', 'Arrefecimento', 'Válvula Termostática'),
            (r'CEBOLAO', 'MOTOR', 'Arrefecimento', 'Cebolão Radiador'),
            (r'MANGUEIRA.*RADIADOR', 'MOTOR', 'Arrefecimento', 'Mangueira Radiador'),
            (r'RESERVATORIO.*EXPANS', 'MOTOR', 'Arrefecimento', 'Reservatório Expansão'),
            (r'TAMPA RADIADOR', 'MOTOR', 'Arrefecimento', 'Tampa Radiador'),
            (r'TAMPA RESERV', 'MOTOR', 'Arrefecimento', 'Tampa Reservatório'),
            
            # MOTOR - Alimentação
            (r'BOMBA.*COMB', 'MOTOR', 'Alimentação', 'Bomba Combustível'),
            (r'BICO INJ', 'MOTOR', 'Alimentação', 'Bico Injetor'),
            (r'REGULADOR.*PRESSAO', 'MOTOR', 'Alimentação', 'Regulador Pressão'),
            
            # MOTOR - Correias
            (r'CORREIA.*DENTADA', 'MOTOR', 'Correias', 'Correia Dentada'),
            (r'CORREIA.*POLY|CORREIA.*PK', 'MOTOR', 'Correias', 'Correia Poly V'),
            (r'CORREIA.*V(?!.*POLY)', 'MOTOR', 'Correias', 'Correia em V'),
            (r'TENSOR', 'MOTOR', 'Correias', 'Tensor'),
            
            # MOTOR - Filtros
            (r'FILTRO AR(?! COND)', 'MOTOR', 'Filtros', 'Filtro Ar'),
            (r'FILTRO OLEO', 'MOTOR', 'Filtros', 'Filtro Óleo'),
            (r'FILTRO COMB', 'MOTOR', 'Filtros', 'Filtro Combustível'),
            (r'FILTRO CABINE|FILTRO AR COND', 'MOTOR', 'Filtros', 'Filtro Cabine'),
            
            # MOTOR - Tampas e Vedações
            (r'TAMPA OLEO', 'MOTOR', 'Tampas e Vedações', 'Tampa Óleo'),
            (r'VARETA NIVEL', 'MOTOR', 'Tampas e Vedações', 'Vareta Nível'),
            (r'JUNTA CABECOTE', 'MOTOR', 'Tampas e Vedações', 'Junta Cabeçote'),
            (r'JUNTA CARTER', 'MOTOR', 'Tampas e Vedações', 'Junta Carter'),
            
            # INTERIOR - Bancos
            (r'CAPA RECLIN', 'INTERIOR', 'Bancos', 'Capa Reclinável'),
            (r'MANOPLA.*REG', 'INTERIOR', 'Bancos', 'Manopla Regulagem'),
            (r'BOTAO.*TRAVA.*BANCO', 'INTERIOR', 'Bancos', 'Botão Trava Banco'),
            (r'DESLIZE.*BANCO', 'INTERIOR', 'Bancos', 'Deslize Banco'),
            (r'ALCA.*BANCO', 'INTERIOR', 'Bancos', 'Alça Banco'),
            
            # INTERIOR - Câmbio
            (r'BOLA.*CAMBIO', 'INTERIOR', 'Câmbio', 'Bola Câmbio'),
            (r'COIFA.*CAMBIO', 'INTERIOR', 'Câmbio', 'Coifa Câmbio'),
            (r'KIT.*TRAMBULADOR', 'INTERIOR', 'Câmbio', 'Kit Trambulador'),
            
            # INTERIOR - Painel
            (r'DIFUSOR.*AR', 'INTERIOR', 'Painel', 'Difusor Ar'),
            (r'MOLDURA.*PAINEL', 'INTERIOR', 'Painel', 'Moldura Painel'),
            (r'COBERTURA.*PAINEL', 'INTERIOR', 'Painel', 'Cobertura Painel'),
            
            # INTERIOR - Volante
            (r'CUBO.*VOLANTE', 'INTERIOR', 'Volante', 'Cubo Volante'),
            (r'CAME.*VOLANTE', 'INTERIOR', 'Volante', 'Came Volante'),
            (r'CINTA.*AIRBAG', 'INTERIOR', 'Volante', 'Cinta Airbag'),
            
            # INTERIOR - Pedais
            (r'KIT.*BORRACHA.*PEDAL|BORRACHA.*PEDAL', 'INTERIOR', 'Pedais', 'Kit Borracha Pedal'),
            
            # INTERIOR - Portas
            (r'PUXADOR.*PORTA', 'INTERIOR', 'Portas', 'Puxador Porta'),
            (r'PINO.*TRAVA', 'INTERIOR', 'Portas', 'Pino Trava'),
            (r'MOLDURA.*MACANETA', 'INTERIOR', 'Portas', 'Moldura Maçaneta'),
            
            # INTERIOR - Diversos
            (r'QUEBRA.*SOL', 'INTERIOR', 'Diversos', 'Quebra-Sol'),
            (r'TAPETE', 'INTERIOR', 'Diversos', 'Tapete'),
            
            # LIMPADOR PARA-BRISA - Palhetas
            (r'PALHETA.*SILICONE', 'LIMPADOR PARA-BRISA', 'Palhetas', 'Palheta Silicone'),
            (r'PALHETA.*TRAS', 'LIMPADOR PARA-BRISA', 'Palhetas', 'Palheta Traseira'),
            (r'PALHETA.*ESP', 'LIMPADOR PARA-BRISA', 'Palhetas', 'Palheta Dianteira Específica'),
            (r'PALHETA', 'LIMPADOR PARA-BRISA', 'Palhetas', 'Palheta Dianteira Comum'),
            
            # LIMPADOR PARA-BRISA - Componentes
            (r'BOMBA.*LIMP', 'LIMPADOR PARA-BRISA', 'Componentes', 'Bomba Limpador'),
            (r'RESERVATORIO.*AGUA|RESERV.*LIMP', 'LIMPADOR PARA-BRISA', 'Componentes', 'Reservatório Água'),
            (r'MOTOR.*LIMP', 'LIMPADOR PARA-BRISA', 'Componentes', 'Motor Limpador'),
            (r'BICO.*EJET', 'LIMPADOR PARA-BRISA', 'Componentes', 'Bico Ejetor'),
            (r'CONEXAO.*LIMP|MANGUEIRA.*LIMP', 'LIMPADOR PARA-BRISA', 'Componentes', 'Conexão/Mangueira'),
            
            # SOM E ACESSÓRIOS - Alto-Falantes
            (r'REPARO.*DRIVER', 'SOM E ACESSÓRIOS', 'Alto-Falantes', 'Reparo Driver'),
            (r'REPARO.*TWEETER', 'SOM E ACESSÓRIOS', 'Alto-Falantes', 'Reparo Tweeter'),
            (r'CAPACITOR', 'SOM E ACESSÓRIOS', 'Alto-Falantes', 'Capacitor'),
            (r'CORNETA', 'SOM E ACESSÓRIOS', 'Alto-Falantes', 'Corneta'),
            
            # SOM E ACESSÓRIOS - Instalação
            (r'CHICOTE.*RADIO', 'SOM E ACESSÓRIOS', 'Instalação', 'Chicote Rádio'),
            (r'ANTENA', 'SOM E ACESSÓRIOS', 'Instalação', 'Antena'),
            (r'ARO.*ADAPT.*ALTO', 'SOM E ACESSÓRIOS', 'Instalação', 'Aro Adaptador Alto-Falante'),
            
            # SOM E ACESSÓRIOS - Acessórios
            (r'CAMERA.*RE', 'SOM E ACESSÓRIOS', 'Acessórios', 'Câmera Ré'),
            (r'SENSOR.*ESTAC', 'SOM E ACESSÓRIOS', 'Acessórios', 'Sensor Estacionamento'),
            
            # QUÍMICOS E LUBRIFICANTES - Óleos Motor
            (r'OLEO.*MOTOR.*5W30|OLEO.*5W30|5W30', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Motor', '5W30'),
            (r'OLEO.*MOTOR.*10W40|OLEO.*10W40|10W40', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Motor', '10W40'),
            (r'OLEO.*MOTOR.*15W40|OLEO.*15W40|15W40', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Motor', '15W40'),
            (r'OLEO.*MOTOR.*20W50|OLEO.*20W50|20W50', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Motor', '20W50'),
            (r'OLEO.*MOTOR.*25W60|OLEO.*25W60|25W60', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Motor', '25W60'),
            
            # QUÍMICOS E LUBRIFICANTES - Óleos Transmissão
            (r'OLEO.*ATF|ATF.*DEXRON', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Transmissão', 'ATF'),
            (r'OLEO.*HIDR', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Transmissão', 'Hidráulico'),
            (r'OLEO.*CAMBIO', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Transmissão', 'Câmbio'),
            
            # QUÍMICOS E LUBRIFICANTES - Óleos Freio
            (r'OLEO FREIO.*DOT3|OLEO FREIO.*DOT 3', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Freio', 'DOT3'),
            (r'OLEO FREIO.*DOT4|OLEO FREIO.*DOT 4', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Freio', 'DOT4'),
            (r'OLEO FREIO.*DOT5|OLEO FREIO.*DOT 5', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Freio', 'DOT5'),
            (r'OLEO FREIO', 'QUÍMICOS E LUBRIFICANTES', 'Óleos Freio', 'DOT3'),
            
            # QUÍMICOS E LUBRIFICANTES - Aditivos
            (r'ADITIVO.*RADIADOR', 'QUÍMICOS E LUBRIFICANTES', 'Aditivos', 'Aditivo Radiador'),
            (r'ADITIVO.*(DIESEL|COMBUST|TRATAMENTO)', 'QUÍMICOS E LUBRIFICANTES', 'Aditivos', 'Aditivo Combustível'),
            (r'ADITIVO', 'QUÍMICOS E LUBRIFICANTES', 'Aditivos', 'Aditivo Radiador'),
            
            # QUÍMICOS E LUBRIFICANTES - Limpeza
            (r'LIMPA CONTATO', 'QUÍMICOS E LUBRIFICANTES', 'Limpeza', 'Limpa Contato'),
            (r'LIMPA.*AR.*COND|GRANADA.*AR.*COND', 'QUÍMICOS E LUBRIFICANTES', 'Limpeza', 'Limpa Ar Condicionado'),
            (r'SHAMPOO|LAVA AUTO', 'QUÍMICOS E LUBRIFICANTES', 'Limpeza', 'Shampoo'),
            (r'LIMPA PARA.*BRISA|LIMPA PARABRISA', 'QUÍMICOS E LUBRIFICANTES', 'Limpeza', 'Limpa Para-brisa'),
            
            # QUÍMICOS E LUBRIFICANTES - Lubrificantes
            (r'SILICONE(?!.*ALTA.*TEMP)', 'QUÍMICOS E LUBRIFICANTES', 'Lubrificantes', 'Silicone'),
            (r'GRAXA', 'QUÍMICOS E LUBRIFICANTES', 'Lubrificantes', 'Graxa'),
            (r'WD40|WD-40', 'QUÍMICOS E LUBRIFICANTES', 'Lubrificantes', 'WD40'),
            (r'VASELINA', 'QUÍMICOS E LUBRIFICANTES', 'Lubrificantes', 'Vaselina'),
            (r'DESCARBONIZANTE', 'QUÍMICOS E LUBRIFICANTES', 'Lubrificantes', 'Descarbonizante'),
            
            # QUÍMICOS E LUBRIFICANTES - Colas e Vedantes
            (r'SILICONE.*ALTA.*TEMP', 'QUÍMICOS E LUBRIFICANTES', 'Colas e Vedantes', 'Silicone Alta Temp'),
            (r'COLA.*(INSTANT|SUPER)', 'QUÍMICOS E LUBRIFICANTES', 'Colas e Vedantes', 'Cola Instantânea'),
            (r'VEDA JUNTA', 'QUÍMICOS E LUBRIFICANTES', 'Colas e Vedantes', 'Veda Junta'),
            
            # FIXAÇÃO E TERMINAIS
            (r'ABRACADEIRA.*NILON|ABRACADEIRA.*NYLON', 'FIXAÇÃO E TERMINAIS', 'Abraçadeiras', 'Abraçadeira Nylon'),
            (r'ABRACADEIRA.*METAL', 'FIXAÇÃO E TERMINAIS', 'Abraçadeiras', 'Abraçadeira Metal'),
            (r'ABRACADEIRA.*MOLA', 'FIXAÇÃO E TERMINAIS', 'Abraçadeiras', 'Abraçadeira Mola'),
            (r'ABRACADEIRA', 'FIXAÇÃO E TERMINAIS', 'Abraçadeiras', 'Abraçadeira Nylon'),
            (r'TERMINAL BATERIA', 'FIXAÇÃO E TERMINAIS', 'Terminais Bateria', 'Terminal Positivo/Negativo'),
            (r'GARRA BATERIA', 'FIXAÇÃO E TERMINAIS', 'Terminais Bateria', 'Garra Bateria'),
            (r'TERMINAL OLHAL', 'FIXAÇÃO E TERMINAIS', 'Terminais Elétricos', 'Terminal Olhal'),
            (r'TERMINAL.*ENCAIXE', 'FIXAÇÃO E TERMINAIS', 'Terminais Elétricos', 'Terminal Encaixe'),
            (r'TERMINAL.*FORQUILHA', 'FIXAÇÃO E TERMINAIS', 'Terminais Elétricos', 'Terminal Forquilha'),
            (r'TERMINAL', 'FIXAÇÃO E TERMINAIS', 'Terminais Elétricos', 'Terminal Encaixe'),
            
            # TRAVAS E ALARMES
            (r'TRAVA ELET.*PORTA', 'TRAVAS E ALARMES', 'Trava Elétrica', 'Trava Porta'),
            (r'CENTRALINA.*(TRAVA|PORTA)', 'TRAVAS E ALARMES', 'Trava Elétrica', 'Centralina'),
            (r'MOTOR FECHADURA', 'TRAVAS E ALARMES', 'Trava Elétrica', 'Motor Fechadura'),
            (r'CABO ACION.*FECH|CABO.*FECH.*PORTA', 'TRAVAS E ALARMES', 'Trava Elétrica', 'Cabo Acionamento'),
            (r'CENTRALINA.*VIDRO', 'TRAVAS E ALARMES', 'Vidro Elétrico', 'Centralina Vidro'),
            (r'CAPA TELECOM', 'TRAVAS E ALARMES', 'Telecomando', 'Capa Telecomando'),
            (r'BOTAO TELECOM', 'TRAVAS E ALARMES', 'Telecomando', 'Botão Telecomando'),
            
            # PARA-CHOQUE E EXTERNA
            (r'GRADE.*PARA.*CHOQUE', 'PARA-CHOQUE E EXTERNA', 'Para-choque', 'Grade Para-choque'),
            (r'PONTEIRA.*PARA.*CHOQUE', 'PARA-CHOQUE E EXTERNA', 'Para-choque', 'Ponteira'),
            (r'REFLETOR.*PARA.*CHOQUE', 'PARA-CHOQUE E EXTERNA', 'Para-choque', 'Refletor'),
            (r'CALHA.*CHUVA', 'PARA-CHOQUE E EXTERNA', 'Proteção', 'Calha Chuva'),
            (r'PROTETOR.*PORTA', 'PARA-CHOQUE E EXTERNA', 'Proteção', 'Protetor Porta'),
            (r'ENGATE.*REBOQUE', 'PARA-CHOQUE E EXTERNA', 'Engate Reboque', 'Engate'),
            (r'TOMADA.*REBOQUE', 'PARA-CHOQUE E EXTERNA', 'Engate Reboque', 'Tomada Reboque'),
            (r'BOLA.*ENGATE', 'PARA-CHOQUE E EXTERNA', 'Engate Reboque', 'Bola Engate'),
            (r'CAPA.*ENGATE', 'PARA-CHOQUE E EXTERNA', 'Engate Reboque', 'Capa Engate'),
            (r'TAMPA TANQUE', 'PARA-CHOQUE E EXTERNA', 'Tampa Combustível', 'Tampa Tanque'),
            
            # SUSPENSÃO E RODAS
            (r'AMORT.*MALA', 'SUSPENSÃO E RODAS', 'Amortecedores', 'Amortecedor Mala'),
            (r'AMORT.*CAP', 'SUSPENSÃO E RODAS', 'Amortecedores', 'Amortecedor Capô'),
            (r'ROLAMENTO RODA.*DNT|ROLAMENTO RODA.*DIANT', 'SUSPENSÃO E RODAS', 'Rolamentos', 'Rolamento Roda Dianteiro'),
            (r'ROLAMENTO RODA.*TRAS', 'SUSPENSÃO E RODAS', 'Rolamentos', 'Rolamento Roda Traseiro'),
            (r'KIT ROLAMENTO RODA', 'SUSPENSÃO E RODAS', 'Rolamentos', 'Rolamento Roda Dianteiro'),
            (r'BUCHA.*(SUSPENSAO|BRACO)', 'SUSPENSÃO E RODAS', 'Buchas', 'Bucha Suspensão'),
            (r'CALOTA', 'SUSPENSÃO E RODAS', 'Rodas', 'Calota'),
            (r'CAMARA AR', 'SUSPENSÃO E RODAS', 'Rodas', 'Câmara de Ar'),
            (r'PARAFUSO RODA', 'SUSPENSÃO E RODAS', 'Rodas', 'Parafuso Roda'),
            (r'PORCA RODA', 'SUSPENSÃO E RODAS', 'Rodas', 'Porca Roda'),
            (r'PRISIONEIRO RODA', 'SUSPENSÃO E RODAS', 'Rodas', 'Prisioneiro'),
            
            # MOTO
            (r'PNEU MOTO.*DNT|PNEU MOTO.*DIANT', 'MOTO', 'Pneus', 'Pneu Dianteiro'),
            (r'PNEU MOTO.*TRAS', 'MOTO', 'Pneus', 'Pneu Traseiro'),
            (r'PNEU MOTO', 'MOTO', 'Pneus', 'Pneu Dianteiro'),
            (r'CAMARA.*MOTO.*DNT|CAMARA AR DNT', 'MOTO', 'Câmaras', 'Câmara Dianteira'),
            (r'CAMARA.*MOTO.*TRAS|CAMARA AR TRAS', 'MOTO', 'Câmaras', 'Câmara Traseira'),
            (r'LAMPADA.*MOTO', 'MOTO', 'Elétrica', 'Lâmpada Moto'),
            (r'VELA.*MOTO', 'MOTO', 'Elétrica', 'Vela Moto'),
            
            # FERRAMENTAS
            (r'CHAVE COMBINADA', 'FERRAMENTAS', 'Chaves', 'Chave Combinada'),
            (r'CHAVE CANHAO', 'FERRAMENTAS', 'Chaves', 'Chave Canhão'),
            (r'CHAVE RODA', 'FERRAMENTAS', 'Chaves', 'Chave Roda'),
            (r'SOLDA.*TUBO', 'FERRAMENTAS', 'Solda', 'Solda Tubo'),
            (r'EXTINTOR', 'FERRAMENTAS', 'Extintor', 'Extintor Incêndio'),
        ]
        
        # Processar produtos
        produtos = Produto.objects.filter(ativo=True)
        total_produtos = produtos.count()
        classificados = 0
        nao_classificados = []
        
        for produto in produtos:
            descricao = produto.descricao.upper()
            encontrou = False
            
            for pattern, cat_nome, subcat_nome, grupo_nome in regras:
                if re.search(pattern, descricao, re.IGNORECASE):
                    try:
                        categoria = Categoria.objects.get(nome=cat_nome)
                        subcategoria = Subcategoria.objects.get(nome=subcat_nome, categoria=categoria)
                        grupo = Grupo.objects.get(nome=grupo_nome, subcategoria=subcategoria)
                        
                        produto.categoria = categoria
                        produto.subcategoria = subcategoria
                        produto.grupo = grupo
                        produto.save()
                        
                        classificados += 1
                        encontrou = True
                        break
                    except (Categoria.DoesNotExist, Subcategoria.DoesNotExist, Grupo.DoesNotExist):
                        pass
            
            if not encontrou:
                nao_classificados.append(produto.descricao)
        
        self.stdout.write('')
        self.stdout.write(f'✅ Produtos classificados: {classificados}/{total_produtos}')
        self.stdout.write(f'❌ Produtos não classificados: {len(nao_classificados)}')
        
        if nao_classificados and len(nao_classificados) <= 50:
            self.stdout.write('')
            self.stdout.write('Produtos não classificados:')
            for desc in nao_classificados[:50]:
                self.stdout.write(f'  - {desc}')
        
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write('✅ PROCESSO CONCLUÍDO!')
        self.stdout.write('=' * 60)