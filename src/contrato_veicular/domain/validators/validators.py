import re
from typing import Dict, Optional, Tuple


class FormValidator:
    """Validador de dados do formulário."""
    @staticmethod
    def clean_numeric_field(value: str, field_name: str) -> str:
        """Remove formatação de campos numéricos."""
        if field_name in ["CPF", "RG", "Telefone"]:
            return re.sub(r'\D', '', value)
        elif field_name == "Valor Final":
            return re.sub(r'[R$\s.]', '', value).replace(',', '.')
        return value
    
    @staticmethod
    def validate_form_data(data: Dict[str, str]) -> Tuple[bool, Optional[str]]:
        """Valida se todos os campos obrigatórios estão preenchidos."""
        if not data:
            return False, "Nenhum dado fornecido"
        
        for field, value in data.items():
            if not value or not value.strip():
                return False, f"Campo obrigatório vazio: {field}"
        
        return True, None
    
    @staticmethod
    def is_placeholder(value: str, placeholder: str) -> bool:
        """Verifica se o valor é um placeholder."""
        return value == placeholder
