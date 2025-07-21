"""Extração de margens & layout do ThesisPUC.cls"""
from pathlib import Path
import re
from typing import Dict

_MARGIN = re.compile(r"\\puc@setallmargins\{(?P<target>\\w+)\}\{(?P<top>[\\d.]+cm)\}\{(?P<bottom>[\\d.]+cm)\}\{(?P<left>[\\d.]+cm)\}\{(?P<right>[\\d.]+cm)\}")


def parse_margins(cls_path: Path) -> Dict[str, Dict[str, str]]:
    """Retorna dict com margens definidas no .cls."""
    margins: Dict[str, Dict[str, str]] = {}
    text = cls_path.read_text(encoding="utf-8", errors="ignore")
    for m in _MARGIN.finditer(text):
        margins[m.group("target")] = {
            "top": m.group("top"),
            "bottom": m.group("bottom"),
            "left": m.group("left"),
            "right": m.group("right"),
        }
    return margins
