"""
Parser de PDF para Pedidos de Fornecedores

Suporta múltiplos formatos de PDF de pedido:
- Conexão Distribuidora (CM Sistemas)
- AC Araujo Distribuidora
- Formato genérico (tentativa de extração automática)
"""

import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import io


class PDFPedidoParser:
    """
    Parser para extrair dados de PDFs de pedidos de fornecedores
    """
    
    def __init__(self):
        self.texto = ""
        self.linhas = []
        self.formato_detectado = None
        self.errors = []
        self.warnings = []
    
    def parse(self, pdf_file) -> Tuple[bool, Dict, List[str]]:
        """
        Faz o parse do PDF
        
        Args:
            pdf_file: Arquivo PDF (file-like object)
            
        Returns:
            Tuple (success, dados, errors)
        """
        self.errors = []
        self.warnings = []
        
        # Extrai texto do PDF
        try:
            self.texto = self._extrair_texto_pdf(pdf_file)
            if not self.texto:
                self.errors.append("Não foi possível extrair texto do PDF")
                return False, {}, self.errors
            
            self.linhas = self.texto.split('\n')
            
        except Exception as e:
            self.errors.append(f"Erro ao ler PDF: {str(e)}")
            return False, {}, self.errors
        
        # Detecta o formato do PDF
        self.formato_detectado = self._detectar_formato()
        
        # Extrai dados baseado no formato
        if self.formato_detectado == 'conexao':
            dados = self._parse_conexao()
        elif self.formato_detectado == 'araujo':
            dados = self._parse_araujo()
        else:
            dados = self._parse_generico()
        
        if not dados.get('itens'):
            self.errors.append("Nenhum item encontrado no PDF")
            return False, {}, self.errors
        
        dados['formato_detectado'] = self.formato_detectado
        dados['success'] = True
        
        return True, dados, self.warnings
    
    def _extrair_texto_pdf(self, pdf_file) -> str:
        """Extrai texto do PDF usando pdfplumber"""
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("Biblioteca pdfplumber não instalada. Execute: pip install pdfplumber")
        
        texto_completo = ""
        
        # Se for bytes, converte para file-like object
        if hasattr(pdf_file, 'read'):
            content = pdf_file.read()
            if hasattr(pdf_file, 'seek'):
                pdf_file.seek(0)
            pdf_file = io.BytesIO(content)
        
        with pdfplumber.open(pdf_file) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo += texto + "\n"
        
        return texto_completo
    
    def _detectar_formato(self) -> str:
        """Detecta o formato do PDF baseado no conteúdo"""
        texto_lower = self.texto.lower()
        
        # Conexão Distribuidora (CM Sistemas)
        if 'cm sistemas' in texto_lower or 'conexao distribuidora' in texto_lower:
            return 'conexao'
        
        # AC Araujo
        if 'araujo' in texto_lower and 'distribuidora' in texto_lower:
            return 'araujo'
        
        # Tenta detectar por estrutura
        if 'listagem de pedidos' in texto_lower:
            return 'conexao'
        
        if 'pedido de venda' in texto_lower and 'cod. barras' in texto_lower:
            return 'araujo'
        
        return 'generico'
    
    def _limpar_valor(self, valor_str: str) -> Decimal:
        """Converte string de valor para Decimal"""
        if not valor_str:
            return Decimal('0.00')
        
        # Remove símbolos de moeda e espaços
        valor_str = valor_str.replace('$', '').replace('R$', '').strip()
        
        # Trata formato brasileiro (1.234,56) e americano (1,234.56)
        if ',' in valor_str and '.' in valor_str:
            # Verifica qual é o separador decimal
            if valor_str.rfind(',') > valor_str.rfind('.'):
                # Formato brasileiro: 1.234,56
                valor_str = valor_str.replace('.', '').replace(',', '.')
            else:
                # Formato americano: 1,234.56
                valor_str = valor_str.replace(',', '')
        elif ',' in valor_str:
            # Só vírgula: assume decimal brasileiro
            valor_str = valor_str.replace(',', '.')
        
        try:
            return Decimal(valor_str)
        except (InvalidOperation, ValueError):
            return Decimal('0.00')
    
    def _limpar_quantidade(self, qtd_str: str) -> Decimal:
        """Converte string de quantidade para Decimal"""
        if not qtd_str:
            return Decimal('0')
        
        # Remove espaços e converte vírgula para ponto
        qtd_str = qtd_str.strip().replace(',', '.')
        
        # Remove zeros à direita desnecessários (ex: 2,000 -> 2)
        try:
            valor = Decimal(qtd_str)
            return valor
        except (InvalidOperation, ValueError):
            return Decimal('0')
    
    def _parse_conexao(self) -> Dict:
        """Parse para formato Conexão Distribuidora (CM Sistemas)"""
        dados = {
            'fornecedor': 'CONEXAO DISTRIBUIDORA DE AUTO PECAS LTDA',
            'numero_pedido': '',
            'data_emissao': None,
            'itens': [],
            'subtotal': Decimal('0.00'),
            'icms_st': Decimal('0.00'),
            'ipi': Decimal('0.00'),
            'total': Decimal('0.00'),
        }
        
        # Extrai número do pedido
        match = re.search(r'Pedido:\s*(\d+)', self.texto)
        if match:
            dados['numero_pedido'] = match.group(1)
        
        # Extrai data de emissão
        match = re.search(r'Dt\.\s*Emiss[ãa]o:\s*(\d{2}/\d{2}/\d{4})', self.texto)
        if match:
            try:
                dados['data_emissao'] = datetime.strptime(match.group(1), '%d/%m/%Y').date()
            except ValueError:
                pass
        
        # Extrai totais
        match = re.search(r'Subtotal:\s*([\d.,]+)', self.texto)
        if match:
            dados['subtotal'] = self._limpar_valor(match.group(1))
        
        match = re.search(r'ICMS-ST:\s*([\d.,]+)', self.texto)
        if match:
            dados['icms_st'] = self._limpar_valor(match.group(1))
        
        match = re.search(r'IPI:\s*([\d.,]+)', self.texto)
        if match:
            dados['ipi'] = self._limpar_valor(match.group(1))
        
        match = re.search(r'T\s*O\s*T\s*A\s*L\s*:\s*([\d.,]+)', self.texto)
        if match:
            dados['total'] = self._limpar_valor(match.group(1))
        
        # Extrai itens
        # Padrão: 001 TG1014002 LAMPADA TORPEDO 36MM 16 LED (PAR) TIGER UN 2,000 60,000 8,5700 17,14
        # Formato: Item Código Descrição Un Quant Saldo Unit Total
        
        # Regex para capturar linha de item
        # O formato pode ter a descrição em múltiplas linhas
        padrao_item = re.compile(
            r'(\d{3})\s+'  # Item (001, 002, etc)
            r'([A-Z0-9]+)\s+'  # Código
            r'(.+?)\s+'  # Descrição (não-greedy)
            r'(UN|CX|PC|KG|LT|MT|PR)\s+'  # Unidade
            r'([\d.,]+)\s+'  # Quantidade
            r'([\d.,]+)\s+'  # Saldo (ignoramos)
            r'([\d.,]+)\s+'  # Valor unitário
            r'([\d.,]+)'  # Valor total
        )
        
        for match in padrao_item.finditer(self.texto):
            item = {
                'numero_item': int(match.group(1)),
                'codigo': match.group(2).strip(),
                'descricao': match.group(3).strip(),
                'unidade': match.group(4).strip(),
                'quantidade': self._limpar_quantidade(match.group(5)),
                'valor_unitario': self._limpar_valor(match.group(7)),
                'valor_total': self._limpar_valor(match.group(8)),
                'codigo_barras': '',
            }
            dados['itens'].append(item)
        
        # Se não encontrou com o padrão acima, tenta outro método
        if not dados['itens']:
            dados['itens'] = self._extrair_itens_conexao_alternativo()
        
        return dados
    
    def _extrair_itens_conexao_alternativo(self) -> List[Dict]:
        """Método alternativo para extrair itens do formato Conexão"""
        itens = []
        
        # Procura por linhas que começam com número de 3 dígitos
        em_itens = False
        item_atual = None
        
        for linha in self.linhas:
            linha = linha.strip()
            
            # Detecta início da seção de itens
            if 'Item' in linha and 'Código' in linha and 'Descrição' in linha:
                em_itens = True
                continue
            
            # Detecta fim da seção de itens
            if 'T O T A L' in linha or 'Subtotal:' in linha:
                em_itens = False
                continue
            
            if not em_itens:
                continue
            
            # Tenta extrair item
            match = re.match(r'^(\d{3})\s+(\S+)\s+(.+)', linha)
            if match:
                # Salva item anterior se existir
                if item_atual:
                    itens.append(item_atual)
                
                # Inicia novo item
                item_atual = {
                    'numero_item': int(match.group(1)),
                    'codigo': match.group(2),
                    'descricao': match.group(3),
                    'unidade': 'UN',
                    'quantidade': Decimal('0'),
                    'valor_unitario': Decimal('0'),
                    'valor_total': Decimal('0'),
                    'codigo_barras': '',
                }
                
                # Tenta extrair valores do restante da linha
                resto = match.group(3)
                valores = re.findall(r'([\d.,]+)', resto)
                if len(valores) >= 3:
                    item_atual['quantidade'] = self._limpar_quantidade(valores[-4]) if len(valores) >= 4 else Decimal('1')
                    item_atual['valor_unitario'] = self._limpar_valor(valores[-2])
                    item_atual['valor_total'] = self._limpar_valor(valores[-1])
                
                # Extrai unidade
                unidade_match = re.search(r'\b(UN|CX|PC|KG|LT|MT|PR)\b', resto)
                if unidade_match:
                    item_atual['unidade'] = unidade_match.group(1)
        
        # Adiciona último item
        if item_atual:
            itens.append(item_atual)
        
        return itens
    
    def _parse_araujo(self) -> Dict:
        """Parse para formato AC Araujo Distribuidora"""
        dados = {
            'fornecedor': 'AC ARAUJO DISTRIBUIDORA DE AUTO PECAS',
            'numero_pedido': '',
            'data_emissao': None,
            'itens': [],
            'subtotal': Decimal('0.00'),
            'icms_st': Decimal('0.00'),
            'ipi': Decimal('0.00'),
            'total': Decimal('0.00'),
        }
        
        # Extrai número do pedido
        match = re.search(r'N[úu]mero do Pedido:\s*(\d+)', self.texto)
        if match:
            dados['numero_pedido'] = match.group(1)
        
        # Extrai data de emissão
        match = re.search(r'Pedido feito em:\s*(\d{2}/\d{2}/\d{4})', self.texto)
        if match:
            try:
                dados['data_emissao'] = datetime.strptime(match.group(1), '%d/%m/%Y').date()
            except ValueError:
                pass
        
        # Extrai total
        match = re.search(r'Total\s+\d+\s+\$?([\d.,]+)', self.texto)
        if match:
            dados['total'] = self._limpar_valor(match.group(1))
        
        # Extrai itens
        # Formato: # PROD. DESCRIÇÃO UNID. COD. BARRAS QTDE. PREÇO UN. PREÇO
        # Exemplo: 6 4T20W50 COD.1024151 LUBRAX SL 4T 20W50 CXC24 1L PC 7891344015750 24 $16.99 $407.76
        
        padrao_item = re.compile(
            r'(\d+)\s+'  # Número do item
            r'([A-Z0-9]+)\s+'  # Código do produto
            r'(.+?)\s+'  # Descrição
            r'(UN|CX|PC|KG|LT|MT|PR)\s+'  # Unidade
            r'(\d{8,14})\s+'  # Código de barras
            r'(\d+)\s+'  # Quantidade
            r'\$?([\d.,]+)\s+'  # Preço unitário
            r'\$?([\d.,]+)'  # Preço total
        )
        
        for match in padrao_item.finditer(self.texto):
            item = {
                'numero_item': int(match.group(1)),
                'codigo': match.group(2).strip(),
                'descricao': match.group(3).strip(),
                'unidade': match.group(4).strip(),
                'codigo_barras': match.group(5).strip(),
                'quantidade': self._limpar_quantidade(match.group(6)),
                'valor_unitario': self._limpar_valor(match.group(7)),
                'valor_total': self._limpar_valor(match.group(8)),
            }
            dados['itens'].append(item)
        
        # Se não encontrou, tenta método alternativo
        if not dados['itens']:
            dados['itens'] = self._extrair_itens_araujo_alternativo()
        
        # Calcula total se não encontrado
        if dados['total'] == 0 and dados['itens']:
            dados['total'] = sum(item['valor_total'] for item in dados['itens'])
        
        dados['subtotal'] = dados['total']
        
        return dados
    
    def _extrair_itens_araujo_alternativo(self) -> List[Dict]:
        """Método alternativo para extrair itens do formato Araujo"""
        itens = []
        
        # Procura por linhas com código de barras (8-14 dígitos)
        for linha in self.linhas:
            # Procura código de barras
            barras_match = re.search(r'\b(\d{8,14})\b', linha)
            if not barras_match:
                continue
            
            codigo_barras = barras_match.group(1)
            
            # Procura valores monetários
            valores = re.findall(r'\$?([\d.,]+)', linha)
            if len(valores) < 2:
                continue
            
            # Procura código do produto (geralmente no início)
            codigo_match = re.match(r'^\s*\d+\s+([A-Z0-9]+)', linha)
            codigo = codigo_match.group(1) if codigo_match else ''
            
            # Extrai descrição (texto entre código e unidade)
            descricao = linha
            
            item = {
                'numero_item': len(itens) + 1,
                'codigo': codigo,
                'descricao': descricao[:100],
                'unidade': 'UN',
                'codigo_barras': codigo_barras,
                'quantidade': self._limpar_quantidade(valores[-3]) if len(valores) >= 3 else Decimal('1'),
                'valor_unitario': self._limpar_valor(valores[-2]),
                'valor_total': self._limpar_valor(valores[-1]),
            }
            itens.append(item)
        
        return itens
    
    def _parse_generico(self) -> Dict:
        """Parse genérico para formatos não reconhecidos"""
        dados = {
            'fornecedor': '',
            'numero_pedido': '',
            'data_emissao': None,
            'itens': [],
            'subtotal': Decimal('0.00'),
            'icms_st': Decimal('0.00'),
            'ipi': Decimal('0.00'),
            'total': Decimal('0.00'),
        }
        
        # Tenta extrair fornecedor (primeira linha com LTDA, EIRELI, etc)
        for linha in self.linhas[:10]:
            if any(x in linha.upper() for x in ['LTDA', 'EIRELI', 'S.A.', 'S/A', 'ME', 'EPP']):
                dados['fornecedor'] = linha.strip()[:100]
                break
        
        # Tenta extrair número do pedido
        match = re.search(r'[Pp]edido[:\s#]*(\d+)', self.texto)
        if match:
            dados['numero_pedido'] = match.group(1)
        
        # Tenta extrair data
        match = re.search(r'(\d{2}/\d{2}/\d{4})', self.texto)
        if match:
            try:
                dados['data_emissao'] = datetime.strptime(match.group(1), '%d/%m/%Y').date()
            except ValueError:
                pass
        
        # Tenta extrair itens (procura linhas com padrão de produto)
        for linha in self.linhas:
            # Procura linhas com valores monetários
            valores = re.findall(r'[\d.,]+', linha)
            if len(valores) >= 3:
                # Tenta identificar como item
                try:
                    # Assume últimos 3 valores são: quantidade, unitário, total
                    quantidade = self._limpar_quantidade(valores[-3])
                    unitario = self._limpar_valor(valores[-2])
                    total = self._limpar_valor(valores[-1])
                    
                    # Valida se faz sentido (quantidade * unitário ≈ total)
                    if quantidade > 0 and unitario > 0 and total > 0:
                        calc = quantidade * unitario
                        if abs(calc - total) < total * Decimal('0.1'):  # 10% de tolerância
                            # Extrai código (primeiro texto alfanumérico)
                            codigo_match = re.search(r'\b([A-Z0-9]{3,20})\b', linha)
                            codigo = codigo_match.group(1) if codigo_match else ''
                            
                            item = {
                                'numero_item': len(dados['itens']) + 1,
                                'codigo': codigo,
                                'descricao': linha[:100],
                                'unidade': 'UN',
                                'codigo_barras': '',
                                'quantidade': quantidade,
                                'valor_unitario': unitario,
                                'valor_total': total,
                            }
                            dados['itens'].append(item)
                except:
                    continue
        
        # Calcula total
        if dados['itens']:
            dados['total'] = sum(item['valor_total'] for item in dados['itens'])
            dados['subtotal'] = dados['total']
        
        self.warnings.append(f"Formato não reconhecido. Extração genérica com {len(dados['itens'])} itens.")
        
        return dados


def parse_pdf_pedido(pdf_file) -> Tuple[bool, Dict, List[str]]:
    """
    Função helper para fazer parse de PDF de pedido
    
    Args:
        pdf_file: Arquivo PDF (file-like object ou path)
        
    Returns:
        Tuple (success, dados, errors)
    """
    parser = PDFPedidoParser()
    return parser.parse(pdf_file)
