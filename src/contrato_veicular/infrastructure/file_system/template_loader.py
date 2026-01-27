import os
import sys
import logging
from typing import List

logger = logging.getLogger(__name__)

class TemplateLoader:
    """Carregador de templates de contrato."""
    
    @staticmethod
    def load_template(filename: str) -> str:
        """Carrega template do contrato"""
        possible_paths: List[str] = []
        
        if os.path.isabs(filename):
            possible_paths.append(filename)
        
        if getattr(sys, 'frozen', False):
            possible_paths.extend([
                os.path.join(sys._MEIPASS, filename),
                os.path.join(os.path.dirname(sys.executable), filename)
            ])
        
        current_file: str = os.path.abspath(__file__)
        project_root: str = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        )
        script_dir: str = os.path.dirname(current_file)
        
        possible_paths.extend([
            os.path.join(project_root, filename),
            os.path.join(os.path.abspath("."), filename),
            os.path.join(script_dir, filename)
        ])
        
        for filepath in possible_paths:
            try:
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()
                        logger.info(f"Template carregado de: {filepath}")
                        return content
            except (IOError, UnicodeDecodeError) as e:
                logger.warning(f"Erro ao ler {filepath}: {e}")
                continue
        
        error_msg = (f"Arquivo {filename} não encontrado nos seguintes locais:\n" + 
                    "\n".join(possible_paths))
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
