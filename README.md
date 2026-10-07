# University Data Projects

Two analytical projects, rebuilt in Python from coursework completed during a **BSc in Tourism Management** at the University of West Attica (2019-2023).
The original assignments were Word/Excel reports; here each one is a reproducible notebook with a documented data-cleaning log, validation of the source data,
appropriate statistics, and a one-page summary.

| Project | What it shows | Summary | Analysis |
|---|---|---|---|
| [**Film Tourism in Greece: Survey Analysis**](film-tourism-survey/) | Survey data cleaning, validation against a published report, confidence intervals, hypothesis tests with multiple-comparison correction (n = 60) | [PDF](film-tourism-survey/Film_Tourism_Survey_Summary.pdf) | [Notebook](film-tourism-survey/analysis.ipynb) |
| [**Entersoft A.E.: Financial Statement Analysis, 2014-2017**](entersoft-financial-analysis/) | Ratio analysis (profitability, liquidity, leverage, working capital), source-data audit against annual reports, quantified impact of data errors | [PDF](entersoft-financial-analysis/Entersoft_Financial_Analysis_Summary.pdf) | [Notebook](entersoft-financial-analysis/analysis.ipynb) |

## What both projects have in common

- **Audit before analysis.** Each starts by testing the source data: the survey is checked against the figures published in the original paper (21 of 24 reproduce exactly; the rest are documented),
  and the financial workbook's inputs are audited line by line against the company's published annual reports (5 transcription errors found and corrected).
- **Findings first, caveats stated.** Results that do not survive correction (survey subgroup differences) are reported as hypotheses, not facts. Assumptions and limitations are listed in every notebook.
- **Reproducible.** Raw data, cleaned data, code, figures and results tables are all in the repo; running the notebook regenerates everything.

## Tools

Python (pandas, NumPy, SciPy, matplotlib), Jupyter, ReportLab, Excel. The original survey analysis used SPSS.

## Reproduce

```bash
cd film-tourism-survey            # or entersoft-financial-analysis
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
python scripts/make_summary_pdf.py
```

## Author

Ioannis (Giannis) Psomas, aspiring data analyst, Athens. [LinkedIn](https://www.linkedin.com/in/giannispsomas)
