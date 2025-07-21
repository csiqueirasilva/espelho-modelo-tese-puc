# espelho-modelo-tese-puc

Gera **formulários / relatórios `.docx`** (Word) diretamente a partir do
template **LaTeX _ThesisPUC_** da PUC-Rio, mantendo capa, folha de rosto,
sumário, figuras e referências bibliográficas.

> **Objetivo**  
> Automatizar a criação de versões Word compatíveis com os
> requisitos de secretaria/biblioteca a partir do mesmo fonte LaTeX da tese.

---

## ✨ Funcionalidades

| Comando | Descrição |
|---------|-----------|
| `espelho2docx convert` | Converte `.tex` → `.docx` (faz download do Pandoc se faltar). |
| `espelho2docx add-controls` | Insere controles de formulário (checkbox, textbox) no DOCX. |
| `espelho2docx fill` | Preenche o formulário via YAML/JSON. |

Internamente:

* **Parser `.cls`** lê margens e fonte do `ThesisPUC.cls`.
* **Parser `.tex`** extrai macros (`\autor{}`, `\titulo{}`…).
* **reference builder** cria um `reference.docx` dinâmico com os estilos Word.
* **Filtro Lua** injeta front-matter e mapeia seções/títulos.
* **Python-docx** pode pós-processar capa, cabeçalho e rodapé, se desejado.

---

## 📦 Instalação

Pré-requisitos:

* Python ≥ 3.10
* [Pandoc ≥ 2.19](https://pandoc.org/install/) (no PATH)

```bash
### Clone o repositório
git clone https://github.com/SEU_USUARIO/espelho-modelo-tese-puc.git
cd espelho-modelo-tese-puc

### Instale dependências no ambiente virtual do Poetry
poetry install

## Uso

#### Converter o exemplo 'julio.tex' em DOCX
poetry run espelho2docx convert examples/julio/julio.tex \
  --out build/julio.docx \
  --bibliography examples/julio/julio.bib
```
