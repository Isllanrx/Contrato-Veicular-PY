# Contrato Veicular

Aplicativo desktop para geração automatizada de contratos de compra e venda de veículos em PDF.

## O que faz

Este aplicativo permite gerar contratos de compra e venda de veículos de forma automatizada, preenchendo um formulário com dados do comprador e do veículo. O sistema:

- Coleta dados através de uma interface gráfica moderna
- Valida todos os campos obrigatórios
- Formata automaticamente CPF, telefone e valores monetários
- Gera um arquivo PDF **protegido** por senha
- Utiliza um **template** de contrato personalizável

## Bibliotecas Utilizadas

- **customtkinter** (>=5.2.0): Interface gráfica moderna e responsiva
- **reportlab** (>=4.0.0): Geração de arquivos PDF
- **PyPDF2** (>=3.0.0): Proteção de PDF com senha
- **tkcalendar** (>=1.6.1): Widget de calendário para seleção de datas

## Requisitos

- Python 3.8 ou superior
- Gerenciador de pacotes: `uv` (recomendado) ou `pip`

## Instalação

### Opção 1: Usando uv (Recomendado)

1. Instale o uv (se ainda não tiver):

```bash
pip install uv
```

1. Clone o repositório ou navegue até o diretório do projeto

1. Crie o ambiente virtual:

```bash
uv venv
```

1. Ative o ambiente virtual:
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (CMD): `.venv\Scripts\activate.bat`
   - Linux/Mac: `source .venv/bin/activate`

1. Sincronize e instale as dependências:

```bash
uv sync
uv pip install -e .
```

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Usar

### Executar a aplicação

Após instalar as dependências, você pode executar de três formas:

#### Opção 1: Executar diretamente o main.py (mais simples)

```bash
python src/contrato_veicular/main.py
```

#### Opção 2: Como módulo Python

```bash
python -m contrato_veicular.main
```

### Arquitetura

- **Domain**: Independente de frameworks, contém regras de negócio puras
- **Application**: Orquestra casos de uso, coordena as camadas
- **Infrastructure**: Implementa detalhes técnicos (UI, PDF, sistema de arquivos)

### Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:

```bash
git clone https://github.com/Isllanrx/Contrato-Veicular-PY.git
cd Contrato-Veicular-PY
```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Desenvolvedor

Desenvolvido por **Isllan Toso Pereira**

- GitHub: [Isllanrx](https://github.com/Isllanrx)
- LinkedIn: [Isllan Toso](https://br.linkedin.com/in/isllantoso)
