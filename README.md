# 🚗 Sistema de Gestão para Autopeças

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Sistema completo de gestão para autopeças desenvolvido em Python com Django**

[Instalação](#-instalação) • [Funcionalidades](#-funcionalidades) • [Documentação](#-documentação) • [Contribuir](#-contribuir)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API REST](#-api-rest)
- [Documentação](#-documentação)
- [Contribuir](#-contribuir)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

O **Sistema de Gestão para Autopeças** é uma solução completa e profissional para gerenciar lojas de autopeças, inspirado no GDoor. O sistema oferece controle total sobre vendas, estoque, clientes, fornecedores e ordens de serviço, com uma interface moderna e intuitiva.

### 🌟 Diferenciais

- ✅ **100% em Português** - Interface totalmente em português brasileiro
- ✅ **Código Limpo** - Segue as melhores práticas do Django e PEP 8
- ✅ **API REST Completa** - Integração fácil com outros sistemas
- ✅ **Responsivo** - Funciona perfeitamente em desktop, tablet e mobile
- ✅ **Gratuito e Open Source** - Use, modifique e distribua livremente
- ✅ **Bem Documentado** - Documentação completa em português

---

## 🚀 Funcionalidades Principais

### 👥 Gestão de Clientes

- Cadastro completo de clientes (Pessoa Física e Jurídica)
- Controle de veículos por cliente
- Histórico de compras e ordens de serviço
- Limite de crédito configurável
- Dados completos: endereço, contatos, documentos

### 📦 Controle de Estoque

- Cadastro de produtos com código de barras
- Categorização hierárquica (categoria e subcategoria)
- Gestão de fornecedores com cotações
- Controle de estoque (mínimo, máximo, atual)
- Localização física dos produtos (loja, setor, prateleira)
- Compatibilidade por veículo (montadora, modelo, versão)
- Múltiplos preços (dinheiro, débito, crédito, atacado)
- Cálculo automático de margem de lucro
- Movimentações de estoque rastreáveis
- Fotos dos produtos
- Histórico de alteração de preços

### 💰 Vendas

- Emissão rápida de vendas (PDV)
- Múltiplas formas de pagamento
- Descontos por item e no total
- Vinculação com cliente e veículo
- Controle de status (Aberta, Finalizada, Cancelada)
- Impressão de cupom/nota
- Busca inteligente de produtos

### 💼 Orçamentos

- Criação de orçamentos detalhados
- Conversão fácil para venda
- Controle de validade
- Status de aprovação
- Observações internas e para o cliente

### 🔧 Ordens de Serviço

- Controle completo de OS para oficinas
- Registro de defeitos (reclamado e constatado)
- Controle de peças utilizadas
- Controle de serviços executados
- Acompanhamento de status
- Controle de prazos
- Valores separados (peças e serviços)
- Vinculação com veículo e mecânico
- Impressão de OS

### 🏢 Gestão de Fornecedores

- Cadastro completo de fornecedores
- Sistema de cotações
- Comparador de preços
- Histórico de compras
- Avaliação de fornecedores

### 📊 Relatórios e Dashboard

- Dashboard com indicadores em tempo real
- Vendas por período
- Produtos mais vendidos
- Estoque crítico (abaixo do mínimo)
- Ordens de serviço em aberto
- Análise de margem de lucro
- Exportação para Excel
- Gráficos interativos

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.8+** - Linguagem de programação
- **Django 5.2+** - Framework web
- **Django REST Framework** - API REST
- **SQLite/PostgreSQL** - Banco de dados
- **Pillow** - Processamento de imagens

### Frontend

- **HTML5/CSS3** - Estrutura e estilo
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript** - Interatividade
- **jQuery** - Manipulação do DOM
- **Chart.js** - Gráficos interativos

### Ferramentas

- **Git** - Controle de versão
- **pip** - Gerenciador de pacotes Python
- **virtualenv** - Ambientes virtuais Python

---

## 📋 Requisitos

### Requisitos de Sistema

- **Sistema Operacional:** Windows 10+, macOS 10.14+, ou Linux (Ubuntu 20.04+)
- **Python:** 3.8 ou superior
- **Memória RAM:** Mínimo 2GB (recomendado 4GB)
- **Espaço em Disco:** Mínimo 500MB
- **Navegador:** Chrome 90+, Firefox 88+, Edge 90+, ou Safari 14+

### Dependências Python

Veja o arquivo `requirements.txt` para a lista completa.

---

## 🔧 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/autopecas-system.git
cd autopecas-system
```

### 2. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

```bash
# Aplicar migrações
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário administrador.

### 6. Cole Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 7. Inicie o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em: `http://localhost:8000`

---

## 💻 Uso

### Acesso Inicial

1. **Interface Administrativa**
   - URL: `http://localhost:8000/admin`
   - Use o superusuário criado anteriormente

2. **Dashboard Principal**
   - URL: `http://localhost:8000/`
   - Visão geral do sistema

3. **PDV (Ponto de Venda)**
   - URL: `http://localhost:8000/pdv/`
   - Interface para vendas rápidas

### Primeiros Passos

1. **Cadastre Categorias**
   - Acesse "Estoque" → "Categorias"
   - Crie categorias e subcategorias

2. **Cadastre Fornecedores**
   - Acesse "Fornecedores" → "Novo Fornecedor"
   - Preencha os dados completos

3. **Cadastre Produtos**
   - Acesse "Estoque" → "Produtos" → "Novo Produto"
   - Preencha informações completas

4. **Cadastre Clientes**
   - Acesse "Clientes" → "Novo Cliente"
   - Adicione veículos se necessário

5. **Realize uma Venda**
   - Acesse o PDV
   - Selecione cliente e produtos
   - Finalize a venda

---

## 📁 Estrutura do Projeto

```
autopecas_system/
│
├── autopecas_system/          # Configurações do projeto
│   ├── settings.py            # Configurações gerais
│   ├── urls.py                # URLs principais
│   └── api_urls.py            # URLs da API
│
├── core/                      # App principal
│   ├── views.py               # Views do dashboard, PDV, etc
│   └── templates/             # Templates HTML
│
├── clientes/                  # App de clientes
│   ├── models.py              # Cliente, Veiculo
│   ├── admin.py               # Interface admin
│   ├── forms.py               # Formulários
│   └── api_views.py           # API REST
│
├── estoque/                   # App de estoque
│   ├── models.py              # Produto, Categoria, Fornecedor, etc
│   ├── admin.py               # Interface admin
│   ├── forms.py               # Formulários
│   └── api_views.py           # API REST
│
├── vendas/                    # App de vendas
│   ├── models.py              # Venda, OrdemServico, Orcamento
│   ├── admin.py               # Interface admin
│   ├── forms.py               # Formulários
│   └── api_views.py           # API REST
│
├── templates/                 # Templates globais
│   ├── base.html              # Template base
│   └── ...
│
├── static/                    # Arquivos estáticos
│   ├── css/                   # Estilos CSS
│   ├── js/                    # Scripts JavaScript
│   └── img/                   # Imagens
│
├── media/                     # Arquivos de mídia (uploads)
│   ├── produtos/              # Fotos de produtos
│   └── montadoras/            # Logos de montadoras
│
├── docs/                      # Documentação
│   ├── MANUAL_USUARIO.md      # Manual do usuário
│   ├── GUIA_RAPIDO.md         # Guia rápido
│   └── API.md                 # Documentação da API
│
├── manage.py                  # Gerenciador Django
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── .gitignore                 # Arquivos ignorados pelo Git
```

---

## 🔌 API REST

O sistema inclui uma API REST completa para integração com outros sistemas.

### Base URL

```
http://localhost:8000/api/
```

### Endpoints Principais

#### Clientes

```http
GET    /api/clientes/              # Listar clientes
GET    /api/clientes/{id}/         # Detalhes de um cliente
POST   /api/clientes/              # Criar cliente
PUT    /api/clientes/{id}/         # Atualizar cliente
DELETE /api/clientes/{id}/         # Deletar cliente
```

#### Produtos

```http
GET    /api/produtos/              # Listar produtos
GET    /api/produtos/{id}/         # Detalhes de um produto
POST   /api/produtos/              # Criar produto
GET    /api/produtos/estoque_baixo/ # Produtos com estoque baixo
```

#### Vendas

```http
GET    /api/vendas/                # Listar vendas
POST   /api/vendas/                # Criar venda
GET    /api/vendas/estatisticas/  # Estatísticas de vendas
```

### Autenticação

A API usa autenticação por token. Veja `docs/API.md` para detalhes completos.

---

## 📚 Documentação

- 📖 **[Manual do Usuário](./docs/MANUAL_USUARIO.md)** - Guia completo do sistema
- 📖 **[Guia Rápido](./docs/GUIA_RAPIDO.md)** - Referência rápida
- 📖 **[Documentação da API](./docs/API.md)** - Endpoints e exemplos
- 📖 **[Changelog](./CHANGELOG.md)** - Histórico de mudanças
- 📖 **[Contribuindo](./docs/CONTRIBUINDO.md)** - Como contribuir

---

## 🤝 Contribuir

Contribuições são sempre bem-vindas! Veja [CONTRIBUINDO.md](./docs/CONTRIBUINDO.md) para saber como contribuir.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Código de Conduta

Este projeto adota um Código de Conduta. Ao participar, você concorda em seguir suas diretrizes.

---

## 🐛 Reportar Bugs

Encontrou um bug? Por favor, [abra uma issue](https://github.com/seu-usuario/autopecas-system/issues) descrevendo:

- Passos para reproduzir o erro
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Ambiente (SO, Python, Django)

---

## 💡 Roadmap

### Versão 1.1 (Em Desenvolvimento)

- [ ] Integração com nota fiscal eletrônica (NF-e)
- [ ] Sistema de backup automático
- [ ] Relatórios avançados com gráficos
- [ ] Exportação de dados para Excel
- [ ] Importação de produtos via planilha

### Versão 1.2 (Planejado)

- [ ] Sistema de contas a pagar/receber
- [ ] Fluxo de caixa
- [ ] Controle de comissões
- [ ] App mobile (Android/iOS)
- [ ] Sistema de CRM

### Versão 2.0 (Futuro)

- [ ] Inteligência artificial para previsão de estoque
- [ ] Integração com marketplaces
- [ ] Multi-loja/Multi-empresa
- [ ] Sistema de fidelidade de clientes

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Sistema de Gestão para Autopeças**

Desenvolvido com ❤️ usando Django

---

## 📞 Contato

- 📧 Email: contato@autopecas-system.com
- 🌐 Website: https://autopecas-system.com
- 💬 Discord: [Junte-se ao servidor](https://discord.gg/autopecas)
- 🐦 Twitter: [@autopecas_sys](https://twitter.com/autopecas_sys)

---

## 🙏 Agradecimentos

- Comunidade Django
- Bootstrap Team
- Todos os contribuidores
- Você, por usar este sistema!

---

## 📊 Estatísticas do Projeto

![GitHub stars](https://img.shields.io/github/stars/seu-usuario/autopecas-system?style=social)
![GitHub forks](https://img.shields.io/github/forks/seu-usuario/autopecas-system?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/seu-usuario/autopecas-system?style=social)

![GitHub issues](https://img.shields.io/github/issues/seu-usuario/autopecas-system)
![GitHub pull requests](https://img.shields.io/github/issues-pr/seu-usuario/autopecas-system)
![GitHub last commit](https://img.shields.io/github/last-commit/seu-usuario/autopecas-system)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐**

**Feito com 💙 usando Django**

</div>
