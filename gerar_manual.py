from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime

# Criar PDF
pdf_file = "MANUAL_SISTEMA_AUTOPECAS.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
story = []
styles = getSampleStyleSheet()

# Estilo customizado para título
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor='#003366',
    spaceAfter=30,
    alignment=TA_CENTER
)

# Estilo para subtítulos
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor='#0066CC',
    spaceAfter=12,
    spaceBefore=12
)

# Capa
story.append(Spacer(1, 3*cm))
story.append(Paragraph("SISTEMA DE GESTÃO", title_style))
story.append(Paragraph("PARA AUTOPEÇAS", title_style))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Manual do Usuário", styles['Heading2']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(f"Versão 1.0 - {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
story.append(PageBreak())

# Índice
story.append(Paragraph("Índice", title_style))
story.append(Spacer(1, 0.5*cm))
indices = [
    "1. Introdução",
    "2. Instalação e Configuração",
    "3. Gestão de Clientes",
    "4. Controle de Estoque",
    "5. Vendas",
    "6. Ordens de Serviço",
    "7. Relatórios",
    "8. Dicas e Boas Práticas",
]
for item in indices:
    story.append(Paragraph(item, styles['Normal']))
    story.append(Spacer(1, 0.3*cm))
story.append(PageBreak())

# 1. Introdução
story.append(Paragraph("1. Introdução", subtitle_style))
intro_text = """
O Sistema de Gestão para Autopeças é uma solução completa desenvolvida em Python com Django,
inspirada no GDoor, um dos sistemas mais utilizados no segmento de autopeças no Brasil.
<br/><br/>
Este sistema oferece controle completo sobre:
<br/>
• Cadastro de clientes (Pessoa Física e Jurídica) com controle de veículos<br/>
• Gestão completa de estoque com controle de fornecedores<br/>
• Emissão de vendas com múltiplas formas de pagamento<br/>
• Ordens de serviço para oficinas mecânicas<br/>
• Relatórios gerenciais e controles financeiros<br/>
<br/>
O sistema foi desenvolvido com foco na facilidade de uso, permitindo que qualquer pessoa
com conhecimentos básicos de informática possa operá-lo sem dificuldades.
"""
story.append(Paragraph(intro_text, styles['BodyText']))
story.append(Spacer(1, 0.5*cm))
story.append(PageBreak())

# 2. Instalação
story.append(Paragraph("2. Instalação e Configuração", subtitle_style))
install_text = """
<b>2.1 Requisitos do Sistema</b><br/>
• Python 3.8 ou superior<br/>
• Django 5.2 ou superior<br/>
• 500 MB de espaço em disco<br/>
• Navegador web moderno (Chrome, Firefox, Edge)<br/>
<br/>
<b>2.2 Instalação</b><br/>
1. Extraia os arquivos do sistema em uma pasta de sua preferência<br/>
2. Abra o terminal/prompt de comando na pasta do sistema<br/>
3. Execute o script de inicialização:<br/>
   • Linux/Mac: ./iniciar.sh<br/>
   • Windows: python manage.py migrate && python manage.py createsuperuser<br/>
<br/>
<b>2.3 Primeiro Acesso</b><br/>
1. Inicie o servidor: python manage.py runserver<br/>
2. Abra o navegador em: http://localhost:8000/admin<br/>
3. Faça login com as credenciais criadas na instalação<br/>
<br/>
<b>2.4 Dados de Exemplo</b><br/>
Para facilitar o aprendizado, o sistema pode criar dados de exemplo automaticamente.
Execute: python manage.py shell < populate_data.py
"""
story.append(Paragraph(install_text, styles['BodyText']))
story.append(PageBreak())

# 3. Clientes
story.append(Paragraph("3. Gestão de Clientes", subtitle_style))
clientes_text = """
<b>3.1 Cadastro de Clientes</b><br/>
O sistema permite cadastrar tanto Pessoa Física quanto Jurídica. Para cadastrar um novo cliente:<br/>
<br/>
1. Acesse o menu "Clientes" → "Adicionar Cliente"<br/>
2. Selecione o tipo (Pessoa Física ou Jurídica)<br/>
3. Preencha os dados básicos:<br/>
   • Nome/Razão Social<br/>
   • CPF ou CNPJ (será validado)<br/>
   • RG ou Inscrição Estadual<br/>
<br/>
4. Preencha os dados de contato:<br/>
   • Telefone fixo (obrigatório)<br/>
   • Celular (opcional)<br/>
   • Email (opcional, mas recomendado)<br/>
<br/>
5. Preencha o endereço completo<br/>
6. Defina o limite de crédito (se aplicável)<br/>
7. Adicione observações relevantes<br/>
8. Marque como ativo/inativo<br/>
9. Clique em "Salvar"<br/>
<br/>
<b>3.2 Cadastro de Veículos</b><br/>
Cada cliente pode ter múltiplos veículos cadastrados:<br/>
<br/>
1. Acesse "Veículos" → "Adicionar Veículo"<br/>
2. Selecione o cliente proprietário<br/>
3. Preencha os dados do veículo:<br/>
   • Placa (formato ABC-1234 ou ABC1D23)<br/>
   • Marca e Modelo<br/>
   • Ano de fabricação e modelo<br/>
   • Cor<br/>
   • Chassi (opcional)<br/>
   • Renavam (opcional)<br/>
   • Quilometragem atual<br/>
<br/>
<b>3.3 Dicas Importantes</b><br/>
• CPF/CNPJ devem ser únicos no sistema<br/>
• Use o campo "Observações" para informações relevantes<br/>
• Mantenha os dados de contato sempre atualizados<br/>
• A quilometragem do veículo ajuda no controle de revisões<br/>
"""
story.append(Paragraph(clientes_text, styles['BodyText']))
story.append(PageBreak())

# 4. Estoque
story.append(Paragraph("4. Controle de Estoque", subtitle_style))
estoque_text = """
<b>4.1 Categorias</b><br/>
Antes de cadastrar produtos, crie categorias para organizá-los:<br/>
• Freios<br/>
• Suspensão<br/>
• Motor<br/>
• Elétrica<br/>
• Filtros<br/>
• Óleos e Lubrificantes<br/>
• Pneus<br/>
• Etc.<br/>
<br/>
<b>4.2 Fornecedores</b><br/>
Cadastre seus fornecedores com todas as informações de contato.
Isso facilita pedidos e controle de compras.<br/>
<br/>
<b>4.3 Cadastro de Produtos</b><br/>
1. Acesse "Produtos" → "Adicionar Produto"<br/>
2. Código do Produto: Use um código único (ex: PAST-001)<br/>
3. Código de Barras: Se houver (facilita vendas)<br/>
4. Descrição: Seja claro e detalhado<br/>
5. Categoria: Selecione a categoria apropriada<br/>
6. Fornecedor: Selecione o fornecedor principal<br/>
<br/>
<b>Aplicação do Produto:</b><br/>
• Marca do veículo (ex: Chevrolet)<br/>
• Modelo (ex: Onix)<br/>
• Ano inicial e final (ex: 2012 a 2023)<br/>
<br/>
<b>Preços:</b><br/>
• Unidade de medida (UN, PC, KG, etc.)<br/>
• Preço de custo<br/>
• Preço de venda<br/>
• Margem de lucro (calculada automaticamente!)<br/>
<br/>
<b>Controle de Estoque:</b><br/>
• Estoque atual<br/>
• Estoque mínimo (alerta quando atingir)<br/>
• Estoque máximo (controle de compras)<br/>
• Localização física (ex: Prateleira A-12)<br/>
<br/>
<b>4.4 Movimentações de Estoque</b><br/>
Registre todas as entradas e saídas:<br/>
• Entrada: Compra de fornecedor<br/>
• Saída: Venda ou uso em OS<br/>
• Ajuste: Correção de estoque<br/>
• Devolução: Retorno de mercadoria<br/>
<br/>
<b>Dicas:</b><br/>
• Atualize o estoque sempre que receber mercadorias<br/>
• Faça inventários periódicos<br/>
• Use a localização para agilizar a separação<br/>
• Configure alertas de estoque mínimo<br/>
"""
story.append(Paragraph(estoque_text, styles['BodyText']))
story.append(PageBreak())

# 5. Vendas
story.append(Paragraph("5. Vendas", subtitle_style))
vendas_text = """
<b>5.1 Processo de Venda</b><br/>
<br/>
1. Acesse "Vendas" → "Adicionar Venda"<br/>
2. Número da Venda: O sistema pode gerar automaticamente<br/>
3. Selecione o Cliente<br/>
4. Selecione o Veículo (se a venda for para um veículo específico)<br/>
5. Escolha o Status:<br/>
   • Aberta: Venda em andamento<br/>
   • Finalizada: Venda concluída<br/>
   • Cancelada: Venda cancelada<br/>
<br/>
6. Forma de Pagamento:<br/>
   • Dinheiro<br/>
   • Cartão de Débito<br/>
   • Cartão de Crédito<br/>
   • PIX<br/>
   • Boleto<br/>
   • Crediário (parcelamento próprio)<br/>
<br/>
7. Informe o nome do Vendedor<br/>
<br/>
<b>5.2 Adicionando Produtos</b><br/>
Na seção "Itens de Venda":<br/>
1. Clique no botão "+" para adicionar um item<br/>
2. Selecione o Produto<br/>
3. Digite a Quantidade<br/>
4. O Valor Unitário é preenchido automaticamente<br/>
5. Aplique Desconto no item se necessário<br/>
6. O Total do item é calculado automaticamente<br/>
7. Adicione quantos itens forem necessários<br/>
<br/>
O sistema calcula automaticamente:<br/>
• Subtotal (soma de todos os itens)<br/>
• Desconto total na venda<br/>
• Total final<br/>
<br/>
<b>5.3 Finalizando a Venda</b><br/>
1. Revise todos os itens<br/>
2. Confira o valor total<br/>
3. Clique em "Salvar"<br/>
4. O estoque é atualizado automaticamente!<br/>
<br/>
<b>Dicas:</b><br/>
• Sempre confira o CPF do cliente para notas fiscais<br/>
• Use o campo "Observações" para informações importantes<br/>
• Vendas "Abertas" permitem edição posterior<br/>
• Vendas "Finalizadas" reduzem o estoque automaticamente<br/>
"""
story.append(Paragraph(vendas_text, styles['BodyText']))
story.append(PageBreak())

# 6. Ordens de Serviço
story.append(Paragraph("6. Ordens de Serviço", subtitle_style))
os_text = """
<b>6.1 Criando uma Ordem de Serviço</b><br/>
<br/>
1. Acesse "Ordens de Serviço" → "Adicionar Ordem de Serviço"<br/>
2. Número da OS: Defina um número sequencial<br/>
3. Selecione o Cliente<br/>
4. Selecione o Veículo<br/>
5. Status da OS:<br/>
   • Aberta: Recém criada<br/>
   • Em Andamento: Em execução<br/>
   • Aguardando Peças: Parada por falta de peças<br/>
   • Finalizada: Concluída<br/>
   • Cancelada: Cancelada<br/>
<br/>
<b>6.2 Informações do Serviço</b><br/>
• Defeito Reclamado: O que o cliente relatou<br/>
• Defeito Constatado: O que foi identificado<br/>
• Serviços Executados: Descrição do que foi feito<br/>
• KM de Entrada: Quilometragem do veículo<br/>
• Data de Entrada: Preenchida automaticamente<br/>
• Data Prevista: Quando ficará pronto<br/>
• Data de Saída: Quando foi entregue<br/>
• Mecânico: Responsável pelo serviço<br/>
<br/>
<b>6.3 Adicionando Peças</b><br/>
Na seção "Peças da OS":<br/>
1. Clique em "+" para adicionar<br/>
2. Selecione o Produto<br/>
3. Digite a Quantidade<br/>
4. O Valor é preenchido automaticamente<br/>
5. O Total é calculado<br/>
<br/>
<b>6.4 Adicionando Serviços</b><br/>
Na seção "Serviços da OS":<br/>
1. Clique em "+" para adicionar<br/>
2. Digite a Descrição do serviço<br/>
3. Informe o Valor do serviço<br/>
<br/>
<b>6.5 Valores e Finalização</b><br/>
O sistema calcula automaticamente:<br/>
• Valor das Peças (soma de todas as peças)<br/>
• Valor dos Serviços (soma de todos os serviços)<br/>
• Total da OS<br/>
<br/>
Clique em "Salvar" para gravar a OS.<br/>
<br/>
<b>Dicas Importantes:</b><br/>
• Sempre registre o defeito reclamado pelo cliente<br/>
• Atualize o status conforme o andamento<br/>
• Use a data prevista para gerenciar prazos<br/>
• O estoque é atualizado quando adiciona peças<br/>
• Mantenha observações detalhadas<br/>
"""
story.append(Paragraph(os_text, styles['BodyText']))
story.append(PageBreak())

# 7. Relatórios
story.append(Paragraph("7. Relatórios e Consultas", subtitle_style))
relatorios_text = """
<b>7.1 Vendas por Período</b><br/>
1. Acesse "Vendas"<br/>
2. Use o filtro de data no topo da tela<br/>
3. Filtre por:<br/>
   • Status (Aberta, Finalizada, Cancelada)<br/>
   • Forma de pagamento<br/>
   • Vendedor<br/>
   • Cliente<br/>
<br/>
<b>7.2 Produtos em Estoque</b><br/>
1. Acesse "Produtos"<br/>
2. Use os filtros:<br/>
   • Categoria<br/>
   • Fornecedor<br/>
   • Marca de veículo<br/>
<br/>
<b>Alertas de Estoque:</b><br/>
• Ordene por "Estoque Atual"<br/>
• Identifique produtos abaixo do estoque mínimo<br/>
• Planeje reposições<br/>
<br/>
<b>7.3 Ordens de Serviço</b><br/>
1. Acesse "Ordens de Serviço"<br/>
2. Filtros disponíveis:<br/>
   • Status<br/>
   • Data de entrada<br/>
   • Mecânico<br/>
   • Cliente<br/>
<br/>
<b>7.4 Movimentações de Estoque</b><br/>
1. Acesse "Movimentações de Estoque"<br/>
2. Veja todo o histórico:<br/>
   • Tipo (Entrada, Saída, Ajuste)<br/>
   • Data<br/>
   • Produto<br/>
   • Quantidade<br/>
   • Responsável<br/>
<br/>
<b>7.5 Dicas para Análises</b><br/>
• Use o período de data para análises mensais<br/>
• Combine múltiplos filtros para consultas específicas<br/>
• Exporte dados quando necessário<br/>
• Faça relatórios periódicos de fechamento<br/>
"""
story.append(Paragraph(relatorios_text, styles['BodyText']))
story.append(PageBreak())

# 8. Boas Práticas
story.append(Paragraph("8. Dicas e Boas Práticas", subtitle_style))
praticas_text = """
<b>8.1 Segurança dos Dados</b><br/>
• Faça backup diário do arquivo db.sqlite3<br/>
• Mantenha senhas fortes e únicas<br/>
• Não compartilhe credenciais de acesso<br/>
• Crie usuários diferentes para cada funcionário<br/>
<br/>
<b>8.2 Organização do Estoque</b><br/>
• Use códigos padronizados para produtos<br/>
• Mantenha fotos dos produtos quando possível<br/>
• Atualize preços regularmente<br/>
• Faça inventários periódicos<br/>
• Organize fisicamente seguindo o sistema<br/>
<br/>
<b>8.3 Atendimento ao Cliente</b><br/>
• Mantenha cadastros sempre atualizados<br/>
• Registre todas as observações importantes<br/>
• Use o histórico para atendimento personalizado<br/>
• Acompanhe prazos de Ordens de Serviço<br/>
<br/>
<b>8.4 Gestão Financeira</b><br/>
• Confira diariamente as vendas do dia<br/>
• Monitore produtos de baixo giro<br/>
• Analise margem de lucro regularmente<br/>
• Controle contas a receber (limite de crédito)<br/>
<br/>
<b>8.5 Manutenção do Sistema</b><br/>
• Mantenha o Python e Django atualizados<br/>
• Faça backup antes de grandes alterações<br/>
• Teste novos recursos em ambiente separado<br/>
• Documente customizações realizadas<br/>
<br/>
<b>8.6 Suporte e Aprendizado</b><br/>
• Consulte a documentação do Django para dúvidas técnicas<br/>
• Treine sua equipe no uso do sistema<br/>
• Comece com funcionalidades básicas<br/>
• Expanda conforme necessidade<br/>
<br/>
<b>8.7 Produtividade</b><br/>
• Use atalhos de teclado no navegador<br/>
• Configure campos padrão para agilizar cadastros<br/>
• Use a busca rápida para encontrar registros<br/>
• Mantenha abas separadas para diferentes módulos<br/>
<br/>
<b>Contatos e Informações:</b><br/>
Sistema desenvolvido com Django Framework<br/>
Documentação: https://docs.djangoproject.com/<br/>
<br/>
Para suporte técnico do Django e Python, consulte as comunidades oficiais.
"""
story.append(Paragraph(praticas_text, styles['BodyText']))

# Construir PDF
doc.build(story)
print(f"✓ Manual gerado com sucesso: {pdf_file}")
