# BAV Study System

Built from the Term IV Business Analysis & Valuation material in `../bav_materials/`
(Prof. Pitabas Mohanty, XLRI Jamshedpur, PGDM BMJ 2025–27, BAVBJ25-4).

| File | What it is |
|---|---|
| `BAV_Field_Manual.html` | The master guide. Beginner-friendly, covers Quiz 1 (multiples), Quiz 2 (DCF/APV), Quiz 3 (cost of capital, cash flow, EVA), the post-Quiz-3 interim block (VC method, private companies, real options, AI valuation, practical/M&A), the quant toolkit, and exam craft. |
| `BAV_Recall_Sheets.html` | 40 single-topic revision sheets in a handwritten notebook style. A4, print or save as PDF with no scaling. |
| `BAV_Question_Bank.html` | Predicted 25-question interim paper under +4/−1 marking, plus a 57-question end-term bank by topic. Interactive scoring, full worked solutions. |
| `build_notes.py` | Generator for `BAV_Recall_Sheets.html`. Edit the `PAGES` list and re-run. |

## Sources used

- Quiz 1, 2 and 3 papers with the professor's own solution keys and mark schemes
- `WACC2026.pdf`, `cashflow.pdf` — cost of capital and cash flow lecture decks
- `aivaln.pdf` — AI in Business Valuation (Lecture 18)
- `pvt_valn.pdf` — Valuation of Private Companies (Kavita Textiles case)
- `XLRI_Presentation_2026.pdf` — Darshan Rathod guest lecture (Lecture 19)
- `Book_8_Aug_2026.pdf` — Chapter 3 of *Business Valuation: Text and Cases* (Taxmann)
- `Adobe_Scan_29_Aug_2026.pdf` — Laura Martin (real options), Sampa Video (APV), and the
  Venture Capital Valuation Problem Set
- `Adobe_Scan_08/27_Aug_2026.pdf` — class notes, Lectures 10–19
- `mohantybavvaluationcombined.skill` — the packaged method reference

Numbers are reproduced from those sources. Check anything you intend to rely on
against the original.

## Look and feel

All three files use the same design system as Volume I (Multiples) and Volume II
(DCF) in `../bav_materials/`: cream paper `#EDE7D6`, gold `#9C7526`, teal `#2B564E`,
rust `#8C3F30`, with Fraunces / Source Sans 3 / IBM Plex Mono. The shared tokens
live in `theme.css`, which is inlined into the two long-form pages at build time.

## Regenerating the PDF

`BAV_Recall_Sheets.pdf` is produced from the HTML with headless Chromium:

```bash
python3 build_notes.py
python3 embed_fonts.py BAV_Recall_Sheets.html /tmp/sheets_embedded.html \
  "https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
# then print /tmp/sheets_embedded.html to A4 with backgrounds on
```

`embed_fonts.py` exists because a page loaded over `file://` gets neither the
Google Fonts stylesheet nor a charset, so it would otherwise print in fallback
fonts with mangled punctuation.

Two print quirks are handled in `build_notes.py`:

- Chromium reserves roughly 11 mm of an A4 page even at `margin: 0`, so each sheet
  is 286 mm tall with trimmed padding rather than a full 297 mm. A full-height
  sheet silently paginates into two pages.
- Page breaks use `.sheet + .sheet { break-before: page }` rather than
  `break-after`, which emitted a stray blank page after the cover.
