import os
import re
import textwrap
import logging
from typing import Dict

from ...domain.entities import ContractData
from ...infrastructure.pdf import PDFGenerator
from ...infrastructure.file_system import TemplateLoader

logger = logging.getLogger(__name__)


class GenerateContractUseCase:
    """Caso de uso para geração de contrato em PDF."""
    def __init__(
        self,
        pdf_generator: PDFGenerator,
        template_loader: TemplateLoader,
        pdf_password: str
    ) -> None:
        self.pdf_generator = pdf_generator
        self.template_loader = template_loader
        self.pdf_password = pdf_password
    
    def execute(self, contract_data: ContractData, template_path: str) -> str:
        """Executa a geração do contrato."""
        template = self.template_loader.load_template(template_path)
        
        contract_text = self._generate_contract_text(template, contract_data.to_dict())
        
        pdf_filename = self._generate_filename(contract_data)
        
        self.pdf_generator.create_pdf(pdf_filename, contract_text)
        
        self.pdf_generator.add_password(pdf_filename, pdf_filename, self.pdf_password)
        
        logger.info(f"Contrato gerado com sucesso: {pdf_filename}")
        return pdf_filename
    
    def _generate_contract_text(self, template: str, data: Dict[str, str]) -> str:
        """Gera o texto do contrato formatado."""
        if not template:
            raise ValueError("Template de contrato não carregado.")
        
        try:
            contract_text = textwrap.dedent(template.format(**data))
            logger.debug("Texto do contrato gerado com sucesso")
            return contract_text
        except KeyError as e:
            error_msg = f"Chave não encontrada no template: {e}"
            logger.error(error_msg, exc_info=True)
            raise ValueError(error_msg)
    
    def _generate_filename(self, contract_data: ContractData) -> str:
        """Gera o caminho completo do arquivo PDF na pasta contratos."""
        contracts_dir: str = self._ensure_contracts_directory()
        
        vehicle_name: str = contract_data.veiculo_data.get("Veículo", "Veiculo")
        vehicle_plate: str = contract_data.veiculo_data.get("Placa do Carro", "Placa")
        
        # Sanitiza nomes removendo caracteres inválidos
        def sanitize_filename(name: str) -> str:
            sanitized: str = re.sub(r'[<>:"/\\|?*]', '', name)
            sanitized = re.sub(r'\s+', '_', sanitized)
            sanitized = re.sub(r'_+', '_', sanitized)
            sanitized = sanitized.strip('_')
            return sanitized if sanitized else "Veiculo"
        
        safe_vehicle_name: str = sanitize_filename(vehicle_name)
        safe_vehicle_plate: str = sanitize_filename(vehicle_plate)
        filename: str = f"{safe_vehicle_name}_{safe_vehicle_plate}.pdf"
        
        full_path: str = os.path.join(contracts_dir, filename)
        logger.debug(f"Caminho do arquivo gerado: {full_path}")
        return full_path
    
    def _ensure_contracts_directory(self) -> str:
        """Garante que a pasta contratos existe na raiz do projeto e retorna o caminho."""
        current_file: str = os.path.abspath(__file__)
        project_root: str = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
        )
        contracts_dir: str = os.path.join(project_root, "contratos")
        
        os.makedirs(contracts_dir, exist_ok=True)
        logger.debug(f"Pasta contratos: {contracts_dir}")
        
        return contracts_dir
