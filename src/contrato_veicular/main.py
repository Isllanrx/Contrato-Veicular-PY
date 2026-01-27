import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox


if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    src_path = current_file.parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    from contrato_veicular.config import setup_logging, logger
    from contrato_veicular.app import ContratoCarro
else:
    from .config import setup_logging, logger
    from .app import ContratoCarro

# Configuração inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
setup_logging()


def main() -> None:
    """Função principal para inicializar a aplicação."""
    try:
        root = ctk.CTk()
        app = ContratoCarro(root)
        
        root.update_idletasks()
        
        logger.info("Aplicação iniciada com sucesso")
        root.mainloop()
    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar aplicação: {e}", exc_info=True)
        messagebox.showerror("Erro Crítico", 
                           f"Erro ao iniciar aplicação:\n{str(e)}")


if __name__ == "__main__":
    main()
