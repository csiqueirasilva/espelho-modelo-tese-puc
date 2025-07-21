from __future__ import annotations
import os, shutil, subprocess, tempfile, uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Sequence
from tqdm.auto import tqdm

from .cls_parser import parse_margins
from .tex_parser import parse_macros
from .reference_builder import build_reference

PACKAGE_DIR = Path(__file__).parent
FILTER_DIR  = PACKAGE_DIR / "filters"

class PandocError(RuntimeError):
    pass

def _ensure_pandoc():
    if shutil.which("pandoc") is None:
        raise PandocError("Pandoc não encontrado no PATH.")

@contextmanager
def _cd(path: Path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)

def tex_to_docx(tex_file: Path, out_file: Path, *, cls_file: Optional[Path] = None,
                bibliography: Optional[Path] = None, extra_args: Optional[Sequence[str]] = None) -> Path:
    _ensure_pandoc()
    tex_file = tex_file.resolve()
    out_file = out_file.resolve()

    # --- construir reference.docx dinâmico
    tmp_dir = Path(tempfile.gettempdir()) / f"puc_ref_{uuid.uuid4().hex}"
    tmp_dir.mkdir()
    ref_doc = tmp_dir / "reference.docx"

    margins = parse_margins(cls_file or PACKAGE_DIR.parent / "ThesisPUC.cls")
    meta    = parse_macros(tex_file)
    build_reference(margins, ref_doc)

    args = ["--from=latex", "--to=docx", "--standalone", "--number-sections",
            f"--resource-path={tex_file.parent}",
            f"--reference-doc={ref_doc}",
            "--lua-filter", str(FILTER_DIR / "thesispuc-frontmatter.lua")]
    if bibliography:
        args += ["--citeproc", f"--bibliography={bibliography}"]
	if cls: args += ["--csl", str(csl)]
    if extra_args:
        args += list(extra_args)

    cmd = ["pandoc", tex_file.name, *args, "-o", str(out_file)]
    with _cd(tex_file.parent):
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as proc, \
             tqdm(desc="Pandoc", unit="line", colour="cyan", dynamic_ncols=True) as bar:
            for line in proc.stdout:
                bar.update(); tqdm.write(line.rstrip())
            proc.wait()
            if proc.returncode != 0:
                raise PandocError(f"Pandoc code {proc.returncode}")

    shutil.rmtree(tmp_dir)
    return out_file
