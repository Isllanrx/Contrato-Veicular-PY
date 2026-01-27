import re
import logging
from typing import Dict, TYPE_CHECKING, Optional
import customtkinter as ctk
from tkinter import messagebox, Frame
from tkinter import Event as TkEvent

if TYPE_CHECKING:
    from .components import UIComponentFactory
    from tkcalendar import DateEntry

try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR: bool = True
except ImportError:
    HAS_TKCALENDAR: bool = False
    DateEntry = None  # type: ignore

from ...config.colors import ColorPalette

logger = logging.getLogger(__name__)


class CalendarDialog:
    """Gerencia diálogos de seleção de data."""
    
    def __init__(
        self, 
        parent: ctk.CTk, 
        fonts: Dict[str, ctk.CTkFont], 
        ui_factory: "UIComponentFactory"
    ) -> None:
        """Inicializa o gerenciador de calendário."""
        self.parent = parent
        self.fonts = fonts
        self.ui_factory = ui_factory
    
    def open_calendar(self, entry: ctk.CTkEntry) -> None:
        """Abre o calendário para seleção de data."""
        if HAS_TKCALENDAR:
            self._open_calendar_tkcalendar(entry)
        else:
            self._open_calendar_simple(entry)
    
    def _open_calendar_tkcalendar(self, entry: ctk.CTkEntry) -> None:
        """Abre calendário usando tkcalendar."""
        calendar_window: ctk.CTkToplevel = self._create_calendar_window("350x380")
        main_frame: ctk.CTkFrame = self._create_calendar_main_frame(calendar_window)
        
        date_picker: Optional[DateEntry] = self._create_date_picker(main_frame)
        if date_picker is None:
            self._handle_calendar_error(calendar_window, entry)
            return
        
        self._setup_calendar_buttons(
            main_frame, calendar_window, entry, date_picker
        )
        calendar_window.after(100, lambda: date_picker.focus())
    
    def _create_calendar_window(self, size: str) -> ctk.CTkToplevel:
        """Cria e configura a janela do calendário."""
        calendar_window: ctk.CTkToplevel = ctk.CTkToplevel(self.parent)
        calendar_window.title("Selecione a Data")
        calendar_window.geometry(size)
        calendar_window.transient(self.parent)
        calendar_window.grab_set()
        calendar_window.configure(fg_color=ColorPalette.BG_DARK)
        
        calendar_window.update_idletasks()
        x: int = (calendar_window.winfo_screenwidth() // 2) - 175
        y: int = (calendar_window.winfo_screenheight() // 2) - 190
        calendar_window.geometry(f"{size}+{x}+{y}")
        
        return calendar_window
    
    def _create_calendar_main_frame(self, window: ctk.CTkToplevel) -> ctk.CTkFrame:
        """Cria o frame principal do calendário."""
        main_frame: ctk.CTkFrame = ctk.CTkFrame(
            window, fg_color=ColorPalette.BG_MEDIUM
        )
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        title_label: ctk.CTkLabel = ctk.CTkLabel(
            main_frame, text="Selecione a Data",
            font=self.fonts['section'], text_color=ColorPalette.ACCENT
        )
        title_label.pack(pady=(15, 20))
        
        return main_frame
    
    def _create_date_picker(self, parent: ctk.CTkFrame) -> Optional[DateEntry]:
        """Cria o widget DateEntry e retorna None em caso de erro."""
        calendar_container: ctk.CTkFrame = ctk.CTkFrame(
            parent, fg_color="transparent"
        )
        calendar_container.pack(pady=10)
        
        tk_frame: Frame = Frame(
            calendar_container, 
            bg=ColorPalette.BG_MEDIUM, 
            highlightthickness=0
        )
        tk_frame.pack()
        
        try:
            date_picker: DateEntry = DateEntry(
                tk_frame, width=18, background=ColorPalette.INPUT_BG,
                foreground=ColorPalette.TEXT_PRIMARY, 
                borderwidth=2, relief='solid',
                date_pattern='dd/mm/yyyy', locale='pt_BR',
                font=('Arial', 12)
            )
            date_picker.pack(pady=15)
            return date_picker
        except (AttributeError, ImportError, ValueError) as e:
            logger.warning(f"Erro ao criar DateEntry: {e}")
            return None
    
    def _handle_calendar_error(
        self, 
        calendar_window: ctk.CTkToplevel, 
        entry: ctk.CTkEntry
    ) -> None:
        error_label: ctk.CTkLabel = ctk.CTkLabel(
            calendar_window,
            text="Erro ao carregar calendário.\nUsando entrada manual...",
            font=self.fonts['label'],
            text_color=ColorPalette.ERROR
        )
        error_label.pack(pady=15)
        calendar_window.after(
            1000, 
            lambda: (calendar_window.destroy(), self._open_calendar_simple(entry))
        )
    
    def _setup_calendar_buttons(
        self,
        main_frame: ctk.CTkFrame,
        calendar_window: ctk.CTkToplevel,
        entry: ctk.CTkEntry,
        date_picker: DateEntry
    ) -> None:
        def confirm_date() -> None:
            self._apply_selected_date(entry, date_picker, calendar_window)
        
        btn_frame: ctk.CTkFrame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        confirm_btn: ctk.CTkButton = self.ui_factory.create_button(
            btn_frame, text="Confirmar", command=confirm_date
        )
        confirm_btn.pack(side="left", padx=8)
        
        cancel_btn: ctk.CTkButton = self.ui_factory.create_button(
            btn_frame, text="Cancelar", command=calendar_window.destroy,
            fg_color=ColorPalette.PRIMARY_DARK
        )
        cancel_btn.pack(side="left", padx=8)
    
    def _apply_selected_date(
        self,
        entry: ctk.CTkEntry,
        date_picker: DateEntry,
        calendar_window: ctk.CTkToplevel
    ) -> None:
        try:
            selected_date = date_picker.get_date()
            formatted_date: str = selected_date.strftime("%d/%m/%Y")
            entry.delete(0, "end")
            entry.insert(0, formatted_date)
            entry.configure(text_color=ColorPalette.TEXT_PRIMARY)
            calendar_window.destroy()
        except (AttributeError, ValueError) as e:
            logger.error(f"Erro ao selecionar data: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao selecionar data: {str(e)}")
    
    def _open_calendar_simple(self, entry: ctk.CTkEntry) -> None:
        """Abre diálogo simples para entrada de data"""
        date_window: ctk.CTkToplevel = self._create_simple_date_window()
        main_frame: ctk.CTkFrame = self._create_simple_date_main_frame(date_window)
        date_input: ctk.CTkEntry = self._create_simple_date_input(main_frame)
        
        self._setup_simple_date_events(
            date_input, main_frame, date_window, entry
        )
    
    def _create_simple_date_window(self) -> ctk.CTkToplevel:
        """Cria e configura a janela de entrada manual de data."""
        date_window: ctk.CTkToplevel = ctk.CTkToplevel(self.parent)
        date_window.title("Selecione a Data")
        date_window.geometry("380x260")
        date_window.transient(self.parent)
        date_window.grab_set()
        date_window.configure(fg_color=ColorPalette.BG_DARK)
        
        date_window.update_idletasks()
        x: int = (date_window.winfo_screenwidth() // 2) - 190
        y: int = (date_window.winfo_screenheight() // 2) - 130
        date_window.geometry(f"380x260+{x}+{y}")
        
        return date_window
    
    def _create_simple_date_main_frame(
        self, window: ctk.CTkToplevel
    ) -> ctk.CTkFrame:
        """Cria o frame principal do diálogo de entrada manual."""
        main_frame: ctk.CTkFrame = ctk.CTkFrame(
            window, fg_color=ColorPalette.BG_MEDIUM
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label: ctk.CTkLabel = ctk.CTkLabel(
            main_frame, text="Digite a Data",
            font=self.fonts['section'], text_color=ColorPalette.ACCENT
        )
        title_label.pack(pady=(10, 15))
        
        instruction: ctk.CTkLabel = ctk.CTkLabel(
            main_frame, text="Formato: DD/MM/AAAA",
            font=self.fonts['label'], text_color=ColorPalette.TEXT_SECONDARY
        )
        instruction.pack(pady=(0, 15))
        
        return main_frame
    
    def _create_simple_date_input(
        self, parent: ctk.CTkFrame
    ) -> ctk.CTkEntry:
        """Cria o campo de entrada de data."""
        date_input: ctk.CTkEntry = self.ui_factory.create_entry(
            parent, placeholder="DD/MM/AAAA", height=45
        )
        date_input.pack(pady=10, padx=30, fill="x")
        date_input.focus()
        return date_input
    
    def _setup_simple_date_events(
        self,
        date_input: ctk.CTkEntry,
        main_frame: ctk.CTkFrame,
        date_window: ctk.CTkToplevel,
        entry: ctk.CTkEntry
    ) -> None:
        date_input.bind("<KeyRelease>", lambda e: self._format_date_input(e, date_input))
        
        def confirm_date() -> None:
            self._validate_and_apply_simple_date(date_input, entry, date_window)
        
        btn_frame: ctk.CTkFrame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        confirm_btn: ctk.CTkButton = self.ui_factory.create_button(
            btn_frame, text="Confirmar", command=confirm_date
        )
        confirm_btn.pack(side="left", padx=8)
        
        cancel_btn: ctk.CTkButton = self.ui_factory.create_button(
            btn_frame, text="Cancelar", command=date_window.destroy,
            fg_color=ColorPalette.PRIMARY_DARK
        )
        cancel_btn.pack(side="left", padx=8)
        
        date_input.bind("<Return>", lambda e: confirm_date())
    
    def _format_date_input(self, event: TkEvent, date_input: ctk.CTkEntry) -> None:
        """Formata a entrada de data enquanto o usuário digita."""
        value: str = date_input.get().replace('/', '')
        formatted: str = self._format_date_string(value)
        
        date_input.delete(0, "end")
        date_input.insert(0, formatted)
    
    def _format_date_string(self, value: str) -> str:
        """Formata string de data conforme o comprimento."""
        if len(value) <= 2:
            return value
        elif len(value) <= 4:
            return f"{value[:2]}/{value[2:]}"
        elif len(value) <= 8:
            return f"{value[:2]}/{value[2:4]}/{value[4:8]}"
        return value
    
    def _validate_and_apply_simple_date(
        self,
        date_input: ctk.CTkEntry,
        entry: ctk.CTkEntry,
        date_window: ctk.CTkToplevel
    ) -> None:
        """Valida e aplica a data digitada manualmente."""
        date_str: str = date_input.get().strip()
        
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            entry.delete(0, "end")
            entry.insert(0, date_str)
            entry.configure(text_color=ColorPalette.TEXT_PRIMARY)
            date_window.destroy()
        else:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
            date_input.focus()
