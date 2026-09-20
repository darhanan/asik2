"""Draw the two UML class diagrams as reportlab Flowables (vector, no rasterizer needed)."""
import math
from reportlab.lib import colors
from reportlab.platypus import Flowable

BORDER = colors.HexColor('#1b3a5c')
HEAD = colors.HexColor('#e8eef4')
TXT = colors.HexColor('#12243a')
LINE = colors.HexColor('#40566d')
STEREO = colors.HexColor('#5a6b7d')

FN, FB, FM = 'Helvetica', 'Helvetica-Bold', 'Courier'


class Box:
    def __init__(self, name, stereo='', attrs=(), ops=(), italic=False):
        self.name, self.stereo = name, stereo
        self.attrs, self.ops, self.italic = list(attrs), list(ops), italic

    def measure(self, c, fs):
        wn = c.stringWidth(self.name, FB, fs + 1)
        ws = c.stringWidth(self.stereo, FN, fs - 1.2) if self.stereo else 0
        wr = max([c.stringWidth(r, FM, fs - 0.8) for r in self.attrs + self.ops] or [0])
        self.w = max(wn, ws, wr) + 14
        lh = fs + 3.2
        self.head = lh + (lh if self.stereo else 0) + 7
        self.h = self.head \
            + (lh * len(self.attrs) + 6 if self.attrs else 0) \
            + (lh * len(self.ops) + 6 if self.ops else 0)
        return self.w, self.h

    def place(self, x, y):
        self.x, self.y = x, y
        return self

    def draw(self, c, fs):
        lh = fs + 3.2
        c.setFillColor(colors.white)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.9)
        c.rect(self.x, self.y, self.w, self.h, stroke=1, fill=1)
        c.setFillColor(HEAD)
        c.rect(self.x, self.y + self.h - self.head, self.w, self.head, stroke=0, fill=1)
        c.setStrokeColor(BORDER)
        c.rect(self.x, self.y, self.w, self.h, stroke=1, fill=0)

        cx = self.x + self.w / 2
        ty = self.y + self.h - lh + 1
        if self.stereo:
            c.setFont(FN, fs - 1.2)
            c.setFillColor(STEREO)
            c.drawCentredString(cx, ty, self.stereo)
            ty -= lh
        c.setFont('Helvetica-BoldOblique' if self.italic else FB, fs + 1)
        c.setFillColor(TXT)
        c.drawCentredString(cx, ty, self.name)

        y = self.y + self.h - self.head
        for group in (self.attrs, self.ops):
            if not group:
                continue
            c.setStrokeColor(BORDER)
            c.setLineWidth(0.7)
            c.line(self.x, y, self.x + self.w, y)
            y -= lh - 1
            c.setFillColor(TXT)
            for r in group:
                italic = r.endswith('{abstract}')
                c.setFont('Courier-Oblique' if italic else FM, fs - 0.8)
                c.drawString(self.x + 7, y, r)
                y -= lh
            y += lh - 6

    # edge anchors
    def T(self, f=.5): return (self.x + self.w * f, self.y + self.h)
    def B(self, f=.5): return (self.x + self.w * f, self.y)
    def L(self, f=.5): return (self.x, self.y + self.h * f)
    def R(self, f=.5): return (self.x + self.w, self.y + self.h * f)


def _head(c, a, b, hollow, size=7.5, spread=0.40):
    (x1, y1), (x2, y2) = a, b
    ang = math.atan2(y2 - y1, x2 - x1)
    l = (x2 - size * math.cos(ang - spread), y2 - size * math.sin(ang - spread))
    r = (x2 - size * math.cos(ang + spread), y2 - size * math.sin(ang + spread))
    if hollow:
        p = c.beginPath()
        p.moveTo(*b); p.lineTo(*l); p.lineTo(*r); p.close()
        c.setFillColor(colors.white)
        c.setStrokeColor(LINE)
        c.drawPath(p, stroke=1, fill=1)
        return ((l[0] + r[0]) / 2, (l[1] + r[1]) / 2)
    c.setStrokeColor(LINE)
    c.line(l[0], l[1], x2, y2)
    c.line(r[0], r[1], x2, y2)
    return b


def conn(c, a, b, kind, label='', fs=6.6, lx=0, ly=0):
    """kind: 'extends' | 'implements' | 'depends' | 'assoc'."""
    c.setStrokeColor(LINE)
    c.setLineWidth(0.85)
    dashed = kind in ('implements', 'depends')
    hollow = kind in ('extends', 'implements')
    c.setDash([2.6, 2.2] if dashed else [])
    end = _head(c, a, b, hollow)
    c.line(a[0], a[1], end[0], end[1])
    c.setDash([])
    if label:
        mx, my = (a[0] + b[0]) / 2 + lx, (a[1] + b[1]) / 2 + ly
        w = c.stringWidth(label, FN, fs) + 4
        c.setFillColor(colors.white)
        c.rect(mx - w / 2, my - 2.2, w, fs + 2.4, stroke=0, fill=1)
        c.setFillColor(colors.HexColor('#3d5266'))
        c.setFont(FN, fs)
        c.drawCentredString(mx, my, label)


def note(c, x, y, lines, fs=6.3):
    lh = fs + 2.6
    w = max(c.stringWidth(l, FM, fs) for l in lines) + 14
    h = lh * len(lines) + 9
    fold = 7
    p = c.beginPath()
    p.moveTo(x, y); p.lineTo(x, y + h); p.lineTo(x + w - fold, y + h)
    p.lineTo(x + w, y + h - fold); p.lineTo(x + w, y); p.close()
    c.setFillColor(colors.HexColor('#fffbe8'))
    c.setStrokeColor(colors.HexColor('#c9a227'))
    c.setLineWidth(0.7)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(colors.HexColor('#5c4a10'))
    c.setFont(FM, fs)
    ty = y + h - lh
    for l in lines:
        c.drawString(x + 6, ty, l)
        ty -= lh
    return w, h


class UML(Flowable):
    """A diagram flowable: builder(c, fs) does the drawing in a WxH coordinate space."""

    def __init__(self, width, native_w, native_h, builder):
        Flowable.__init__(self)
        self.width = width
        self.scale = width / native_w
        self.height = native_h * self.scale
        self.native = (native_w, native_h)
        self.builder = builder

    def draw(self):
        c = self.canv
        c.saveState()
        c.scale(self.scale, self.scale)
        self.builder(c)
        c.restoreState()
