# Contrato Veicular

Aplicativo desktop para geração automatizada de contratos de compra e venda de veículos em PDF.

## Captura de tela

![Interface do aplicativo — formulário de dados do comprador e do veículo](Tela_aplicacao.png)

## Visão geral

O sistema coleta dados por meio de uma interface gráfica, valida campos obrigatórios, aplica formatação (CPF, telefone, valores) e gera um PDF a partir de um template, com opção de proteção por senha.

## Funcionalidades

- Formulário com interface gráfica (CustomTkinter)
- Validação de campos obrigatórios
- Formatação automática de CPF, telefone e valores monetários
- Geração de PDF protegido por senha
- Uso de template de contrato personalizável

## Stack tecnológica

| Componente   | Biblioteca    | Versão mínima |
|-------------|---------------|---------------|
| Interface   | customtkinter | >= 5.2.0      |
| PDF         | reportlab     | >= 4.0.0      |
| PDF (senha) | PyPDF2        | >= 3.0.0      |
| Datas       | tkcalendar    | >= 1.6.1      |

## Pré-requisitos

- Python 3.8 ou superior
- Ambiente com suporte a Tkinter (incluído na maioria das instalações oficiais do Python no Windows)

## Instalação

### Com uv (recomendado)

Na raiz do repositório:

```bash
uv sync
```

Isso cria o ambiente virtual em `.venv` e instala o projeto e as dependências declaradas em `pyproject.toml`.

### Com pip

```bash
python -m venv .venv
```

Ative o ambiente virtual (Windows PowerShell: `.venv\Scripts\Activate.ps1`) e execute:

```bash
pip install -e .
```

Alternativa equivalente às dependências listadas:

```bash
pip install -r requirements.txt
```

## Execução

Com `uv`, na raiz do projeto:

```bash
uv run contrato
```

Com o ambiente ativado e o pacote instalado em modo editável:

```bash
python -m contrato_veicular.main
```

Também é possível executar diretamente:

```bash
python src/contrato_veicular/main.py
```

## Arquitetura do código

Estrutura em camadas sob `src/contrato_veicular/`:

- **Domain**: regras de negócio, entidades, validadores e formatadores (sem dependência de UI ou PDF)
- **Application**: casos de uso que orquestram validação e geração do contrato
- **Infrastructure**: PDF, carregamento de templates, componentes de interface e utilitários de UI

## Repositório

```bash
git clone https://github.com/Isllanrx/Contrato-Veicular-PY.git
cd Contrato-Veicular-PY
```

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE).

## Autor

**Isllan Toso Pereira**

- GitHub: [Isllanrx](https://github.com/Isllanrx)
- LinkedIn: [Isllan Toso](https://br.linkedin.com/in/isllantoso)
