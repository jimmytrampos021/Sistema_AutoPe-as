"""
Comando Django para importar cotações da Conexão Distribuidora de Auto Peças

USO:
1. Copie este arquivo para: estoque/management/commands/importar_cotacao_conexao.py
2. Crie os arquivos __init__.py necessários se não existirem
3. Execute: python manage.py importar_cotacao_conexao

O comando irá:
- Cadastrar o fornecedor "Conexão Distribuidora de Auto Peças Ltda"
- Buscar produtos existentes no estoque por palavras-chave
- Criar cotações com os preços dos PDFs
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
from estoque.models import Fornecedor, Produto, CotacaoFornecedor


class Command(BaseCommand):
    help = 'Importa cotações da Conexão Distribuidora de Auto Peças'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('IMPORTAÇÃO DE COTAÇÕES - CONEXÃO DISTRIBUIDORA'))
        self.stdout.write(self.style.WARNING('=' * 70))
        
        # 1. Criar ou buscar o fornecedor
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj='00000000000000',  # Atualizar com CNPJ real
            defaults={
                'razao_social': 'CONEXAO DISTRIBUIDORA DE AUTO PECAS LTDA',
                'nome_fantasia': 'Conexão Distribuidora',
                'telefone': '',
                'celular': '',
                'email': '',
                'site': '',
                'contato_principal': 'ALEXANDRE',
                'cep': '',
                'logradouro': '',
                'numero': '',
                'complemento': '',
                'bairro': '',
                'cidade': '',
                'estado': 'RJ',
                'forma_pagamento_padrao': 'B',  # Boleto
                'prazo_entrega_dias': 3,
                'pedido_minimo': Decimal('0.00'),
                'frete_gratis_acima': Decimal('0.00'),
                'classificacao': 4,
                'observacoes': 'Fornecedor importado dos pedidos - Período Mai/2025 a Nov/2025',
                'ativo': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Fornecedor criado: {fornecedor.nome_fantasia}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Fornecedor encontrado: {fornecedor.nome_fantasia}'))
        
        # 2. Dados dos produtos extraídos dos PDFs
        # Formato: (palavras_busca, descricao_fornecedor, preco_min, preco_max, codigo_fornecedor)
        produtos_cotacao = [
            # === LÂMPADAS FAROL ===
            (['H1', '12V', '55W', 'TIGER'], 'LAMPADA H1 3200K 12V/55W HALOGENA TIGER', 4.09, 4.09, 'TG1015H1'),
            (['H1', '12V', '55W', 'KX3'], 'LAMPADA H1 3200K 12V/55W HALOGENA KX3', 4.99, 4.99, 'KX3H1'),
            (['H4', '12V', '60', '55', 'TIGER'], 'LAMPADA H4 3200K 12V 60/55W HALOGENA TIGER', 8.99, 8.99, 'TG1015H4'),
            (['H4', '12V', '60', '55', 'PHILIPS', '12342'], 'LAMPADA H4 3200K 12V 60/55W HALOGENA PHILIPS', 16.18, 16.42, '12342C1'),
            (['H7', '12V', '55W', 'TIGER'], 'LAMPADA H7 3200K 12V/55W HALOGENA TIGER', 5.65, 7.99, 'TG1015H7'),
            (['H7', '12V', '55W', 'PHILIPS', '12972'], 'LAMPADA H7 3200K 12V/55W HALOGENA PHILIPS', 19.91, 19.91, '12972C1'),
            (['H11', '12V', '55W', 'KX3'], 'LAMPADA H11 3200K 12V/55W HALOGENA KX3', 11.70, 11.70, 'KX3H11'),
            (['HB3', '12V', 'TIGER'], 'LAMPADA HB3 3200K 12V/61W HALOGENA TIGER', 10.79, 10.79, 'TG1015HB3'),
            (['HB4', '12V', 'TIGER'], 'LAMPADA HB4 3200K 12V/61W HALOGENA TIGER', 8.99, 8.99, '789988680597'),
            
            # === LÂMPADAS SINALIZAÇÃO ===
            (['1141', '12V', '21W', 'CINOY'], 'LAMPADA 1 POLO 12V/21W HALOGENA 1141 CINOY', 1.62, 1.62, 'YN121141'),
            (['1141', 'AMARELA', 'CINOY'], 'LAMPADA 1 POLO 12V/21W AMARELA CINOY', 2.02, 2.02, 'YN121141AM'),
            (['1034', '12V', '21', '5W', 'CINOY'], 'LAMPADA 2 POLOS 12V 21/5W HALOGENA 1034 CINOY', 1.62, 1.62, 'YN121034'),
            (['T20', 'CINOY', '2 POLO'], 'LAMPADA 2 POLOS 12V 21/5W T20 HALOGENA CINOY', 3.60, 3.60, 'YN126942'),
            (['PINGO', 'T10', '5W', 'CINOY'], 'LAMPADA PINGO T10 12V/5W CINOY', 0.65, 0.65, 'YN122825'),
            (['PINGO', 'T10', '5W', 'KX3'], 'LAMPADA PINGO T10 12V/5W KX3', 0.65, 0.65, 'KXW5W'),
            (['PINGO', 'T15', '16W', 'KX3'], 'LAMPADA PINGO T15 12V/16W KX3', 0.65, 0.65, 'KXW16W'),
            (['PINGO', 'LED', 'CINOY'], 'LAMPADA PINGO 4 LED (PAR) CINOY', 4.99, 4.99, 'YNLH025'),
            (['67', '12V', '5W', 'KX3'], 'LAMPADA 067 12V/5W HALOGENA KX3', 1.25, 1.25, 'KXR5W'),
            
            # === ÓLEOS MOTOR ===
            (['10W30', 'MOTO', 'PANTHER'], 'OLEO 10W30 4T MOTO SL PANTHER', 19.35, 19.35, 'PAN 10W30 M'),
            (['10W30', 'SEMI', 'PANTHER'], 'OLEO 10W30 SEMI SINTETICO SL PANTHER', 18.48, 18.48, 'PAN 10W30 S'),
            (['10W40', 'SEMI', 'PANTHER'], 'OLEO 10W40 SEMI SINTETICO PANTHER', 18.65, 18.65, 'PAN 10W40 S'),
            (['15W40', 'SEMI', 'MAXITEC'], 'OLEO 15W40 SEMI SINTETICO SL MAXITEC', 16.42, 16.42, 'MAXITEC 15'),
            (['15W40', 'SEMI', 'TEXAS'], 'OLEO 15W40 SEMI SINTETICO TEXAS', 12.59, 12.59, 'TEX 15W40 S'),
            (['20W50', 'MOTO', 'LUBRIX'], 'OLEO 20W50 4T MOTO LUBRIX', 13.05, 13.05, 'LUB 20W50 M'),
            (['20W50', 'MINERAL', 'BRADOCK'], 'OLEO 20W50 MINERAL SL BRADOCK', 11.90, 13.85, 'BRA 20W50 P'),
            (['20W50', 'MINERAL', 'TEXAS'], 'OLEO 20W50 MINERAL TEXAS', 10.90, 10.90, 'TEX 20W50 P'),
            (['2T', '200ML', 'RADNAQ'], 'OLEO 2T 200ML RADNAQ', 6.16, 6.16, 'RAD 2T 200'),
            (['2T', '500ML', 'PANTHER'], 'OLEO 2T API-TC 500ML PANTHER', 12.30, 12.30, 'PAN 2T 500'),
            (['5W30', 'SINTETICO', 'BRADOCK'], 'OLEO 5W30 SINTETICO BRADOCK', 15.86, 15.86, 'BRA 5W30 S'),
            (['5W30', 'SINTETICO', 'RADNAQ'], 'OLEO 5W30 SINTETICO RADNAQ', 16.80, 16.80, 'RAD 5W30'),
            (['5W30', 'SINTETICO', 'TEXAS'], 'OLEO 5W30 SINTETICO TEXAS', 15.45, 15.45, 'TEX 5W30 S'),
            (['5W40', 'SINTETICO', 'MEGA'], 'OLEO 5W40 SINTETICO MEGA', 15.45, 15.45, 'MEGA 5W40 S'),
            
            # === ÓLEOS TRANSMISSÃO ===
            (['ATF', '500ML', 'PANTHER'], 'OLEO ATF 20W 500ML PANTHER', 10.40, 10.40, 'PAN ATF 500'),
            (['ATF', 'LITRO', 'BRADOCK'], 'OLEO ATF 20W LITRO BRADOCK', 14.00, 14.00, 'BRA ATF L'),
            (['ATF', 'LITRO', 'MEGA'], 'OLEO ATF 20W LITRO MEGA', 11.99, 11.99, 'MEGA ATF L'),
            (['ATF', 'LITRO', 'PANTHER'], 'OLEO ATF 20W LITRO PANTHER', 16.76, 16.76, 'PAN ATF L'),
            
            # === ÓLEOS FREIO ===
            (['DOT3', '500ML', 'RADNAQ'], 'OLEO FREIO DOT3 500ML RADNAQ', 11.75, 11.93, 'RAD7030'),
            (['DOT3', '500ML', 'VARGA', 'TRW'], 'OLEO FREIO DOT3 500ML VARGA TRW', 20.56, 20.56, 'RCLF00021'),
            (['DOT4', '500ML', 'RADNAQ'], 'OLEO FREIO DOT4 500ML RADNAQ', 14.04, 14.18, 'RAD7040'),
            
            # === FUSÍVEIS ===
            (['FUSIVEL', 'LAMINA', '10'], 'FUSIVEL LAMINA 10 AMP DNI', 0.60, 0.60, 'DNI316010'),
            (['FUSIVEL', 'LAMINA', '15'], 'FUSIVEL LAMINA 15 AMP DNI', 0.60, 0.60, 'DNI316015'),
            (['FUSIVEL', 'LAMINA', '20'], 'FUSIVEL LAMINA 20 AMP DNI', 0.60, 0.60, 'DNI316020'),
            (['FUSIVEL', 'MINI', '10'], 'FUSIVEL MINI 10 AMP DNI', 0.60, 0.60, 'DNI317010'),
            (['FUSIVEL', 'MINI', '15'], 'FUSIVEL MINI 15 AMP DNI', 0.60, 0.60, 'DNI317015'),
            (['FUSIVEL', 'MINI', '20'], 'FUSIVEL MINI 20 AMP DNI', 0.60, 0.60, 'DNI317020'),
            (['FUSIVEL', 'MINI', '25'], 'FUSIVEL MINI 25 AMP TECH ONE', 0.60, 0.60, 'PWE2649'),
            (['FUSIVEL', 'MAXI', '30'], 'FUSIVEL MAXI LAMINA 30 AMP TECH ONE', 1.81, 1.81, '489522821968'),
            (['FUSIVEL', 'MAXI', '40'], 'FUSIVEL MAXI LAMINA 40 AMP TECH ONE', 1.81, 1.81, '489522821969'),
            
            # === ADITIVOS E ÁGUA ===
            (['ADITIVO', 'RADIADOR', '1L', 'PANTHER'], 'ADITIVO RADIADOR PRONTO USO ROSA 1L PANTHER', 3.79, 4.05, 'PAN AD PU R'),
            (['ADITIVO', 'RADIADOR', '1L', 'PARAFLU'], 'ADITIVO RADIADOR PRONTO USO ROSA 1L PARAFLU', 15.61, 15.61, '3004'),
            (['ADITIVO', 'RADIADOR', '1L', 'WATER', 'COOLANT'], 'ADITIVO RADIADOR PRONTO USO ROSA 1L WATER COOLANT', 3.68, 3.84, 'MSZ333 1L'),
            (['ADITIVO', 'RADIADOR', '5L', 'WATER', 'COOLANT'], 'ADITIVO RADIADOR PRONTO USO ROSA 5L WATER COOLANT', 12.99, 12.99, 'MSZ509 5L'),
            (['AGUA', 'DESMINERALIZADA', '1L'], 'AGUA DESMINERALIZADA 1L WATER COOLANT', 3.26, 3.26, 'MSZ323 1L'),
            (['AGUA', 'DESMINERALIZADA', '5L'], 'AGUA DESMINERALIZADA 5L WATER COOLANT', 10.99, 10.99, 'MSZ503 5L'),
            (['SOLUCAO', 'BATERIA'], 'SOLUCAO BATERIA 1LT WATER', 11.99, 11.99, 'MSZ345'),
            
            # === QUÍMICOS - LIMPEZA ===
            (['DESCARBONIZANTE', '300ML', 'TECBRIL'], 'DESCARBONIZANTE 300ML TECBRIL', 14.03, 14.03, '5920272'),
            (['DESCARBONIZANTE', '300ML', 'CAR', '80'], 'DESCARBONIZANTE 300ML CAR 80', 24.54, 24.54, 'CAR80'),
            (['DESENGRIPANTE', '300ML', 'TECBRIL'], 'DESENGRIPANTE BRIL LUB 300ML TECBRIL', 6.99, 6.99, '5920275'),
            (['DESENGRIPANTE', 'WHITE', 'LUB', 'ORBI'], 'DESENGRIPANTE WHITE LUB 300ML ORBI', 11.25, 11.25, '146'),
            (['LIMPA', 'CONTATO', '300ML', 'TECBRIL'], 'LIMPA CONTATO 300ML/200G TECBRIL', 11.50, 11.50, '5920152'),
            (['LIMPA', 'AR', 'CARRO', 'NOVO', 'ORBI'], 'LIMPA AR CARRO NOVO 200ML ORBI', 12.54, 12.54, '5977'),
            (['LIMPA', 'PARABRISA', 'RADNAQ'], 'LIMPA PARABRISA 100ML RADNAQ', 3.08, 3.73, 'RAD5041'),
            (['LIMPA', 'PNEUS', 'RADNAQ'], 'LIMPA PNEUS 500ML RADNAQ', 6.08, 6.44, 'RAD8090'),
            (['LIMPA', 'PNEUS', 'PROAUTO'], 'LIMPA PNEUS AUTOCRAFT 500ML PROAUTO', 7.13, 7.13, 'PR280'),
            (['LAVA', 'AUTOS', 'CERA', 'RADNAQ'], 'LAVA AUTOS C/CERA 500ML RADNAQ', 7.27, 7.27, 'RAD8081'),
            (['LAVA', 'AUTOS', 'PROAUTO'], 'LAVA AUTOS AUTOCRAFT 500ML PROAUTO', 6.68, 6.68, 'PR260'),
            
            # === QUÍMICOS - LUBRIFICANTES ===
            (['SILICONE', 'AEROSOL', 'LAVANDA', 'RADNAQ'], 'SILICONE AEROSOL LAVANDA 300ML RADNAQ', 12.72, 12.72, 'RAD6030'),
            (['SILICONE', 'AEROSOL', 'LAVANDA', 'TECBRIL'], 'SILICONE AEROSOL LAVANDA 300ML TECBRIL', 13.46, 13.46, '5920151'),
            (['SILICONE', 'LIQUIDO', '100ML', 'RADNAQ'], 'SILICONE LIQUIDO 100ML RADNAQ', 6.16, 6.16, 'RAD7010'),
            (['SILICONE', 'ALTA', 'TEMPERATURA', 'PRETO', 'ABRO'], 'SILICONE ALTA TEMPERATURA PRETO 998 ABRO', 29.56, 29.56, '998'),
            (['SILICONE', 'ALTA', 'TEMPERATURA', 'CINZA', 'ABRO'], 'SILICONE ALTA TEMPERATURA CINZA 999 ABRO', 29.56, 29.56, '999'),
            (['VASELINA', 'LIQUIDA', '1LT', 'NAFTA'], 'VASELINA LIQUIDA 1LT NAFTA', 17.96, 19.01, '27'),
            (['VASELINA', 'AEROSOL', 'RADNAQ'], 'VASELINA AEROSOL 300ML RADNAQ', 14.00, 14.00, 'RAD6090'),
            (['GRAXA', 'BRANCA', '80G', 'RADNAQ'], 'GRAXA BRANCA BISNAGA 80G RADNAQ', 4.31, 4.31, 'RAD3020'),
            (['GRAXA', 'GRAFITADA', '80G', 'RADNAQ'], 'GRAXA GRAFITADA BISNAGA 80G RADNAQ', 3.78, 3.78, 'RAD3022'),
            (['GRAXA', 'AZUL', '500G', 'INCOLLUB'], 'GRAXA AZUL MP2 NLGI-2 500G INCOLLUB', 17.90, 17.90, 'GRAXA AZ 500'),
            (['CERA', 'PASTA', 'PROAUTO'], 'CERA PASTA TRADICIONAL 200G PROAUTO', 11.13, 11.13, 'PR204'),
            
            # === PALHETAS ===
            (['PALHETA', 'SILICONE', '15', 'TIGER'], 'PALHETA SILICONE 15" TIGER', 6.29, 6.29, 'TG0501015'),
            (['PALHETA', 'SILICONE', '24', 'TIGER'], 'PALHETA SILICONE 24" TIGER', 6.29, 6.29, 'TG0501024'),
            
            # === BATERIAS / PILHAS ===
            (['CR2016', 'KX3'], 'BATERIA ALARME 3V (05 UNIDADES) CR2016 KX3', 7.45, 7.45, 'KB2016'),
            (['CR2032', 'KX3'], 'BATERIA ALARME 3V (05 UNIDADES) CR2032 KX3', 7.45, 8.21, 'KB2032'),
            
            # === FILTROS ===
            (['FILTRO', 'OLEO', 'UNIVERSAL', 'SEINECA'], 'FILTRO OLEO UNIVERSAL TM3 SEINECA', 10.71, 10.71, 'SMF7002'),
            (['FILTRO', 'AR', 'FIESTA', 'ECOSPORT', 'SEINECA'], 'FILTRO AR FIESTA/ECOSPORT 1.6 SEINECA', 16.19, 16.19, 'SAF8098'),
            
            # === PEÇAS DIVERSAS ===
            (['BOMBA', 'COMBUSTIVEL', 'FLEX', 'SEINECA'], 'BOMBA COMB FLEX UNIVERSAL SEINECA', 74.44, 74.44, 'SEI0002'),
            (['CABO', 'VELA', 'GOL', 'SANTANA', 'NGK'], 'CABO VELA GOL, SANTANA AP 1.8/2.0 NGK', 114.34, 114.34, 'STV18'),
            (['RESERVATORIO', 'GOL', 'FOX', 'MARVINI'], 'RESERVATORIO GOL GV/GVI FOX MARVINI', 60.72, 60.72, 'M046'),
            (['RADIO', 'USB', 'FIRSTOPTION'], 'RADIO USB/SD/BT/FM/MP3 FIRSTOPTION', 70.99, 70.99, 'M8850B'),
            
            # === ACESSÓRIOS ===
            (['FITA', 'ISOLANTE', '10M', 'KX3'], 'FITA ISOLANTE 10M KX3', 2.59, 2.59, 'KX1075'),
            (['FITA', 'DUPLA', 'FACE', 'MARCON'], 'FITA DUPLA FACE 3M/9,5MM MARCON', 7.60, 7.60, '18000'),
            (['KIT', 'LIMPEZA', 'AUTO', 'RADNAQ'], 'KIT LIMPEZA AUTO HYPER RADNAQ', 33.49, 33.49, 'RAD8200'),
            (['ODORIZANTE', 'FOLHINHA', 'RADNAQ'], 'ODORIZANTE FOLHINHA RADNAQ', 5.76, 5.76, 'RAD4020'),
            (['ODORIZANTE', 'GEL', 'RADNAQ'], 'ODORIZANTE GEL OCEAN 60G RADNAQ', 5.40, 5.40, 'RAD4034'),
        ]
        
        # 3. Processar cada produto
        cotacoes_criadas = 0
        produtos_encontrados = 0
        produtos_nao_encontrados = []
        
        for palavras_busca, descricao_forn, preco_min, preco_max, codigo_forn in produtos_cotacao:
            # Construir query de busca
            query = Q()
            for palavra in palavras_busca:
                query &= Q(descricao__icontains=palavra)
            
            # Buscar produtos
            produtos = Produto.objects.filter(query, ativo=True)
            
            if produtos.exists():
                produtos_encontrados += 1
                produto = produtos.first()  # Pega o primeiro encontrado
                
                # Usar preço médio se houver variação
                preco_medio = Decimal(str((preco_min + preco_max) / 2)).quantize(Decimal('0.01'))
                
                # Criar ou atualizar cotação
                cotacao, created = CotacaoFornecedor.objects.update_or_create(
                    produto=produto,
                    fornecedor=fornecedor,
                    defaults={
                        'preco_unitario': preco_medio,
                        'quantidade_minima': 1,
                        'prazo_entrega_dias': 3,
                        'forma_pagamento': 'B',  # Boleto
                        'valor_frete': Decimal('0.00'),
                        'observacoes': f'Código fornecedor: {codigo_forn}',
                        'data_cotacao': timezone.now().date(),
                        'validade_dias': 30,
                        'ativo': True,
                    }
                )
                
                if created:
                    cotacoes_criadas += 1
                    self.stdout.write(f'  ✅ {produto.codigo} | {produto.descricao[:40]} → R$ {preco_medio}')
                else:
                    self.stdout.write(f'  🔄 {produto.codigo} | {produto.descricao[:40]} → R$ {preco_medio} (atualizado)')
            else:
                produtos_nao_encontrados.append((descricao_forn, codigo_forn))
        
        # 4. Resumo final
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.SUCCESS(f'✅ Cotações criadas: {cotacoes_criadas}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Produtos encontrados: {produtos_encontrados}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Produtos não encontrados: {len(produtos_nao_encontrados)}'))
        self.stdout.write(self.style.WARNING('=' * 70))
        
        if produtos_nao_encontrados:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Produtos do fornecedor não encontrados no estoque:'))
            for desc, cod in produtos_nao_encontrados[:20]:
                self.stdout.write(f'  ❌ [{cod}] {desc}')
            if len(produtos_nao_encontrados) > 20:
                self.stdout.write(f'  ... e mais {len(produtos_nao_encontrados) - 20} produtos')
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Importação concluída!'))
        self.stdout.write(self.style.SUCCESS('Acesse o Comparador de Preços para ver as cotações.'))