"""Gera reference.docx em tempo‑real, ajustando margens e estilos básicos."""
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def _cm_to_float(val: str) -> float:
    """Converte '2.5cm' → 2.5 (float)."""
    return float(val.rstrip("cm"))


def build_reference(margins: dict, out_path):
    doc = Document()

    # ── margens da seção principal ────────────────────────────────────────────
    sec = doc.sections[0]
    m = margins.get("text", {})
    sec.top_margin    = Cm(_cm_to_float(m.get("top",    "2.5cm")))
    sec.bottom_margin = Cm(_cm_to_float(m.get("bottom", "2.5cm")))
    sec.left_margin   = Cm(_cm_to_float(m.get("left",   "3cm")))
    sec.right_margin  = Cm(_cm_to_float(m.get("right",  "2cm")))

    styles = doc.styles

    # ── estilo Normal (Times 12, parágrafo justificado) ───────────────────────
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.first_line_indent = Cm(1.25)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ── Heading 1 (Arial 14 pt, centrado) ─────────────────────────────────────
    if "Heading 1" in styles:
        h1 = styles["Heading 1"]
    else:
        h1 = styles.add_style("Heading 1", 1)
    h1.font.name = "Arial"
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    caption = styles.add_style("Caption", 1)
    caption.base_style = normal
    caption.font.italic = True
    caption.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    heading2 = styles.add_style("Heading 2", 1)
    heading2.base_style = normal
    heading2.font.name = "Arial"
    heading2.font.bold = True
    heading2.font.size = Pt(12)

    heading3 = styles.add_style("Heading 3", 1)
    heading3.base_style = normal
    heading3.font.name = "Arial"
    heading3.font.size = Pt(12)
    heading3.font.bold = True

    doc.save(out_path)
