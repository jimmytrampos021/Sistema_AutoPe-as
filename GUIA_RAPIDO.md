# ⚡ Guia Rápido - Sistema Autopeças

**Versão 1.0.1** | **Atualizado em: 24/11/2025**

---

## 🚀 Instalação Rápida (5 minutos)

### Pré-requisitos
- Python 3.8+ instalado
- Terminal/Prompt de comando
- Conexão com internet

### Passo a Passo

```bash
# 1. Clone o projeto
git clone https://github.com/seu-usuario/autopecas-system.git
cd autopecas-system

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure o banco
python manage.py migrate

# 6. Crie superusuário
python manage.py createsuperuser

# 7. Inicie o servidor
python manage.py runserver
```

**Pronto!** Acesse: http://localhost:8000

---

## 🎯 Primeira Utilização

### 1. Acesse o Admin
- URL: http://localhost:8000/admin
- Use o superusuário criado

### 2. Configure o Sistema

#### A. Cadastre Categorias de Produtos
```
Admin → Estoque → Categorias → Adicionar
```
Exemplos:
- Motor (com subcategorias: Filtros, Correias, Velas)
- Suspensão (com subcategorias: Amortecedores, Molas, Kits)
- Freios (com subcategorias: Pastilhas, Discos, Lonas)

#### B. Cadastre Fornecedores
```
Admin → Estoque → Fornecedores → Adicionar
```
Preencha:
- Nome fantasia e razão social
- CNPJ
- Contatos
- Endereço

#### C. Cadastre Produtos
```
Admin → Estoque → Produtos → Adicionar
```
Campos essenciais:
- Código (único)
- Descrição
- Categoria
- Preço de custo
- Preço de venda
- Estoque mínimo

#### D. Cadastre Clientes
```
Admin → Clientes → Clientes → Adicionar
```
Dados básicos:
- Tipo (PF ou PJ)
- Nome/Razão Social
- CPF/CNPJ
- Telefone
- Endereço

---

## 💡 Funcionalidades Principais

### 📊 Dashboard
**URL:** http://localhost:8000/

**O que mostra:**
- Vendas do dia e do mês
- OS em aberto
- Produtos com estoque baixo
- Últimas vendas
- Alertas importantes

**Atualização:** Automática a cada 5 minutos

---

### 💰 PDV (Ponto de Venda)
**URL:** http://localhost:8000/pdv/

**Como usar:**

1. **Selecione o Cliente**
   - Digite o nome no campo de busca
   - Clique no cliente desejado

2. **Adicione Produtos**
   - Use a busca rápida
   - Clique no produto para adicionar
   - Ajuste quantidade com +/-

3. **Aplique Descontos** (opcional)
   - Por item: clique no campo desconto
   - No total: use o campo no resumo

4. **Escolha Forma de Pagamento**
   - Dinheiro
   - Débito
   - Crédito
   - Outros

5. **Finalize**
   - Clique em "Finalizar Venda"
   - Imprima o cupom (opcional)

**Atalhos de Teclado:**
- `F1`: Nova venda
- `F2`: Buscar cliente
- `F3`: Buscar produto
- `F9`: Finalizar venda
- `ESC`: Cancelar

---

### 📦 Gestão de Estoque

#### Adicionar Produto
```
Estoque → Produtos → Novo Produto
```

**Campos Obrigatórios:**
- Código
- Descrição
- Categoria
- Preço de custo
- Preço de venda

**Campos Opcionais Importantes:**
- Código de barras (para leitura rápida)
- Estoque mínimo (para alertas)
- Estoque máximo (para controle)
- Localização (setor/prateleira)
- Foto do produto

#### Movimentar Estoque
```
Estoque → Movimentações → Nova Movimentação
```

**Tipos de Movimentação:**
- **Entrada**: Compra de fornecedor
- **Saída**: Venda ou consumo
- **Ajuste**: Correção de inventário
- **Devolução**: Retorno de cliente

**Importante:** Toda movimentação é registrada e não pode ser apagada (auditoria).

---

### 🔧 Ordem de Serviço

#### Criar Nova OS
```
Vendas → Ordens de Serviço → Nova OS
```

**Fluxo:**

1. **Dados Iniciais**
   - Cliente
   - Veículo
   - KM de entrada
   - Defeito reclamado

2. **Diagnóstico**
   - Defeito constatado
   - Serviços necessários

3. **Peças e Serviços**
   - Adicione peças usadas
   - Adicione serviços executados
   - Valores calculados automaticamente

4. **Status**
   - Aberta: OS criada
   - Em Andamento: Serviço sendo executado
   - Aguardando Peças: Esperando chegada de peças
   - Finalizada: Serviço concluído
   - Cancelada: OS cancelada

**Dica:** Use o campo "Data Prevista" para controlar prazos.

---

### 💼 Orçamentos

#### Criar Orçamento
```
Vendas → Orçamentos → Novo Orçamento
```

**Como funciona:**
1. Crie o orçamento com produtos e valores
2. Cliente aprova ou não
3. Se aprovado: converta em venda com 1 clique

**Validade:**
- Configure validade em dias
- Sistema alerta quando próximo do vencimento

---

### 📊 Relatórios

#### Vendas por Período
```
Relatórios → Vendas → Por Período
```

**Filtros disponíveis:**
- Data início/fim
- Cliente específico
- Forma de pagamento
- Status da venda

**Exportação:** Clique em "Exportar Excel"

#### Produtos Mais Vendidos
```
Relatórios → Produtos → Mais Vendidos
```

**Informações:**
- Ranking de produtos
- Quantidade vendida
- Valor total
- Margem de lucro

#### Estoque Crítico
```
Relatórios → Estoque → Crítico
```

**Mostra:**
- Produtos abaixo do estoque mínimo
- Produtos zerados
- Sugestão de compra

---

## 🔍 Buscas e Filtros

### Busca Rápida de Produtos

**Busca por:**
- Código do produto
- Descrição
- Código de barras
- Aplicação (modelo de veículo)
- Código original

**Exemplo:**
```
Pesquisar: "pastilha gol"
Resultado: Pastilha de Freio VW Gol G5/G6 2008-2023
```

### Filtros Avançados

**No admin, use os filtros laterais:**
- Por categoria
- Por fornecedor
- Por situação (ativo/inativo)
- Por estoque (crítico/normal/alto)

---

## ⚙️ Configurações Importantes

### Alterar Preços em Lote

1. Vá em "Estoque → Produtos"
2. Selecione os produtos
3. Ações → "Atualizar preços"
4. Defina percentual de aumento/desconto

### Backup do Banco de Dados

**Manual:**
```bash
# Fazer backup
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

**Automático:**
Configure um script no cron (Linux) ou Agendador de Tarefas (Windows).

### Alterar Senha

```bash
python manage.py changepassword nome_usuario
```

---

## 🆘 Problemas Comuns

### Não consigo fazer login
**Solução:**
```bash
python manage.py changepassword seu_usuario
```

### Erro "Table doesn't exist"
**Solução:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Produtos não aparecem no PDV
**Verificar:**
1. Produto está marcado como "Ativo"?
2. Produto tem preço de venda configurado?
3. Produto tem estoque > 0?

### Imagens não carregam
**Verificar:**
1. `MEDIA_URL` e `MEDIA_ROOT` configurados?
2. Servidor servindo arquivos de mídia?

Em desenvolvimento, adicione ao `urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Servidor muito lento
**Soluções:**
1. Use PostgreSQL ao invés de SQLite (produção)
2. Ative cache do Django
3. Otimize queries (use select_related)

---

## 📱 Atalhos do Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + K` | Busca rápida |
| `F1` | Nova venda |
| `F2` | Buscar cliente |
| `F3` | Buscar produto |
| `F5` | Atualizar página |
| `F9` | Finalizar venda |
| `ESC` | Cancelar/Fechar |
| `Ctrl + S` | Salvar formulário |

---

## 📞 Suporte

### Documentação Completa
- [Manual do Usuário](./docs/MANUAL_USUARIO.md)
- [Documentação da API](./docs/API.md)
- [Changelog](./CHANGELOG.md)

### Reportar Problemas
- [Abrir Issue no GitHub](https://github.com/seu-usuario/autopecas-system/issues)
- Email: suporte@autopecas-system.com

### Comunidade
- [Discord](https://discord.gg/autopecas)
- [Fórum](https://forum.autopecas-system.com)

---

## 💡 Dicas Profissionais

### 1. Organização de Códigos
Use padrão consistente:
```
MOT-001  → Motor
SUS-001  → Suspensão
FRE-001  → Freio
```

### 2. Estoque Mínimo
Defina baseado em:
- Tempo de reposição do fornecedor
- Giro do produto
- Sazonalidade

### 3. Margem de Lucro
O sistema calcula automaticamente:
```
Margem = ((Preço Venda - Preço Custo) / Preço Custo) × 100
```

### 4. Inventário Regular
Faça contagem mensal:
1. Exporte lista de produtos
2. Conte fisicamente
3. Ajuste diferenças
4. Registre movimentação tipo "Ajuste"

### 5. Backup
**Regra 3-2-1:**
- 3 cópias dos dados
- 2 mídias diferentes
- 1 cópia fora do local

---

## ✅ Checklist Diário

- [ ] Verificar vendas do dia
- [ ] Conferir OS em aberto
- [ ] Checar produtos com estoque baixo
- [ ] Atualizar status de OS
- [ ] Fazer backup (se configurado)

---

## 🚀 Próximos Passos

1. ✅ Configure todas as categorias
2. ✅ Cadastre seus fornecedores principais
3. ✅ Importe seu estoque atual
4. ✅ Cadastre seus clientes regulares
5. ✅ Configure preços e margens
6. ✅ Treine sua equipe
7. ✅ Comece a usar no dia a dia!

---

**Dúvidas?** Consulte o [Manual Completo](./docs/MANUAL_USUARIO.md)

**Desenvolvido com ❤️ usando Django**
