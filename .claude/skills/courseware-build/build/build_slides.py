#!/usr/bin/env python3
"""Generate the AI for Network Security (TGS-2024051414) slide deck — all-white Tertiary house style.

Every visual component is the house set from the wsq-slides reference deck:
cover, section, content, two_col, cards3, tile_grid, flow_h, process_map,
decision_map, compare_table, worked_example, chart_slide, steps_slide,
trainer_slide, big_statement, activity_overview, step_slide, test_slide, brk.
Content comes entirely from course_data.py + data_domain1..4.py so the deck
stays 100% aligned with the LP, LG, labs and assessment.
"""
import os, sys, copy, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import ChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
from data_domain4 import DOMAIN4
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3 + DOMAIN4

def _find_repo(start):
    """Locate the course repo (a dir containing both courseware/ and labs/).
    Env COURSE_REPO overrides. Keeps the build working wherever the skill lives."""
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))
REPO = _find_repo(HERE)
ASSETS = os.path.join(os.path.dirname(HERE), "assets")   # co-located with the skill

# ---------------- palette (matches reference) ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

# ---------------- motion: restrained transitions + build animation ----------------
# House rule: ONE transition family for the whole deck (morph is unavailable in the
# OOXML PowerPoint 2010 transition set that python-pptx can emit, so we use a short
# push/fade pair). Content slides fade; section dividers push. Nothing else moves.
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"

def _transition(s, kind="fade", speed="med"):
    """Attach a restrained slide transition. kind: fade | push | wipe."""
    sld = s._element
    for old in sld.findall(qn("p:transition")):
        sld.remove(old)
    tr = etree.SubElement(sld, qn("p:transition"))
    tr.set("spd", speed)
    tr.set("advClick", "1")
    if kind == "fade":
        etree.SubElement(tr, qn("p:fade"))
    elif kind == "push":
        el = etree.SubElement(tr, qn("p:push")); el.set("dir", "l")
    elif kind == "wipe":
        el = etree.SubElement(tr, qn("p:wipe")); el.set("dir", "r")
    # keep the transition last in the slide element (schema order)
    sld.append(tr)
    return tr

# Appear-on-click build for a list of shape ids — used ONLY on process maps so the
# trainer can reveal one stage at a time. No spins, no flying, no sound.
_TIMING = """<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">
<p:childTnLst>{pars}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"""

_PAR = """<p:par><p:cTn id="{i0}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i1}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i2}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{nt}">
<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{i3}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i4}" dur="400"/>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""

def _build_on_click(s, spids):
    """Fade each shape id in on click, in order. Used sparingly (process maps)."""
    if not spids:
        return
    pars, nid = [], 10
    for k, spid in enumerate(spids):
        pars.append(_PAR.format(i0=nid, i1=nid+1, i2=nid+2, i3=nid+3, i4=nid+4,
                                spid=spid, nt="clickEffect" if k == 0 else "afterEffect"))
        nid += 10
    sld = s._element
    for old in sld.findall(qn("p:timing")):
        sld.remove(old)
    sld.append(etree.fromstring(_TIMING.format(pars="".join(pars))))

def connector(s, x1, y1, x2, y2, color, width=Pt(2.0), arrow=True):
    """A REAL PowerPoint connector line (not a typed arrow glyph)."""
    cx, cy = min(x1, x2), min(y1, y2)
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    cn.line.color.rgb = color; cn.line.width = width
    ln = cn.line._get_or_add_ln()
    if arrow:
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle"); tail.set("w", "med"); tail.set("len", "med")
    return cn

def chevron(s, x, y, w, h, color):
    """A staged chevron shape — the real CHEVRON autoshape, not a text glyph."""
    sp = s.shapes.add_shape(MSO_SHAPE.CHEVRON, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    sp.line.fill.background(); sp.shadow.inherit = False
    return sp

def roundrect(s, x, y, w, h, color, line=None, adj=0.10):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1.25)
    sp.shadow.inherit = False
    try: sp.adjustments[0] = adj
    except Exception: pass
    return sp

def diamond(s, x, y, w, h, color, line=None):
    sp = s.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1.25)
    sp.shadow.inherit = False
    return sp

def label_in(sp, text, size, color, bold=True):
    """Put centred text inside an autoshape."""
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = color; r.font.name = "Arial"
    return sp

PAGE={"n":1}   # the cover is slide 1 and carries no number, so numbering starts at 2
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def _ellipsis(text,limit):
    """Truncate on a WORD boundary with an ellipsis — never slice mid-word."""
    t=" ".join(str(text).split())
    if len(t)<=limit: return t
    cut=t[:limit]
    sp=cut.rfind(" ")
    if sp>limit*0.55: cut=cut[:sp]
    return cut.rstrip(" ,.;:-—(") + "…"

def _short_cmd(cmd,limit=30):
    """Shorten a shell command for a caption. Paths/URLs have no spaces, so a
    word-boundary ellipsis cuts them mid-token — drop the runner prefix and keep the
    meaningful tail (the script/target) instead."""
    c=" ".join(str(cmd).split())
    for pre in ("uv run python ","uv run ","python3 ","python ","bash ","sh "):
        if c.startswith(pre): c=c[len(pre):]; break
    if len(c)<=limit: return c
    parts=c.split(" ")
    head=parts[0]
    rest=" ".join(parts[1:]).strip()
    if rest:
        # a URL argument → keep the verb and the host, drop the path
        m=re.match(r'https?://([^/\s]+)',rest)
        if m:
            for cand in (f"{head} {m.group(1)}/…", f"{head} {m.group(1)}"):
                if len(cand)<=limit: return cand
        # "git clone …/repo" — keep the verb plus the final path segment
        tail=rest.rstrip("/").split("/")[-1]
        cand=f"{head} …/{tail}" if "/" in rest else f"{head} {tail}"
        if len(cand)<=limit: return cand
        if len(head)+2<=limit: return _ellipsis(head,limit-2)+" …"
    if "/" in c:                   # a bare path → keep the last segment
        tail=c.rstrip("/").split("/")[-1]
        if len(tail)+2<=limit: return "…/"+tail
    return _ellipsis(c,limit)

def _wrapped_h(text, width_in, size, cpl_per_inch=1.80):
    """Estimated rendered height (inches) of `text` wrapped into `width_in` at `size` pt.
    Same model as _fit_size, exposed so layouts can ASSERT containment rather than
    trusting SHAPE_TO_FIT_TEXT, which no renderer honours.

    cpl_per_inch is calibrated for Arial: 2.05 was optimistic and let three card
    bodies overflow their border by ~0.11in. 1.80 matches the measured render.
    NOTE: an estimator-based assert can only confirm its own assumptions — the
    authoritative check is verify_render.py, which rasterises the built PDF."""
    import math as _m
    chars_per_line = max(1, int(width_in * cpl_per_inch * (12.0 / size) * 6.0))
    return _m.ceil(len(text) / chars_per_line) * ((size * 1.22) / 72.0)


def _fit_size(text, width_in, height_in, base, min_size=8.0, cpl_per_inch=1.80):
    """Choose the largest font size (stepping down from `base`) at which `text`
    wraps inside a box of width_in x height_in. NEVER truncates — the standard
    forbids hiding content behind an ellipsis, so we shrink to fit instead."""
    import math as _m
    size = float(base)
    while size > min_size:
        chars_per_line = max(1, int(width_in * cpl_per_inch * (12.0 / size) * 6.0))
        lines = _m.ceil(len(text) / chars_per_line)
        line_h = (size * 1.22) / 72.0
        if lines * line_h <= height_in:
            return round(size, 1)
        size -= 0.5
    return min_size


def _fit_title(title,size=29):
    """Shrink long titles so they never wrap into the hairline rule below."""
    n=len(title)
    if n<=52: return size
    if n<=66: return 25
    if n<=82: return 22
    return 20

def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    txt(s,Inches(0.85),Inches(0.88),Inches(11.9),Inches(0.78),
        [[(title,_fit_title(title),INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    # course badge (top-right) — AI + shield mark drawn natively, always on brand
    bx,by_,bw,bh=Inches(10.55),Inches(0.62),Inches(2.05),Inches(1.24)
    rect(s,bx,by_,bw,bh,BLUE)
    rect(s,bx,by_,bw,Inches(0.07),TEAL)
    txt(s,bx,int(by_+Inches(0.16)),bw,Inches(0.56),[[("AI",30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,bx,int(by_+Inches(0.72)),bw,Inches(0.42),[[("NETWORK SECURITY",8.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,40,INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,RGBColor(0xE2,0xE8,0xF0),True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=16)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=16,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s
import math
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    """Grid of light panels, each with a coloured icon/number badge + text.
    items: list of strings (or (title,caption) tuples). Much richer than a bullet list."""
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],size+2,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    """Horizontal numbered flow: coloured chips connected by chevrons."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def process_map(title,stages,kicker=None,color=BLUE,synthesis=None,animate=True):
    """STAGED PROCESS MAP — real rounded-rect stages joined by real connectors with
    arrowheads, each stage numbered, optional synthesis band. stages: list of
    (label, detail). This replaces flow_h wherever a genuine process is taught."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(stages); X0=Inches(0.85); TOTW=Inches(11.63)
    gap=Inches(0.42); cw=int((TOTW-gap*(n-1))/n)
    y=Inches(2.35); ch=Inches(2.35) if synthesis else Inches(3.0)
    spids=[]
    for i,st in enumerate(stages):
        lbl,detail=(st if isinstance(st,tuple) else (st,""))
        x=int(X0+(cw+gap)*i)
        box=roundrect(s,x,y,cw,ch,LIGHT,line=LINE)
        rect(s,x,y,cw,Inches(0.11),color)
        bd=Inches(0.62)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,[[(str(i+1),24,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        # Label band: the FULL label, auto-shrunk to fit. Never truncated.
        lbl_w=(cw-Inches(0.28))/914400.0
        det_h=Inches(0.72) if detail else Emu(0)
        lbl_h=(ch-Inches(1.18)-det_h)/914400.0
        lsz=_fit_size(lbl, lbl_w, lbl_h, 13, min_size=8.5)
        txt(s,x+Inches(0.14),int(y+Inches(1.06)),cw-Inches(0.28),int(ch-Inches(1.18)-det_h),
            [[(lbl,lsz,INK,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        if detail:
            # Full caption, wrapped over up to two lines and auto-shrunk. Never truncated.
            det_w=(cw-Inches(0.2))/914400.0
            dsz=_fit_size(detail, det_w, 0.66, 9.5, min_size=6.5)
            txt(s,x+Inches(0.1),int(y+ch-Inches(0.78)),cw-Inches(0.2),Inches(0.72),
                [[(detail,dsz,GREY,False)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        spids.append(box.shape_id)
        if i<n-1:   # REAL connector in the gap, with an arrowhead
            cy=int(y+ch/2)
            cn=connector(s,int(x+cw+Inches(0.06)),cy,int(x+cw+gap-Inches(0.06)),cy,color)
            spids.append(cn.shape_id)
    if synthesis:
        by=int(y+ch+Inches(0.34))
        rect(s,Inches(0.85),by,Inches(11.63),Inches(1.15),LIGHT)
        rect(s,Inches(0.85),by,Inches(0.11),Inches(1.15),color)
        txt(s,Inches(1.15),int(by+Inches(0.12)),Inches(11.1),Inches(0.32),
            [[(synthesis[0].upper(),11,color,True)]])
        txt(s,Inches(1.15),int(by+Inches(0.46)),Inches(11.1),Inches(0.62),
            [[(synthesis[1],13,INK,False)]])
    if animate: _build_on_click(s,spids)
    footer(s); return s

def decision_map(title,question,yes,no,kicker=None,color=VIOLET,note=None):
    """A real decision diamond with two branches drawn as connectors — used for
    'which pattern do I choose' teaching moments."""
    s=head(slide(),title,kicker,kcolor=color)
    # a diamond's usable text area is ~50% of its box — size generously or text spills
    # past the facets. 4.6 x 2.7 fits 2-3 short lines at 12pt.
    dx,dy,dw,dh=Inches(0.85),Inches(2.75),Inches(4.6),Inches(2.7)
    d=diamond(s,dx,dy,dw,dh,color); label_in(d,question,12,WHITE)
    bx=Inches(6.1); bw=Inches(6.35); bh=Inches(1.5)
    ys=[Inches(2.15),Inches(4.35)]
    for (hdr,items),by,col in zip([yes,no],ys,[TEAL,AMBER]):
        b=roundrect(s,bx,by,bw,bh,LIGHT,line=LINE)
        rect(s,bx,by,Inches(0.11),bh,col)
        txt(s,bx+Inches(0.3),int(by+Inches(0.16)),bw-Inches(0.55),Inches(0.4),[[(hdr,15,col,True)]])
        txt(s,bx+Inches(0.3),int(by+Inches(0.6)),bw-Inches(0.55),Inches(0.82),[[(items,12,INK,False)]])
        connector(s,int(dx+dw),int(dy+dh/2),bx,int(by+bh/2),col)
    if note:
        rect(s,Inches(0.85),Inches(6.15),Inches(11.63),Inches(0.72),LIGHT)
        txt(s,Inches(1.15),Inches(6.28),Inches(11.1),Inches(0.5),[[(note,12,GREY,False)]])
    footer(s); return s

def compare_table(title,headers,rows,kicker=None,accent=BLUE,note=None):
    """A real comparison matrix — the substantive alternative to two bullet columns."""
    s=head(slide(),title,kicker,kcolor=accent)
    X0=Inches(0.85); TOTW=Inches(11.63); ncol=len(headers)
    first=int(TOTW*0.26); rest=int((TOTW-first)/(ncol-1))
    widths=[first]+[rest]*(ncol-1)
    y=Inches(1.95); hh=Inches(0.52)
    x=X0
    for i,h in enumerate(headers):
        col=accent if i==0 else PALETTE[(i-1)%len(PALETTE)]
        rect(s,x,y,widths[i],hh,col)
        txt(s,x+Inches(0.14),y,widths[i]-Inches(0.28),hh,[[(h,13,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
        x+=widths[i]
    # body must end above the note band AND the footer (7.05). Budget it explicitly.
    ry=int(y+hh)
    BOTTOM=Inches(6.88)-(Inches(1.24) if note else Emu(0))
    avail=BOTTOM-ry
    rh=int(min(Inches(0.78),avail/max(len(rows),1)))
    for r,row in enumerate(rows):
        x=X0
        for i,cell in enumerate(row):
            fill=LIGHT if r%2==0 else WHITE
            rect(s,x,ry,widths[i],rh,fill,line=LINE)
            bold=(i==0)
            txt(s,x+Inches(0.14),ry,widths[i]-Inches(0.28),rh,
                [[(cell,11.5,INK if bold else GREY,bold)]],anchor=MSO_ANCHOR.MIDDLE)
            x+=widths[i]
        ry+=rh
    if note:
        rect(s,X0,int(ry+Inches(0.22)),TOTW,Inches(0.92),LIGHT)
        rect(s,X0,int(ry+Inches(0.22)),Inches(0.11),Inches(0.92),accent)
        txt(s,X0+Inches(0.3),int(ry+Inches(0.34)),TOTW-Inches(0.6),Inches(0.66),
            [[("WHEN IT MATTERS  ",11,accent,True),(note,12,INK,False)]])
    footer(s); return s

def worked_example(title,intro,code,explain,kicker=None,accent=TEAL):
    """A worked example: the code on the left, the line-by-line reading on the right.
    This is what turns a decorative lab slide into a teaching slide."""
    s=head(slide(),title,kicker,kcolor=accent)
    txt(s,Inches(0.85),Inches(1.9),Inches(11.63),Inches(0.46),[[(intro,15,GREY,False)]])
    cx,cw=Inches(0.85),Inches(6.5)
    rect(s,cx,Inches(2.5),cw,Inches(4.15),RGBColor(0x0B,0x12,0x20))
    tb=s.shapes.add_textbox(cx+Inches(0.22),Inches(2.62),cw-Inches(0.44),Inches(3.9))
    tf=tb.text_frame; tf.word_wrap=True
    for i,ln in enumerate(code):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(2)
        r=p.add_run(); r.text=ln; r.font.size=Pt(11); r.font.name="Consolas"
        col=RGBColor(0x9C,0xDC,0xFE)
        st=ln.strip()
        if st.startswith("#"): col=RGBColor(0x6A,0x99,0x55)
        elif "=" in ln and not st.startswith(("def","class")): col=RGBColor(0xD4,0xD4,0xD4)
        if st.startswith(("def ","class ","from ","import ")): col=RGBColor(0xC5,0x86,0xC0)
        r.font.color.rgb=col
    ex,ew=Inches(7.65),Inches(4.83)
    for i,(lbl,body) in enumerate(explain[:4]):
        y=int(Inches(2.5)+(Inches(1.0)+Inches(0.05))*i)
        col=PALETTE[i%len(PALETTE)]
        rect(s,ex,y,ew,Inches(1.0),LIGHT); rect(s,ex,y,Inches(0.09),Inches(1.0),col)
        txt(s,ex+Inches(0.26),int(y+Inches(0.1)),ew-Inches(0.45),Inches(0.32),[[(lbl,12,col,True)]])
        txt(s,ex+Inches(0.26),int(y+Inches(0.42)),ew-Inches(0.45),Inches(0.52),[[(body,11,INK,False)]])
    footer(s); return s

def steps_slide(act_title,steps,kicker,accent=TEAL,part=None,start=1):
    """Substantive lab procedure: numbered steps WITH their commands, up to 5 per
    slide. Replaces the old one-sentence step slide."""
    s=head(slide(),act_title+(f" — {part}" if part else ""),kicker,kcolor=accent)
    y0=Inches(1.92); n=len(steps); gapy=Inches(0.1)
    AVAIL=Inches(4.92)          # 1.92 → 6.84, clear of the 7.05 footer
    rh=int((AVAIL-gapy*(n-1))/max(n,1))          # nominal equal share (used for sizing)
    # ONE heading size for the whole slide (a per-row spread reads as a rendering
    # fault), and a FLOOR of 11pt so nothing drops below projection-legible. The
    # heading BAND grows to two lines instead of the type shrinking — the row is
    # 1.12in tall and a one-line band at 0.36in was wasting the space beneath it.
    FLOOR=11.0
    _tw=Inches(10.6)/914400.0
    _has_cmd=any(c for t,c in steps)
    # try a 1-line band first; if any command-bearing step cannot reach the floor
    # on one line, give every heading a 2-line band and recompute.
    def _fits(band_in):
        sz=[_fit_size(t,_tw,band_in,12.5,min_size=FLOOR) for t,c in steps if c]
        sz+=[_fit_size(t,_tw,(rh-Inches(0.12))/914400.0,12.5,min_size=FLOOR) for t,c in steps if not c]
        return min(sz) if sz else 12.5
    HEAD_H=Inches(0.36)
    UNIFORM=_fits(0.30)
    if _has_cmd and UNIFORM < 12.0:
        HEAD_H=Inches(0.60)                 # two lines
        UNIFORM=_fits(0.54)
    assert UNIFORM >= FLOOR, f"step text fell to {UNIFORM}pt — below the {FLOOR}pt floor"
    # PROPORTIONAL ROW HEIGHTS — a command that wraps to two lines needs a taller
    # row than a one-line discussion step. Equal slices are what clipped the bar.
    _bar_w=Inches(10.2)/914400.0
    def _need(t,c):
        h=(HEAD_H/914400.0)+0.14
        if c:
            one=c.split("\n")[0]
            _cs=10.5 if len(one)<=96 else (9.5 if len(one)<=112 else 9.0)
            h+=_wrapped_h("$ "+one,_bar_w,_cs)+0.22
        return max(h,0.62)
    needs=[_need(t,c) for t,c in steps]
    total=sum(needs)
    span=(AVAIL-gapy*(n-1))/914400.0
    heights=[int(max(nd/total*span,0.60)*914400) for nd in needs]
    # never exceed the band
    over=sum(heights)+gapy*(n-1)-AVAIL
    if over>0:
        heights=[int(h-over/len(heights)) for h in heights]
    ytop=y0
    for i,(text,cmd) in enumerate(steps):
        rh=heights[i]
        y=int(ytop); ytop=y+rh+gapy; col=PALETTE[i%len(PALETTE)]
        rect(s,Inches(0.85),y,Inches(11.63),rh,LIGHT); rect(s,Inches(0.85),y,Inches(0.09),rh,col)
        bd=Inches(0.4)
        oval(s,Inches(1.06),int(y+rh/2-bd/2),bd,bd,col)
        txt(s,Inches(1.06),int(y+rh/2-bd/2),bd,bd,[[(str(start+i),13,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        if cmd:
            # The heading is auto-shrunk to fit ONE line of its own band, so it can
            # never wrap down into the code bar underneath it.
            txt(s,Inches(1.62),int(y+Inches(0.05)),Inches(10.6),HEAD_H,
                [[(text,UNIFORM,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
            cb_y=int(y+Inches(0.05)+HEAD_H+Inches(0.04))
            cb_avail=int(y+rh-Inches(0.07)-cb_y)
            one=cmd.split("\n")[0]
            # A browser URL is not a shell command — prefix it with a link glyph
            # rather than a "$" prompt, which would tell the learner to type it
            # into a terminal.
            is_url=one.startswith(("http://","https://"))
            prefix="\u2192  " if is_url else "$ "
            # The bar is sized from the command's WRAPPED height (not a fixed one
            # line), so a two-line command is never sliced by the bar edge. If the
            # wrapped bar cannot fit the card, shrink the type until it does.
            bar_w=Inches(10.2)/914400.0
            csz=10.5 if len(one)<=96 else (9.5 if len(one)<=112 else 9.0)
            pad=Inches(0.10)
            while csz > 7.0:
                need=int(_wrapped_h(prefix+one, bar_w, csz)*914400)+2*pad
                if need <= cb_avail: break
                csz-=0.5
            cb_h=min(cb_avail, max(Inches(0.28),
                     int(_wrapped_h(prefix+one, bar_w, csz)*914400)+2*pad))
            cb_y=int(y+rh-Inches(0.07)-cb_h)      # bottom-align inside the card
            rect(s,Inches(1.62),cb_y,Inches(10.5),cb_h,RGBColor(0x0B,0x12,0x20))
            assert cb_y+cb_h <= y+rh, "code bar spills its card"
            txt(s,Inches(1.78),cb_y,Inches(10.2),cb_h,
                [[(prefix+one,csz,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
        else:
            txt(s,Inches(1.62),y,Inches(10.6),rh,[[(text,UNIFORM,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

def chart_slide(title,categories,series,kicker=None,accent=BLUE,
                kind="bar",insight=None,number_format='0'):
    """NATIVE PowerPoint chart (fully editable, not a picture) + an insight band.
    kind: bar | column | line | pie | doughnut. series: list of (name, values)."""
    s=head(slide(),title,kicker,kcolor=accent)
    cd=ChartData(); cd.categories=categories
    for nm,vals in series: cd.add_series(nm,vals,number_format)
    ctype={"bar":XL_CHART_TYPE.BAR_CLUSTERED,"column":XL_CHART_TYPE.COLUMN_CLUSTERED,
           "line":XL_CHART_TYPE.LINE_MARKERS,"pie":XL_CHART_TYPE.PIE,
           "doughnut":XL_CHART_TYPE.DOUGHNUT}.get(kind,XL_CHART_TYPE.COLUMN_CLUSTERED)
    ch_h=Inches(3.55) if insight else Inches(4.75)
    gf=s.shapes.add_chart(ctype,Inches(0.85),Inches(1.95),Inches(11.63),ch_h,cd)
    ch=gf.chart
    ch.has_title=False
    ch.font.size=Pt(12); ch.font.name="Arial"; ch.font.color.rgb=INK
    if kind in ("pie","doughnut") or len(series)>1:
        ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout=False; ch.legend.font.size=Pt(11)
    else:
        ch.has_legend=False
    # house palette per point (pie/doughnut) or per series (bar/column/line)
    try:
        if kind in ("pie","doughnut"):
            pts=ch.plots[0]
            for i,pt in enumerate(pts.points):
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb=PALETTE[i%len(PALETTE)]
        else:
            for i,sr in enumerate(ch.series):
                col=PALETTE[i%len(PALETTE)]
                if kind=="line":
                    sr.format.line.color.rgb=col; sr.format.line.width=Pt(2.5)
                else:
                    sr.format.fill.solid(); sr.format.fill.fore_color.rgb=col
    except Exception:
        pass
    try:
        pl=ch.plots[0]; pl.has_data_labels=True
        dl=pl.data_labels; dl.font.size=Pt(10); dl.font.color.rgb=INK
        dl.number_format=number_format; dl.number_format_is_linked=False
        if kind in ("pie","doughnut"): dl.position=XL_LABEL_POSITION.OUTSIDE_END
    except Exception:
        pass
    if insight:
        by=Inches(5.72)
        rect(s,Inches(0.85),by,Inches(11.63),Inches(1.1),LIGHT)
        rect(s,Inches(0.85),by,Inches(0.11),Inches(1.1),accent)
        txt(s,Inches(1.15),int(by+Inches(0.12)),Inches(11.1),Inches(0.3),
            [[("WHAT THE DATA SHOWS",11,accent,True)]])
        txt(s,Inches(1.15),int(by+Inches(0.44)),Inches(11.1),Inches(0.6),
            [[(insight,12,INK,False)]])
    footer(s); return s

def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    """Profile-card layout: avatar badge + name/role panel on the left, labelled
    info tiles on the right. rows: list of (LABEL, value); blank value → fill-in line."""
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def activity_overview(tag,title,desc,build,services,kicker,objective=None,test=None):
    """Lab briefing — now a full teaching slide: the tag chip, the description, and a
    3-tile band covering objective / deliverable / toolchain, plus the success test."""
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.88),Inches(1.7),Inches(0.46),TEAL)
    txt(s,Inches(0.85),Inches(1.88),Inches(1.7),Inches(0.46),[[(tag,15,WHITE,True)]],
        align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    if objective:
        txt(s,Inches(2.72),Inches(1.88),Inches(9.7),Inches(0.46),
            [[(objective,12,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    # INTRO PARAGRAPH — shrink to fit its own band so it can never wrap down into
    # the card row painted below it. SHAPE_TO_FIT_TEXT is not honoured by the
    # renderers, so the height is computed here and asserted.
    INTRO_Y=Inches(2.5); INTRO_W=Inches(11.63)
    CARD_Y=Inches(3.86); CARD_H=Inches(2.0)
    intro_h=(CARD_Y-Inches(0.16))-INTRO_Y                # hard ceiling: clear of the cards
    dsz=_fit_size(desc, INTRO_W/914400.0, intro_h/914400.0, 17, min_size=12.0)
    assert _wrapped_h(desc, INTRO_W/914400.0, dsz) <= intro_h/914400.0 + 0.01, \
        f"lab intro overflows into the card row on '{title}'"
    txt(s,Inches(0.85),INTRO_Y,INTRO_W,intro_h,[[(desc,dsz,INK,False)]])

    tiles=[(BLUE,"YOU'LL BUILD",build),(TEAL,"TOOLCHAIN",services),
           (VIOLET,"DONE WHEN",test or "The lab runs end to end without error.")]
    tw=Inches(3.71); xs=[Inches(0.85),Inches(4.81),Inches(8.77)]
    body_w=(tw-Inches(0.45))/914400.0
    body_h=(CARD_H-Inches(0.62))/914400.0                # inner height under the label
    # ONE body size across the three cards — a per-card size reads as a fault.
    bsz=min(_fit_size(b, body_w, body_h, 12, min_size=8.5) for _,_,b in tiles)
    for (col,lbl,body),x in zip(tiles,xs):
        assert _wrapped_h(body, body_w, bsz) <= body_h + 0.01, \
            f"card body '{lbl}' overflows its card on '{title}'"
        rect(s,x,CARD_Y,tw,CARD_H,LIGHT); rect(s,x,CARD_Y,tw,Inches(0.1),col)
        txt(s,x+Inches(0.24),int(CARD_Y+Inches(0.18)),tw-Inches(0.45),Inches(0.3),[[(lbl,11,col,True)]])
        txt(s,x+Inches(0.24),int(CARD_Y+Inches(0.52)),tw-Inches(0.45),int(CARD_H-Inches(0.62)),
            [[(body,bsz,INK,False)]])
    footer(s); return s
def step_slide(kicker,act_title,n,total,text,cmd=""):
    s=head(slide(),act_title,kicker,TEAL)
    oval(s,Inches(0.85),Inches(2.5),Inches(1.4),Inches(1.4),TEAL)
    txt(s,Inches(0.85),Inches(2.74),Inches(1.4),Inches(0.9),[[(str(n),38,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.95),Inches(1.95),Inches(11),Inches(0.4),[[(f"STEP {n} OF {total}",13,GREY,True)]])
    txt(s,Inches(2.55),Inches(2.4),Inches(10.1),Inches(1.3),[[(text,23,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    if cmd:
        rect(s,Inches(2.55),Inches(4.15),Inches(10.1),Inches(0.95),RGBColor(0x0B,0x12,0x20))
        txt(s,Inches(2.8),Inches(4.28),Inches(9.7),Inches(0.7),[[("$ "+cmd,13,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def test_slide(act_title,text,kicker,troubleshoot=None):
    """Verification slide — the success criterion PLUS a troubleshooting band, so it
    teaches diagnosis rather than stating one sentence."""
    s=head(slide(),act_title,kicker,TEAL)
    GREEN=RGBColor(0x12,0x7A,0x3E)
    rect(s,Inches(0.85),Inches(1.95),Inches(11.63),Inches(2.15),RGBColor(0xE8,0xF7,0xEE))
    rect(s,Inches(0.85),Inches(1.95),Inches(0.11),Inches(2.15),GREEN)
    txt(s,Inches(1.2),Inches(2.12),Inches(11),Inches(0.44),[[("✅  Expected result",17,GREEN,True)]])
    txt(s,Inches(1.2),Inches(2.62),Inches(11.0),Inches(1.35),[[(text,15,INK,False)]])
    tb=troubleshoot or [
        ("Nothing happens","Check the .env file is in the labs folder and the key has no quotes or spaces."),
        ("Auth or 401 error","Re-copy the API key from AI Studio; confirm GOOGLE_GENAI_USE_VERTEXAI=0."),
        ("ModuleNotFoundError","Run uv sync again, and prefix commands with uv run so the venv is used."),
    ]
    txt(s,Inches(0.85),Inches(4.32),Inches(11.63),Inches(0.34),
        [[("IF IT DOESN'T WORK",11,AMBER,True)]])
    tw=Inches(3.71); xs=[Inches(0.85),Inches(4.81),Inches(8.77)]
    for i,(sym,fix) in enumerate(tb[:3]):
        x=xs[i]
        rect(s,x,Inches(4.7),tw,Inches(1.72),LIGHT); rect(s,x,Inches(4.7),tw,Inches(0.09),AMBER)
        symsz=_fit_size(sym,(tw-Inches(0.45))/914400.0,0.5,12.5,min_size=9.0)
        fixsz=_fit_size(fix,(tw-Inches(0.45))/914400.0,1.02,11,min_size=8.0)
        txt(s,x+Inches(0.24),Inches(4.84),tw-Inches(0.45),Inches(0.52),[[(sym,symsz,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.24),Inches(5.38),tw-Inches(0.45),Inches(1.04),[[(fix,fixsz,GREY,False)]])
    footer(s); return s
def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); PAGE["n"]+=1


# ============================================================ COURSE-SPECIFIC SLIDES

def lms_download_slide():
    """Download Course Material — a VISUAL browser mock of the LMS portal, not a text link."""
    s=head(slide(),"Download Your Course Material",
           "LMS / TMS  ·  lms-tms.tertiaryinfotech.com",kcolor=BLUE)
    # --- browser chrome mock (left) ---
    bx,by,bw,bh=Inches(0.85),Inches(1.95),Inches(6.55),Inches(4.7)
    rect(s,bx,by,bw,bh,WHITE,line=LINE)
    rect(s,bx,by,bw,Inches(0.52),RGBColor(0xE9,0xEE,0xF5))
    for i,col in enumerate([RGBColor(0xF5,0x6B,0x5F),RGBColor(0xF6,0xBE,0x4F),RGBColor(0x62,0xC5,0x54)]):
        oval(s,int(bx+Inches(0.2)+Inches(0.28)*i),int(by+Inches(0.17)),Inches(0.18),Inches(0.18),col)
    rect(s,int(bx+Inches(1.2)),int(by+Inches(0.12)),int(bw-Inches(1.45)),Inches(0.3),WHITE,line=LINE)
    txt(s,int(bx+Inches(1.34)),int(by+Inches(0.12)),int(bw-Inches(1.6)),Inches(0.3),
        [[("🔒  lms-tms.tertiaryinfotech.com",10,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    # portal header bar
    rect(s,int(bx+Inches(0.01)),int(by+Inches(0.52)),int(bw-Inches(0.02)),Inches(0.62),BLUE)
    txt(s,int(bx+Inches(0.28)),int(by+Inches(0.52)),Inches(4.4),Inches(0.62),
        [[("Tertiary Infotech  ·  LMS / TMS",13,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,int(bx+bw-Inches(1.9)),int(by+Inches(0.52)),Inches(1.6),Inches(0.62),
        [[("My Courses  ▾",10,WHITE,False)]],anchor=MSO_ANCHOR.MIDDLE,align=PP_ALIGN.RIGHT)
    # course card
    cy=int(by+Inches(1.32))
    rect(s,int(bx+Inches(0.28)),cy,int(bw-Inches(0.56)),Inches(0.72),LIGHT)
    rect(s,int(bx+Inches(0.28)),cy,Inches(0.09),Inches(0.72),TEAL)
    txt(s,int(bx+Inches(0.52)),cy,Inches(5.4),Inches(0.72),
        [[("AI for Network Security",13,INK,True)],[(C.COURSE_CODE+"   ·   2 days",10,GREY,False)]],
        anchor=MSO_ANCHOR.MIDDLE,space=2)
    # download rows
    files=[("Trainer Slides",".pptx",BLUE),("Learner Guide",".pdf",TEAL),
           ("Lesson Plan",".pdf",VIOLET),("Labs / Activities","folder",AMBER)]
    ry=int(cy+Inches(0.86))
    for i,(nm,ext,col) in enumerate(files):
        y=int(ry+Inches(0.6)*i)
        rect(s,int(bx+Inches(0.28)),y,int(bw-Inches(0.56)),Inches(0.5),WHITE,line=LINE)
        rect(s,int(bx+Inches(0.4)),int(y+Inches(0.08)),Inches(0.34),Inches(0.34),col)
        txt(s,int(bx+Inches(0.88)),y,Inches(3.3),Inches(0.5),
            [[(nm,11.5,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
        txt(s,int(bx+Inches(4.2)),y,Inches(1.0),Inches(0.5),
            [[(ext,10,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
        dl=rect(s,int(bx+bw-Inches(1.5)),int(y+Inches(0.09)),Inches(1.05),Inches(0.32),col)
        txt(s,int(bx+bw-Inches(1.5)),int(y+Inches(0.09)),Inches(1.05),Inches(0.32),
            [[("Download",9,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    # --- numbered steps (right) ---
    steps=[("1 · Go to the LMS portal","Open lms-tms.tertiaryinfotech.com in your browser."),
           ("2 · Log in","Sign in with the e-mail you used to register for this course."),
           ("3 · Open this course","Select 'AI for Network Security' from your course list."),
           ("4 · Download","Take the Trainer Slides, Learner Guide and Lesson Plan."),
           ("5 · Get the labs","Open labs/ — each lab has its own step-by-step guide."),
           ("6 · Keep them open","You may use these materials in the open-book assessment.")]
    sx,sw=Inches(7.72),Inches(4.76)
    sy=Inches(1.95); sh_=Inches(0.74); gy=Inches(0.055)
    for i,(hd,bd_) in enumerate(steps):
        y=int(sy+(sh_+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,sx,y,sw,sh_,LIGHT); rect(s,sx,y,Inches(0.09),sh_,col)
        txt(s,sx+Inches(0.26),int(y+Inches(0.08)),sw-Inches(0.45),Inches(0.28),[[(hd,11.5,col,True)]])
        txt(s,sx+Inches(0.26),int(y+Inches(0.36)),sw-Inches(0.45),Inches(0.34),[[(bd_,10.5,INK,False)]])
    footer(s); return s


def labs_access_slide():
    """Access the Hands-On Labs — with the GitHub repo URL as a REAL clickable hyperlink."""
    s=head(slide(),"Access the Hands-On Labs","12 LABS  ·  GITHUB REPOSITORY",kcolor=TEAL)
    # repo URL bar with a real hyperlink
    rect(s,Inches(0.85),Inches(1.92),Inches(11.63),Inches(0.78),RGBColor(0x0B,0x12,0x20))
    tb=s.shapes.add_textbox(Inches(1.15),Inches(1.98),Inches(11.1),Inches(0.66))
    tf=tb.text_frame; tf.word_wrap=True
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.LEFT
    r0=p.add_run(); r0.text="⌥  "; r0.font.size=Pt(15); r0.font.color.rgb=TEAL
    r=p.add_run(); r.text=C.REPO_URL
    r.font.size=Pt(15); r.font.name="Consolas"; r.font.bold=True
    r.font.color.rgb=RGBColor(0x9C,0xDC,0xFE)
    r.hyperlink.address=C.REPO_URL
    # two option cards
    opts=[(BLUE,"Option A · Clone with Git",
           ["Open a terminal in the folder you want the labs in.",
            "Run the clone command below.",
            "The labs/ folder appears with one folder per lab."],
           f"git clone {C.REPO_URL}.git"),
          (TEAL,"Option B · Download the ZIP",
           ["Open the repository link above in your browser.",
            "Click the green Code button, then Download ZIP.",
            "Unzip it anywhere on your laptop and open labs/."],
           "")]
    xs=[Inches(0.85),Inches(6.75)]; cw=Inches(5.73)
    for (col,ttl,lines,cmd),x in zip(opts,xs):
        rect(s,x,Inches(3.0),cw,Inches(2.85),LIGHT); rect(s,x,Inches(3.0),cw,Inches(0.11),col)
        txt(s,x+Inches(0.28),Inches(3.2),cw-Inches(0.5),Inches(0.4),[[(ttl,15,col,True)]])
        bullets(s,x+Inches(0.28),Inches(3.72),cw-Inches(0.5),Inches(1.3),
                [(l,0) for l in lines],size=11.5,mcolor=col,gap=7)
        if cmd:
            rect(s,x+Inches(0.28),Inches(5.18),cw-Inches(0.56),Inches(0.5),RGBColor(0x0B,0x12,0x20))
            txt(s,x+Inches(0.44),Inches(5.18),cw-Inches(0.8),Inches(0.5),
                [[("$ "+cmd,9.5,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
    # note band
    rect(s,Inches(0.85),Inches(6.05),Inches(11.63),Inches(0.82),LIGHT)
    rect(s,Inches(0.85),Inches(6.05),Inches(0.11),Inches(0.82),AMBER)
    txt(s,Inches(1.15),Inches(6.17),Inches(11.1),Inches(0.6),
        [[("EVERY LAB IS SELF-CONTAINED  ",11,AMBER,True),
          ("Each labs/lab-NN-*/ folder holds its own step-by-step guide, sample data and expected output. Scan only networks you own or are authorised in writing to test.",11.5,INK,False)]])
    footer(s); return s


def day_timeline_slide():
    """Lesson Plan — a two-column visual day timeline (time chips + session cards),
    replacing what would otherwise be a wall of dashes."""
    s=head(slide(),"Lesson Plan — 2 Days, 8 Training Hours per Day",
           "SCHEDULE  ·  8 instructional hours per day  ·  1-hour lunch + 2 tea breaks",kcolor=BLUE)
    days=[("DAY 1","AI-Assisted Analysis & Risk Planning",BLUE,[
            ("9:30","Welcome, learning outcomes, digital attendance (AM)"),
            ("10:00","Core concepts — network security, the CIA triad, why AI"),
            ("11:30","Topic 1 — Threat & vulnerability analysis (Labs 1–2)"),
            ("13:30","Lunch · digital attendance (PM)"),
            ("14:30","Lab 3 · Topic 2 — Risk assessment & planning"),
            ("16:30","Topic 2 continued (Labs 4–6) · Day 1 recap")]),
          ("DAY 2","Security Measures & Incident Response",TEAL,[
            ("9:30","Day 1 review · digital attendance (AM)"),
            ("9:45","Topic 3 — Designing AI-enhanced security measures"),
            ("11:30","Topic 3 continued (Labs 7–9)"),
            ("13:30","Lunch · digital attendance (PM)"),
            ("14:30","Topic 4 — Incident documentation & response (Labs 10–11)"),
            ("16:15","Lab 12 · recap · TRAQOM · assessment attendance"),
            ("16:45","Briefing for Assessment"),
            ("17:00","WA-SAQ 1 hr, then Case Study 1 hr")])]
    xs=[Inches(0.85),Inches(6.75)]; cw=Inches(5.73)
    for (tag,theme,col,rows),x in zip(days,xs):
        rect(s,x,Inches(1.9),cw,Inches(0.72),col)
        txt(s,x+Inches(0.26),Inches(1.98),cw-Inches(0.5),Inches(0.3),[[(tag,13,WHITE,True)]])
        txt(s,x+Inches(0.26),Inches(2.26),cw-Inches(0.5),Inches(0.3),[[(theme,10.5,WHITE,False)]])
        ry=Inches(2.74); rh=Inches(0.50); gy=Inches(0.055)
        for i,(tm,what) in enumerate(rows):
            y=int(ry+(rh+gy)*i)
            rect(s,x,y,cw,rh,LIGHT); rect(s,x,y,Inches(0.08),rh,col)
            rect(s,x+Inches(0.22),int(y+Inches(0.11)),Inches(0.78),Inches(0.34),col)
            txt(s,x+Inches(0.22),int(y+Inches(0.11)),Inches(0.78),Inches(0.34),
                [[(tm,9.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            wsz=_fit_size(what,(cw-Inches(1.36))/914400.0,0.5,10.5,min_size=8.0)
            txt(s,x+Inches(1.14),y,cw-Inches(1.36),rh,[[(what,wsz,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s


def practice_exam_slide():
    """Practice Exam — exams.tertiaryinfotech.com, with a REAL clickable hyperlink."""
    s=head(slide(),"Practice Exam — Test Yourself Before the Assessment",
           "TEST YOURSELF  ·  exams.tertiaryinfotech.com",kcolor=VIOLET)
    rect(s,Inches(0.85),Inches(1.92),Inches(11.63),Inches(0.78),RGBColor(0x0B,0x12,0x20))
    tb=s.shapes.add_textbox(Inches(1.15),Inches(1.98),Inches(11.1),Inches(0.66))
    tf=tb.text_frame; tf.word_wrap=True
    p=tf.paragraphs[0]
    r0=p.add_run(); r0.text="🎯  "; r0.font.size=Pt(15); r0.font.color.rgb=VIOLET
    r=p.add_run(); r.text=C.EXAM_URL
    r.font.size=Pt(15); r.font.name="Consolas"; r.font.bold=True
    r.font.color.rgb=RGBColor(0x9C,0xDC,0xFE)
    r.hyperlink.address=C.EXAM_URL
    tiles=[("Open the practice exam portal","Go to exams.tertiaryinfotech.com and find the Network Security practice exam."),
           ("Attempt it before the assessment","Sit it under exam conditions — closed book, timed — so the result means something."),
           ("Review every wrong answer","Trace each one back to the slide and Learner Guide section that covers it."),
           ("Re-attempt until consistent","Repeat until you are scoring consistently, not just once."),
           ("It mirrors the knowledge questions","The practice questions rehearse the same K1–K4 knowledge the WA-SAQ assesses."),
           ("It does not replace the labs","The Case Study assesses ability — for that, rebuild the labs, don't re-read them.")]
    xs=[Inches(0.85),Inches(6.75)]; cw=Inches(5.73); th=Inches(1.16); gy=Inches(0.12)
    for i,(hd,bd_) in enumerate(tiles):
        col=PALETTE[i%len(PALETTE)]
        x=xs[i%2]; y=int(Inches(3.05)+(th+gy)*(i//2))
        rect(s,x,y,cw,th,LIGHT); rect(s,x,y,Inches(0.09),th,col)
        txt(s,x+Inches(0.28),int(y+Inches(0.12)),cw-Inches(0.5),Inches(0.34),[[(hd,12,col,True)]])
        txt(s,x+Inches(0.28),int(y+Inches(0.48)),cw-Inches(0.5),Inches(0.58),[[(bd_,11,INK,False)]])
    footer(s); return s


# ---------------------------------------------------------------- per-topic depth
def _t1_ndr():
    tile_grid("Network Detection and Response (NDR)",[
     ("What it is","A platform that applies behavioural AI to network traffic to detect attacker activity that endpoint and perimeter tools miss."),
     ("Reconnaissance","Spots scanning and enumeration — one host suddenly touching many hosts or many ports."),
     ("Credential abuse","Flags an account used from a new device, a new location or at an impossible hour."),
     ("Lateral movement","Detects east-west traffic that crosses a zone boundary it has never crossed before."),
     ("Data staging & exfiltration","Notices collection into an unusual location and outbound volume that breaks the baseline."),
     ("Encrypted traffic","Infers behaviour from flow metadata — timing, volume and direction — without needing to decrypt.")],
     kicker="LO1 · THE ATTACK LIFECYCLE",cols=2,size=13,accent=TEAL)

def _t1_pattern_of_life():
    process_map("Building a 'Pattern of Life' Baseline",[
     ("Observe","Every connection, device and identity"),
     ("Profile","Normal peers, ports, volumes, hours"),
     ("Establish","A per-entity, not global, baseline"),
     ("Compare","Score each new event against it"),
     ("Re-learn","Update as the network legitimately changes")],
     kicker="LO1 · HOW THE MODEL LEARNS NORMAL",color=BLUE,
     synthesis=("WHY PER-ENTITY","A backup server moving 400 GB at 02:00 is normal; a laptop doing it is not. A single global threshold cannot express that — a per-entity baseline can."))

def _t1_attacks():
    tile_grid("The Threat Landscape You Are Defending Against",[
     ("Malware & ransomware","Code that encrypts, steals or destroys — increasingly polymorphic, so its signature changes every build."),
     ("Phishing & social engineering","The most common initial access route; AI-generated lures are now fluent and personalised."),
     ("DDoS","Floods a service until it is unavailable — an attack on the availability leg of the CIA triad."),
     ("Man-in-the-middle","Intercepts or alters traffic in transit; defeated by strong encryption and certificate validation."),
     ("Advanced Persistent Threats","Patient, well-resourced intruders who dwell for months — behaviour analytics is the main way to find them."),
     ("Living off the Land (LOTL)","Uses the built-in admin tools already on the host, so there is no malware file to detect."),
     ("Insider threat","An authorised user acting against the organisation — only detectable as a deviation from their own norm."),
     ("AI-enabled attacks","Adversaries use AI to raise the speed, scale and quality of attacks — defence must match that tempo.")],
     kicker="K2 · WHAT YOU ARE UP AGAINST",cols=2,size=13,accent=AMBER)

def _t1_vuln_priority():
    compare_table("Prioritising Vulnerabilities — Three Approaches",
     ["Approach","How it ranks","Weakness","Verdict"],
     [["CVSS only","By base severity score","Ignores whether it is exploited and what the asset is worth","Necessary, not sufficient"],
      ["CVSS + KEV","Severity, with known-exploited first","Still ignores business context","Much better — free and fast"],
      ["AI-assisted contextual","Predicted exploitability x asset criticality x exposure","Needs a trustworthy asset register","Best — and it is what Lab 3 builds"]],
     kicker="LO1 · A2 · TURNING A SCAN INTO A WORKLIST",accent=VIOLET,
     note="A ranking you cannot explain is a ranking nobody will fund. Whatever method you choose, write the formula down so the order is reproducible.")

def _t2_risk_formula():
    process_map("From Asset to Treated Risk",[
     ("Inventory","Discover and classify every asset"),
     ("Value","Rate C, I and A business impact"),
     ("Assess","Score likelihood x impact"),
     ("Treat","Mitigate, transfer, avoid or accept"),
     ("Monitor","Review on a defined cadence")],
     kicker="LO2 · THE RISK MANAGEMENT CYCLE",color=VIOLET,
     synthesis=("THE DISCIPLINE","Every step produces a named artefact — asset register, impact rating, risk register, treatment plan, review schedule. If a step has no artefact, it did not happen."))

def _t2_matrix():
    compare_table("The 5x5 Risk Matrix — Reading the Score",
     ["Impact ↓ / Likelihood →","1 Rare","2 Unlikely","3 Possible","4 Likely","5 Almost certain"],
     [["5 · Severe","5 Med","10 High","15 Critical","20 Critical","25 Critical"],
      ["4 · Major","4 Low","8 Med","12 High","16 Critical","20 Critical"],
      ["3 · Moderate","3 Low","6 Med","9 Med","12 High","15 Critical"],
      ["2 · Minor","2 Low","4 Low","6 Med","8 Med","10 High"],
      ["1 · Negligible","1 Low","2 Low","3 Low","4 Low","5 Med"]],
     kicker="LO2 · A2 · SCORING CONSISTENTLY",accent=AMBER,
     note="Bands: 1–4 Low · 5–9 Medium · 10–14 High · 15–25 Critical. Agree the bands before you score, or every reviewer will argue the colour instead of the risk.")

def _t2_treatments():
    tile_grid("The Four Risk Treatments",[
     ("Mitigate","Reduce likelihood or impact with a control. The default choice — and the one that costs money."),
     ("Transfer","Shift the financial consequence to someone else, typically insurance or a contractual clause. The risk still happens."),
     ("Avoid","Stop doing the activity that creates the risk — decommission the service, drop the feature, close the port."),
     ("Accept","Consciously carry the risk, with a named accepting authority and a written rationale. Not the same as ignoring it."),
     ("Every risk gets exactly one","A blank treatment column is an unmanaged risk wearing a spreadsheet."),
     ("Residual risk is what remains","After the treatment is applied. If residual still exceeds appetite, the treatment was not enough.")],
     kicker="LO2 · A4 · DECIDING WHAT TO DO",cols=2,size=13,accent=TEAL)

def _t2_frameworks():
    compare_table("Two Frameworks You Will Use Together",
     ["","NIST Cybersecurity Framework 2.0","NIST AI Risk Management Framework"],
     [["Protects","The network and the organisation","The AI system itself"],
      ["Functions","Govern · Identify · Protect · Detect · Respond · Recover","Govern · Map · Measure · Manage"],
      ["You use it to","Structure the control set and find coverage gaps","Structure how you assess and manage AI risk"],
      ["In this course","Lab 6 maps your plan to the six functions","Lab 9 hardens the AI you deployed"],
      ["Why both","Deploying AI to defend the network adds a second thing to defend — the AI","Neither framework covers the other's scope"]],
     kicker="LO2 · K4 · THE PLANNING SCAFFOLD",accent=BLUE,
     note="A plan that secures the network with AI but never assesses the AI's own risk has simply moved the weakest link, not removed it.")

def _t3_defence_depth():
    tile_grid("Defence in Depth — the Three Control Categories",[
     ("Physical controls","Locks, badge access, CCTV, secure racks and cable management. If someone can touch the switch, the rest is negotiable."),
     ("Technical controls","Firewalls, IDS/IPS, encryption, authentication, endpoint protection, segmentation — the controls this course configures."),
     ("Administrative controls","Policies, standards, procedures, training and review. These are what keep the technical controls correct over time."),
     ("Preventive","Stops the event happening — a firewall rule, an access control, patching."),
     ("Detective","Notices that it happened — logging, IDS, anomaly detection, audit."),
     ("Corrective","Restores after it happened — backups, failover, the incident response playbook.")],
     kicker="K3 · LAYERING THE CONTROLS",cols=2,size=13)

def _t3_phases():
    process_map("The Three Phases of Network Security Design",[
     ("Planning","Requirements, risk, constraints, zones"),
     ("Building","Configure, harden, segment, test"),
     ("Management","Monitor, tune, review, change control")],
     kicker="LO3 · A5 · THE PHASE MODEL",color=BLUE,
     synthesis=("A5 IN ONE LINE","Define what the design must achieve (planning), make it real and prove it works (building), and keep it correct as the network changes (management). A design with no management phase decays within a quarter."))

def _t3_zerotrust():
    tile_grid("Segmentation and Zero Trust",[
     ("Why segment","A flat network means one compromised laptop can reach the domain controller. Segmentation makes lateral movement expensive."),
     ("VLANs and subnets","The basic separation — different departments, different functions, different trust levels."),
     ("DMZ","A buffer zone for internet-facing services, so a compromised web server is not inside the internal network."),
     ("Micro-segmentation","Per-workload policy rather than per-subnet — the granular end of the same idea."),
     ("Zero trust","Never trust, always verify. Location on the network stops being a reason to grant access."),
     ("Default deny","The rule that makes segmentation real: allow what is explicitly required, block everything else.")],
     kicker="K3 · SHRINKING THE BLAST RADIUS",cols=2,size=13,accent=TEAL)

def _t3_ai_controls():
    tile_grid("AI-Enhanced Controls You Will Specify",[
     ("AI-powered firewall","Adapts rule sets to observed traffic patterns instead of relying purely on static hand-written rules."),
     ("AI-enhanced IDS/IPS","Learns normal protocol and volume behaviour per segment, so it flags what a static threshold would miss."),
     ("UEBA","User and Entity Behaviour Analytics — profiles each user and device against its own history, not a global norm."),
     ("Adaptive access control","Scores device posture, behaviour, location and time, then steps up authentication or blocks as risk rises."),
     ("NAC with AI classification","Fingerprints and classifies devices as they join, so an unknown device does not silently get a trusted VLAN."),
     ("AI policy optimisation","Recommends rule changes from observed traffic, and finds the shadowed and over-broad rules humans leave behind.")],
     kicker="LO3 · A6 · DEVELOPING THE MEASURES",cols=2,size=13,accent=VIOLET)

def _t3_access_control():
    tile_grid("Access Control, Authentication and Secure Remote Access",[
     ("Least privilege","Every account and service gets the minimum access it needs to do its job — and no more. The single most effective limit on what a compromise can reach."),
     ("Access control models","Discretionary (DAC), Role-Based (RBAC) and Attribute-Based (ABAC). RBAC is the practical default: permissions attach to a role, not to a person."),
     ("ACLs","Access Control Lists on routers and switches enforce which source may reach which destination on which port — the device-level expression of the zone matrix."),
     ("AAA","Authentication, Authorisation and Accounting via RADIUS or TACACS+ — centralises who may log in, what they may do, and what they did."),
     ("Multi-factor authentication (MFA)","Something you know plus something you have or are. It defeats credential stuffing and password reuse, which is how most account takeover starts."),
     ("VPN for remote access","An encrypted tunnel over an untrusted network. Terminate it into a restricted zone with individual accounts and MFA — never a shared account into the flat internal network.")],
     kicker="K3 · CONTROLLING WHO GETS IN",cols=2,size=13,accent=BLUE)


def _t3_adversarial():
    compare_table("NIST AI 100-2 — Attacks Against AI Systems",
     ["Attack class","What the adversary does","Against your NDR model","Primary mitigation"],
     [["Evasion","Crafts input that the deployed model misclassifies","Slows a scan until it falls inside the baseline","Adversarial training; ensemble and rate-independent features"],
      ["Poisoning","Corrupts the training data or the model itself","Seeds 'normal-looking' attack traffic during learning","Data provenance, integrity verification, anomaly checks on training data"],
      ["Privacy","Extracts training data or model details from outputs","Infers your network topology from detection behaviour","Output minimisation, differential privacy, access control"],
      ["Misuse (GenAI)","Abuses a generative model to produce harmful output","Turns your security copilot into a recon assistant","Guardrails, prompt filtering, least-privilege tool access"]],
     kicker="LO3 · SECURING THE AI ITSELF",accent=AMBER,
     note="NIST AI 100-2e2025 covers predictive AI (evasion, poisoning, privacy) and adds misuse for generative AI. MITRE ATLAS maps the same ground as adversary tactics and techniques.")

def _t3_nsa_cisa():
    process_map("NSA / CISA — Deploying AI Systems Securely",[
     ("Secure the environment","Governance, architecture, hardened config"),
     ("Protect the AI system","Validate, encrypt, control access, monitor"),
     ("Secure operation & maintenance","Audit, update, respond, retire safely")],
     kicker="LO3 · A7 · THE JOINT GUIDANCE",color=TEAL,
     synthesis=("THE THREE CATEGORIES","The April 2024 joint Cybersecurity Information Sheet from NSA, CISA, FBI and international partners organises AI deployment security into these three stages. Lab 9 turns them into your hardening checklist."))

def _t3_data_security():
    tile_grid("Protecting the Data Your AI Learns From",[
     ("Provenance tracking","Record where every dataset came from — cryptographically signed, append-only ledgers where the stakes justify it."),
     ("Integrity verification","Cryptographic hashes and checksums on data at rest and in transit, so silent corruption is detectable."),
     ("Digital signatures","Sign dataset revisions so an unauthorised change to training data cannot pass unnoticed."),
     ("Classification & access control","Apply sensitivity-based access to training data, exactly as you would to production data."),
     ("Encryption","Strong encryption in transit and at rest across every stage of the pipeline, not only the final store."),
     ("Continuous assessment","Re-assess data risk on a schedule — data drift degrades a model quietly, without any alert firing.")],
     kicker="LO3 · CISA / NSA AI DATA SECURITY",cols=2,size=13,accent=BLUE)

def _t4_logging():
    tile_grid("Logging — the Evidence Base of Incident Response",[
     ("Syslog","The standard for network devices and Unix hosts; forwards to a central collector over UDP/TCP 514 or TLS."),
     ("Windows Event Log","Security, System and Application channels; forwarded with WEF or an agent to the same collector."),
     ("Flow records","NetFlow, sFlow and IPFIX summarise who talked to whom, when and how much — cheap, and enough for most correlation."),
     ("Firewall & IDS logs","Allow and deny decisions plus signature hits — the boundary record of what tried to cross."),
     ("Time synchronisation","Every source on NTP against the same reference. Skewed clocks make cross-source correlation worthless."),
     ("Retention & integrity","Keep long enough to investigate a slow intrusion, and store so that an attacker with local admin cannot rewrite it.")],
     kicker="LO4 · A7 · WHAT TO LOG AND WHY",cols=2,size=13)

def _t4_siem_soar():
    compare_table("SIEM vs SOAR vs XDR",
     ["","SIEM","SOAR","XDR"],
     [["Primary job","Collect and correlate events into incidents","Execute the response playbook","Detect and respond across layers in one platform"],
      ["Core input","Logs from everywhere","An alert plus a playbook","Endpoint, network, identity and cloud telemetry"],
      ["Core output","A prioritised incident","An action taken automatically","A correlated incident with response built in"],
      ["Where AI helps","Correlation, deduplication, ranking","Deciding which playbook and when","Cross-layer correlation and root cause"],
      ["Human role","Investigate and decide","Approve high-impact actions","Investigate, and own the decision"]],
     kicker="LO4 · K4 · THE OPERATIONS STACK",accent=TEAL,
     note="The names blur between vendors. Judge a platform by what it actually does with your telemetry, not by which of these three words appears on the datasheet.")

def _t4_triage():
    process_map("AI-Assisted Alert Triage",[
     ("Ingest","Raw alerts from every source"),
     ("Deduplicate","Collapse repeats into one with a count"),
     ("Cluster","Group by host, time and campaign"),
     ("Enrich","Add asset value and threat intel"),
     ("Rank","Order by investigation priority")],
     kicker="LO4 · SOLVING THE REAL BOTTLENECK",color=VIOLET,
     synthesis=("WHY THIS MATTERS MOST","Detection is rarely the failure point — the failure is that the true alert was sitting in a queue nobody could read. Triage is where AI returns the most analyst time."))

def _t4_ir_lifecycle():
    process_map("The NIST SP 800-61 Incident Response Lifecycle",[
     ("Preparation","Playbooks, tooling, training, contacts"),
     ("Detection & analysis","Confirm, scope and classify the incident"),
     ("Containment","Stop the spread without destroying evidence"),
     ("Eradication & recovery","Remove the cause, restore, verify"),
     ("Post-incident","Lessons learned feed back into the plan")],
     kicker="LO4 · K4 · THE LIFECYCLE",color=BLUE,
     synthesis=("AI ACCELERATES, IT DOES NOT OWN","AI speeds up detection, scoping and drafting. Classification, containment authority and the lessons-learned judgement stay with a named responder."))

def _t4_documentation():
    tile_grid("What a Defensible Incident Record Contains",[
     ("Identification","Incident ID, detection time, who detected it, who is handling it, current status."),
     ("Evidence-based timeline","Every entry timestamped in UTC with the log line or capture that proves it."),
     ("Classification","Severity, with the written criteria that produced it — so the rating can be reviewed, not just asserted."),
     ("Affected assets","Named from the asset register, with criticality and the data classification each one holds."),
     ("Actions taken","Each with a timestamp and the person who took it, including the options considered and rejected."),
     ("Evidence inventory","Every artefact with its storage location, its hash and who has access to it."),
     ("Notifications","Who was told, when, and which obligations were considered — including PDPA notification to the PDPC where engaged."),
     ("Lessons learned","What detected it, what delayed the response, and the one control change that goes back into the plan.")],
     kicker="LO4 · A8 · THE DELIVERABLE",cols=2,size=13,accent=AMBER)

def _t4_automation_boundary():
    decision_map("Can This Response Step Be Automated?",
     "Is the action\nreversible, and is its\nblast radius smaller\nthan the incident?",
     ("YES — automate it","Block a single source address, quarantine one file, expire one session, raise an alert. Fast, reversible, contained."),
     ("NO — require approval","Isolate a production server, disable an executive's account, block an entire subnet. A named person approves."),
     kicker="LO4 · A9 · THE HUMAN-IN-THE-LOOP BOUNDARY",
     note="Ask the question before the incident, not during it. An automated action that takes a hospital's patient system offline to stop a low-severity alert is itself the incident.")

TOPIC_EXTRAS = {
 1:[_t1_attacks,_t1_pattern_of_life,_t1_ndr,_t1_vuln_priority],
 2:[_t2_risk_formula,_t2_matrix,_t2_treatments,_t2_frameworks],
 3:[_t3_defence_depth,_t3_phases,_t3_zerotrust,_t3_access_control,_t3_ai_controls,_t3_adversarial,_t3_nsa_cisa,_t3_data_security],
 4:[_t4_logging,_t4_siem_soar,_t4_triage,_t4_ir_lifecycle,_t4_documentation,_t4_automation_boundary],
}



# ---------------- build-time guards ----------------
# A chip label cut mid-sentence reads as a complete instruction and misleads the
# learner. Fail the build rather than ship one.
_STOPWORDS={"a","an","the","of","to","in","on","for","from","with","and","or","by",
            "into","at","as","is","are","that","this","your","you","it","its","be",
            "so","if","when","than","then","each","every","only","not","no"}
def _assert_labels_whole():
    bad=[]
    for _a in ACTIVITIES:
        for _lbl in (_a.get("stages") or []):
            _last=_lbl.rstrip(".").split()[-1].lower() if _lbl.split() else ""
            if _last in _STOPWORDS or "…" in _lbl or len(_lbl) > 34:
                bad.append((_a["num"], _lbl))
    if bad:
        raise SystemExit("BUILD FAILED — truncated or over-long process-map labels:\n" +
                         "\n".join(f"  Lab {n}: {l!r}" for n,l in bad))
_assert_labels_whole()

# ============================================================ BUILD
cover()

# ---------------- ADMIN ----------------
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
tile_grid("Digital Attendance (Mandatory)",[
 ("Three times a day","Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR","The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit","Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum","A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role","Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise","Network security, cybersecurity, applied machine learning and secure infrastructure design."),
  ("Certification","CompTIA Security+ ce · AWS Certified Machine Learning Engineer · AWS Solutions Architect · AWS AI Practitioner."),
  ("Delivers","WSQ courses on AI for network security, cybersecurity, ethical hacking and IT infrastructure."),
  ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA",accent=BLUE)
content("Let's Know Each Other",[
 "Your name, organisation and role.",
 "Your experience with networking, IT operations or security (if any).",
 "Any experience you already have with AI or machine-learning tools.",
 "What you would like to be able to detect, defend or automate after this course."],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
lms_download_slide()
tile_grid("Skills Framework Alignment",[
 ("TSC Title", C.TSC_TITLE),
 ("TSC Code", C.TSC_CODE),
 ("K1 / K2", "ICT networks and their configuration; types of network attacks, vulnerabilities and related weaknesses."),
 ("K3 / K4", "Types and techniques of network security measures; risk management plans and procedures."),
 ("A1 – A4", "Identify threats, analyse security risks, determine assets requiring protection and create risk management plans."),
 ("A5 – A9", "Define security phases, develop measures, design auditing and IR procedures, document incidents and implement configurations.")],
 kicker="SKILLS FRAMEWORK  ·  "+C.TSC_CODE,cols=2,size=13,accent=VIOLET)
day_timeline_slide()
tile_grid("Learning Outcomes", C.LO_TILES,
 kicker="WHAT YOU'LL ACHIEVE",cols=2,size=15)
tile_grid("Course Outline",[
 (f"Topic {t['code']} — {t['title']}", t["subtitle"]) for t in C.TOPICS],
 kicker="FOUR TOPICS  ·  12 HANDS-ON LABS",cols=1,size=15)
tile_grid("Briefing for Assessment",[
 ("Do · Clear your desk","Place phones and other materials under the table or on the floor."),
 ("Don't · No recording","No photos or recording of assessment scripts."),
 ("Don't · No discussion","Work individually — no discussion during the assessment."),
 ("Do · Black or blue pen","Use a black or blue pen for hard-copy assessments."),
 ("Don't · No correction fluid","No liquid paper or correction tape may be used."),
 ("Do · Stop on time","Scripts are collected when time is up.")],
 kicker="BEFORE YOU START",cols=2,size=14,accent=AMBER)
tile_grid("Assessment",[
 ("Written Assessment (WA-SAQ)","Short-Answer Questions · 1 hour · open book. Tests the underpinning knowledge K1–K4."),
 ("Case Study (CS)","A realistic organisational scenario · 1 hour · open book. Tests the abilities A1–A9."),
 ("Open book","You may use the course slides, the Learner Guide and approved materials only."),
 ("Eligibility","A minimum of 75% attendance is required to be eligible for assessment and funding."),
 ("Result","You are assessed as Competent (C) or Not Yet Competent (NYC) on each instrument."),
 ("Appeals","An appeal process is available if you wish to contest an assessment outcome.")],
 kicker="FINAL ASSESSMENT",cols=2,size=14)
process_map("Assessment Flow",[
 ("TRAQOM survey","Scan the QR code on the LMS"),
 ("Digital attendance","Scan the SSG assessment QR"),
 ("Sit WA then CS","Open book · 1 hour each"),
 ("Submit on the LMS","Upload your completed answers"),
 ("Sign the record","Sign the Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY",color=BLUE,
 synthesis=("REMEMBER","All five steps are mandatory for WSQ funding — missing the digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Criteria for Funding",[
 ("Attendance","A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
 ("Assessment","Complete both assessment components and be assessed as 'Competent'."),
 ("Digital attendance","Scan the SSG QR code for AM, PM and Assessment on every training day."),
 ("TRAQOM survey","Complete the mandatory TRAQOM course feedback survey on the LMS.")],
 kicker="WSQ FUNDING",cols=2,size=15,accent=AMBER)
tile_grid("Set Up Before We Start",[(n,d) for n,d in C.LAB_TOOLS],
 kicker="LAB ENVIRONMENT",cols=2,size=14,accent=TEAL)
labs_access_slide()
tile_grid("Interactive Practice Tools",[(n,d) for n,d in C.BROWSER_TOOLS],
 kicker="BROWSER TOOLS USED IN THE LABS",cols=2,size=13,accent=VIOLET)

# ---------------- CORE CONCEPTS ----------------
section("CORE CONCEPTS","Network Security, and Why It Now Needs AI","")
tile_grid("What Is Network Security?",[
 ("A combination of controls","The policies, processes and technologies that protect a network and the data crossing it from unauthorised access, misuse and disruption."),
 ("Layered, not a single tool","Defence in depth: many coordinated layers, so that if one control fails another still stops the attacker."),
 ("Protects data everywhere","Data at rest, data in transit and data in processing — plus the infrastructure and the people using it."),
 ("The first line of defence","Detect threats, locate the attack, block access, encrypt the data and keep the network available.")],
 kicker="THE BIG IDEA",cols=2,size=15)
tile_grid("The CIA Triad — the Three Goals of Security",[
 ("Confidentiality","Only authorised parties can read the data — delivered by encryption, access control and strong authentication."),
 ("Integrity","Data is not altered without detection — delivered by cryptographic hashing, digital signatures and validation checks."),
 ("Availability","Services stay up and reachable — delivered by DDoS protection, redundancy and resilient design."),
 ("Every control serves the triad","When you evaluate any security control, ask which of the three goals it protects — and at what cost to the others.")],
 kicker="THE FRAMEWORK BEHIND EVERY CONTROL",cols=2,size=15,accent=TEAL)
tile_grid("The Language of Networks",[
 ("Host and endpoint","Any device with an address on the network — a laptop, a server, a phone, a camera, a sensor."),
 ("Switch and router","Switches move frames inside a segment; routers move packets between segments and enforce the boundary."),
 ("Firewall","The policy enforcement point between zones — it decides which traffic is allowed to cross."),
 ("Port and service","A service listens on a port; an open port is a door, and every open door is an entry to defend."),
 ("Protocol","The agreed rules for an exchange — HTTP, DNS, SMB, SSH. Some encrypt by default and some do not."),
 ("Segment and zone","A group of hosts with a shared trust level; the boundary between zones is where control is applied.")],
 kicker="SHARED VOCABULARY",cols=2,size=14)
big_statement("Attacks now move at machine speed. Defence cannot stay manual.",
 "Signature matching only finds what someone has already named — and an analyst can only read so many alerts an hour. Artificial intelligence closes both gaps.",
 "WHY AI, WHY NOW",color=BLUE)
compare_table("Traditional Detection vs AI-Driven Detection",
 ["Dimension","Signature-based","AI / behavioural"],
 [["What it matches","A known pattern in a threat database","A deviation from learned normal behaviour"],
  ["Zero-day exploits","Structurally cannot detect — no signature exists","Can detect, because the behaviour is still abnormal"],
  ["Polymorphic malware","Easily evaded by changing the pattern","Harder to evade — the behaviour must also change"],
  ["False positives","Low on known threats, blind to the rest","Higher initially; falls as the model is tuned"],
  ["Analyst effort","Manual triage of every alert","Deduplicated, clustered and ranked before a human sees it"],
  ["Explainability","Excellent — the rule says exactly why","Varies — this is why explainability is a requirement, not a nicety"]],
 kicker="LO1 · THE CORE COMPARISON",accent=BLUE,
 note="Neither replaces the other. Signatures give precision on named threats; AI gives coverage of the unnamed. A mature operation runs both.")
process_map("How AI Anomaly Detection Works",[
 ("Collect","Traffic, logs, flows and identity events"),
 ("Learn","Build the pattern of life baseline"),
 ("Score","Measure deviation from that baseline"),
 ("Correlate","Join with asset value and threat intel"),
 ("Act","Rank, alert, or contain automatically")],
 kicker="THE DETECTION PIPELINE",color=TEAL,
 synthesis=("THE POINT","The model never learns what an attack is — it learns what normal is, and reports what fails to fit. That is why it can catch a threat nobody has named yet."))
tile_grid("Where AI Is Applied in Network Security",[
 ("AI network monitoring","Real-time visibility across hybrid and multi-cloud estates; surfaces misconfigurations and vulnerable assets."),
 ("Anomaly detection","Learns normal activity and flags deviations in real time — unusual logins, odd hours, unexpected data volumes."),
 ("AI threat detection","Correlates logs, flows and user behaviour to spot malware, ransomware and multi-stage attacks."),
 ("Automated response (SOAR)","Isolates a host, revokes a credential or blocks an address in seconds, cutting mean time to remediate."),
 ("Vulnerability prioritisation","Predicts exploitability and business impact, turning a long scan report into a ranked worklist."),
 ("Adaptive access control","Scores device, behaviour, location and time, and steps up authentication when risk rises."),
 ("Phishing detection (NLP)","Reads tone and wording for social-engineering markers; computer vision spots fake login pages."),
 ("GenAI security copilots","Answer questions in natural language, summarise intelligence and draft incident reports.")],
 kicker="EIGHT APPLICATIONS",cols=2,size=13,accent=VIOLET)
chart_slide("Where Course Time Goes — Topic Weighting",
 ["Topic 01 — Threat & Vulnerability Analysis",
  "Topic 02 — Risk Assessment & Planning",
  "Topic 03 — Designing & Implementing Measures",
  "Topic 04 — Incident Documentation & Response"],
 [("Share of course (%)",[int(str(t["weighting"]).replace("%","")) for t in C.TOPICS])],
 kicker="LESSON PLAN · TIME ALLOCATION",accent=BLUE,kind="column",
 insight="Topic 3 carries the largest weighting because designing and implementing the security measures is where most of the assessable practical ability (A5–A7) sits — plan your revision accordingly.",
 number_format='0"%"')
chart_slide("Enterprise Adoption of AI-Augmented Security Platforms",
 ["2023","2026 (Gartner forecast)"],
 [("Organisations using AI-augmented security automation (%)",[20,60])],
 kicker="THE INDUSTRY SHIFT",accent=TEAL,kind="column",
 insight="Gartner forecasts that over 60% of organisations will rely on cybersecurity platforms with AI-augmented automation in 2026, up from under 20% in 2023 — AI in the SOC has moved from novelty to baseline expectation.",
 number_format='0"%"')
tile_grid("What AI Does NOT Do",[
 ("It does not remove the analyst","AI assists, it does not replace. Context, judgement and accountability stay human."),
 ("It does not explain itself for free","If you cannot say why the model flagged something, you cannot defend the decision. Demand explainability."),
 ("It is not immune to attack","Evasion, poisoning, privacy and misuse attacks target the model itself — we cover these in Topic 3."),
 ("It does not fix bad data","A model trained on incomplete or skewed logs will confidently produce incomplete or skewed results."),
 ("It does not own the decision","Destructive or wide-blast-radius actions need a named human approver, every time."),
 ("It does not stay accurate by itself","Models drift as the network changes; retraining and revalidation are operational work, not a one-off.")],
 kicker="SETTING EXPECTATIONS HONESTLY",cols=2,size=14,accent=AMBER)
decision_map("Should This Detection Be a Rule or a Model?",
 "Can you write down\nexactly what the\nbad behaviour\nlooks like?",
 ("YES — write a rule","A signature or a threshold rule gives precision, an instant explanation, and no training data. Use it for known, well-defined patterns."),
 ("NO — train a model","When 'bad' is only definable as 'not normal', use a behavioural model. Accept that it needs a baseline, tuning and explainability work."),
 kicker="LO1 · DESIGN DECISION",
 note="Most real detections need both: the rule catches the named threat cheaply, the model covers the space of threats nobody has named yet.")

# ---------------- TOPICS + ACTIVITIES ----------------
TOPIC_ACTS = {t["num"]: [a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}
CARD_COLORS=[BLUE,TEAL,VIOLET]
for t in C.TOPICS:
    section(f"TOPIC {t['code']}", t["title"], t["code"], t["subtitle"])
    tile_grid(f"Topic {t['code']} — What It Covers and How It Is Assessed",[
      ("Learning outcome", " · ".join(t["los"])+" — "+[lo for lo in C.LEARNING_OUTCOMES if lo.startswith(t["los"][0])][0].split(": ",1)[1]),
      ("Knowledge assessed (WA-SAQ)", " · ".join(f"{k}: {dict(C.KNOWLEDGE)[k]}" for k in t["ks"])),
      ("Abilities assessed (Case Study)", " · ".join(f"{a}: {dict(C.ABILITIES)[a]}" for a in t["abil"])),
      ("Hands-on labs", "Labs "+", ".join(str(a["num"]) for a in TOPIC_ACTS[t["num"]])+f" — {t['weighting']} of course time.")],
      kicker=f"TOPIC {t['code']} · ROADMAP",cols=1,size=13,accent=VIOLET)
    cons=t["concepts"]
    half=(len(cons)+1)//2
    for ci,chunk in enumerate([cons[:half],cons[half:]]):
        if not chunk: continue
        suffix="" if ci==0 else " (continued)"
        tile_grid(f"Key Concepts — Topic {t['code']}{suffix}", chunk,
                  kicker=f"TOPIC WEIGHTING {t['weighting']}", cols=2, size=14)
    for extra in TOPIC_EXTRAS.get(t["num"],[]):
        extra()
    acts=TOPIC_ACTS[t["num"]]
    cards=[]
    for gi,a in enumerate(acts[:3]):
        cards.append((CARD_COLORS[gi], f"Lab {a['num']}",
                      [a["title"], "", a["objective"].split("—",1)[-1].strip()[:120]]))
    cards3(f"Hands-On Labs — Topic {t['code']}", cards, kicker="WHAT YOU'LL DO")
    for a in acts:
        activity_overview(f"LAB {a['num']}", a["title"], a["desc"], a["build"], a["services"],
                          kicker=f"TOPIC {t['code']} · HANDS-ON",
                          objective=a.get("objective"), test=a.get("test"))
        # Stage labels are AUTHORED in data_domainN.py ("stages"), never derived by
        # truncating a step sentence — a silently cut label reads as if it were the
        # whole instruction. The build asserts this below.
        names=a.get("stages") or []
        stg=[]
        for i,(stext,scmd) in enumerate(a["steps"][:5]):
            lbl=names[i] if i < len(names) else stext.split(".")[0].strip()
            stg.append((lbl, "with a command" if scmd else "discussion step"))
        if len(stg)>=3:
            process_map(f"How Lab {a['num']} Runs", stg,
                        kicker=f"LAB {a['num']} · PROCESS MAP", color=TEAL,
                        synthesis=("THE POINT", a["objective"]))
        allsteps=a["steps"]
        # Balance the split instead of filling 5 and spilling the remainder: an
        # 11-step lab must not end on a single-step slide with 70% empty space.
        import math as _m
        CH=5
        nchunk=max(1,_m.ceil(len(allsteps)/CH))
        base,extra=divmod(len(allsteps),nchunk)
        chunks=[];  _i=0
        for _c in range(nchunk):
            take=base+(1 if _c<extra else 0)
            chunks.append(allsteps[_i:_i+take]); _i+=take
        assert not any(len(c)<2 for c in chunks) or len(allsteps)<2, \
            f"orphan step slide in a lab with {len(allsteps)} steps"
        for ci,ch in enumerate(chunks):
            steps_slide(a["title"], ch, kicker=f"LAB {a['num']} · PROCEDURE",
                        part=(f"Part {ci+1}/{len(chunks)}" if len(chunks)>1 else None),
                        start=sum(len(x) for x in chunks[:ci])+1)
        tb=a.get("troubleshoot")
        tb_tiles=None
        if tb:
            parts=[p.strip() for p in tb.split(". ") if p.strip()]
            tb_tiles=[]
            for p in parts[:3]:
                if "—" in p:
                    sym,fix=p.split("—",1)
                elif " - " in p:
                    sym,fix=p.split(" - ",1)
                else:
                    sym,fix=p[:40],p
                tb_tiles.append((sym.strip(), fix.strip().rstrip(".")+"."))
        test_slide(a["title"], a["test"], kicker=f"LAB {a['num']} · VERIFY", troubleshoot=tb_tiles)
    tile_grid(f"Recap — Topic {t['code']}",
      [(f"Lab {a['num']} — {a['title']}", a["objective"].split("—",1)[-1].strip()) for a in acts],
      kicker="TOPIC RECAP", cols=1, size=14, accent=TEAL)

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Achieved",[
 ("LO1 · Threats & vulnerabilities","Mapped an ICT network and read its configuration, baselined normal traffic, trained an anomaly model, and produced a prioritised vulnerability worklist."),
 ("LO2 · Assets & risk plans","Built a classified asset register, scored a risk register with AI-challenged likelihoods, and produced a risk management plan mapped to the NIST CSF."),
 ("LO3 · Security measures","Designed a three-phase segmented architecture, implemented a default-deny ruleset with tuned detections, and hardened the AI itself against adversarial attack."),
 ("LO4 · Incidents & response","Specified logging, triaged alerts with AI, documented an incident to evidentiary standard, and implemented and tested a response playbook.")],
 kicker="LEARNING OUTCOMES",cols=2,size=13)
tile_grid("Continue Your Learning",[
 ("NIST Cybersecurity Framework 2.0","https://www.nist.gov/cyberframework — the reference for Govern, Identify, Protect, Detect, Respond and Recover."),
 ("NIST AI 100-2 Adversarial ML","https://csrc.nist.gov/pubs/ai/100/2/e2025/final — the taxonomy of attacks against AI systems."),
 ("NSA/CISA Deploying AI Systems Securely","https://www.cisa.gov/ai — the joint guidance you applied in Lab 9."),
 ("MITRE ATLAS","https://atlas.mitre.org/ — adversary tactics and techniques targeting AI systems, with real case studies."),
 ("CISA Known Exploited Vulnerabilities","https://www.cisa.gov/known-exploited-vulnerabilities-catalog — the KEV list you used to prioritise."),
 ("Rebuild the labs","Redo each lab on your own network with written authorisation, until the workflow is automatic.")],
 kicker="NEXT STEPS",cols=2,size=13)
practice_exam_slide()
tile_grid("Recommended Courses",[
 ("WSQ - Network Securities for Beginners","Build the underlying networking and security foundations if you want more depth on the fundamentals."),
 ("WSQ - Ethical Hacking and Penetration Testing","Learn to test your own defences the way an attacker would."),
 ("WSQ - Machine Learning with Python","Go deeper on the models behind the anomaly detection you built in Labs 2 and 9."),
 ("WSQ - Cybersecurity Incident Response","Extend Topic 4 into a full incident-response and digital-forensics capability.")],
 kicker="CONTINUE WITH TERTIARY INFOTECH",cols=1,size=14)
tile_grid("Support",[
 ("Email","enquiry@tertiaryinfotech.com"),
 ("Telephone","+65 6100 0613"),
 ("Website","www.tertiarycourses.com.sg"),
 ("LMS / TMS","lms-tms.tertiaryinfotech.com"),
 ("Practice exam","exams.tertiaryinfotech.com"),
 ("Course labs","github.com/tertiarycourses/TGS-2024051414-AI-for-Network-Security")],
 kicker="WE'RE HERE TO HELP  ·  DURING AND AFTER THE CLASS",cols=2,size=14)
tile_grid("Assessment",[
 ("Written Assessment (WA-SAQ)","1 hour · open book · short-answer knowledge questions covering K1–K4."),
 ("Case Study (CS)","1 hour · open book · a realistic organisational scenario covering A1–A9."),
 ("Digital attendance","Remember to take the Assessment digital attendance (TRAQOM) before you start."),
 ("Submit on the LMS","Upload your completed answers at https://lms-tms.tertiaryinfotech.com/")],
 kicker="WRAP-UP",cols=2,size=15)
process_map("Assessment Flow",[
 ("TRAQOM survey","Scan the QR code on the LMS"),
 ("Digital attendance","Scan the SSG assessment QR"),
 ("Sit WA then CS","Open book · 1 hour each"),
 ("Submit on the LMS","Upload your completed answers"),
 ("Sign the record","Sign the Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY",color=BLUE,
 synthesis=("REMEMBER","All five steps are mandatory for WSQ funding — missing the digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Digital Attendance (Mandatory)",[
 ("Three times a day","Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR","The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit","Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum","A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
big_statement("Thank You!","You can now apply AI to network threat analysis, risk management, security design and incident response — and defend the AI itself.","STAY SECURE",color=TEAL)

# ---------------- restrained motion pass ----------------
DIVIDER_IDS=set()
for s in prs.slides:
    txts=[sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
    joined=" ".join(txts)
    is_div=any(k in joined for k in ("COURSE ADMINISTRATION","CORE CONCEPTS","WRAP-UP")) or \
           any(t["title"] in joined and f"TOPIC {t['code']}" in joined for t in C.TOPICS)
    _transition(s,"push" if is_div else "fade",speed="fast" if not is_div else "med")

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides._sldIdLst)} slides)")
