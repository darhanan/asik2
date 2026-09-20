// Convert the assignment report Markdown into a Word .docx.
const fs = require('fs');
const path = require('path');
const SCRATCH = process.env.DOCX_MODULES || path.join(__dirname, '..');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, LevelFormat, convertInchesToTwip,
} = require(path.join(SCRATCH, 'node_modules', 'docx'));

const [SRC, DST] = process.argv.slice(2);
const md = fs.readFileSync(SRC, 'utf8').split('\n');

const NAVY = '1B3A5C', DARK = '12243A', CODE = '9C2A2A', GREY = '5A6B7D';
const CONTENT_W = 9360;           // 6.5in of usable width in DXA

// Split a line into runs, honouring **bold**, *italic* and `code`.
function runs(text, base = {}) {
  const out = [];
  const re = /(`[^`]+`|\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*))/g;
  let last = 0, m;
  const push = (t, extra) => { if (t) out.push(new TextRun({ text: t, ...base, ...extra })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), {});
    const tok = m[0];
    if (tok.startsWith('`')) push(tok.slice(1, -1), { font: 'Consolas', color: CODE, size: 18 });
    else if (tok.startsWith('**')) push(tok.slice(2, -2), { bold: true });
    else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last), {});
  return out.length ? out : [new TextRun({ text: '', ...base })];
}

const splitRow = (l) => l.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());

function makeTable(rows) {
  const ncol = rows[0].length;
  // Weight columns by content length so wide prose columns get the room.
  const weights = [];
  for (let i = 0; i < ncol; i++) {
    let longest = 0;
    for (const r of rows) longest = Math.max(longest, (r[i] || '').length);
    weights.push(Math.max(longest, 6));
  }
  const total = weights.reduce((a, b) => a + b, 0);
  let widths = weights.map((w) => Math.max(Math.round((CONTENT_W * w) / total), 700));
  const scale = CONTENT_W / widths.reduce((a, b) => a + b, 0);
  widths = widths.map((w) => Math.round(w * scale));
  widths[ncol - 1] += CONTENT_W - widths.reduce((a, b) => a + b, 0);

  const mkCell = (txt, header, i) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: header
      ? { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' }
      : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: (txt.split('<br>')).map((part) => new Paragraph({
      spacing: { after: 0, line: 240 },
      children: runs(part, header
        ? { bold: true, color: 'FFFFFF', size: 17 }
        : { size: 17 }),
    })),
  });

  return new Table({
    columnWidths: widths,
    width: { size: CONTENT_W, type: WidthType.DXA },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: Array.from({ length: ncol }, (_, i) => mkCell(r[i] || '', ri === 0, i)),
    })),
  });
}

function codeBlock(lines) {
  return lines.map((l, idx) => new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: 'F4F5F7', color: 'auto' },
    spacing: { before: idx === 0 ? 100 : 0, after: idx === lines.length - 1 ? 140 : 0, line: 230 },
    indent: { left: 120 },
    children: [new TextRun({ text: l || ' ', font: 'Consolas', size: 15, color: '1A1A1A' })],
  }));
}

function imagePara(file, maxW) {
  const buf = fs.readFileSync(file);
  // Read PNG pixel dimensions from the IHDR chunk to preserve aspect ratio.
  const pw = buf.readUInt32BE(16), ph = buf.readUInt32BE(20);
  const w = maxW, h = Math.round((ph / pw) * maxW);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 160 },
    children: [new ImageRun({ type: 'png', data: buf, transformation: { width: w, height: h } })],
  });
}

const children = [];
let i = 0;
while (i < md.length) {
  const line = md[i];

  if (/^\[\[UML:(fm|af)\]\]\s*$/.test(line)) {
    const kind = line.match(/^\[\[UML:(fm|af)\]\]/)[1];
    children.push(imagePara(
      kind === 'fm' ? 'docs/uml-factory-method.png' : 'docs/uml-abstract-factory.png', 624));
    i++; continue;
  }

  if (line.startsWith('```')) {
    i++; const buf = [];
    while (i < md.length && !md[i].startsWith('```')) buf.push(md[i++]);
    i++; children.push(...codeBlock(buf)); continue;
  }

  if (line.startsWith('|') && i + 1 < md.length && /^\|[\s:|-]+\|?\s*$/.test(md[i + 1])) {
    const rows = [splitRow(line)]; i += 2;
    while (i < md.length && md[i].startsWith('|')) rows.push(splitRow(md[i++]));
    children.push(makeTable(rows));
    children.push(new Paragraph({ spacing: { after: 140 }, children: [] }));
    continue;
  }

  if (/^---+\s*$/.test(line)) {
    children.push(new Paragraph({
      spacing: { before: 60, after: 140 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'C2CCD6' } },
      children: [],
    }));
    i++; continue;
  }

  const h = line.match(/^(#{1,3})\s+(.*)$/);
  if (h) {
    const lvl = h[1].length;
    children.push(new Paragraph({
      heading: [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][lvl - 1],
      spacing: { before: lvl === 1 ? 0 : 240, after: 120 },
      children: runs(h[2], { color: lvl === 1 ? DARK : NAVY, bold: true,
                             size: lvl === 1 ? 32 : lvl === 2 ? 25 : 21 }),
    }));
    i++; continue;
  }

  if (line.startsWith('> ')) {
    const buf = [];
    while (i < md.length && md[i].startsWith('>')) buf.push(md[i++].replace(/^>\s?/, '').trim());
    children.push(new Paragraph({
      indent: { left: 260 }, spacing: { after: 140 },
      children: runs(buf.join(' '), { italics: true, color: '4A4A4A', size: 19 }),
    }));
    continue;
  }

  const li = line.match(/^\s*([-*]|\d+\.)\s+(.*)$/);
  if (li) {
    const ordered = /\d/.test(li[1]);
    while (i < md.length) {
      const m2 = md[i].match(/^\s*([-*]|\d+\.)\s+(.*)$/);
      if (!m2) break;
      let txt = m2[2]; i++;
      while (i < md.length && md[i].trim() && !/^\s*([-*]|\d+\.)\s+|^#|^\||^```|^---+\s*$|^>/.test(md[i]))
        txt += ' ' + md[i++].trim();
      children.push(new Paragraph({
        numbering: { reference: ordered ? 'num' : 'bul', level: 0 },
        spacing: { after: 80, line: 276 },
        children: runs(txt, { size: 19 }),
      }));
    }
    continue;
  }

  if (!line.trim()) { i++; continue; }

  // Plain paragraph: join wrapped lines, but honour markdown hard breaks (two trailing spaces).
  const buf = [line]; i++;
  while (i < md.length && md[i].trim() &&
         !/^#|^\||^```|^---+\s*$|^>|^\s*([-*]|\d+\.)\s+|^\[\[UML:/.test(md[i])) buf.push(md[i++]);
  const kids = [];
  buf.forEach((b, n) => {
    kids.push(...runs(b.trim(), { size: 19 }));
    if (n < buf.length - 1) kids.push(b.endsWith('  ')
      ? new TextRun({ break: 1 }) : new TextRun({ text: ' ', size: 19 }));
  });
  children.push(new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: 140, line: 276 }, children: kids,
  }));
}

const doc = new Document({
  creator: 'Darkhan Tynyshtyk',
  title: 'Assignment 2 - Factory Method and Abstract Factory',
  numbering: {
    config: [
      { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
    ],
  },
  styles: { default: { document: { run: { font: 'Calibri', size: 19 } } } },
  sections: [{
    properties: { page: { margin: {
      top: convertInchesToTwip(0.8), bottom: convertInchesToTwip(0.8),
      left: convertInchesToTwip(1), right: convertInchesToTwip(1) } } },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(DST, b); console.log('WROTE', DST, b.length, 'bytes'); });
