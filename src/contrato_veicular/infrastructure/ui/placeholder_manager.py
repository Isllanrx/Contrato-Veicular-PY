import customtkinter as ctk
from ...config.colors import ColorPalette


class PlaceholderManager:
    """Gerencia placeholders de campos do formulário."""
    @staticmethod
    def remove_placeholder(entry: ctk.CTkEntry, placeholder: str) -> None:
        """Remove placeholder de um campo de entrada."""
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.configure(text_color=ColorPalette.TEXT_PRIMARY)
    
    @staticmethod
    def restore_placeholder(entry: ctk.CTkEntry, placeholder: str) -> None:
        """Restaura placeholder em um campo vazio."""
        if not entry.get().strip() and placeholder:
            entry.insert(0, placeholder)
            entry.configure(text_color=ColorPalette.TEXT_MUTED)
