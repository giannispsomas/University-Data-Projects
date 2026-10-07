"""Builds the one-page PDF summary from results/ and figures/ (run the notebook first)."""
import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.utils import ImageReader

P = Path(__file__).resolve().parents[1]   # project root, independent of the working directory
S = json.loads((P / "results" / "summary.json").read_text(encoding="utf-8"))
INK, INK2, MUTED, BLUE, RULE = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e"), colors.HexColor("#898781"), colors.HexColor("#2a78d6"), colors.HexColor("#e1e0d9")

h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=INK, spaceAfter=2)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=8.6, leading=11, textColor=INK2, spaceAfter=7)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=INK, spaceBefore=7, spaceAfter=3)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=8.6, leading=11.4, textColor=INK)
bul = ParagraphStyle("bul", parent=body, leftIndent=9, bulletIndent=0, spaceAfter=2.5)
small = ParagraphStyle("small", parent=body, fontSize=7.6, leading=9.8, textColor=INK2)
cell = ParagraphStyle("cell", parent=body, fontSize=7.4, leading=9)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")

K = {r["indicator"]: r for r in S["key"]}
def pct(label):  r = K[label]; return f'{r["pct"]*100:.0f}%'
def ci(label):   r = K[label]; return f'{r["ci_low"]*100:.0f}-{r["ci_high"]*100:.0f}%'
import pandas as pd
_csv = pd.read_csv(P / "results" / "hypothesis_tests.csv")
TESTS = _csv.to_dict("records")
T = {t["id"]: t for t in TESTS}
trav = S["travel_by_segment_pct"]

doc = SimpleDocTemplate(str(P / "Film_Tourism_Survey_Summary.pdf"), pagesize=A4,
                        leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.3*cm, bottomMargin=1.1*cm,
                        title="Film Tourism in Greece: Survey Analysis", author="Ioannis (Giannis) Psomas")
W = A4[0] - 3.2*cm
el = []
el += [Paragraph("Film Tourism in Greece: Survey Analysis", h1),
       Paragraph("University of West Attica, Dept. of Tourism Management &nbsp;|&nbsp; Case Studies in Tourism, 2022-23 &nbsp;|&nbsp; "
                 f"n = {S['n']} respondents &nbsp;|&nbsp; Python (pandas, SciPy, matplotlib)", sub)]

el.append(Paragraph("<b>Question:</b> is there demand for film-location tourism in Greece, and do students differ from other respondents? "
                    "Re-analysis of an original 60-response questionnaire, rebuilt reproducibly with confidence intervals and corrected tests.", body))
el.append(Paragraph("Key findings", h2))
k_aw, k_vis = "Know places where films were shot", "Have visited a film set"
k_tr, k_st, k_pr = "Would travel to visit a film set", "Rate state management of film sets as inappropriate", "Believe film tourism has prospects in Greece"
t1 = T["T1"]
el += [
    Paragraph(f"<b>High awareness, low experience.</b> {pct(k_aw)} know places where films were shot, but only {pct(k_vis)} (95% CI {ci(k_vis)}) have visited a film set.", bul, bulletText="•"),
    Paragraph(f"<b>Latent demand.</b> {pct(k_tr)} (CI {ci(k_tr)}) say they would travel to visit a film set; 18% say no. Motivation is spread across the 1-10 scale (median {S['motivation_median']:.0f}).", bul, bulletText="•"),
    Paragraph(f"<b>Perceived governance gap.</b> {pct(k_st)} (CI {ci(k_st)}) rate the state's management of film sets as inappropriate, while {pct(k_pr)} see prospects for film tourism.", bul, bulletText="•"),
    Paragraph(f"<b>Students are more willing to travel</b> than other respondents ({trav['Students']['Yes']:.0f}% vs {trav['Others']['Yes']:.0f}%; {t1['effect']}; Fisher p = {t1['p_raw']:.3f}) "
              f"<b>but the result does not survive correction</b> for the 7 tests run (Holm-adjusted p = {t1['p_holm']:.2f}). It is a hypothesis for a larger study, not an established effect.", bul, bulletText="•"),
]

img1 = Image(str(P / "figures" / "fig1_key_indicators.png")); r = img1.imageHeight / img1.imageWidth
img1.drawWidth = 12.2*cm; img1.drawHeight = 12.2*cm * r
img2 = Image(str(P / "figures" / "fig2_travel_by_segment.png")); r2 = img2.imageHeight / img2.imageWidth
img2.drawWidth = 12.2*cm; img2.drawHeight = 12.2*cm * r2
el += [Spacer(1, 3), img1, Spacer(1, 2), img2]

el.append(Paragraph("Hypothesis tests (pre-specified, Holm-corrected)", h2))
rows = [[Paragraph(x, cellb) for x in ["Comparison", "Test", "Effect", "p", "p (Holm)"]]]
for t in TESTS:
    rows.append([Paragraph(t["comparison"], cell), Paragraph(t["test"], cell), Paragraph(t["effect"], cell),
                 Paragraph(f'{t["p_raw"]:.3f}', cell), Paragraph(f'{t["p_holm"]:.2f}', cell)])
tb = Table(rows, colWidths=[6.6*cm, 2.3*cm, 5.0*cm, 1.15*cm, 1.45*cm])
tb.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.8, INK2), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
                        ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
el.append(tb)

el.append(Paragraph("Method and limitations", h2))
el.append(Paragraph(
    f"<b>Method.</b> Data cleaned with a documented log (Excel-corrupted date cells repaired, labels harmonised, mismatched headers fixed); "
    f"{S['validation_exact']} of {S['validation_total']} figures in the original paper reproduced exactly (the rest differ by one respondent). "
    "Wilson 95% intervals for proportions; Fisher exact, Mann-Whitney U and Spearman tests; Holm correction. "
    "<b>Limitations.</b> Convenience sample (65% students, only 3 professionals), stated intentions rather than behaviour, low power for subgroup tests.", small))
doc.build(el)
print("pdf written")
