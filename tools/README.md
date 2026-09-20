# tools

Scripts that build the submission documents from `docs/report-full.md`.
`docs/report-full.md` is itself generated from `docs/report-content.md` with the Clean Code
section inlined from `docs/clean-code-evidence.md`.

## PDF report

`md2pdf.py` renders the report Markdown into the submission PDF. The two UML class diagrams
are drawn as vector graphics by `umldiag.py` (layouts) on top of `umlpdf.py` (drawing
primitives), and embedded wherever a `[[UML:fm]]` or `[[UML:af]]` marker appears.

```bash
python3 -m venv venv && ./venv/bin/pip install reportlab
./venv/bin/python tools/md2pdf.py docs/report-full.md Assignment2_SE-2523_Tynyshtyk_Darkhan.pdf
```

## Word report

`md2docx.js` renders the same Markdown into a `.docx`, embedding the diagrams from
`docs/uml-factory-method.png` and `docs/uml-abstract-factory.png`.

```bash
npm install docx
node tools/md2docx.js docs/report-full.md Assignment2_SE-2523_Tynyshtyk_Darkhan.docx
```

If `docx` is installed somewhere other than the repository root, point the script at it:

```bash
DOCX_MODULES=/path/to/dir/containing/node_modules node tools/md2docx.js ...
```

## Regenerating the diagram images

The PNGs used by the Word report are exported from the same vector drawings as the PDF:

```bash
./venv/bin/python tools/export_uml_png.py
```
