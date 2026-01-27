import os
import textwrap
import logging
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Gerador de arquivos PDF."""
    @staticmethod
    def create_pdf(filename: str, contract_text: str) -> None:
        """Cria arquivo PDF com o conteúdo do contrato."""
        try:
            if "Erro" in contract_text:
                raise ValueError(contract_text)
            
            pdf_canvas: canvas.Canvas = PDFGenerator._create_canvas(filename)
            PDFGenerator._render_text(pdf_canvas, contract_text)
            pdf_canvas.save()
            logger.info(f"PDF criado com sucesso: {filename}")
        except (ValueError, IOError) as e:
            logger.error(f"Erro ao criar PDF {filename}: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar PDF {filename}: {e}", exc_info=True)
            raise Exception(f"Erro ao criar arquivo PDF: {str(e)}")
    
    @staticmethod
    def _create_canvas(filename: str) -> canvas.Canvas:
        """Cria e configura o canvas do PDF."""
        pdf_canvas: canvas.Canvas = canvas.Canvas(filename, pagesize=A4)
        pdf_canvas.setFont("Helvetica", 9)
        return pdf_canvas
    
    @staticmethod
    def _render_text(pdf_canvas: canvas.Canvas, contract_text: str) -> None:
        """Renderiza o texto do contrato no canvas."""
        width: float
        height: float
        width, height = A4
        
        y_position: float = height - 40
        line_height: int = 12
        min_y: int = 40

        for paragraph in contract_text.split('\n\n'):
            if not paragraph.strip():
                y_position -= line_height
                continue
            
            y_position = PDFGenerator._render_paragraph(
                pdf_canvas, paragraph, y_position, line_height, min_y, height
            )
            y_position -= line_height
    
    @staticmethod
    def _render_paragraph(
        pdf_canvas: canvas.Canvas,
        paragraph: str,
        y_position: float,
        line_height: int,
        min_y: int,
        page_height: float
    ) -> float:
        current_y: float = y_position
        
        for line in textwrap.wrap(paragraph, width=100):
            current_y = PDFGenerator._draw_line_if_fits(
                pdf_canvas, line, current_y, line_height, min_y, page_height
            )
        
        return current_y
    
    @staticmethod
    def _draw_line_if_fits(
        pdf_canvas: canvas.Canvas,
        line: str,
        y_position: float,
        line_height: int,
        min_y: int,
        page_height: float
    ) -> float:
        if y_position < min_y:
            PDFGenerator._new_page(pdf_canvas)
            y_position = page_height - 40
        
        pdf_canvas.drawString(30, y_position, line)
        return y_position - line_height
    
    @staticmethod
    def _new_page(pdf_canvas: canvas.Canvas) -> None:
        """Cria uma nova página no PDF."""
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica", 9)
    
    @staticmethod
    def add_password(input_pdf: str, output_pdf: str, password: str) -> None:
        """Adiciona senha de proteção ao PDF."""
        try:
            if not os.path.exists(input_pdf):
                raise FileNotFoundError(f"Arquivo PDF não encontrado: {input_pdf}")
            
            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(output_pdf, 'wb') as f:
                writer.write(f)

            logger.info(f"Senha adicionada ao PDF: {output_pdf}")
        except FileNotFoundError as e:
            logger.error(f"Arquivo não encontrado: {e}", exc_info=True)
            raise
        except IOError as e:
            logger.error(f"Erro de IO ao proteger PDF: {e}", exc_info=True)
            raise Exception(f"Erro ao adicionar senha ao PDF: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao proteger PDF: {e}", exc_info=True)
            raise Exception(f"Erro ao adicionar senha ao PDF: {str(e)}")
