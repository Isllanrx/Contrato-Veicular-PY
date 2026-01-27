import logging

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
