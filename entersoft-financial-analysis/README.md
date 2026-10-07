# Entersoft A.E.: Financial Statement Analysis, 2014-2017

Rebuild of a university financial-analysis assignment for the course *Analysis of Financial Statements* (University of West Attica, Dept. of Tourism Management, 2nd semester, 2019-20).
The original was a Word report comparing pre-computed ratios year by year. This project **recomputes every ratio from the raw statement items, audits the inputs against Entersoft's published annual reports,
corrects what does not match**, and then analyses the verified numbers.

**One-page summary:** [`Entersoft_Financial_Analysis_Summary.pdf`](Entersoft_Financial_Analysis_Summary.pdf) &nbsp;|&nbsp; **Full analysis:** [`analysis.ipynb`](analysis.ipynb) / [`analysis.html`](analysis.html)

## Headline results (parent-company statements, EUR)

| Area | Finding |
|---|---|
| **Audit** | **5 of 76 inputs were wrong** vs the annual reports: opex 2015/2016 transposed, depreciation 2014/2015 transposed, a EUR 2,000 typo in 2017 opex. Sales, profit before tax and every balance-sheet line matched exactly |
| Impact of the errors | Workbook EBIT margin 5.4% (2015) and 20.5% (2016) vs **12.4% and 14.4%** verified; opex/sales 58.1% and 44.6% vs 51.1% and 50.7% |
| Profitability | Margin step-down in 2015 (gross margin 69% to 63%, EBIT margin 24% to 12%), then stable at 14-15% while sales grew 12-15% a year |
| 2017 | Sales +12.5% but profit before tax flat: financial expense up five-fold on EUR 1.4m of new short-term borrowing; interest cover 31x to 7x |
| Liquidity / working capital | Current ratio 3.4-4.5x, equity 69-85% of assets; but receivables = 54-60% of sales (about 200-220 days; 160-177 ex-VAT) vs 7-56 days of supplier credit |
| Original conclusion | Ranking 2014 > 2016 > 2017 > 2015 (by profit before tax) **confirmed** on verified data |

## What this project demonstrates

- **Source-data audit:** the errors were detected by rebuilding the income statement and reconciling to reported profit (a gap of +/-EUR 489,773), then confirmed and fully diagnosed against the published reports.
- Financial ratio analysis: profitability, liquidity, leverage, working-capital efficiency, growth (CAGR, year-on-year).
- Quantifying the impact of data errors on conclusions (workbook vs corrected ratios), and reporting what did and did not change.

## Structure

```
analysis.ipynb                              full analysis (executed)
analysis.html                               same, for viewing without Jupyter
scripts/make_summary_pdf.py                 rebuilds the one-page PDF from results/ and figures/
Entersoft_Financial_Analysis_Summary.pdf    one-page summary
data/raw/                                   statements as transcribed in the coursework workbook (EUR)
data/reference/                             official parent-company figures read from the annual reports (FY2015-FY2017)
data/processed/                             workbook as transcribed, and the corrected statements used in the analysis
figures/                                    charts
results/                                    ratios, errors found, reconciliation, impact of corrections, summary.json
```

## Run it

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
python scripts/make_summary_pdf.py
```

## Sources and limitations

- Official figures: Entersoft S.A. annual financial reports for FY2015, FY2016 and FY2017 (Athens Exchange / Euronext Athens filings), **parent-company ("Company") columns**; entered by hand with page references in the notebook.
- The coursework figures were collected from Entersoft's published financial data with guidance from the course instructor and transcribed into a workbook.
- Parent-company (standalone) statements only, not the consolidated group (whose figures differ, e.g. 2016 sales EUR 10.7m group vs 8.0m parent).
- Year-end balances only (no averages), pre-tax profit only, four years, one company, no peer benchmark.
