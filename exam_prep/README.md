# BAV — Exam Question Bank

45 solved multiple-choice questions on the Business Analysis & Valuation course,
set out as handwritten notebook pages.

| | |
|---|---|
| Questions | 45 (40 core + 5 guest lecture) |
| Format | 4 options, full worked solution, highlighted answer |
| Pages | 21 |
| Compile | `pdflatex BAV_Exam_Question_Bank.tex` (twice) |

## Sections

| | Topic | Questions |
|---|---|---|
| A | The five consistencies | 1–8 |
| B | DCF variants and why they must agree | 9–17 |
| C | Cost of capital, relevering and circularity | 18–26 |
| D | Terminal value, multiples and relative valuation | 27–35 |
| E | Applied: the cement valuations | 36–40 |
| F | Guest lecture: M&A, synergy and exchange ratios | 41–45 |

## Notes

**Every number is checkable.** Section B runs on the OLP Limited test vector from the
course text (all four methods reconcile to Rs 460m). Section E uses the actual Ambuja
and UltraTech figures from `../equity_reports/`, so the arithmetic ties back to the
models. All answers were verified numerically against `equity_reports/build/model.py`
before the questions were written.

**Section F is an assumption.** The five guest-lecture questions are written on M&A,
synergy valuation and exchange ratios — the module the course carries separately from
the core syllabus. If the guest session covered something else, those five should be
replaced; the rest of the bank is unaffected.

**Design.** Ruled-notebook background with a red margin rule, Comic Neue throughout,
circled question numbers, green formula boxes, yellow highlighter on answers, and
green ★ Remember lines for the traps. Comic Neue was chosen over the more
authentically handwritten Augie face because Augie renders `6` almost identically to
`b`, which is unusable in a paper this dense with figures.

Layout lives in `qstyle.sty`; content in `BAV_Exam_Question_Bank.tex`.
