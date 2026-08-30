# Cement Sector — Business Analysis and Valuation

Two equity research reports (Ambuja Cements, UltraTech Cement) with a combined
appendix, plus the corrected valuation models behind them.
Valuation date **31 March 2026**, market data at the 30 March close.

| | Ambuja Cements | UltraTech Cement |
|---|---|---|
| Stance | **SELL** | **SELL** |
| Intrinsic value | **Rs 99.42** | **Rs 5,024.02** |
| Market price | Rs 400.90 | Rs 10,745 |
| Downside | −75.2% | −53.2% |
| Basis | Consolidated | Standalone core + subsidiaries |
| Explicit horizon | 10 years | 5 years |
| WACC | 11.36% | 11.43% |
| Classification | Difficult to value | Easy to value |

## Layout

The reports use a two-stream layout: **the left column carries the write-up, the
right column carries the exhibits related to it**, flowing across full pages. This
is implemented with `paracol` rather than `multicols`, so the two streams are
independent and stay aligned section by section.

Every page of Part I carries the Ambuja mark in the running header, and every page
of Part II the UltraTech mark, via `\runheadlogo{<file>}{<label>}` in `ibstyle.sty`.

### Swapping in the real company logos

`fig/logo_amb.png` and `fig/logo_utcl.png` are **typeset wordmarks, not the
companies' trademark logos** — the network egress policy blocks every company domain,
so no real logo file could be fetched, and imitating a company's branding would be
worse than a plain typographic mark. To use the real logos, drop the PNG files in at
those two paths and recompile. Nothing else changes: the header geometry, the cover
blocks and the `\includegraphics` heights all stay as they are. A transparent PNG
roughly 6:1 wide works best.

## Photographs and product images

Board and management headshots, the Ambuja product pack shots and the plant-footprint
map are the **companies' own published images**, extracted from the earlier combined
report supplied as input (`Cement_Sector_UltraTech_Ambuja_Combined_Report.pdf`), which
sourced them from the FY2025-26 annual reports and company pages. They were extracted
programmatically — see `build/extract_assets.py` — rather than fetched or generated,
because the network blocks the company sites and synthesising images of real, named
individuals would not be acceptable in any case.

Provenance for each set is recorded in Appendix I:

| Asset | Source |
|---|---|
| Ambuja board, 8 headshots | FY2025-26 Integrated Annual Report, pp. 230–231 |
| Ambuja leadership, 10 headshots | Same report, pp. 232–233 |
| Ambuja product pack shots, 5 | Same report, Product Portfolio |
| Ambuja plant map | Same report, At a Glance |
| UltraTech board and management, 16 | UltraTech Board of Directors / Management Team pages |

## What is here

```
Cement_Equity_Reports.tex     master document — compile this
ibstyle.sty                   all layout, colour and callout definitions
parts/00_front.tex            cover and contents
parts/01_ambuja.tex           Part I  — Ambuja Cements (sections 1–13)
parts/02_ultratech.tex        Part II — UltraTech Cement (sections 14–27)
parts/03_appendix.tex         Part III — combined appendix (A–L)
parts/_tables.tex             auto-generated data tables (do not hand-edit)
fig/                          52 exhibits + 2 header marks (build/charts_*.py)
fig/people/                   34 board and management headshots
fig/products/                 5 product pack shots
assets_extracted/             raw images pulled from the supplied earlier report
models/                       the two CORRECTED Excel valuation models
build/                        chart generation, the audit re-implementation,
                              and the Excel correction script
_source/                      the two workbooks exactly as received
```

## Compiling

```bash
pdflatex Cement_Equity_Reports.tex
pdflatex Cement_Equity_Reports.tex     # twice, so page references settle
```

Requires a TeX Live installation with `paracol`, `tcolorbox`, `titlesec`,
`fancyhdr`, `booktabs`, `colortbl`, `enumitem`, `ragged2e`, `needspace`,
`helvet` and `extarticle` (texlive-latex-extra covers all of them).

To regenerate the exhibits or the corrected workbooks:

```bash
cd build
python3 charts_amb.py && python3 charts_utcl.py && python3 charts_app.py
python3 fix_excel.py
```

`build/model.py` is an independent re-implementation of both valuations in plain
Python, sharing no code with the workbooks. It was written to audit them and it
reproduces Ambuja's published value to the paisa, UltraTech's to within 2.5 paise,
Ambuja's published sensitivity grid cell for cell, and the EVA-to-enterprise-value
identity for both. Every exhibit is generated from it, so the charts and the
models cannot drift apart.

## The corrected models

`models/` contains the two workbooks with the Appendix B corrections applied. Each
carries a new **`Corrections`** sheet listing every change — what the cell was,
what it now is, and why — plus the open items that were deliberately *not* changed.
Both recalculate on open and both still reconcile across all five DCF methods.

The corrections that moved the answer:

- **Beta relever (both).** Both workbooks state a constant D/V policy with
  continuous rebalancing (Harris–Pringle) and discount the tax shield at ρ, but
  relevered beta with the fixed-debt Hamada formula; Ambuja's additionally carried
  a sign error, computing `(1+t)` where even Hamada needs `(1−t)`. Corrected to
  `β_U(1+D/E)`. Ambuja Rs 98.85 → Rs 99.42; UltraTech Rs 5,148.18 → Rs 5,024.02.

The corrections that fixed broken cells without moving the answer:

- **UltraTech sensitivity grid** discounted P&L row 17 (depreciation) instead of
  row 24 (FCFF), built its terminal value off row 14 (revenue) instead of row 21
  (NOPAT), and omitted the non-controlling interest — printing Rs 27,314–117,876
  per share against a base case of Rs 5,148. Rebuilt.
- **UltraTech historical NOPAT** referenced an empty cell for the tax rate, so the
  published ten-year ROIC series was pre-tax (14.4% for FY2025-26 rather than the
  correct after-tax 10.8%).
- **Ambuja** `Source Data!C32` and `C34`, and `Terminal!B21`, all referenced blank
  rows and printed −3,570, 100% and 0 respectively.
- **Ambuja** `Relative Valuation!C48` hardcoded a stale DCF value of Rs 114.87.
- Stale narrative text in both workbooks, and blocks duplicated five and six times
  on three Ambuja sheets.

Two items were **left unchanged and flagged**, because resolving them needs a
judgement the disclosed data does not support: UltraTech's India Cements stake
(the bridge, the balance sheet and the Entity Build sheet give three different
figures, and the stake's operations are already inside the forecast's subsidiary
block, so adding it would double-count roughly Rs 197 per share); and the terminal
ROIC fade switch, which ships off while the audit log claims it was switched on.

None of the corrections changes either recommendation. The largest moves Ambuja by
0.6% and UltraTech by 2.4%, against downside of 75% and 53%.

## Company-profile sections

Sections 2 and 15 cover the company and its history, products and brands, the board
and senior management (with photographs), the shareholders and the shareholding
pattern, and the operating footprint. Full-width board, management and product
spreads follow each, in the style of the earlier report.

Section 3 and Section 16 add a **margin stack, working capital and depreciation**
analysis for each company — the FY2025-26 evidence for why Ambuja's cost improvement
never reached the operating line while UltraTech's did. That analysis also resolves a
previously unquantified audit item: Note 49 discloses Rs 607 crore of intangible
amortisation against a forecast that holds the intangible balance flat, so the
asset-consistency gap now carries a number (and it runs against the recommendation).

One sourcing item remains open: the reported UltraTech managing-director transition
effective 1 April 2026, which falls the day after the valuation date and affects no
number in the report. It is logged as row 32 of the Source Log.

## Sourcing

Financial statement data is from company annual reports and exchange filings; the
risk-free rate is the FBIL 10-year G-Sec par yield published by the RBI; the equity
risk premium and the unlevered sector beta are Damodaran (NYU Stern), January 2026.
No figure comes from a financial data aggregator. The three open sourcing items are
listed in Appendix I and on each workbook's `Corrections` sheet.

Prepared for an academic valuation exercise. Not investment advice.
