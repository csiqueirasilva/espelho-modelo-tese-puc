import re
from pathlib import Path
from typing import Dict

MACROS = {
    "autor":        r"\\autor\s*{([^}]*)}",
    "titulopt":     r"\\titulo\s*{([^}]*)}",
    "titulouk":     r"\\titulouk\s*{([^}]*)}",
    "departamento": r"\\departamento\s*{([^}]*)}",
    "programa":     r"\\programa\s*{([^}]*)}",
    "cidade":       r"\\cidade\s*{([^}]*)}",
    "ano":          r"\\ano\s*{([^}]*)}",
}

def parse_macros(tex_file: Path) -> Dict[str, str]:
    """Retorna dicionário {macro:conteúdo}."""
    text = tex_file.read_text(encoding="utf-8", errors="ignore")
    return {k: re.search(pat, text).group(1).strip()
            for k, pat in MACROS.items()
            if re.search(pat, text)}
