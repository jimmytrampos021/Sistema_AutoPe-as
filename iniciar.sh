#!/bin/bash
# Script de inicialização do Sistema Autopeças

echo "=================================="
echo "Sistema de Gestão para Autopeças"
echo "=================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Passo 1:${NC} Verificando instalação do Django..."
if ! python3 -c "import django" 2>/dev/null; then
    echo "Instalando Django..."
    pip install -r requirements.txt --break-system-packages
else
    echo -e "${GREEN}✓${NC} Django já instalado"
fi

echo ""
echo -e "${BLUE}Passo 2:${NC} Aplicando migrações do banco de dados..."
python3 manage.py migrate

echo ""
echo -e "${BLUE}Passo 3:${NC} Criando superusuário..."
echo "Digite as credenciais para o administrador do sistema:"
python3 manage.py createsuperuser

echo ""
echo -e "${BLUE}Passo 4:${NC} Deseja popular o banco com dados de exemplo? (s/n)"
read -r resposta
if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    python3 manage.py shell < populate_data.py
    echo -e "${GREEN}✓${NC} Dados de exemplo criados!"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Sistema pronto para uso!${NC}"
echo "=================================="
echo ""
echo "Para iniciar o servidor, execute:"
echo "  python3 manage.py runserver"
echo ""
echo "Depois acesse no navegador:"
echo "  http://localhost:8000/admin"
echo ""
echo "Documentação completa em: README.md"
echo "Guia rápido em: GUIA_RAPIDO.md"
