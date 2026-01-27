from typing import Dict, Optional, Callable
import customtkinter as ctk
from ...config.colors import ColorPalette


class UIComponentFactory:
    """Factory para criação de componentes"""
    def __init__(self, fonts: Dict[str, ctk.CTkFont]) -> None:
        """Inicializa o factory com configurações de fonte."""
        self.fonts = fonts
    
    def create_button(self, parent: ctk.CTkFrame, text: str, command: Callable,
                     width: Optional[int] = 130, height: int = 40, 
                     fg_color: str = ColorPalette.ACCENT,
                     hover_color: str = ColorPalette.PRIMARY_LIGHT,
                     **kwargs) -> ctk.CTkButton:

        defaults = {
            'font': self.fonts.get('button', self.fonts.get('label')),
            'corner_radius': 10,
            'border_width': 0
        }
        defaults.update(kwargs)
        
        button_kwargs = {
            'text': text,
            'command': command,
            'height': height,
            'fg_color': fg_color,
            'hover_color': hover_color,
            **defaults
        }
        
        if width is not None and width != 0:
            button_kwargs['width'] = width
        
        return ctk.CTkButton(parent, **button_kwargs)
    
    def create_entry(self, parent: ctk.CTkFrame, placeholder: str = "",
                    height: int = 42, **kwargs) -> ctk.CTkEntry:
        defaults = {
            'font': self.fonts.get('input'),
            'corner_radius': 10,
            'border_width': 1,
            'border_color': ColorPalette.BORDER,
            'fg_color': ColorPalette.INPUT_BG,
            'text_color': ColorPalette.TEXT_PRIMARY,
            'height': height
        }
        defaults.update(kwargs)
        
        entry = ctk.CTkEntry(parent, **defaults)
        if placeholder:
            entry.insert(0, placeholder)
            entry.configure(text_color=ColorPalette.TEXT_MUTED)
        
        return entry
