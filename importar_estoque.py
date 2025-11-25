# ============================================
# SCRIPT: importar_estoque.py
# Importa produtos do arquivo Excel para o banco de dados
# 
# COMO USAR:
# python manage.py shell -c "exec(open('importar_estoque.py').read())"
# ============================================

import os
import sys
from decimal import Decimal, InvalidOperation

import pandas as pd
from estoque.models import Produto, Categoria, Fabricante

def limpar_valor_decimal(valor):
    """Converte valor do Excel para Decimal"""
    if pd.isna(valor) or valor == '' or valor is None:
        return Decimal('0.00')
    
    try:
        if isinstance(valor, (int, float)):
            return Decimal(str(valor)).quantize(Decimal('0.01'))
        
        valor_str = str(valor).strip()
        valor_str = valor_str.replace('.', '')
        valor_str = valor_str.replace(',', '.')
        return Decimal(valor_str).quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError):
        return Decimal('0.00')

def limpar_valor_inteiro(valor):
    """Converte valor do Excel para inteiro"""
    if pd.isna(valor) or valor == '' or valor is None:
        return 0
    
    try:
        if isinstance(valor, (int, float)):
            return int(valor)
        
        valor_str = str(valor).strip()
        valor_str = valor_str.replace('.', '').replace(',', '.')
        return int(float(valor_str))
    except (ValueError, TypeError):
        return 0

print("=" * 60)
print("IMPORTACAO DE ESTOQUE")
print("=" * 60)

arquivo = 'estoque.xls'
if not os.path.exists(arquivo):
    print(f"ERRO: Arquivo '{arquivo}' nao encontrado!")
    print("Copie o arquivo para a pasta raiz do projeto (C:\\Loja-main\\)")
else:
    print(f"\nLendo arquivo {arquivo}...")
    df = pd.read_excel(arquivo, header=None, skiprows=13)
    df = df[df[1].notna() & (df[1] != 'INT') & (df[1] != '')]
    
    total_linhas = len(df)
    print(f"Encontrados {total_linhas} produtos para importar.\n")
    
    # ETAPA 1: Criar Categorias
    print("ETAPA 1: Criando categorias...")
    
    categorias_excel = df[5].dropna().unique()
    categorias_map = {}
    ignorar = ['CATEGORIA', '', None]
    
    for cat_nome in categorias_excel:
        if cat_nome in ignorar or pd.isna(cat_nome):
            continue
        
        cat_nome_limpo = str(cat_nome).strip().upper()
        
        if cat_nome_limpo == 'SUSPESAO':
            cat_nome_limpo = 'SUSPENSAO'
        elif cat_nome_limpo == 'TRANSMICAO':
            cat_nome_limpo = 'TRANSMISSAO'
        elif cat_nome_limpo == 'LIMPEZA E ':
            cat_nome_limpo = 'LIMPEZA'
        elif cat_nome_limpo == 'ARREFECIMENTO ':
            cat_nome_limpo = 'ARREFECIMENTO'
        
        categoria, criada = Categoria.objects.get_or_create(
            nome=cat_nome_limpo,
            defaults={'descricao': f'Categoria {cat_nome_limpo}', 'ativo': True}
        )
        
        categorias_map[cat_nome_limpo] = categoria
        categorias_map[str(cat_nome).strip()] = categoria
        
        if criada:
            print(f"   Criada: {cat_nome_limpo}")
    
    # ETAPA 2: Criar Fabricante Padrao
    print("\nETAPA 2: Verificando fabricante padrao...")
    
    fabricante_padrao, criado = Fabricante.objects.get_or_create(
        nome='DIVERSOS',
        defaults={'pais_origem': 'Brasil', 'ativo': True}
    )
    print(f"   Fabricante 'DIVERSOS': {'criado' if criado else 'ja existe'}")
    
    # Categoria padrao
    categoria_padrao, _ = Categoria.objects.get_or_create(
        nome='PADRAO',
        defaults={'descricao': 'Categoria Padrao', 'ativo': True}
    )
    categorias_map['PADRAO'] = categoria_padrao
    
    # ETAPA 3: Importar Produtos
    print(f"\nETAPA 3: Importando {total_linhas} produtos...")
    
    produtos_criados = 0
    produtos_atualizados = 0
    produtos_erro = 0
    
    for index, row in df.iterrows():
        try:
            codigo = str(row[1]).strip() if pd.notna(row[1]) else ''
            descricao = str(row[2]).strip() if pd.notna(row[2]) else 'SEM DESCRICAO'
            categoria_nome = str(row[5]).strip() if pd.notna(row[5]) else 'PADRAO'
            estoque = limpar_valor_inteiro(row[7])
            preco_custo = limpar_valor_decimal(row[10])
            preco_venda = limpar_valor_decimal(row[13])
            
            if not codigo or codigo == 'INT' or codigo == 'nan':
                continue
            
            # Buscar categoria
            categoria = categorias_map.get(categoria_nome)
            if not categoria:
                categoria = categorias_map.get(categoria_nome.upper())
            if not categoria:
                categoria = categoria_padrao
            
            produto_existente = Produto.objects.filter(codigo=codigo).first()
            
            if produto_existente:
                produto_existente.descricao = descricao[:200]
                produto_existente.categoria = categoria
                produto_existente.estoque_atual = estoque
                produto_existente.preco_custo = preco_custo
                produto_existente.preco_venda_dinheiro = preco_venda
                produto_existente.save()
                produtos_atualizados += 1
            else:
                Produto.objects.create(
                    codigo=codigo,
                    descricao=descricao[:200],
                    categoria=categoria,
                    fabricante=fabricante_padrao,
                    preco_custo=preco_custo,
                    preco_venda_dinheiro=preco_venda,
                    preco_venda_debito=preco_venda,
                    preco_venda_credito=preco_venda,
                    estoque_atual=estoque,
                    estoque_minimo=0,
                    estoque_maximo=0,
                    estoque_reservado=0,
                    loja='1',
                    unidade_medida='UN',
                    ativo=True,
                )
                produtos_criados += 1
            
            total_processados = produtos_criados + produtos_atualizados + produtos_erro
            if total_processados % 500 == 0:
                print(f"   Processados: {total_processados}/{total_linhas}")
                
        except Exception as e:
            produtos_erro += 1
            if produtos_erro <= 10:
                print(f"   Erro no codigo {codigo}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("RESUMO DA IMPORTACAO")
    print("=" * 60)
    print(f"Produtos criados:     {produtos_criados}")
    print(f"Produtos atualizados: {produtos_atualizados}")
    print(f"Produtos com erro:    {produtos_erro}")
    print(f"Total processado:     {produtos_criados + produtos_atualizados + produtos_erro}")
    print("=" * 60)
    print("\nImportacao concluida!")