"""Render the assignment report Markdown into a formatted PDF."""
import re
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, KeepTogether,
                                ListFlowable, ListItem, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)

SRC, DST = sys.argv[1], sys.argv[2]

ss = getSampleStyleSheet()
BODY = ParagraphStyle('Body', parent=ss['Normal'], fontName='Helvetica', fontSize=9.5,
                      leading=13.5, alignment=TA_JUSTIFY, spaceAfter=6)
H1 = ParagraphStyle('H1', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=16,
                    leading=20, spaceBefore=4, spaceAfter=10, textColor=colors.HexColor('#12243a'))
H2 = ParagraphStyle('H2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=12.5,
                    leading=16, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#1b3a5c'))
H3 = ParagraphStyle('H3', parent=ss['Heading3'], fontName='Helvetica-Bold', fontSize=10.5,
                    leading=14, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#24506e'))
CODE = ParagraphStyle('Code', parent=ss['Code'], fontName='Courier', fontSize=7.6, leading=9.8,
                      textColor=colors.HexColor('#1a1a1a'), backColor=colors.HexColor('#f4f5f7'),
                      borderPadding=5, leftIndent=3, spaceBefore=4, spaceAfter=8)
QUOTE = ParagraphStyle('Quote', parent=BODY, leftIndent=12, textColor=colors.HexColor('#4a4a4a'),
                       fontName='Helvetica-Oblique', borderPadding=0)
CELL = ParagraphStyle('Cell', parent=BODY, fontSize=7.6, leading=10, alignment=0, spaceAfter=0)
CELLH = ParagraphStyle('CellH', parent=CELL, fontName='Helvetica-Bold',
                       textColor=colors.white)


def inline(text):
    """Convert inline markdown (**bold**, *italic*, `code`) to reportlab markup."""
    out, parts = [], re.split(r'(`[^`]+`)', text)
    for part in parts:
        if part.startswith('`') and part.endswith('`') and len(part) > 1:
            out.append('<font face="Courier" size="8.5" color="#9c2a2a">'
                       + escape(part[1:-1]) + '</font>')
        else:
            s = escape(part).replace('&lt;br&gt;', '<br/>')
            s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
            s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
            out.append(s)
    return ''.join(out)


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def make_table(rows, width):
    header, body = rows[0], rows[1:]
    ncol = len(header)
    data = [[Paragraph(inline(c), CELLH) for c in header]]
    for r in body:
        r = (r + [''] * ncol)[:ncol]
        data.append([Paragraph(inline(c), CELL) for c in r])

    # Give wide free-text columns more room than short label columns.
    def longest_word(cell):
        plain = re.sub(r'[`*]', '', cell).replace('<br>', ' ')
        return max((len(w) for w in plain.split()), default=0)

    weights, minima = [], []
    for i in range(ncol):
        col = [r[i] if i < len(r) else '' for r in rows]
        weights.append(max(max((len(c) for c in col), default=0), 6))
        # Reserve room for the widest single word plus cell padding.
        minima.append(max(longest_word(c) for c in col) * 5.0 + 10)

    total = sum(weights)
    col_widths = [max(width * w / total, m) for w, m in zip(weights, minima)]
    # Shrink only the columns that still have slack above their minimum.
    overflow = sum(col_widths) - width
    if overflow > 0:
        slack = [w - m for w, m in zip(col_widths, minima)]
        pool = sum(slack)
        if pool > 0:
            take = min(overflow, pool)
            col_widths = [w - take * (sl / pool) for w, sl in zip(col_widths, slack)]
        else:
            scale = width / sum(col_widths)
            col_widths = [w * scale for w in col_widths]
    elif overflow < 0:
        col_widths = [w - overflow * -1 * 0 for w in col_widths]
        scale = width / sum(col_widths)
        col_widths = [w * scale for w in col_widths]

    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1b3a5c')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b9c3cd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#f4f6f8')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


lines = open(SRC, encoding='utf-8').read().split('\n')
story, i = [], 0
FRAME_W = A4[0] - 3.4 * cm

while i < len(lines):
    line = lines[i]

    if line.startswith('```'):
        i += 1
        buf = []
        while i < len(lines) and not lines[i].startswith('```'):
            buf.append(lines[i])
            i += 1
        i += 1
        story.append(Preformatted('\n'.join(buf), CODE))
        continue

    if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|?\s*$', lines[i + 1]):
        rows = [split_row(line)]
        i += 2
        while i < len(lines) and lines[i].startswith('|'):
            rows.append(split_row(lines[i]))
            i += 1
        story.append(make_table(rows, FRAME_W))
        story.append(Spacer(1, 8))
        continue

    if re.match(r'^---+\s*$', line):
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width='100%', thickness=0.6,
                                color=colors.HexColor('#c2ccd6'), spaceAfter=8))
        i += 1
        continue

    m = re.match(r'^(#{1,3})\s+(.*)$', line)
    if m:
        style = {1: H1, 2: H2, 3: H3}[len(m.group(1))]
        story.append(Paragraph(inline(m.group(2)), style))
        i += 1
        continue

    if line.startswith('> '):
        buf = []
        while i < len(lines) and lines[i].startswith('>'):
            buf.append(lines[i].lstrip('>').strip())
            i += 1
        story.append(Paragraph(inline(' '.join(buf)), QUOTE))
        story.append(Spacer(1, 4))
        continue

    if re.match(r'^\s*[-*]\s+|^\s*\d+\.\s+', line):
        items, ordered = [], bool(re.match(r'^\s*\d+\.\s+', line))
        while i < len(lines) and re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]):
            txt = re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i])
            i += 1
            while i < len(lines) and lines[i].strip() and \
                    not re.match(r'^\s*([-*]|\d+\.)\s+|^#|^\||^```|^---+\s*$|^>', lines[i]):
                txt += ' ' + lines[i].strip()
                i += 1
            items.append(ListItem(Paragraph(inline(txt), BODY), leftIndent=16))
        story.append(ListFlowable(items, bulletType='1' if ordered else 'bullet',
                                  bulletFontSize=8, leftIndent=14, spaceAfter=6))
        continue

    if not line.strip():
        i += 1
        continue

    buf = [line]
    i += 1
    while i < len(lines) and lines[i].strip() and \
            not re.match(r'^#|^\||^```|^---+\s*$|^>|^\s*([-*]|\d+\.)\s+', lines[i]):
        buf.append(lines[i])
        i += 1
    # Markdown hard break: a line ending in two spaces starts a new line.
    joined, out = '', []
    for n, b in enumerate(buf):
        out.append(inline(b.rstrip()))
        if b.endswith('  ') and n < len(buf) - 1:
            out.append('<br/>')
        elif n < len(buf) - 1:
            out.append(' ')
    story.append(Paragraph(''.join(out), BODY))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#7a838c'))
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, f'Page {doc.page}')
    canvas.restoreState()


doc = BaseDocTemplate(DST, pagesize=A4, topMargin=1.7 * cm, bottomMargin=1.8 * cm,
                      leftMargin=1.7 * cm, rightMargin=1.7 * cm,
                      title='Assignment 2 - Factory Method and Abstract Factory')
frame = Frame(doc.leftMargin, doc.bottomMargin, FRAME_W,
              A4[1] - 3.5 * cm, id='main')
doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=footer)])
doc.build(story)
print('WROTE', DST)
