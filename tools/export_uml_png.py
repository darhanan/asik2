"""Export the two UML class diagrams as high-resolution PNGs for the Word report."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pypdfium2 as pdfium
from reportlab.pdfgen import canvas

from umldiag import af_flowable, fm_flowable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 760.0
MARGIN = 10.0
SCALE = 3.2

for name, flow in (('uml-factory-method', fm_flowable), ('uml-abstract-factory', af_flowable)):
    flowable = flow(WIDTH)
    pdf_path = os.path.join(ROOT, 'docs', name + '.tmp.pdf')
    c = canvas.Canvas(pdf_path, pagesize=(WIDTH + 2 * MARGIN, flowable.height + 2 * MARGIN))
    flowable.drawOn(c, MARGIN, MARGIN)
    c.showPage()
    c.save()

    png_path = os.path.join(ROOT, 'docs', name + '.png')
    pdfium.PdfDocument(pdf_path)[0].render(scale=SCALE).to_pil().save(png_path)
    os.remove(pdf_path)
    print('wrote', png_path)
