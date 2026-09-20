# tools

`md2pdf.py` renders the report Markdown into the submission PDF.

```bash
python3 -m venv venv && ./venv/bin/pip install reportlab
./venv/bin/python tools/md2pdf.py docs/report-full.md Assignment2_SE-2523_Tynyshtyk_Darkhan.pdf
```

`docs/report-full.md` is generated from `docs/report-content.md` with the Clean Code
section inlined from `docs/clean-code-evidence.md`.
