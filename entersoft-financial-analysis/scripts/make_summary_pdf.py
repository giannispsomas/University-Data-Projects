"""Builds the one-page PDF summary from results/ and figures/ (run the notebook first)."""
import json
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

P = Path(__file__).resolve().parents[1]   # project root, independent of the working directory
S = json.loads((P / "results" / "summary.json").read_text())
R = pd.read_csv(P / "results" / "ratios.csv", index_col=0)
INK, INK2, RULE = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e"), colors.HexColor("#e1e0d9")
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=INK, spaceAfter=2)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=8.6, leading=11, textColor=INK2, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=INK, spaceBefore=6, spaceAfter=3)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=8.5, leading=11.2, textColor=INK)
bul = ParagraphStyle("bul", parent=body, leftIndent=9, spaceAfter=2.2)
small = ParagraphStyle("small", parent=body, fontSize=7.6, leading=9.8, textColor=INK2)
cell = ParagraphStyle("cell", parent=body, fontSize=7.6, leading=9.2)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
cellr = ParagraphStyle("cellr", parent=cell, alignment=2)
cellbr = ParagraphStyle("cellbr", parent=cellb, alignment=2)

doc = SimpleDocTemplate(str(P / "Entersoft_Financial_Analysis_Summary.pdf"), pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm,
                        topMargin=1.2*cm, bottomMargin=1.0*cm, title="Entersoft A.E.: Financial Statement Analysis 2014-2017", author="Ioannis (Giannis) Psomas")
el = [Paragraph("Entersoft A.E.: Financial Statement Analysis, 2014-2017", h1),
      Paragraph("University of West Attica, Dept. of Tourism Management &nbsp;|&nbsp; Analysis of Financial Statements, 2019-20 &nbsp;|&nbsp; Python (pandas, matplotlib), Excel", sub),
      Paragraph("<b>Question:</b> how did an Athens-listed software company perform over four years, and do the coursework workbook's inputs match the published annual reports? "
                "The inputs were audited line by line against Entersoft's parent-company annual reports (FY2015-FY2017) before any analysis.", body),
      Paragraph("Key findings", h2)]
el += [
 Paragraph("<b>Audit result: 5 of 76 inputs were wrong.</b> Operating expenses for 2015/2016 and depreciation for 2014/2015 were transposed, and 2017 operating expenses had a EUR 2,000 typo. Everything else (sales, profit before tax, every balance-sheet line) matched exactly. The corrected EBIT margin is 12.4% for 2015 (workbook: 5.4%) and 14.4% for 2016 (workbook: 20.5%).", bul, bulletText="•"),
 Paragraph("<b>Profitability stepped down in 2015, then held.</b> Sales fell 0.9% while cost of sales rose 17.8%: gross margin 69% to 63% and EBIT margin 24% to 12%. It then stabilised at 14-15% in 2016-17 while sales grew 12-15% a year.", bul, bulletText="•"),
 Paragraph("<b>2017: more sales, no more profit.</b> Profit before tax was flat (EUR 1.14m) because financial expense rose five-fold with EUR 1.4m of new short-term borrowing; interest cover fell from 31x to 7x.", bul, bulletText="•"),
 Paragraph("<b>Strong liquidity, weak working capital.</b> Current ratio 3.4-4.5x and equity funding 69-85% of assets, but receivables equal 54-60% of sales (about 200-220 days, 160-177 excluding VAT) against 7-56 days of supplier credit.", bul, bulletText="•"),
 Paragraph("<b>Original conclusion holds.</b> Ranked by profit before tax, 2014 > 2016 > 2017 > 2015 is confirmed on verified data; only the opex- and depreciation-based ratios in the original were distorted.", bul, bulletText="•"),
]
rows_spec = [("Sales (EUR m)", None), ("Sales growth", "pct"), ("Gross margin", "pct"), ("EBIT margin", "pct"), ("EBITDA margin", "pct"),
             ("Current ratio", "x1"), ("Total liabilities / equity", "x2"), ("Interest cover (EBIT / financial expense)", "x1"),
             ("Receivables days", "d"), ("Payables days", "d")]
yrs = S["years"]; sales = S["income"]["sales"]
fmt = lambda k, v: {"pct": f"{v*100:.1f}%", "x1": f"{v:.1f}x", "x2": f"{v:.2f}x", "d": f"{v:.0f}"}[k]
rows = [[Paragraph("Ratio", cellb)] + [Paragraph(str(y), cellbr) for y in yrs]]
rows.append([Paragraph("Sales (EUR m)", cell)] + [Paragraph(f"{v/1e6:.2f}", cellr) for v in sales])
for name, kind in rows_spec[1:]:
    rows.append([Paragraph(name.replace(" (EBIT / financial expense)", " (EBIT / fin. exp.)"), cell)] + [Paragraph(fmt(kind, float(v)), cellr) for v in R.loc[name].values])
tb = Table(rows, colWidths=[6.2*cm] + [2.2*cm]*4, hAlign="LEFT")
tb.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.8, INK2), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE), ("TOPPADDING", (0, 0), (-1, -1), 1.3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.3), ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
def img(name, w):
    i = Image(str(P / "figures" / name)); r = i.imageHeight / i.imageWidth; i.drawWidth = w; i.drawHeight = w * r; return i
el += [Paragraph("Key ratios (recomputed from raw statement items)", h2), tb, Spacer(1, 4),
       img("fig1_growth_and_margins.png", 13.6*cm), Spacer(1, 2), img("fig2_workbook_vs_annual_report.png", 13.6*cm)]
el.append(Paragraph("Method and limitations", h2))
el.append(Paragraph("<b>Method.</b> Income statement rebuilt from line items; the mismatch with reported profit (+/- EUR 489,773 in 2015/2016) exposed the errors, which were then confirmed line by line against the annual reports; the corrected statements reconcile to reported profit within EUR 2. "
                    "<b>Limitations.</b> Parent-company (standalone) statements only, four years of year-end balances, pre-tax profit only, one company and no peer benchmark.", small))
doc.build(el); print("pdf ok")
