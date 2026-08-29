#!/usr/bin/env python3
"""Generate the AI for Network Security (TGS-2024051414) Lesson Plan (LP) DOCX, Tertiary house format.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded 2-day schedule tables (9:00am-6:00pm, 8 training hours/day, 1h
lunch, tea excluded; the final assessment sits at the end of Day 2). Topics/labs come from
course_data + the domain data files so the LP stays aligned with the deck,
guide and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"; ASSESS_FILL="E8F7EE"

def lab_titles(nums):
    return "; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT if a['num'] in nums)


def _deck_lab_slides():
    """Read the CURRENT deck and map each lab number -> the slide its briefing sits on.
    Derived at build time so the LP's slide references can never drift from the PPT."""
    import glob, re as _re
    try:
        from pptx import Presentation
    except ImportError:
        return {}
    cands = sorted(glob.glob(os.path.join(REPO, "courseware", "*.pptx")))
    if not cands:
        return {}
    deck = Presentation(cands[0])
    out = {}
    for i, sl in enumerate(deck.slides, 1):
        for sh in sl.shapes:
            if sh.has_text_frame:
                _t = sh.text_frame.text.strip()
                m = _re.fullmatch(r"LAB (\d+)", _t)
                if m and int(m.group(1)) not in out:
                    out[int(m.group(1))] = i          # briefing slide = block START
                v = _re.fullmatch(r"LAB (\d+) · VERIFY", _t)
                if v:
                    out[("end", int(v.group(1)))] = i  # VERIFY slide = block END
    return out


LAB_SLIDE = _deck_lab_slides()


def _deck_title_slides():
    """Map a slide TITLE -> its slide number in the current deck, so the LP's
    non-lab slide references also derive from the PPT and cannot drift."""
    import glob
    try:
        from pptx import Presentation
    except ImportError:
        return {}
    cands = sorted(glob.glob(os.path.join(REPO, "courseware", "*.pptx")))
    if not cands:
        return {}
    deck = Presentation(cands[0])
    out = {}
    for i, sl in enumerate(deck.slides, 1):
        texts = [sh.text_frame.text.strip() for sh in sl.shapes
                 if sh.has_text_frame and sh.text_frame.text.strip()]
        if len(texts) > 1:
            key = texts[1].split("\n")[0].strip()
            out.setdefault(key, i)          # first occurrence
            out["LAST:" + key] = i          # last occurrence (admin block repeats at the end)
    return out


TITLE_SLIDE = _deck_title_slides()


def _at(title, fallback=""):
    n = TITLE_SLIDE.get(title)
    return str(n) if n else fallback


def _num(title, fallback):
    return TITLE_SLIDE.get(title, fallback)


def _span(first, last, fallback=""):
    a, b = TITLE_SLIDE.get(first), TITLE_SLIDE.get(last)
    return f"{a}-{b}" if a and b else fallback


def lab_slides(nums):
    """'Slides 41-56' — from the FIRST lab's briefing to the LAST lab's VERIFY slide.
    Using the last briefing as the range end silently dropped a third of each topic's
    hands-on slides, so the end bound is resolved explicitly."""
    starts = [LAB_SLIDE[n] for n in nums if n in LAB_SLIDE]
    ends = [LAB_SLIDE[("end", n)] for n in nums if ("end", n) in LAB_SLIDE]
    if not starts:
        return ""
    first = min(starts)
    last = max(ends) if ends else max(starts)
    return f"Slides {first}-{last}" if last > first else f"Slide {first}"

# ------------------------------------------------ schedule (single source of truth for timing)
# (start, end, minutes, kind, activity_text)  kind: admin/topic/lab/break/lunch/assess/recap
SCHEDULE = {
 1: ("AI-Assisted Threat & Vulnerability Analysis · AI-Powered Risk Assessment and Management Planning", [
    ("9:30","10:00",30,"admin","Welcome, course introduction, ground rules, learning outcomes and mandatory digital attendance (AM)"),
    ("10:00","11:15",75,"topic","Core concepts — network security and the CIA triad; why signature-based detection fails against zero-day, polymorphic and Living-off-the-Land attacks; where AI is applied in network security (concepts + demo)"),
    ("11:15","11:30",15,"break","Tea break"),
    ("11:30","13:30",120,"lab","Topic 1 — AI-Assisted Network Threat and Vulnerability Analysis: ICT networks and configuration (K1), the threat landscape (K2), pattern-of-life baselines, NDR and AI vulnerability prioritisation (concepts). Hands-on: "+lab_titles([1,2])),
    ("13:30","14:30",60,"lunch","Lunch break"),
    ("14:30","16:15",105,"lab","Hands-on: "+lab_titles([3])+". Topic 2 — AI-Powered Network Risk Assessment and Management Planning: asset discovery and classification, CIA business impact (concepts)"),
    ("16:15","16:30",15,"break","Tea break"),
    ("16:30","19:00",150,"lab","Topic 2 continued — risk scoring on the 5x5 matrix, the four treatments, NIST CSF 2.0 and the NIST AI RMF (concepts). Hands-on: "+lab_titles([4,5,6])+". Day 1 recap, Q&A and PM digital attendance"),
 ]),
 2: ("Designing & Implementing AI-Enhanced Security Measures · AI-Assisted Incident Documentation and Response", [
    ("9:30","9:45",15,"recap","Day 1 recap and mandatory digital attendance (AM)"),
    ("9:45","11:15",90,"topic","Topic 3 — Designing and Implementing AI-Enhanced Network Security Measures: defence in depth and the three control categories; the planning, building and management phases; segmentation, zero trust and access control (K3, concepts + demo)"),
    ("11:15","11:30",15,"break","Tea break"),
    ("11:30","13:30",120,"lab","Topic 3 continued — AI-enhanced firewalls, IDS/IPS, UEBA and adaptive access control; securing the AI itself (NIST AI 100-2 attack taxonomy, NSA/CISA deployment guidance, MITRE ATLAS). Hands-on: "+lab_titles([7,8,9])),
    ("13:30","14:30",60,"lunch","Lunch break"),
    ("14:30","16:00",90,"lab","Topic 4 — AI-Assisted Security Incident Documentation and Response: logging and audit design, SIEM/SOAR, AI alert triage, the NIST SP 800-61 lifecycle and incident documentation standards (K4, concepts). Hands-on: "+lab_titles([10,11])),
    ("16:00","16:15",15,"break","Tea break"),
    ("16:15","16:45",30,"lab","Hands-on: "+lab_titles([12])+". Course recap, TRAQOM survey and assessment digital attendance"),
    ("16:45","17:00",15,"assess","Briefing for Assessment"),
    ("17:00","18:00",60,"assess","Written Assessment — Short-Answer Questions (WA-SAQ), 1 hour, open book. Assesses the underpinning knowledge K1-K4"),
    ("18:00","19:00",60,"assess","Case Study (CS), 1 hour, open book. Assesses the abilities A1-A9 against a realistic organisational scenario"),
 ]),
}

# ------------------------------------------------ slide references per schedule row
# Keyed by (day, start time). Lab rows resolve from the live deck via lab_slides(); the
# concept/admin rows carry the fixed admin + core-concept slide ranges of the deck.
SLIDE_REF = {
 (1,"9:30"):  "1-" + str(_num("Interactive Practice Tools", 19)),
 (1,"10:00"): _span("Network Security, and Why It Now Needs AI","Should This Detection Be a Rule or a Model?","20-31"),
 (1,"11:15"): "",
 (1,"11:30"): _at("AI-Assisted Network Threat and Vulnerability Analysis","32") + "-" + str((LAB_SLIDE.get(3,51) - 1) if LAB_SLIDE else 50),
 (1,"13:30"): "",
 (1,"14:30"): (str(LAB_SLIDE.get(3,51)) + "-" + str(LAB_SLIDE.get(4,66) - 1)) if LAB_SLIDE else "51-65",
 (1,"16:15"): "",
 (1,"16:30"): (str(LAB_SLIDE.get(4,66)) + "-" + str(_num("Designing and Implementing AI-Enhanced Network Security Measures", 82) - 1)) if LAB_SLIDE else "66-81",
 (2,"9:30"):  "",
 (2,"9:45"):  (_at("Designing and Implementing AI-Enhanced Network Security Measures","82") + "-" + str(LAB_SLIDE.get(7,95) - 1)) if LAB_SLIDE else "82-94",
 (2,"11:15"): "",
 (2,"11:30"): (str(LAB_SLIDE.get(7,95)) + "-" + str(_num("AI-Assisted Security Incident Documentation and Response", 113) - 1)) if LAB_SLIDE else "95-112",
 (2,"13:30"): "",
 (2,"14:30"): (_at("AI-Assisted Security Incident Documentation and Response","113") + "-" + str(LAB_SLIDE.get(12,135) - 1)) if LAB_SLIDE else "113-134",
 (2,"16:00"): "",
 (2,"16:15"): (str(LAB_SLIDE.get(12,135)) + ", " + _span("Course Summary & Next Steps","Support","142-147")) if LAB_SLIDE else "135, 142-147",
 (2,"16:45"): _at("Briefing for Assessment","13"),
 (2,"17:00"): _span("LAST:Assessment","LAST:Assessment Flow","152-153"),
 (2,"18:00"): _span("LAST:Assessment","LAST:Digital Attendance (Mandatory)","152-154"),
}

# The assessment start time is READ from the schedule, so this sentence can never
# contradict the table underneath it.
def _first_assess_start():
    for _day in sorted(SCHEDULE):
        for _st,_en,_m,_k,_t in SCHEDULE[_day][1]:
            # the BRIEFING is an assess-kind row but is not the assessment itself —
            # the sentence must name when the first paper actually starts.
            if _k == "assess" and "Briefing" not in _t:
                _h,_mm = _st.split(":")
                _h = int(_h)
                _suffix = "am" if _h < 12 else "pm"
                _h12 = _h if 1 <= _h <= 12 else (_h - 12 if _h > 12 else 12)
                return f"{_h12}:{_mm} {_suffix}"
    return "the end of the day"
_ASSESS_START = _first_assess_start()


# ------------------------------------------------ slide-reference sanity guard
# Auto-derived references fail silently by producing plausible-looking wrong
# numbers, so every emitted reference is range-checked against the live deck.
def _assert_slide_refs():
    import glob, re as _re
    try:
        from pptx import Presentation
    except ImportError:
        return
    cands = sorted(glob.glob(os.path.join(REPO, "courseware", "*.pptx")))
    if not cands:
        return
    total = len(Presentation(cands[0]).slides._sldIdLst)
    bad = []
    for key, ref in SLIDE_REF.items():
        for part in str(ref).split(","):
            part = part.strip()
            if not part:
                continue
            nums = [int(x) for x in _re.findall(r"\d+", part)]
            if not nums:
                continue
            if any(n < 1 or n > total for n in nums):
                bad.append((key, ref, f"outside 1..{total}"))
            elif len(nums) == 2 and nums[1] < nums[0]:
                bad.append((key, ref, "inverted range"))
    # A bounds check alone is NOT enough: a wrong-but-in-range reference still
    # passes it (152-155 was in range and still wrong). So also assert that each
    # SEMANTIC row points at a slide whose title actually matches the row.
    EXPECT = {
        (2, "16:45"): "Briefing for Assessment",
        (2, "17:00"): "Assessment",
        (2, "18:00"): "Assessment",
    }
    for key, want in EXPECT.items():
        ref = str(SLIDE_REF.get(key, ""))
        first = _re.findall(r"\d+", ref)
        if not first:
            continue
        n = int(first[0])
        # TITLE_SLIDE holds BOTH the first occurrence (bare key) and the last
        # ("LAST:" key). The admin block repeats at the end of the deck, so a
        # match on either is legitimate — checking only the bare keys reported a
        # false failure on the end-block Assessment slide.
        titles = [t[5:] if t.startswith("LAST:") else t
                  for t, i in TITLE_SLIDE.items() if i == n]
        if want not in titles:
            bad.append((key, ref, f"slide {n} is {titles or ['?']}, expected {want!r}"))
    if bad:
        raise SystemExit("BUILD FAILED — bad LP slide references:\n" +
                         "\n".join(f"  {k}: {r!r} ({why})" for k, r, why in bad))
_assert_slide_refs()

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
_VCR = [
 ("1.0",C.VERSION_DATE,
  "Initial release of the AI for Network Security lesson plan — 2 days, 8 instructional hours per "
  "day, 4 topics aligned to LO1-LO4 and TSC "+C.TSC_CODE+", 12 hands-on AI-assisted labs, and the "
  "WA-SAQ + Case Study assessment on Day 2.",C.TRAINER),
 ("1.1",C.VERSION_DATE,
  "Quality-audit revision. Process-map stage labels are now authored short names in the single source (never derived by truncation), with a build-time guard; procedure-slide headings use one uniform size per slide; the Support slide became a tile grid; the day schedule moved to a 9:30 am start with exactly 8 instructional hours per day (lunch and tea breaks excluded, enforced by assertion); the Case Study is 1 hour, matching the paper and the deck.",C.TRAINER),
 ("1.2",C.VERSION_DATE,
  "Wired the browser practice tools into the lab procedures. The IP Calculator now scopes the scan in Lab 1 and carves the security zones in Lab 7; the PCAP Analyzer triages the capture in Lab 2 and summarises capture evidence in Lab 11; the Cybersecurity Simulator grounds the likelihood scores in Lab 5; the Cryptography Toolkit demonstrates the confidentiality control in Lab 8 and hash tamper-evidence in Lab 11; RegexLab builds and negatively tests the log filters in Lab 10. Hacklab and FauxBank are documented as optional, unassessed extension work.",C.TRAINER),
]
prodoc.add_version_control(doc,_VCR)
_vcr_versions=[r[0] for r in _VCR]
assert len(_vcr_versions)==len(set(_vcr_versions)), \
    f"duplicate rows in the Document Version Control Record: {_vcr_versions}"
assert _vcr_versions[-1]==C.VERSION.lstrip("v"), \
    f"version control record ends at {_vcr_versions[-1]}, but the build is {C.VERSION}"
prodoc.add_toc(doc)

def H(text,level=1):
    h=doc.add_heading(text,level=level); return h

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("Duration","2 days · 8 instructional hours per day (16 hours)"),
      ("Daily Timing","Day 1: 9:30 am – 7:00 pm · Day 2: 9:30 am – 7:00 pm (1-hour lunch and two 15-minute tea breaks, excluded from the 8 instructional hours)"),
      ("Mode","Instructor-led, hands-on AI-assisted network security labs against authorised lab targets"),
      ("Skills Framework","TSC: "+C.TSC_TITLE+"  ("+C.TSC_CODE+")"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          f"Final assessment is conducted on Day {max(SCHEDULE)} from {_ASSESS_START}.",
          "Knowledge (K1-K4) is assessed by the WA-SAQ; abilities (A1-A9) are assessed by the Case Study.",
          C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None,align=None):
    cell.text=""; p=cell.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,
           "admin":"F3F5F8","recap":"F3F5F8","lab":None}

H("Course Schedule",1)
for day,(theme,rows) in SCHEDULE.items():
    H(f"Day {day} — {theme}",2)
    tbl=doc.add_table(rows=0,cols=4); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity","Slides"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=0
    for start,end,mins,kind,text in rows:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        set_cell(cells[3],SLIDE_REF.get((day,start),""),size=9,fill=fill)
        if kind not in ("lunch","break"): training+=mins
    # widths
    for row in tbl.rows:
        row.cells[0].width=Inches(1.0); row.cells[1].width=Inches(0.75)
        row.cells[2].width=Inches(4.05); row.cells[3].width=Inches(1.0)
    p=doc.add_paragraph(); r=p.add_run(f"Total instructional time: {training} minutes ({training//60} hours), excluding the 1-hour lunch and the two 15-minute tea breaks."); r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    assert training==480, f"Day {day} instructional minutes = {training}, expected 480 (breaks excluded)"

H("Lab Reference (aligned to learning outcomes and TSC statements)",1)
tt=doc.add_table(rows=0,cols=5); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic / Learning unit","Weighting","K / A assessed","Labs","Slides"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],", ".join(tp["ks"])+" | "+", ".join(tp["abil"]),size=9.5,fill=TOPIC_FILL)
    set_cell(cells[3],", ".join(f"Lab {a['num']}" for a in acts),size=9.5)
    set_cell(cells[4],lab_slides([a["num"] for a in acts]),size=9.5)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
