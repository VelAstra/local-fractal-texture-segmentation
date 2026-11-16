"""
pdf_engine.py - Two-pass NumberedCanvas and Document Builder for UGM Reports
Follows the official Universitas Gadjah Mada (UGM) thesis layout rules:
- Paper Size: A4
- Margins: Left 4.0 cm, Right 3.0 cm, Top 3.0 cm, Bottom 3.0 cm
- Two-pass NumberedCanvas for 'Halaman X dari Y'
- Running header and footer with academic rule lines (suppressed on page 1)
- Zero raw emojis, pure formal academic typography
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that accumulates page states to accurately calculate
    and display total page count in footers ('Halaman X dari Y').
    Automatically suppresses running headers and footers on the cover page (page 1).
    """

    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Exclude cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Dimensions & Margins
        # Left margin: 4.0 cm, Right margin: 3.0 cm
        # Width: A4[0] = 595.27 pt (~21.0 cm)
        # Height: A4[1] = 841.89 pt (~29.7 cm)
        x_left = 4.0 * cm
        x_right = A4[0] - 3.0 * cm
        y_header = A4[1] - 2.0 * cm
        y_header_line = A4[1] - 2.2 * cm
        y_footer_line = 2.2 * cm
        y_footer = 1.8 * cm

        # -----------------------------------------------------
        # Running Header
        # -----------------------------------------------------
        header_text = "Laporan Teknis Proyek Capstone Mandiri - DIKE FMIPA UGM"
        self.drawString(x_left, y_header, header_text)

        # Header rule line (UGM Gold accent)
        self.setStrokeColor(colors.HexColor("#B8860B"))
        self.setLineWidth(0.75)
        self.line(x_left, y_header_line, x_right, y_header_line)

        # -----------------------------------------------------
        # Running Footer
        # -----------------------------------------------------
        # Footer rule line (Border light)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(x_left, y_footer_line, x_right, y_footer_line)

        footer_text = "Departemen Ilmu Komputer dan Elektronika"
        page_str = f"Halaman {self._pageNumber} dari {page_count}"

        self.drawString(x_left, y_footer, footer_text)
        self.drawRightString(x_right, y_footer, page_str)

        self.restoreState()


class UGMReportBuilder:
    """
    Standardized PDF builder configured with UGM thesis margins and page size.
    """

    def __init__(self, output_path):
        self.output_path = output_path
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=4.0 * cm,
            rightMargin=3.0 * cm,
            topMargin=3.0 * cm,
            bottomMargin=3.0 * cm,
        )

    def build(self, story):
        """
        Compiles the story flowables into the PDF using NumberedCanvas.
        """
        self.doc.build(story, canvasmaker=NumberedCanvas)
