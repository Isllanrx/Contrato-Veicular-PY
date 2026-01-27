import re
import logging
from typing import Dict, Optional

from ...domain.validators import FormValidator
from ...domain.entities import PLACEHOLDERS

logger = logging.getLogger(__name__)


class ValidateFormUseCase:
    """Caso de uso para validação de dados do formulário."""
    def __init__(self, validator: FormValidator) -> None:
        """Inicializa o caso de uso."""
        self.validator = validator
    
    def execute(self, raw_data: Dict[str, str]) -> Optional[Dict[str, str]]:
        """Valida e limpa os dados do formulário."""
        cleaned_data: Dict[str, str] = {}
        
        for field, value in raw_data.items():
            placeholder: str = PLACEHOLDERS.get(field, "")
            clean_value: str = "" if value == placeholder else value
            cleaned_value: str = self.validator.clean_numeric_field(clean_value, field)

            if not cleaned_value:
                logger.warning(f"Campo obrigatório vazio: {field}")
                return None
            
            cleaned_data[field] = cleaned_value
        
        logger.info("Dados do formulário validados com sucesso")
        return cleaned_data
