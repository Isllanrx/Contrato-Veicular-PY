from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FormField:
    """Campo do formulário"""
    name: str
    placeholder: str
    is_formatted: bool = False
    is_multiline: bool = False
    is_date: bool = False


@dataclass
class ContractData:
    """Dados do contrato validados"""
    comprador_data: Dict[str, str]
    veiculo_data: Dict[str, str]
    
    def to_dict(self) -> Dict[str, str]:
        """Converte para dicionário único"""
        return {**self.comprador_data, **self.veiculo_data}


COMPRADOR_FIELDS: List[str] = [
    "Nome", "CPF", "RG", "Telefone", "N°", "Rua", "Bairro", "Cidade", "Estado"
]

VEICULO_FIELDS: List[str] = [
    "Veículo", "Ano", "Placa do Carro", "Renavam do Carro", 
    "Valor Final", "Km Atual", "Condição", "Dia de Venda"
]

PLACEHOLDERS: Dict[str, str] = {
    "Nome": "Ex: João da Silva",
    "CPF": "000.000.000-00",
    "RG": "Ex: 123456789",
    "Telefone": "(00) 00000-0000",
    "N°": "Ex: 123",
    "Rua": "Ex: Rua das Flores",
    "Bairro": "Ex: Centro",
    "Cidade": "Ex: Vitória",
    "Estado": "Ex: ES",
    "Veículo": "Ex: Honda Civic",
    "Ano": "Ex: 2020",
    "Placa do Carro": "ABC-1234",
    "Renavam do Carro": "12345678901",
    "Valor Final": "R$ 50.000,00",
    "Km Atual": "Ex: 50000",
    "Condição": "Descreva a condição do veículo...",
    "Dia de Venda": "Clique para selecionar a data"
}

FORMATTED_FIELDS: List[str] = ["CPF", "Telefone", "Valor Final"]

CONTRATO_PATH: str = "contrato.txt"
PDF_PASSWORD: str = "12345"
