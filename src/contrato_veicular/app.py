import os
import re
import webbrowser
import logging
from typing import Dict, List, Optional, Callable, Union, Any
import customtkinter as ctk
from tkinter import messagebox

from .config import (
    ColorPalette,
    COMPRADOR_FIELDS,
    VEICULO_FIELDS,
    PLACEHOLDERS,
    CONTRATO_PATH,
    PDF_PASSWORD,
    FORMATTED_FIELDS,
)
from .domain import FormatterService, ContractData
from .infrastructure import (
    PDFGenerator,
    TemplateLoader,
    UIComponentFactory,
    CalendarDialog,
    PlaceholderManager,
)
from .application import GenerateContractUseCase, ValidateFormUseCase

logger = logging.getLogger(__name__)


class ContratoCarro:
    """Classe principal para geração de contratos de veículos em PDF."""
    
    COMPRADOR_FIELDS: List[str] = COMPRADOR_FIELDS
    VEICULO_FIELDS: List[str] = VEICULO_FIELDS
    PLACEHOLDERS: Dict[str, str] = PLACEHOLDERS
    CONTRATO_PATH: str = CONTRATO_PATH
    PDF_PASSWORD: str = PDF_PASSWORD
    FORMATTED_FIELDS: List[str] = FORMATTED_FIELDS
    
    def __init__(self, root: ctk.CTk) -> None:
        """Inicializa a aplicação."""
        self.root = root
        self._configure_window()
        self._init_fonts()
        self._init_services()
        
        self.entries: Dict[str, Union[ctk.CTkEntry, ctk.CTkTextbox]] = {}
        self.create_widgets()
        
        self.root.update_idletasks()
        self.root.update()
    
    def _init_services(self) -> None:
        """Inicializa serviços auxiliares e casos de uso."""
        # Infrastructure
        self.ui_factory = UIComponentFactory(self.fonts)
        self.placeholder_manager = PlaceholderManager()
        self.calendar_dialog = CalendarDialog(self.root, self.fonts, self.ui_factory)
        pdf_generator = PDFGenerator()
        template_loader = TemplateLoader()
        
        # Application - Casos de uso
        from .domain.validators import FormValidator
        self.validate_form_use_case = ValidateFormUseCase(FormValidator())
        self.generate_contract_use_case = GenerateContractUseCase(
            pdf_generator, template_loader, self.PDF_PASSWORD
        )
    
    def _configure_window(self) -> None:
        """Configura propriedades da janela principal."""
        self.root.title("Contrato Paulo Veículos - Gerador Automatizado")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 700)
        self.root.resizable(True, True)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.configure(fg_color=ColorPalette.BG_DARK)
        
        self._setup_window_events()
    
    def _setup_window_events(self) -> None:
        """Configura eventos da janela para evitar bugs visuais de animação."""
        try:
            tk_widget = self.root.winfo_toplevel()
            
            self._updating = False
            
            # Handler para redimensionamento
            def on_configure(event: Optional[Any] = None) -> None:
                """Atualiza a janela ao redimensionar, evitando animações bugadas."""
                if event and event.widget == tk_widget and not self._updating:
                    self._updating = True
                    self.root.after_idle(lambda: self._finish_update())
            
            def _finish_update() -> None:
                """Finaliza atualização após redimensionamento."""
                self.root.update_idletasks()
                self._updating = False
            
            self._finish_update = _finish_update
            
            # Handler para maximização/restauração
            def on_map(event: Optional[Any] = None) -> None:
                """Atualiza quando a janela é exibida após minimizar/maximizar."""
                self.root.after(100, lambda: self.root.update_idletasks())
            
            # Aplica os bindings
            tk_widget.bind("<Configure>", on_configure, add=True)
            tk_widget.bind("<Map>", on_map, add=True)
            
        except Exception:
            pass
    
    def _init_fonts(self) -> None:
        """Inicializa configurações de fonte."""
        self.fonts = {
            'title': ctk.CTkFont(size=28, weight="bold"),
            'subtitle': ctk.CTkFont(size=14),
            'section': ctk.CTkFont(size=20, weight="bold"),
            'label': ctk.CTkFont(size=15, weight="bold"),
            'input': ctk.CTkFont(size=14),
            'button': ctk.CTkFont(size=17, weight="bold"),
            'footer': ctk.CTkFont(size=12)
        }
    
    def create_widgets(self) -> None:
        """Cria todos os widgets da interface."""
        self.create_header()
        self._create_scrollable_content()
        self.create_action_buttons()
        self.create_footer()
    
    def _create_scrollable_content(self) -> None:
        """Cria container principal com scroll."""
        self.central_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.central_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.central_container.grid_columnconfigure(0, weight=1)
        self.central_container.grid_rowconfigure(0, weight=1)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.central_container, fg_color="transparent", corner_radius=0
        )
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        
        self.main_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.main_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        self._create_section_frames()
    
    def _create_section_frames(self) -> None:
        """Cria frames para seções do formulário."""
        frame_config = {
            'corner_radius': 15,
            'fg_color': ColorPalette.BG_MEDIUM,
            'border_width': 1,
            'border_color': ColorPalette.ACCENT
        }
        
        self.comprador_frame = ctk.CTkFrame(self.main_container, **frame_config)
        self.comprador_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.comprador_frame.grid_columnconfigure(0, weight=1)
        self.comprador_frame.grid_rowconfigure(1, weight=1)
        
        self.veiculo_frame = ctk.CTkFrame(self.main_container, **frame_config)
        self.veiculo_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.veiculo_frame.grid_columnconfigure(0, weight=1)
        self.veiculo_frame.grid_rowconfigure(1, weight=1)
        
        self.create_section(self.comprador_frame, "Dados do Comprador", 
                          self.COMPRADOR_FIELDS, is_vehicle=False)
        self.create_section(self.veiculo_frame, "Dados do Veículo", 
                          self.VEICULO_FIELDS, is_vehicle=True)
    
    def create_header(self) -> None:
        """Cria o cabeçalho da aplicação."""
        header_frame = ctk.CTkFrame(
            self.root, height=110, corner_radius=0,
            fg_color=ColorPalette.BG_MEDIUM, border_width=0
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame, text="Contrato Paulo Veículos",
            font=self.fonts['title'], text_color=ColorPalette.ACCENT
        )
        title_label.pack(pady=(18, 8))
        
        subtitle_label = ctk.CTkLabel(
            header_frame, text="Sistema Automatizado de Geração de Contratos",
            font=self.fonts['subtitle'], text_color=ColorPalette.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 18))
    
    def create_action_buttons(self) -> None:
        """Cria os botões de ação principais."""
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        
        self.generate_button = self.ui_factory.create_button(
            button_frame, text="Gerar Contrato em PDF",
            command=self.generate_pdf,
            width=None, height=60,
            corner_radius=12, text_color="white"
        )
        self.generate_button.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
    
    def create_footer(self) -> None:
        """Cria o rodapé da aplicação."""
        footer_frame = ctk.CTkFrame(
            self.root, height=70, corner_radius=0,
            fg_color=ColorPalette.BG_DARK,
            border_width=1, border_color=ColorPalette.BG_MEDIUM
        )
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.pack_propagate(False)
        
        dev_container = ctk.CTkFrame(footer_frame, fg_color="transparent")
        dev_container.pack(side="right", padx=25, pady=20)
        
        developed_label = ctk.CTkLabel(
            dev_container, text="Desenvolvido por Isllan Toso",
            font=self.fonts['footer'], text_color=ColorPalette.TEXT_MUTED
        )
        developed_label.pack(side="right", padx=8)
        
        self.linkedin_button = self.ui_factory.create_button(
            dev_container, text="LinkedIn", command=self.open_linkedin,
            width=140, height=35,
            fg_color=ColorPalette.PRIMARY_DARK
        )
        self.linkedin_button.pack(side="right", padx=8)
    
    def create_section(self, parent_frame: ctk.CTkFrame, title: str, 
                      fields: List[str], is_vehicle: bool = False) -> None:
        """Cria uma seção de campos do formulário."""
        title_label = ctk.CTkLabel(
            parent_frame, text=title,
            font=self.fonts['section'], text_color=ColorPalette.ACCENT
        )
        title_label.grid(row=0, column=0, pady=(20, 25), padx=20, sticky="ew")
        
        inner_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        inner_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 20))
        inner_frame.grid_columnconfigure(0, weight=1)
        
        for idx, field in enumerate(fields):
            self._create_field(inner_frame, field, idx, is_vehicle)
    
    def _create_field(self, parent: ctk.CTkFrame, field: str, 
                     idx: int, is_vehicle: bool) -> None:
        """Cria um campo individual do formulário."""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.grid(row=idx, column=0, sticky="ew", pady=12)
        field_frame.grid_columnconfigure(1, weight=1)
        
        label = ctk.CTkLabel(
            field_frame, text=f"{field}:",
            font=self.fonts['label'], width=180, anchor="w",
            text_color=ColorPalette.TEXT_PRIMARY
        )
        label.grid(row=0, column=0, padx=(0, 15), sticky="w")
        
        if is_vehicle and field == "Condição":
            self.entries[field] = self._create_textbox(field_frame, field)
        elif field == "Dia de Venda":
            self.entries[field] = self._create_date_field(field_frame)
        else:
            self.entries[field] = self._create_entry(field_frame, field)
    
    def _create_entry(self, parent: ctk.CTkFrame, field: str) -> ctk.CTkEntry:
        """Cria campo de entrada padrão com placeholder."""
        placeholder = self.PLACEHOLDERS.get(field, "")
        entry = self.ui_factory.create_entry(parent, placeholder=placeholder)
        
        if placeholder:
            entry.bind("<FocusIn>", lambda e, f=field: self._on_entry_focus_in(f))
            entry.bind("<FocusOut>", lambda e, f=field: self._on_entry_focus_out(f))
        
        if field in self.FORMATTED_FIELDS:
            entry.bind("<KeyRelease>", lambda e, f=field: self._format_field(f))
        
        entry.grid(row=0, column=1, sticky="ew")
        return entry
    
    def _create_textbox(self, parent: ctk.CTkFrame, field: str) -> ctk.CTkTextbox:
        """Cria campo de texto multiline."""
        textbox = ctk.CTkTextbox(
            parent, height=120, font=self.fonts['input'],
            corner_radius=10, border_width=1,
            border_color=ColorPalette.BORDER,
            fg_color=ColorPalette.INPUT_BG,
            text_color=ColorPalette.TEXT_PRIMARY
        )
        placeholder = self.PLACEHOLDERS.get(field, "")
        if placeholder:
            textbox.insert("1.0", placeholder)
            textbox.configure(text_color=ColorPalette.TEXT_MUTED)
            textbox.bind("<FocusIn>", lambda e, f=field: self._on_textbox_focus_in(f))
            textbox.bind("<FocusOut>", lambda e, f=field: self._on_textbox_focus_out(f))
        textbox.grid(row=0, column=1, sticky="ew")
        return textbox
    
    def _create_date_field(self, parent: ctk.CTkFrame) -> ctk.CTkEntry:
        """Cria campo de data com botão de calendário."""
        date_container = ctk.CTkFrame(parent, fg_color=ColorPalette.INPUT_BG, corner_radius=10)
        date_container.grid(row=0, column=1, sticky="ew")
        date_container.grid_columnconfigure(0, weight=1)
        
        placeholder = self.PLACEHOLDERS.get("Dia de Venda", "")
        date_entry = self.ui_factory.create_entry(
            date_container, placeholder=placeholder, height=42
        )
        date_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        calendar_btn = self.ui_factory.create_button(
            date_container, text="Calendário", width=50, height=42,
            command=lambda: self.calendar_dialog.open_calendar(date_entry)
        )
        calendar_btn.grid(row=0, column=1, sticky="ew")
        
        date_entry.bind("<FocusIn>", lambda e, de=date_entry: self._on_date_focus_in(de))
        date_entry.bind("<FocusOut>", lambda e, de=date_entry: self._on_date_focus_out(de))
        return date_entry
    
    def _on_entry_focus_in(self, field: str) -> None:
        """Remove placeholder quando o campo recebe foco."""
        entry = self.entries[field]
        placeholder = self.PLACEHOLDERS.get(field, "")
        self.placeholder_manager.remove_placeholder(entry, placeholder)
    
    def _on_entry_focus_out(self, field: str) -> None:
        """Adiciona placeholder se o campo estiver vazio."""
        entry = self.entries[field]
        placeholder = self.PLACEHOLDERS.get(field, "")
        self.placeholder_manager.restore_placeholder(entry, placeholder)
    
    def _on_textbox_focus_in(self, field: str) -> None:
        """Remove placeholder do textbox quando recebe foco."""
        textbox = self.entries[field]
        placeholder = self.PLACEHOLDERS.get(field, "")
        if textbox.get("1.0", "end-1c") == placeholder:
            textbox.delete("1.0", "end")
            textbox.configure(text_color=ColorPalette.TEXT_PRIMARY)
    
    def _on_textbox_focus_out(self, field: str) -> None:
        """Adiciona placeholder no textbox se estiver vazio."""
        textbox = self.entries[field]
        placeholder = self.PLACEHOLDERS.get(field, "")
        if not textbox.get("1.0", "end-1c").strip() and placeholder:
            textbox.insert("1.0", placeholder)
            textbox.configure(text_color=ColorPalette.TEXT_MUTED)
    
    def _on_date_focus_in(self, entry: ctk.CTkEntry) -> None:
        """Remove placeholder do campo de data."""
        placeholder = self.PLACEHOLDERS.get("Dia de Venda", "")
        self.placeholder_manager.remove_placeholder(entry, placeholder)
    
    def _on_date_focus_out(self, entry: ctk.CTkEntry) -> None:
        """Adiciona placeholder no campo de data se estiver vazio"""
        placeholder = self.PLACEHOLDERS.get("Dia de Venda", "")
        self.placeholder_manager.restore_placeholder(entry, placeholder)
    
    def _format_field(self, field: str) -> None:
        """Formata automaticamente os campos conforme o tipo."""
        entry = self.entries[field]
        current_value = entry.get()
        if current_value == self.PLACEHOLDERS.get(field, ""):
            return
        
        numbers = re.sub(r'\D', '', current_value)
        formatters: Dict[str, Callable[[str], str]] = {
            "CPF": lambda n: FormatterService.format_cpf(n) if len(n) <= 11 else current_value,
            "Telefone": lambda n: FormatterService.format_phone(n) if len(n) <= 11 else current_value,
            "Valor Final": lambda n: FormatterService.format_currency(n) if n else current_value
        }
        
        if field in formatters:
            formatted = formatters[field](numbers)
            if formatted != current_value:
                entry.delete(0, "end")
                entry.insert(0, formatted)
                entry.configure(text_color=ColorPalette.TEXT_PRIMARY)
    
    def generate_pdf(self) -> None:
        """Orquestra a geração do PDF do contrato."""
        validated_data: Optional[Dict[str, str]] = self._validate_form_data()
        if not validated_data:
            return
        
        self._disable_generate_button()
        
        try:
            contract_data: ContractData = self._create_contract_data(validated_data)
            pdf_filename: str = self._execute_contract_generation(contract_data)
            self._show_success_message(pdf_filename)
        except (ValueError, FileNotFoundError) as e:
            self._handle_generation_error(e)
        except Exception as e:
            self._handle_generation_error(e)
        finally:
            self._enable_generate_button()
    
    def _validate_form_data(self) -> Optional[Dict[str, str]]:
        """Valida dados do formulário e retorna dados validados ou None."""
        raw_data: Dict[str, str] = self._get_raw_form_data()
        if not raw_data:
            self.show_error("Por favor, preencha todos os campos antes de gerar o contrato.")
            return None
        
        validated_data: Optional[Dict[str, str]] = self.validate_form_use_case.execute(raw_data)
        if not validated_data:
            self.show_error("Por favor, preencha todos os campos antes de gerar o contrato.")
            return None
        
        return validated_data
    
    def _create_contract_data(self, validated_data: Dict[str, str]) -> ContractData:
        """Cria entidade ContractData a partir dos dados validados."""
        comprador_data: Dict[str, str] = {
            k: v for k, v in validated_data.items() 
            if k in self.COMPRADOR_FIELDS
        }
        veiculo_data: Dict[str, str] = {
            k: v for k, v in validated_data.items() 
            if k in self.VEICULO_FIELDS
        }
        return ContractData(comprador_data, veiculo_data)
    
    def _execute_contract_generation(self, contract_data: ContractData) -> str:
        """Executa a geração do contrato usando o caso de uso."""
        pdf_filename: str = self.generate_contract_use_case.execute(
            contract_data, self.CONTRATO_PATH
        )
        logger.info(f"PDF gerado com sucesso: {pdf_filename}")
        return pdf_filename
    
    def _show_success_message(self, pdf_filename: str) -> None:
        """Exibe mensagem de sucesso após geração do PDF."""
        absolute_path: str = os.path.abspath(pdf_filename)
        filename_only: str = os.path.basename(pdf_filename)
        
        messagebox.showinfo(
            "PDF Gerado com Sucesso!", 
            f"Contrato gerado com sucesso!\n\n"
            f"Arquivo: {filename_only}\n"
            f"Pasta: contratos/\n"
            f"Local completo: {absolute_path}\n\n"
            f"A senha do PDF é: {self.PDF_PASSWORD}"
        )
    
    def _handle_generation_error(self, error: Exception) -> None:
        """Trata erros durante a geração do PDF."""
        logger.error(f"Erro ao gerar PDF: {error}", exc_info=True)
        self.show_error(f"Erro ao gerar o PDF:\n{str(error)}")
    
    def _disable_generate_button(self) -> None:
        """Desabilita o botão de geração durante o processamento."""
        self.generate_button.configure(state="disabled", text="Gerando PDF...")
        self.root.update()
    
    def _enable_generate_button(self) -> None:
        """Reabilita o botão de geração após o processamento."""
        self.generate_button.configure(state="normal", text="Gerar Contrato em PDF")
        self.root.update()
    
    def _get_raw_form_data(self) -> Dict[str, str]:
        """Obtém dados brutos do formulário"""
        return {
            field: (
                widget.get("1.0", "end").strip() 
                if field == "Condição" 
                else widget.get().strip()
            )
            for field, widget in self.entries.items()
        }

    def show_error(self, message: str) -> None:
        """Exibe uma mensagem de erro ao usuário."""
        logger.error(f"Erro exibido ao usuário: {message}")
        messagebox.showerror("Erro", message)

    def open_linkedin(self) -> None:
        """Abre o perfil do LinkedIn"""
        try:
            webbrowser.open("https://br.linkedin.com/in/isllantoso")
            logger.info("LinkedIn aberto no navegador")
        except Exception as e:
            logger.error(f"Erro ao abrir LinkedIn: {e}", exc_info=True)
            self.show_error(f"Erro ao abrir LinkedIn: {str(e)}")
