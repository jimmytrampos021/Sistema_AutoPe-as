"""
Parser de XML de Nota Fiscal Eletrônica (NF-e)

Este módulo é responsável por:
- Ler e validar arquivos XML de NF-e
- Extrair dados do fornecedor, produtos, valores
- Converter para estrutura compatível com o sistema
"""

import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re


class NFEXMLParser:
    """
    Parser para arquivos XML de NF-e
    
    Suporta NF-e versão 4.0 (atual)
    """
    
    # Namespaces da NF-e
    NAMESPACES = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe',
    }
    
    def __init__(self, xml_content: str = None, xml_file=None):
        """
        Inicializa o parser
        
        Args:
            xml_content: String com o conteúdo XML
            xml_file: Arquivo XML (file-like object)
        """
        self.xml_content = xml_content
        self.xml_file = xml_file
        self.root = None
        self.nfe = None
        self.infNFe = None
        self.errors = []
        
    def parse(self) -> bool:
        """
        Faz o parse do XML
        
        Returns:
            True se parse foi bem sucedido
        """
        try:
            if self.xml_file:
                # Lê o arquivo
                content = self.xml_file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                self.xml_content = content
            
            if not self.xml_content:
                self.errors.append("Conteúdo XML vazio")
                return False
            
            # Remove BOM se existir
            self.xml_content = self.xml_content.lstrip('\ufeff')
            
            # Parse do XML
            self.root = ET.fromstring(self.xml_content)
            
            # Encontra o elemento NFe
            self.nfe = self._find_element(self.root, './/nfe:NFe')
            if self.nfe is None:
                # Tenta sem namespace
                self.nfe = self.root.find('.//NFe')
            
            if self.nfe is None:
                # O próprio root pode ser o NFe ou nfeProc
                if 'NFe' in self.root.tag:
                    self.nfe = self.root
                elif 'nfeProc' in self.root.tag:
                    self.nfe = self._find_element(self.root, './/nfe:NFe')
                    if self.nfe is None:
                        for child in self.root:
                            if 'NFe' in child.tag:
                                self.nfe = child
                                break
            
            if self.nfe is None:
                self.errors.append("Elemento NFe não encontrado no XML")
                return False
            
            # Encontra infNFe
            self.infNFe = self._find_element(self.nfe, './/nfe:infNFe')
            if self.infNFe is None:
                for child in self.nfe:
                    if 'infNFe' in child.tag:
                        self.infNFe = child
                        break
            
            if self.infNFe is None:
                self.errors.append("Elemento infNFe não encontrado no XML")
                return False
                
            return True
            
        except ET.ParseError as e:
            self.errors.append(f"Erro ao fazer parse do XML: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Erro inesperado: {str(e)}")
            return False
    
    def _find_element(self, parent, path: str):
        """Encontra elemento considerando namespace"""
        element = parent.find(path, self.NAMESPACES)
        if element is None:
            # Tenta sem namespace
            clean_path = path.replace('nfe:', '')
            element = parent.find(clean_path)
        return element
    
    def _get_text(self, parent, path: str, default: str = '') -> str:
        """Obtém texto de um elemento"""
        element = self._find_element(parent, path)
        if element is None:
            # Tenta busca direta
            for child in parent.iter():
                tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                search_name = path.split(':')[-1] if ':' in path else path
                search_name = search_name.replace('./', '').replace('/', '')
                if tag_name == search_name:
                    return child.text or default
        return element.text if element is not None and element.text else default
    
    def _get_decimal(self, parent, path: str, default: Decimal = Decimal('0.00')) -> Decimal:
        """Obtém valor decimal de um elemento"""
        text = self._get_text(parent, path, '')
        if text:
            try:
                return Decimal(text.replace(',', '.'))
            except InvalidOperation:
                pass
        return default
    
    def _get_int(self, parent, path: str, default: int = 0) -> int:
        """Obtém valor inteiro de um elemento"""
        text = self._get_text(parent, path, '')
        if text:
            try:
                return int(text)
            except ValueError:
                pass
        return default
    
    def get_chave_acesso(self) -> str:
        """Retorna a chave de acesso da NF-e"""
        if self.infNFe is not None:
            # Chave está no atributo Id
            chave = self.infNFe.get('Id', '')
            if chave.startswith('NFe'):
                chave = chave[3:]
            return chave
        return ''
    
    def get_dados_nota(self) -> Dict:
        """
        Extrai dados gerais da nota fiscal
        
        Returns:
            Dicionário com dados da nota
        """
        if self.infNFe is None:
            return {}
        
        # Busca elemento ide (identificação)
        ide = self._find_element(self.infNFe, 'nfe:ide')
        if ide is None:
            for child in self.infNFe:
                if 'ide' in child.tag:
                    ide = child
                    break
        
        if ide is None:
            return {}
        
        # Data de emissão
        data_emissao_str = self._get_text(ide, 'nfe:dhEmi')
        if not data_emissao_str:
            data_emissao_str = self._get_text(ide, 'nfe:dEmi')
        
        data_emissao = None
        if data_emissao_str:
            try:
                # Formato ISO com timezone
                if 'T' in data_emissao_str:
                    data_emissao = datetime.fromisoformat(
                        data_emissao_str.replace('Z', '+00:00')
                    ).date()
                else:
                    data_emissao = datetime.strptime(data_emissao_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        return {
            'numero_nf': self._get_text(ide, 'nfe:nNF'),
            'serie': self._get_text(ide, 'nfe:serie', '1'),
            'natureza_operacao': self._get_text(ide, 'nfe:natOp'),
            'data_emissao': data_emissao,
            'chave_acesso': self.get_chave_acesso(),
            'modelo': self._get_text(ide, 'nfe:mod', '55'),
            'tipo_operacao': self._get_text(ide, 'nfe:tpNF', '0'),  # 0=entrada, 1=saída
        }
    
    def get_dados_emitente(self) -> Dict:
        """
        Extrai dados do emitente (fornecedor)
        
        Returns:
            Dicionário com dados do fornecedor
        """
        if self.infNFe is None:
            return {}
        
        emit = self._find_element(self.infNFe, 'nfe:emit')
        if emit is None:
            for child in self.infNFe:
                if 'emit' in child.tag:
                    emit = child
                    break
        
        if emit is None:
            return {}
        
        # Endereço
        enderEmit = self._find_element(emit, 'nfe:enderEmit')
        if enderEmit is None:
            for child in emit:
                if 'enderEmit' in child.tag:
                    enderEmit = child
                    break
        
        endereco = {}
        if enderEmit is not None:
            endereco = {
                'logradouro': self._get_text(enderEmit, 'nfe:xLgr'),
                'numero': self._get_text(enderEmit, 'nfe:nro'),
                'complemento': self._get_text(enderEmit, 'nfe:xCpl'),
                'bairro': self._get_text(enderEmit, 'nfe:xBairro'),
                'cidade': self._get_text(enderEmit, 'nfe:xMun'),
                'uf': self._get_text(enderEmit, 'nfe:UF'),
                'cep': self._get_text(enderEmit, 'nfe:CEP'),
                'telefone': self._get_text(enderEmit, 'nfe:fone'),
            }
        
        cnpj = self._get_text(emit, 'nfe:CNPJ')
        if cnpj:
            # Formata CNPJ
            cnpj = re.sub(r'\D', '', cnpj)
            if len(cnpj) == 14:
                cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        
        return {
            'cnpj': cnpj,
            'razao_social': self._get_text(emit, 'nfe:xNome'),
            'nome_fantasia': self._get_text(emit, 'nfe:xFant') or self._get_text(emit, 'nfe:xNome'),
            'inscricao_estadual': self._get_text(emit, 'nfe:IE'),
            'email': self._get_text(emit, 'nfe:email'),
            **endereco
        }
    
    def get_itens(self) -> List[Dict]:
        """
        Extrai todos os itens da nota fiscal
        
        Returns:
            Lista de dicionários com dados dos itens
        """
        if self.infNFe is None:
            return []
        
        itens = []
        
        # Busca todos os elementos det (detalhe)
        for det in self.infNFe.iter():
            if 'det' in det.tag and det.tag.endswith('det'):
                item = self._parse_item(det)
                if item:
                    itens.append(item)
        
        return itens
    
    def _parse_item(self, det) -> Optional[Dict]:
        """Parse de um item da nota"""
        numero_item = det.get('nItem', '1')
        
        # Busca prod (dados do produto)
        prod = None
        for child in det:
            if 'prod' in child.tag:
                prod = child
                break
        
        if prod is None:
            return None
        
        # Busca imposto
        imposto = None
        for child in det:
            if 'imposto' in child.tag:
                imposto = child
                break
        
        # Valores de impostos
        valor_ipi = Decimal('0.00')
        valor_icms_st = Decimal('0.00')
        
        if imposto is not None:
            # IPI
            for ipi in imposto.iter():
                if 'IPI' in ipi.tag:
                    valor_ipi = self._get_decimal(ipi, 'nfe:vIPI')
                    if valor_ipi == 0:
                        # Tenta IPITrib
                        for trib in ipi.iter():
                            if 'IPITrib' in trib.tag:
                                valor_ipi = self._get_decimal(trib, 'nfe:vIPI')
                                break
                    break
            
            # ICMS ST
            for icms in imposto.iter():
                if 'ICMS' in icms.tag:
                    for child in icms:
                        valor_icms_st = self._get_decimal(child, 'nfe:vICMSST')
                        if valor_icms_st > 0:
                            break
                    break
        
        # Código de barras
        codigo_barras = self._get_text(prod, 'nfe:cEAN')
        if codigo_barras in ['SEM GTIN', 'SEM EAN', '']:
            codigo_barras = self._get_text(prod, 'nfe:cEANTrib', '')
            if codigo_barras in ['SEM GTIN', 'SEM EAN']:
                codigo_barras = ''
        
        return {
            'numero_item': int(numero_item),
            'codigo_produto_fornecedor': self._get_text(prod, 'nfe:cProd'),
            'codigo_barras': codigo_barras,
            'descricao': self._get_text(prod, 'nfe:xProd'),
            'ncm': self._get_text(prod, 'nfe:NCM'),
            'cest': self._get_text(prod, 'nfe:CEST'),
            'cfop': self._get_text(prod, 'nfe:CFOP'),
            'unidade': self._get_text(prod, 'nfe:uCom', 'UN'),
            'quantidade': self._get_decimal(prod, 'nfe:qCom', Decimal('0')),
            'valor_unitario': self._get_decimal(prod, 'nfe:vUnCom', Decimal('0')),
            'valor_total': self._get_decimal(prod, 'nfe:vProd', Decimal('0')),
            'valor_desconto': self._get_decimal(prod, 'nfe:vDesc', Decimal('0')),
            'valor_ipi': valor_ipi,
            'valor_icms_st': valor_icms_st,
        }
    
    def get_totais(self) -> Dict:
        """
        Extrai os totais da nota fiscal
        
        Returns:
            Dicionário com valores totais
        """
        if self.infNFe is None:
            return {}
        
        # Busca total
        total = self._find_element(self.infNFe, 'nfe:total')
        if total is None:
            for child in self.infNFe:
                if 'total' in child.tag:
                    total = child
                    break
        
        if total is None:
            return {}
        
        # Busca ICMSTot
        icms_tot = None
        for child in total.iter():
            if 'ICMSTot' in child.tag:
                icms_tot = child
                break
        
        if icms_tot is None:
            return {}
        
        return {
            'valor_produtos': self._get_decimal(icms_tot, 'nfe:vProd'),
            'valor_desconto': self._get_decimal(icms_tot, 'nfe:vDesc'),
            'valor_frete': self._get_decimal(icms_tot, 'nfe:vFrete'),
            'valor_seguro': self._get_decimal(icms_tot, 'nfe:vSeg'),
            'valor_outras_despesas': self._get_decimal(icms_tot, 'nfe:vOutro'),
            'valor_ipi': self._get_decimal(icms_tot, 'nfe:vIPI'),
            'valor_icms_st': self._get_decimal(icms_tot, 'nfe:vST'),
            'valor_total': self._get_decimal(icms_tot, 'nfe:vNF'),
        }
    
    def get_all_data(self) -> Dict:
        """
        Extrai todos os dados da nota fiscal
        
        Returns:
            Dicionário completo com todos os dados
        """
        if not self.parse():
            return {
                'success': False,
                'errors': self.errors
            }
        
        return {
            'success': True,
            'nota': self.get_dados_nota(),
            'emitente': self.get_dados_emitente(),
            'itens': self.get_itens(),
            'totais': self.get_totais(),
        }


def parse_xml_file(xml_file) -> Tuple[bool, Dict, List[str]]:
    """
    Função helper para fazer parse de arquivo XML
    
    Args:
        xml_file: Arquivo XML (file-like object)
        
    Returns:
        Tuple (success, data, errors)
    """
    parser = NFEXMLParser(xml_file=xml_file)
    data = parser.get_all_data()
    
    if data.get('success'):
        return True, data, []
    else:
        return False, {}, data.get('errors', ['Erro desconhecido'])


def parse_xml_string(xml_content: str) -> Tuple[bool, Dict, List[str]]:
    """
    Função helper para fazer parse de string XML
    
    Args:
        xml_content: String com conteúdo XML
        
    Returns:
        Tuple (success, data, errors)
    """
    parser = NFEXMLParser(xml_content=xml_content)
    data = parser.get_all_data()
    
    if data.get('success'):
        return True, data, []
    else:
        return False, {}, data.get('errors', ['Erro desconhecido'])
