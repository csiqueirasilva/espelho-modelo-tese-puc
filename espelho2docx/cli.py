import click
from pathlib import Path
from .pandoc import tex_to_docx
from .form_builder import add_controls, fill_form

@click.group()
def cli():
    """Ferramentas para gerar .docx da tese PUC-Rio."""

@cli.command()
@click.argument("tex_file", type=click.Path(exists=True))
@click.option("--out", "-o", default="build/base.docx")
def convert(tex_file: str, out: str):
    """Converte .tex em .docx básico (sem controles)."""
    tex_to_docx(Path(tex_file), Path(out))

@cli.command()
@click.argument("docx_in", type=click.Path(exists=True))
@click.option("--out", "-o", default="build/form.docx")
def add_controls_cmd(docx_in, out):
    """Insere controles de formulário no DOCX."""
    add_controls(Path(docx_in), Path(out))

@cli.command()
@click.argument("docx_in", type=click.Path(exists=True))
@click.option("--data", "-d", required=True, type=click.Path())
@click.option("--out", "-o", default="build/preenchido.docx")
def fill(docx_in, data, out):
    """Preenche o formulário com um arquivo de dados YAML/JSON."""
    fill_form(Path(docx_in), Path(data), Path(out))
