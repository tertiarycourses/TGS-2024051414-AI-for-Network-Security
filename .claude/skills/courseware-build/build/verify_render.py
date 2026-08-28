#!/usr/bin/env python3
"""
verify_render.py — check the BUILT PDF, not the builder's own estimate.

An estimator-based assert inside build_slides.py can only ever confirm its own
assumptions: if the chars-per-line model is optimistic, the assert passes and the
text still overflows in the render. This script closes that loop by measuring the
actual rasterised/text-extracted geometry of the produced PDF.

Checks, per slide:
  1. no text line extends below the slide's usable area (the footer band)
  2. no text line sits on or below the bottom edge of the light card it belongs to
  3. no text line extends past the left/right margins

Usage:
    python3 verify_render.py <deck.pdf>            # exits non-zero on any failure
    python3 verify_render.py <deck.pdf> --report   # list findings, always exit 0
"""
import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("verify_render.py needs PyMuPDF:  pip install pymupdf")

TOL = 1.0          # pt — ignore sub-point rounding between renderers
FOOTER_TOP = 0.985 # fraction of page height below which nothing may print
                   # (the house footer legitimately sits at ~0.955)
LEFT_M = 0.030     # fraction of page width
RIGHT_M = 0.972


def _cards(page):
    """Bottom edges of the light content cards drawn on this slide.

    The house style paints each card as a filled rectangle in LIGHT (#F5F8FC).
    A text line whose bottom sits below its card's bottom is the overflow defect
    this script exists to catch.
    """
    out = []
    for d in page.get_drawings():
        if d.get("fill") is None:
            continue
        r, g, b = d["fill"]
        # LIGHT #F5F8FC and white cards; skip the dark code bars and accent bars
        # the house LIGHT card (#F5F8FC). Pure white is the slide background,
        # not a card — including it made every containment test short-circuit.
        if 0.93 < r < 0.99 and 0.95 < g < 0.995 and b > 0.96:
            rect = d["rect"]
            if 100 < rect.width < page.rect.width * 0.98 and 40 < rect.height:
                out.append(rect)
    return out


def check(pdf_path, report_only=False):
    doc = fitz.open(pdf_path)
    findings = []

    for i, page in enumerate(doc, 1):
        H, W = page.rect.height, page.rect.width
        foot = H * FOOTER_TOP
        cards = _cards(page)

        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                x0, y0, x1, y1 = ln["bbox"]
                txt = "".join(sp["text"] for sp in ln["spans"]).strip()
                if not txt:
                    continue

                if y1 > foot + TOL:
                    findings.append((i, "below the page", txt[:56], round(y1 - foot, 1)))
                if x0 < W * LEFT_M - TOL:
                    findings.append((i, "past left margin", txt[:56], round(W * LEFT_M - x0, 1)))
                if x1 > W * RIGHT_M + TOL:
                    findings.append((i, "past right margin", txt[:56], round(x1 - W * RIGHT_M, 1)))

                # The card this line belongs to = the SMALLEST card whose
                # horizontal span contains it and which starts above it. Taking
                # the first match let a larger enclosing rect mask the overflow.
                # A line BELONGS to a card only if it starts inside that card
                # vertically as well as horizontally — otherwise a line in the
                # row below is wrongly attributed to the row above and every
                # multi-row tile grid reports a false overflow. Among the cards
                # that actually contain the line's start point, take the smallest.
                owner = None
                for c in cards:
                    inside_x = c.x0 - 2 <= x0 and x1 <= c.x1 + 2
                    starts_in = c.y0 - 2 <= y0 <= c.y1 + 2
                    if inside_x and starts_in:
                        if owner is None or c.get_area() < owner.get_area():
                            owner = c
                if owner is not None and y1 > owner.y1 + TOL:
                    findings.append((i, "past its card bottom", txt[:56],
                                     round(y1 - owner.y1, 1)))

    if findings:
        print(f"\n  verify_render: {len(findings)} finding(s) in {os.path.basename(pdf_path)}")
        for pg, kind, txt, by in findings:
            print(f"    slide {pg:>3}  {kind:<22} +{by:>5}pt   {txt!r}")
    else:
        print(f"  verify_render: {os.path.basename(pdf_path)} — "
              f"{doc.page_count} pages, no overflow in the actual render.")

    return 0 if (report_only or not findings) else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(check(sys.argv[1], "--report" in sys.argv))
