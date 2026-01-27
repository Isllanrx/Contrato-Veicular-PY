from typing import Dict

class FormatterService:
    """Serviço de formatação de dados"""
    
    @staticmethod
    def format_cpf(numbers: str) -> str:
        """Formata CPF no padrão brasileiro"""
        if not numbers:
            return ""
        length_formats: Dict[int, str] = {
            3: numbers,
            6: f"{numbers[:3]}.{numbers[3:]}",
            9: f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:]}"
        }
        if len(numbers) in length_formats:
            return length_formats[len(numbers)]
        return f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:9]}-{numbers[9:11]}"
    
    @staticmethod
    def format_phone(numbers: str) -> str:
        """Formata telefone no padrão brasileiro"""
        if not numbers:
            return ""
        length_formats: Dict[int, str] = {
            2: f"({numbers}",
            6: f"({numbers[:2]}) {numbers[2:]}",
            10: f"({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}"
        }
        if len(numbers) in length_formats:
            return length_formats[len(numbers)]
        return f"({numbers[:2]}) {numbers[2:7]}-{numbers[7:11]}"
    
    @staticmethod
    def format_currency(numbers: str) -> str:
        """Formata valor monetário no padrão brasileiro"""
        if not numbers:
            return "R$ 0,00"
        
        numbers = numbers.lstrip('0') or '0'
        
        if len(numbers) == 1:
            return f"R$ 0,0{numbers}"
        if len(numbers) == 2:
            return f"R$ 0,{numbers}"
        
        reais_str: str = numbers[:-2] or '0'
        centavos: str = numbers[-2:]
        reais_int: int = int(reais_str)
        reais_formatted: str = f"{reais_int:,}".replace(',', '.')
        
        return f"R$ {reais_formatted},{centavos}"
