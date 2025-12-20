# 📦 Módulo de Compras/Entrada de Mercadorias

## 🚀 Instalação

### 1. Copie os arquivos para as pastas corretas:

```
C:\Sistema_AutoPe-as-main\
├── compras/                    <-- Copie a pasta compras/ aqui
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── views.py
│   └── utils/
│       ├── __init__.py
│       └── xml_parser.py
│
├── templates/
│   ├── base.html              <-- SUBSTITUA pelo novo base.html
│   └── compras/               <-- Copie a pasta compras/ para dentro de templates/
│       ├── entrada_lista.html
│       ├── entrada_xml.html
│       ├── entrada_manual.html
│       └── entrada_detalhe.html
│
├── estoque/
├── vendas/
├── ...
```

### 2. Adicione o app ao `settings.py`

```python
INSTALLED_APPS = [
    # ... outros apps
    'compras',  # Adicione esta linha
]
```

### 3. Adicione as URLs ao `urls.py` principal

No arquivo `autopecas_system/urls.py`, adicione:

```python
urlpatterns = [
    # ... outras urls
    path('compras/', include('compras.urls', namespace='compras')),
]
```

### 4. Execute as migrações

```bash
python manage.py makemigrations compras
python manage.py migrate
```

### 5. (Opcional) Crie o superusuário se ainda não tiver

```bash
python manage.py createsuperuser
```

---

## 📋 Funcionalidades

### ✅ Entrada Manual
- Criação de nota fiscal manualmente
- Adição de itens um a um
- Vinculação com produtos existentes

### ✅ Importação de XML
- Upload de arquivo XML da NF-e
- Extração automática de dados
- Cadastro automático de fornecedor (se não existir)
- Vinculação automática de produtos (por código de barras/código)

### ✅ Conferência de Itens
- Conferência de quantidade
- Detecção de divergências
- Conferência em lote

### ✅ Vinculação de Produtos
- Busca por código, código de barras ou descrição
- Vinculação automática em lote
- Cadastro de novo produto a partir do item da NF

### ✅ Finalização
- Atualização automática de estoque
- Atualização de preço de custo
- Recálculo de preço de venda (opcional)
- Criação/atualização de cotações do fornecedor
- Geração de movimentação de estoque
- Histórico de alteração de preços

---

## 🔗 URLs Disponíveis

| URL | Descrição |
|-----|-----------|
| `/compras/` | Lista de entradas |
| `/compras/importar-xml/` | Importar XML de NF-e |
| `/compras/entrada-manual/` | Criar entrada manual |
| `/compras/<id>/` | Detalhes da entrada |
| `/compras/<id>/conferencia-rapida/` | Conferência rápida |

---

## 📊 Models Criados

### NotaFiscalEntrada
Representa uma nota fiscal de entrada com:
- Dados da NF (número, série, chave de acesso)
- Valores (produtos, frete, impostos, total)
- Configurações de entrada
- Status e auditoria

### ItemNotaEntrada
Representa um item da nota com:
- Dados do XML (código, descrição, NCM)
- Quantidades e valores
- Vínculo com produto do sistema
- Status de conferência

### LogEntradaMercadoria
Registro de todas as operações realizadas na entrada.

---

## ⚙️ Configurações de Entrada

| Opção | Descrição |
|-------|-----------|
| Atualizar Preço de Custo | Atualiza o preço de custo dos produtos |
| Recalcular Preço de Venda | Calcula novo preço baseado na margem |
| Ratear Frete | Distribui o frete no custo de cada item |
| Atualizar Cotação | Cria/atualiza cotação do fornecedor |

---

## 🔄 Fluxo de Trabalho

```
1. IMPORTAR XML ou CRIAR MANUAL
         ↓
2. VINCULAR PRODUTOS (automático ou manual)
         ↓
3. CONFERIR QUANTIDADES
         ↓
4. FINALIZAR ENTRADA
         ↓
   - Estoque atualizado
   - Preços atualizados
   - Cotações criadas
   - Movimentação registrada
```

---

## 📝 Notas

- O módulo requer que os models `Produto`, `Fornecedor`, `Categoria`, `Fabricante`, 
  `MovimentacaoEstoque`, `CotacaoFornecedor` e `HistoricoPreco` existam no app `estoque`.

- O sistema tenta vincular produtos automaticamente por:
  1. Código de barras (EAN/GTIN)
  2. Código do produto
  3. Referência do fabricante

- Itens não vinculados impedem a finalização da entrada.

---

## 🐛 Problemas Comuns

### Erro: "No module named 'compras'"
→ Verifique se a pasta `compras` está na raiz do projeto e se o app está em `INSTALLED_APPS`.

### Erro de migração
→ Execute `python manage.py makemigrations compras` antes de `migrate`.

### Templates não encontrados
→ Verifique se a estrutura de pastas está correta: `compras/templates/compras/`.

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.
