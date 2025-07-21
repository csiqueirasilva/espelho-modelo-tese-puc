"""
espelho2docx.form_builder
-------------------------
Insere e preenche *Content Controls* no DOCX usando **docx-form**.

Dependências:
    • python-docx      (manipular parágrafos, tabelas, etc.)
    • docx-form        (editar content controls) :contentReference[oaicite:1]{index=1}
    • ruamel.yaml ou PyYAML (para YAML); json (built-in)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml
from docx_form import DocxForm


def add_controls(
    src_docx: Path,
    dst_docx: Path,
    *,
    tag_map: Mapping[str, str] | None = None,
) -> Path:
    """
    Cria controles de formulário definidos em ``tag_map``.

    Se ``tag_map`` for None, apenas clona o arquivo.
    A chave é o *placeholder* a buscar; o valor é o *tag* do controle.
    """
    doc = DocxForm(str(src_docx))

    if tag_map:
        # Percorre todos os parágrafos à procura do placeholder
        # e transforma em PlainTextContentControl.
        from docx_form.content_controls import PlainTextContentControl

        for paragraph in doc._document.paragraphs:  # type: ignore
            for placeholder, tag in tag_map.items():
                if placeholder in paragraph.text:
                    # Substitui por controle
                    paragraph.text = ""
                    cc = PlainTextContentControl.new(tag)
                    cc.set_text(placeholder)
                    paragraph._p.append(cc._element)  # low-level add

    doc.save(str(dst_docx))
    return dst_docx


def fill_form(template_docx: Path, data_file: Path, out_docx: Path) -> Path:
    """
    Preenche *todos* os controles cujos tags existam no YAML/JSON.

    Exemplo YAML
    ------------
    autor: "Julio César Álvarez Iglesias"
    titulo: "Microscopia Digital ..."
    data_defesa: "2012-08-09"
    """
    mapping: dict[str, Any] = _load_mapping(data_file)

    doc = DocxForm(str(template_docx))

    for ctrl in doc.content_control_forms_and_form_fields:
        tag = getattr(ctrl, "tag", None) or getattr(ctrl, "_tag", None)
        if tag and tag in mapping:
            _set_value(ctrl, mapping[tag])

    doc.save(str(out_docx))
    return out_docx


def _load_mapping(path: Path) -> dict[str, Any]:
    if path.suffix.lower() in {".yml", ".yaml"}:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    raise ValueError("Arquivo de dados deve ser YAML ou JSON")


def _set_value(control, value: Any) -> None:
    """
    Altera texto ou checkbox dependendo do tipo de controle.
    """
    from docx_form.content_controls import (
        CheckBoxContentControl,
        PlainTextContentControl,
        RichTextContentControl,
    )

    if isinstance(control, (PlainTextContentControl, RichTextContentControl)):
        control.set_text(str(value))
    elif isinstance(control, CheckBoxContentControl):
        control.set_check_box(bool(value))
