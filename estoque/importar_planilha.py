import pandas as pd
from django.db import transaction
from estoque.models import Produto, Categoria

CAMINHO_ARQUIVO = r"C:\Loja-main\estoque\estoque.xlsx"

def gerar_sku_unico(sku_base):
    """Gera um SKU único adicionando sufixos -1, -2, -3..."""
    sku = sku_base
    contador = 1
    while Produto.objects.filter(codigo_sku=sku).exists():
        sku = f"{sku_base}-{contador}"
        contador += 1
    return sku

def importar_estoque():
    print("📦 Lendo planilha...")

    df = pd.read_excel(CAMINHO_ARQUIVO)

    produtos_criados = 0
    produtos_atualizados = 0

    for index, row in df.iterrows():

        sku_original = str(row.get("CÓDIGO", "")).strip()

        if not sku_original:
            print(f"⚠ Linha {index} ignorada — SKU vazio")
            continue

        sku = sku_original

        # 🔥 Se SKU já existe → gerar automático
        if Produto.objects.filter(codigo_sku=sku).exists():
            novo_sku = gerar_sku_unico(sku)
            print(f"⚠ SKU '{sku}' duplicado → gerando '{novo_sku}'")
            sku = novo_sku

        codigo_barras = str(row.get("BARRAS", "")).strip()
        nome = str(row.get("REFERÊNCIA", "")).strip()
        fabricante = str(row.get("FABRICANTE", "")).strip()

        preco = float(row.get("PREÇO", 0) or 0)
        estoque = float(row.get("ESTOQUE", 0) or 0)

        categoria, _ = Categoria.objects.get_or_create(nome="Genérico")

        try:
            with transaction.atomic():
                produto, created = Produto.objects.update_or_create(
                    codigo_interno=row.get("INT"),
                    defaults={
                        "codigo_sku": sku,
                        "codigo_barras": codigo_barras,
                        "nome": nome,
                        "marca": fabricante,
                        "preco_venda_credito": preco,
                        "estoque_atual": estoque,
                        "categoria": categoria,
                    }
                )

                if created:
                    produtos_criados += 1
                    print(f"➕ Criado: {sku} - {nome}")
                else:
                    produtos_atualizados += 1
                    print(f"🔄 Atualizado: {sku} - {nome}")

        except Exception as e:
            print(f"❌ Erro na linha {index}: {e}")

    print("\n=====================================")
    print("🎉 IMPORTAÇÃO FINALIZADA")
    print(f"Produtos criados: {produtos_criados}")
    print(f"Produtos atualizados: {produtos_atualizados}")
    print("=====================================\n")
