"""Coleta de metadados das macros no arquivo .tex principal."""
from pathlib import Path
import re
from typing import Dict

MACROS = {
    "autor":        r"\\autor\s*{([^}]*)}",
    "titulo":       r"\\titulo\s*{([^}]*)}",
    "subtitulo":    r"\\subtitulo\s*{([^}]*)}",
    "dia":          r"\\dia\s*{([^}]*)}",
    "mes":          r"\\mes\s*{([^}]*)}",
    "ano":          r"\\ano\s*{([^}]*)}",
    "cidade":       r"\\cidade\s*{([^}]*)}",
    "agradecimentos": r"\\agradecimentos\s*{([^}]*)}",
}


def parse_macros(tex_file: Path) -> Dict[str, str]:
    text = tex_file.read_text(encoding="utf-8", errors="ignore")
    return {k: re.search(pat, text).group(1).strip() for k, pat in MACROS.items() if re.search(pat, text)}
