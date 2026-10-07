# Film Tourism in Greece: Survey Analysis

Reproducible re-analysis of a 60-response questionnaire on film-location tourism in Greece, originally collected for the
*Case Studies in Tourism* course (University of West Attica, Dept. of Tourism Management, 2022-23). The original paper reported
descriptive percentages; this project rebuilds the analysis in Python with documented data cleaning, confidence intervals and
multiple-comparison-corrected hypothesis tests.

**One-page summary:** [`Film_Tourism_Survey_Summary.pdf`](Film_Tourism_Survey_Summary.pdf) &nbsp;|&nbsp; **Full analysis:** [`analysis.ipynb`](analysis.ipynb) / [`analysis.html`](analysis.html)

## Headline results (n = 60)

| Finding | Result |
|---|---|
| Know places where films were shot | 97% (95% CI 89-99%) |
| Have visited a film set | 30% (20-43%) |
| Would travel to visit a film set | 58% (46-70%) |
| Rate state management of film sets as inappropriate | 60% (47-71%) |
| Students vs others: would travel | 69% vs 38%, OR 3.7 (1.2-10.4), Fisher p = 0.028, **Holm-adjusted p = 0.19 (not significant after correction)** |

The main message: high awareness of film locations but low direct experience, with real but unconfirmed differences between
students and other respondents. See the notebook for the full set of 7 pre-specified tests and the limitations.

## What this project demonstrates

- **Data cleaning with an audit trail:** repaired Excel auto-converted dates, harmonised inconsistent labels, found and fixed swapped
  headers, parsed free-text numbers; all logged and asserted in code.
- **Validation against a published source:** 21 of 24 figures in the original paper reproduced exactly; the 3 differences (one respondent each) are documented.
- **Appropriate statistics for small samples:** Wilson confidence intervals, Fisher exact, Mann-Whitney U, Spearman, effect sizes, Holm correction.
- **Honest reporting:** results that do not survive multiple-testing correction are labelled as hypotheses, not findings.

## Structure

```
analysis.ipynb                  full analysis (executed)
analysis.html                   same, for viewing without Jupyter
scripts/make_summary_pdf.py     rebuilds the one-page PDF from results/ and figures/
Film_Tourism_Survey_Summary.pdf one-page summary
data/raw/                       original responses (anonymous), as exported
data/processed/survey_clean.csv cleaned dataset used in the analysis
figures/                        charts used in the notebook and summary
results/                        tables (tests, indicators, validation, themes) and summary.json
```

## Run it

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
python scripts/make_summary_pdf.py
```

## Notes

- Survey responses are anonymous (no names or contact details). Free-text answers are in Greek.
- Convenience sample (65% students, 3 professionals): findings describe this sample, not the Greek population.
