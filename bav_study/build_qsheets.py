#!/usr/bin/env python3
"""Build the 40 solved MCQs as handwritten-style A4 sheets.

Same sheet chrome as build_notes.py: ruled paper, red margin rule, the
study-kit cream/gold palette, and the print geometry that makes Chromium
emit one A4 page per sheet.
"""

HEAD = r"""<title>BAV Solved MCQs</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --desk:#CFC7B0; --sheet:#F8F4E6; --line:#E0D6BC; --margin:#C99B93;
  --ink:#1C2A33; --ink-2:#2B3B47; --pencil:#54626C;
  --red:#8C3F30; --green:#2B564E; --amber:#9C7526; --edge:#C7BE9F;
  --gold:#9C7526; --gold-bright:#B8912F; --paper-2:#E3DBC4;
}
*{box-sizing:border-box}
body{background:var(--desk);margin:0;font-family:"Kalam",cursive;color:var(--ink)}
.stack{display:flex;flex-direction:column;align-items:center;gap:22px;padding:22px 12px 60px}

.sheet{
  width:210mm; min-height:297mm; background:var(--sheet); position:relative;
  padding:16mm 14mm 14mm 26mm; border:1px solid var(--edge);
  box-shadow:0 2px 10px rgba(0,0,0,.16);
  background-image:repeating-linear-gradient(to bottom,transparent,transparent 7.4mm,var(--line) 7.4mm,var(--line) 7.5mm);
  background-position:0 16mm;
  font-size:16.5px; line-height:7.5mm; overflow:hidden;
}
.sheet::before{content:"";position:absolute;left:20mm;top:0;bottom:0;width:1px;background:var(--margin)}
.sheet::after{content:attr(data-pg);position:absolute;right:14mm;bottom:6mm;
  font-size:13px;color:var(--pencil);font-family:"IBM Plex Mono",monospace}

/* ---------- question block ---------- */
.qb{margin:0 0 5mm}
.qb + .qb{border-top:1px dashed var(--edge);padding-top:4mm}
.qhead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1mm}
.qno{font-family:"Fraunces",Georgia,serif;font-weight:700;font-size:19px;
  color:var(--ink);letter-spacing:-.01em}
.qtag{font-size:12.5px;color:var(--red);font-weight:700;letter-spacing:.03em;
  flex:0 0 auto;padding-left:10px}
.stem{margin:0 0 2mm}
.opts{margin:0 0 2mm;padding-left:2mm}
.opt{display:flex;gap:7px;align-items:flex-start}
.opt .k{font-weight:700;color:var(--pencil);flex:0 0 auto;width:16px}
.opt.right .k{color:var(--red)}
.opt.right .txt{position:relative;font-weight:700}
.opt.right .txt::after{content:"";position:absolute;left:-6px;right:-6px;top:-1px;bottom:-1px;
  border:1.6px solid var(--red);border-radius:14px/50%;
  transform:rotate(-.5deg);pointer-events:none}
.ans{font-weight:700;color:var(--red);margin:0 0 2mm}
.work{border:1px solid var(--edge);border-left:3px solid var(--gold);
  padding:2mm 3mm;margin:0;background:transparent}
.work .wl{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:1mm}
.f{font-family:"IBM Plex Mono",monospace;font-size:13.5px;line-height:7.5mm;
  white-space:pre-wrap;overflow-x:auto;margin:0}
.f b{color:var(--red)}
p{margin:0 0 2mm}
ul{margin:0 0 2mm;padding-left:18px;list-style:none}
li{position:relative;margin:0}
li::before{content:"·";position:absolute;left:-12px;font-weight:700;color:var(--ink-2)}
b,strong{font-weight:700}
.red{color:var(--red);font-weight:700}
.grn{color:var(--green);font-weight:700}
.pen{color:var(--pencil)}
.trapline{color:var(--red);font-weight:700;margin:1mm 0 0}

/* ---------- cover ---------- */
.cover{display:block;padding-top:70mm;background-image:none}
.cover::before{content:none}
.cover::after{content:none}
.cover h1{font-size:54px;line-height:1.04;margin:0 0 4mm;font-weight:700;
  font-family:"Fraunces",Georgia,serif;letter-spacing:-.02em}
.cover .sub{font-size:19px;color:var(--pencil);line-height:9mm}

@media(max-width:230mm){
  .sheet{width:100%;min-height:auto;padding:14mm 8mm 14mm 16mm}
  .sheet::before{left:11mm}
}
@page{size:A4;margin:0}
@media print{
  body{background:#fff}
  .stack{display:block;gap:0;padding:0}
  /* Chromium reserves ~11mm of an A4 page even at margin:0, so the sheet is
     shortened and the padding trimmed to keep the same content area. */
  .sheet{box-shadow:none;border:0;width:210mm;
        height:286mm;min-height:0;overflow:hidden;margin:0 auto;
        padding:12mm 14mm 6mm 26mm}
  .cover{padding-top:62mm}
  .sheet::after{bottom:1.5mm}
  .sheet + .sheet{break-before:page}
  .toolbar{display:none!important}
}
.toolbar{position:sticky;top:0;z-index:9;background:var(--desk);width:100%;
  padding:10px 16px;border-bottom:1px solid var(--edge);
  font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--pencil);
  display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.toolbar b{color:var(--ink)}
</style>

<div class="toolbar"><b>BAV · 40 Solved MCQs</b> · every answer worked out · print or save as PDF at A4, no scaling</div>
<div class="stack">
"""

Q = []


def q(topic, stem, opts, ans, work, pyq=False):
    """The correct option is written first in the source; build() shuffles them
    so the printed answer key is not a column of As. No working refers to an
    option by letter, so the shuffle is safe.

    pyq=True marks a question reproduced from Prof. Mohanty's own End Term
    Pattern slides rather than written for this set."""
    Q.append(dict(topic=topic, stem=stem, opts=opts, ans=ans, work=work, pyq=pyq))


# =============================================== ACTUAL PYQs (1–3)
# Reproduced from Prof. Mohanty's "End Term Pattern" slides, photographed in
# the Lecture 18 class notes. Marking on those slides: +4 for a correct
# answer, −1 for a wrong one.
q("Terminal value",
  "The EBITDA of a company in the last year of the explicit forecasting period is $200 million. "
  "The free cash flow for the same year is $80 million. The cost of capital is 12%. "
  "If the terminal growth rate is 5%, what is the terminal EBITDA multiple?",
  ["6.0×", "5.7×", "8.6×", "15.0×"], 0,
  "<div class='f'>TV = FCF × (1+g) ÷ (WACC − g) = 80 × 1.05 ÷ (0.12 − 0.05)\n"
  "   = 84 ÷ 0.07 = <b>$1,200m</b>\n"
  "Terminal EBITDA multiple = TV ÷ EBITDA = 1,200 ÷ 200 = <b>6.0×</b></div>"
  "<p class='trapline'>⚠ 5.7× is what you get by dropping the (1+g): 80/0.07 = 1,142.9 ÷ 200. "
  "15.0× divides by the FCF instead of the EBITDA.</p>"
  "<p class='grn'>This is the <b>multiplier consistency</b> check in reverse: your Gordon terminal "
  "value implies a multiple, and 6.0× is what a mature, modestly growing business should look like. "
  "If it had come out at 25×, the g or the WACC would be wrong.</p>", pyq=True)

q("VC method",
  "After Series A the cap table is: founders 1,000,000 shares, Series A 250,000 shares "
  "(total 1,250,000). The Series A investor holds 20%. At Series B the pre-money is $50 million "
  "and a new investor puts in $20 million. If Series A wants to hold 20% after Series B, "
  "approximately how much must it invest in Series B?",
  ["$5 million", "$4 million", "$3 million", "$14 million"], 0,
  "<div class='f'>Price per share = $50m ÷ 1.25m shares = <b>$40.00</b>\n"
  "Series A's existing stake = 250,000 × 40 = <b>$10m</b>\n\n"
  "Let x = what Series A puts in. Post-money = 50 + 20 + x = 70 + x\n"
  "     (10 + x) ÷ (70 + x) = 0.20\n"
  "     10 + x = 14 + 0.2x   ⟹   0.8x = 4   ⟹   <b>x = $5m</b></div>"
  "<p class='trapline'>⚠ $4m is the trap: 20% of the $70m post-money is $14m, less the $10m already "
  "held. That ignores the fact that <b>your own investment enlarges the post-money too.</b> "
  "You must solve for x on both sides.</p>"
  "<p class='pen'>Check: A buys 5 ÷ 40 = 125,000 shares → holds 375,000 of "
  "1,250,000 + 500,000 + 125,000 = 1,875,000 = <b>20.0%</b> ✓</p>", pyq=True)

q("Quant",
  "An analyst regressed the P/E of 10 companies in a sector on their projected growth rate in EPS. "
  "Figures in brackets are t-statistics:<br>"
  "<span class='f' style='display:block;margin:1mm 0'>P/E = 16.38 + 1.2 × g(EPS)\n"
  "      (3.24)   (0.8)</span>"
  "Which is the most likely interpretation?",
  ["None of the above",
   "The ROE of an average company in the industry is lower than the required rate of return",
   "Companies with a higher projected growth in EPS do necessarily trade at a higher P/E",
   "Factors other than growth in EPS have no impact on the P/E of these companies"], 0,
  "<div class='f'>n = 10, k = 2  ⟹  df = 8, 5% critical t ≈ <b>2.31</b>\n"
  "intercept t = 3.24  ⟹  significant\n"
  "<b>slope t = 0.8  ⟹  NOT significant</b> — growth does not explain P/E in this sample</div>"
  "<p>Take the options one at a time. The growth option is <u>contradicted</u> by the insignificant "
  "slope. \"Other factors have no impact\" <u>overclaims</u> — an insignificant growth coefficient "
  "says growth does not explain P/E, not that nothing else does. The ROE statement is not "
  "addressable from this regression at all. So <b>none of the above.</b></p>"
  "<p class='trapline'>⚠ The whole question turns on reading the bracketed numbers as "
  "<b>t-statistics, not standard errors.</b> Rule of thumb |t| &gt; 2; with only 10 observations "
  "the bar is higher still at 2.31.</p>", pyq=True)

# ======================================================= MULTIPLES (1–5)
q("Multiples",
  "A company earns an ROE of 15%, has a cost of equity of 15%, and grows at 6% a year. "
  "What is its justified price-to-book ratio?",
  ["1.0×", "1.5×", "2.5×", "Cannot be found without the payout ratio"], 0,
  "<div class='f'>P/B = (ROE − g) ÷ (K_e − g) = (0.15 − 0.06) ÷ (0.15 − 0.06) = <b>1.0×</b></div>"
  "<p class='grn'>When ROE = K_e the g cancels — P/B is 1.0 whatever the growth rate. "
  "The company earns exactly what its shareholders demand, so growth creates nothing (NPVGO = 0).</p>")

q("Multiples",
  "A firm is expected to grow at 0% and trades at a P/E of 12.5×. What is its cost of equity?",
  ["8.0%", "12.5%", "6.25%", "Cannot be found without ROE"], 0,
  "<div class='f'>At g = 0:  P/E = 1 ÷ K_e  ⟹  K_e = 1 ÷ 12.5 = <b>8.0%</b></div>"
  "<p class='trapline'>⚠ The ROE term vanishes at zero growth — which is exactly why P/E tells you "
  "nothing about ROE there, and P/B does.</p>")

q("Multiples",
  "Company A trades at 15× with 10% growth; Company B at 24× with 20% growth. "
  "Which looks cheaper on PEG, and what is the objection to relying on it?",
  ["B at 1.2 vs A at 1.5 — but PEG assumes P/E is linear in g and ignores risk entirely",
   "A at 1.5 vs B at 1.2 — PEG always favours low growth",
   "They are identical once growth is netted off",
   "PEG cannot be compared across different growth rates"], 0,
  "<div class='f'>PEG_A = 15 ÷ 10 = <b>1.5</b>   PEG_B = 24 ÷ 20 = <b>1.2</b>  ⟹ B looks cheaper</div>"
  "<p>But P/E is <b>convex</b> in g — g sits in the numerator through the payout term and in the "
  "denominator through (K_e − g). So dividing by g systematically flatters fast growers. "
  "PEG also carries no risk term: same PEG, very different betas, not equally attractive.</p>")

q("Multiples",
  "Reported PAT is ₹120 cr, which includes a ₹30 cr post-tax gain on the sale of surplus land. "
  "There are 10 cr shares and the price is ₹250. What is the normalised P/E?",
  ["27.8×", "20.8×", "25.0×", "22.5×"], 0,
  "<div class='f'>Normalised PAT = 120 − 30 = <b>₹90 cr</b>   EPS = 90 ÷ 10 = <b>₹9.00</b>\n"
  "Normalised P/E = 250 ÷ 9 = <b>27.8×</b>   <span class='pen'>(reported P/E = 250 ÷ 12 = 20.8×)</span></div>"
  "<p class='trapline'>⚠ A gain on sale of assets is <b>not recurring</b> — by his 2×2 it is ignored "
  "entirely. The stock is a third more expensive than the reported number suggests.</p>")

# ======================================================= DCF FAMILY (6–12)
q("DCF",
  "EBIT ₹300m in perpetuity, tax 30%, cost of equity 18%, debt ₹200m at 10%, zero growth. "
  "What is the equity value by the FCFE route?",
  ["₹1,088.9m", "₹1,166.7m", "₹1,288.9m", "₹980.0m"], 0,
  "<div class='f'>Interest = 200 × 10% = 20\n"
  "PAT = (300 − 20) × 0.7 = <b>196</b>   <span class='pen'>(g = 0, so FCFE = PAT)</span>\n"
  "Equity = 196 ÷ 0.18 = <b>₹1,088.9m</b>\n"
  "EV = 1,088.9 + 200 = ₹1,288.9m</div>"
  "<p class='grn'>Note the order: FCFE needs no weights, so equity comes first — and only then can "
  "you build market-value weights for the WACC. That is the escape from circularity.</p>")

q("DCF",
  "For the same firm, what is the capital cash flow and the rate it must be discounted at?",
  ["CCF = 216 at a pre-tax WACC of 16.76%",
   "CCF = 210 at a WACC of 16.29%",
   "CCF = 216 at a WACC of 16.29%",
   "CCF = 210 at a pre-tax WACC of 16.76%"], 0,
  "<div class='f'>FCF = 300 × 0.7 = 210\n"
  "CCF = FCF + t·K_d·D = 210 + (0.30 × 20) = <b>216</b>\n"
  "pre-tax WACC = (1088.9/1288.9)(18%) + (200/1288.9)(10%) = <b>16.759%</b>\n"
  "check: 216 ÷ 0.16759 = <b>1,288.9</b> ✓  same EV</div>"
  "<p class='trapline'>⚠ CCF already contains the tax shield, so the discount rate must NOT carry "
  "the (1−t). Using the after-tax WACC of 16.29% counts the shield twice and overstates value.</p>")

q("DCF",
  "A levered firm has K_e = 20%, K_d = 10%, D/E = 0.5 and a tax rate of 30%. "
  "What is ρ, the unlevered cost of equity?",
  ["17.41%", "16.67%", "18.18%", "15.00%"], 0,
  "<div class='f'>K_e = ρ + (ρ − K_d)(1 − t)(D/E)\n"
  "20 = ρ + (ρ − 10)(0.7)(0.5) = ρ + 0.35ρ − 3.5\n"
  "23.5 = 1.35ρ  ⟹  ρ = <b>17.407%</b></div>"
  "<p class='pen'>ρ is pure business risk — what shareholders would demand with no debt at all. "
  "It is the starting point for every APV valuation.</p>")

q("DCF",
  "Year-5 free cash flow is ₹240m, terminal growth 5%, WACC 12%. What is the present value of the "
  "terminal value today?",
  ["₹2,042.7m", "₹3,600.0m", "₹1,823.9m", "₹2,144.9m"], 0,
  "<div class='f'>TV at end of yr 5 = 240 × 1.05 ÷ (0.12 − 0.05) = 252 ÷ 0.07 = <b>₹3,600m</b>\n"
  "PV = 3,600 ÷ 1.12⁵ = 3,600 ÷ 1.76234 = <b>₹2,042.7m</b></div>"
  "<p class='trapline'>⚠ Two slips live here. ₹1,823.9m drops the (1+g); discounting six periods "
  "instead of five gives ₹1,823.8m as well. The TV sits at the <b>end</b> of year 5, so it comes "
  "back exactly five periods.</p>")

q("DCF",
  "Your FCF model gives an equity value of ₹500 cr and your FCFE model ₹460 cr. The model uses a "
  "constant WACC, growth of 6%, and holds debt fixed at ₹200 cr. What is the most likely cause?",
  ["Net new borrowing of g × D = ₹12 cr a year is missing from FCFE",
   "The tax rate has been applied to PBT instead of EBIT",
   "The terminal value has been discounted one period too many",
   "The beta was estimated over the wrong window"], 0,
  "<div class='f'>constant WACC  ⟹  constant D/E  ⟹  debt must grow at g\n"
  "net new borrowing = g × D = 0.06 × 200 = <b>₹12 cr each year</b>\n"
  "FCFE = FCF − Interest(1−t) + <b>net new borrowing</b></div>"
  "<p class='grn'>Nine times out of ten this is the cause of an FCF/FCFE mismatch. Either let the "
  "debt grow at g and keep the rates constant, or hold debt fixed and switch to APV.</p>")

q("DCF",
  "Enterprise value is ₹1,000 cr. The firm has ₹200 cr of debt, ₹100 cr of preference capital, "
  "₹50 cr of surplus cash excluded from the cash flows, and a contingent liability with an expected "
  "value of ₹20 cr. What is the equity value?",
  ["₹730 cr", "₹750 cr", "₹700 cr", "₹630 cr"], 0,
  "<div class='f'>1,000  + 50 surplus cash  − 200 debt  − 100 preference  − 20 contingent\n"
  "= <b>₹730 cr</b></div>"
  "<p class='trapline'>⚠ Preference capital is a claim ahead of equity — it goes into the WACC at "
  "its own cost with <b>no (1−t)</b>, and it must come out at the bridge. Miss it and you hand the "
  "preference holders' money to the equity.</p>")


q("Terminal value",
  "A terminal year shows EBITDA of $250 million and free cash flow of $100 million. "
  "An exit multiple of 8× EBITDA is applied and terminal growth is 4%. "
  "What cost of capital is implied by that exit multiple?",
  ["9.2%", "9.0%", "5.2%", "13.2%"], 0,
  "<div class='f'>TV = 8 × 250 = <b>$2,000m</b>\n"
  "TV = FCF(1+g) ÷ (WACC − g)  ⟹  2,000 = 104 ÷ (WACC − 0.04)\n"
  "WACC − 0.04 = 104 ÷ 2,000 = 0.052  ⟹  <b>WACC = 9.2%</b></div>"
  "<p class='grn'>The mirror of the PYQ: there you were given the WACC and asked for the multiple; "
  "here you are given the multiple and asked for the rate. Same identity, rearranged. "
  "If the WACC your model actually uses is 13%, then an 8× exit multiple is too generous.</p>")

# ======================================================= COST OF CAPITAL / BETA (13–18)
q("Cost of capital",
  "A company has migrated to section 115BAA. Its pre-tax cost of debt is 9.5%. "
  "What is the after-tax cost of debt?",
  ["7.11%", "7.13%", "6.18%", "9.50%"], 0,
  "<div class='f'>§115BAA effective rate = 22% + 10% surcharge + 4% cess = <b>25.168%</b>\n"
  "K_d(1 − t) = 9.5% × (1 − 0.25168) = <b>7.109%</b></div>"
  "<p class='pen'>7.13% is the answer from a rounded 25%; 6.18% uses the old regime's 34.94%. "
  "Check the regime in the tax note of the annual report — never assume it.</p>")

q("Beta",
  "The covariance between a stock's returns and the index is 0.0288 and the variance of the index "
  "is 0.0225. What is the stock's beta?",
  ["1.28", "0.78", "1.20", "0.64"], 0,
  "<div class='f'>β = Cov(r_i, r_m) ÷ Var(r_m) = 0.0288 ÷ 0.0225 = <b>1.28</b></div>"
  "<p class='pen'>Equivalently β = ρ × (σ_i ÷ σ_m). Here σ_m = √0.0225 = 15%. If the stock's σ were "
  "24%, then ρ = 1.28 × 15/24 = 0.80 and R² = 0.64.</p>")

q("Beta",
  "A comparable company has a levered beta of 1.30, a debt-to-equity ratio of 0.80 and a tax rate "
  "of 25%. What is its unlevered beta?",
  ["0.81", "0.72", "1.04", "0.87"], 0,
  "<div class='f'>β_U = β_L ÷ [1 + (1 − t)(D/E)]\n"
  "    = 1.30 ÷ [1 + 0.75 × 0.80] = 1.30 ÷ 1.60 = <b>0.8125</b></div>"
  "<p class='grn'>Unlever each peer with <b>its own</b> D/E and tax rate, take the <b>median</b> "
  "(robust to outliers in a small sample), then relever at your company's target D/E.</p>")

q("Beta",
  "A company makes a 1-for-4 rights issue at ₹200 when the cum-rights price is ₹300. "
  "What price should the return series use on the ex-rights day?",
  ["₹280", "₹260", "₹275", "₹250"], 0,
  "<div class='f'>TERP = (4 × 300 + 1 × 200) ÷ 5 = (1,200 + 200) ÷ 5 = <b>₹280</b></div>"
  "<p class='trapline'>⚠ The price 'falling' from ₹300 to ₹280 is not a −6.7% return — it is the "
  "arithmetic of issuing cheap shares. Unadjusted, that day enters the beta regression as a "
  "spurious negative return.</p>")

q("Cost of capital",
  "The spot rate is ₹85/$, the dollar interest rate is 2% and the rupee rate is 6.5%. "
  "What is the one-year forward rate under interest rate parity?",
  ["₹88.75/$", "₹81.41/$", "₹89.25/$", "₹85.00/$"], 0,
  "<div class='f'>Forward = Spot × (1 + r_₹) ÷ (1 + r_$)\n"
  "        = 85 × 1.065 ÷ 1.02 = 85 × 1.04412 = <b>₹88.75</b></div>"
  "<p class='pen'>This is why a dollar loan at 6% is not 6% debt for an Indian borrower: convert the "
  "whole schedule at expected forwards and take the rupee IRR. In his worked case a 6% dollar loan "
  "came out at a rupee cost of <b>12.30%</b>.</p>")

# ======================================================= CASH FLOW / EVA (19–23)
q("Cash flow",
  "NOPAT ₹400m, depreciation ₹120m, capex ₹260m, increase in operating working capital ₹60m, "
  "increase in other non-interest-bearing liabilities ₹15m. What is free cash flow?",
  ["₹215m", "₹200m", "₹185m", "₹245m"], 0,
  "<div class='f'>Gross cash flow  = 400 + 120           = <b>520</b>\n"
  "Gross investment = 260 + 60 − 15      = <b>305</b>\n"
  "Free cash flow   = 520 − 305          = <b>₹215m</b></div>"
  "<p class='pen'>An increase in non-interest-bearing liabilities is a <i>source</i> of funds, so it "
  "reduces the investment the business needs.</p>")

q("ROIC",
  "NOPAT for FY25 is ₹375 cr. Operating invested capital was ₹2,500 cr at the end of FY24 and "
  "₹2,800 cr at the end of FY25. What is ROIC for FY25?",
  ["15.0%", "13.4%", "14.2%", "11.9%"], 0,
  "<div class='f'>ROIC = NOPAT_t ÷ OIC_(t−1) = 375 ÷ 2,500 = <b>15.0%</b></div>"
  "<p class='trapline'>⚠ Mind the lag. This year's profit was earned on <b>last year's</b> capital. "
  "Using the closing figure gives 13.4%, and using the average gives 14.2% — both understate the "
  "return the business actually earned on the capital it had.</p>")

q("Terminal value",
  "An analyst's terminal year shows NOPAT ₹600m with <b>net investment of zero</b>, ROIC 14%, "
  "WACC 11%, and a terminal value of ₹7,500m from an exit multiple. What is the corrected terminal value?",
  ["₹6,011.9m", "₹7,500.0m", "₹5,833.3m", "₹6,500.0m"], 0,
  "<div class='f'>mistake: NI = 0 forces g = 0, but the exit multiple implies positive g\n"
  "g  = (TV × WACC − FCF) ÷ (TV + FCF) = (825 − 600) ÷ 8,100 = <b>2.778%</b>\n"
  "IR = g ÷ ROIC = 2.778 ÷ 14 = <b>19.84%</b>\n"
  "NI = 600 × 19.84% = <b>119.05</b>    FCF = 600 − 119.05 = <b>480.95</b>\n"
  "TV = 480.95 × 1.02778 ÷ (0.11 − 0.02778) = <b>₹6,011.9m</b></div>"
  "<p class='trapline'>⚠ The naive figure overstates terminal value by ₹1,488m — about 25% — "
  "because it credits growth the company never paid for.</p>")

# ======================================================= VC METHOD (24–28)
q("VC method",
  "A fund invests $10m and requires 40% a year for five years. Exit-year earnings are projected at "
  "$12m and comparables trade at 15×. What share must the fund own at exit?",
  ["29.9%", "25.0%", "35.9%", "22.4%"], 0,
  "<div class='f'>Terminal value = 15 × 12 = <b>$180m</b>\n"
  "FV of investment = 10 × 1.40⁵ = 10 × 5.3782 = <b>$53.78m</b>\n"
  "Required share = 53.78 ÷ 180 = <b>29.88%</b></div>")

q("VC method",
  "The fund now insists management must own 12% of the company by exit. "
  "What share must it require today?",
  ["33.95%", "41.88%", "26.29%", "29.88%"], 0,
  "<div class='f'>required today = required at exit ÷ (1 − dilution)\n"
  "               = 29.88% ÷ (1 − 0.12) = <b>33.95%</b></div>"
  "<p class='trapline'>⚠ Dilution is <b>multiplicative</b>, not additive. 29.88 + 12 = 41.88% is the "
  "trap. The option pool is funded entirely out of the founders' stake.</p>")

q("VC method",
  "The company has 4m shares before the round. The fund takes 33.95% for $10m. "
  "What is the price per share?",
  ["$4.86", "$5.87", "$7.36", "$2.94"], 0,
  "<div class='f'>New shares = 4m × [0.3395 ÷ (1 − 0.3395)] = 4m × 0.5140 = <b>2.056m</b>\n"
  "Price = $10m ÷ 2.056m = <b>$4.864</b>\n"
  "check: post = 10 ÷ 0.3395 = 29.46 ⟹ pre = 19.46 ⟹ 19.46 ÷ 4m = <b>$4.86</b> ✓</div>"
  "<p class='pen'>Without the option pool the price would be $5.87 — the pool costs the founders "
  "about a rupee in every six of share price.</p>")

q("Anti-dilution",
  "Series A holds 8m shares with a conversion price of $2.00. Total shares outstanding before the "
  "new round are 20m. The company raises $6m by issuing 5m new shares. Under weighted-average "
  "anti-dilution, what is Series A's new conversion price?",
  ["$1.84", "$2.00", "$1.20", "$1.53"], 0,
  "<div class='f'>NCP = [(OB × OCP) + New$] ÷ OA\n"
  "    = [(20m × $2.00) + $6m] ÷ (20m + 5m)\n"
  "    = ($40m + $6m) ÷ 25m = <b>$1.84</b></div>"
  "<p class='grn'>Series A now converts into 8m × (2.00 ÷ 1.84) = 8.70m shares. The new investor's "
  "percentage is unchanged — the protection transfers value <b>from the founders</b> to the earlier "
  "investor. A full ratchet would reset the price all the way to the new round's price.</p>")


q("VC method",
  "Founders hold 2,000,000 shares and Series A holds 500,000 (20% of 2.5m). At Series B the "
  "pre-money is $60 million and a new investor puts in $15 million. How much must Series A invest "
  "to stay at 20%?",
  ["$3.75 million", "$3.00 million", "$4.50 million", "$15.00 million"], 0,
  "<div class='f'>Price = $60m ÷ 2.5m = <b>$24.00</b>   A's stake = 500,000 × 24 = <b>$12m</b>\n"
  "(12 + x) ÷ (60 + 15 + x) = 0.20\n"
  "12 + x = 15 + 0.2x  ⟹  0.8x = 3  ⟹  <b>x = $3.75m</b></div>"
  "<p class='pen'>Post-money = $78.75m; A holds $15.75m = 20.0% ✓. "
  "$3.00m is the trap of taking 20% of the $75m post-money and subtracting the $12m already held — "
  "it forgets that your own cheque raises the post-money.</p>")

# ======================================================= PRIVATE COMPANY (29–32)
q("Private valuation",
  "An owner-manager draws ₹6 lakh a year; the market salary for the role is ₹30 lakh. "
  "Reported PAT is ₹2.40 cr and the tax rate is 25%. What is normalised PAT?",
  ["₹2.22 cr", "₹2.16 cr", "₹2.40 cr", "₹1.96 cr"], 0,
  "<div class='f'>Salary shortfall = 30 − 6 = ₹24 lakh = ₹0.24 cr (pre-tax)\n"
  "After-tax effect  = 0.24 × (1 − 0.25) = <b>₹0.18 cr</b>\n"
  "Normalised PAT    = 2.40 − 0.18       = <b>₹2.22 cr</b></div>"
  "<p class='pen'>Normalisation runs both ways: owners often <i>under</i>pay themselves to flatter "
  "profit before a sale, just as often as they overpay to reduce tax. Also strip personal "
  "expenses, ghost-employee salaries and non-recurring items.</p>")

q("Private valuation",
  "A comparable has a beta of 0.90 and its regression against the index has an R² of 0.36. "
  "With a risk-free rate of 7% and an equity risk premium of 7%, what cost of equity applies to a "
  "completely undiversified owner?",
  ["17.5%", "13.3%", "24.5%", "10.5%"], 0,
  "<div class='f'>ρ = √R² = √0.36 = 0.60\n"
  "Total beta = β ÷ ρ = 0.90 ÷ 0.60 = <b>1.50</b>\n"
  "K_e = 7% + 1.50 × 7% = <b>17.5%</b>   <span class='pen'>(diversified: 7 + 0.9×7 = 13.3%)</span></div>"
  "<p class='grn'>Total beta is the rigorous version of the 'double the beta' shortcut. An owner "
  "holding only this asset bears the whole σ, not just the systematic part.</p>")

q("Private valuation",
  "A 100% control stake in a private company is worth ₹300 cr. You are valuing a <b>20% minority</b> "
  "stake. Applying a 20% minority discount and a 25% DLOM, what is that stake worth?",
  ["₹36 cr", "₹48 cr", "₹45 cr", "₹60 cr"], 0,
  "<div class='f'>Pro-rata share      = 300 × 20%        = <b>₹60 cr</b>\n"
  "Less minority disc. = 60 × (1 − 0.20)  = <b>₹48 cr</b>\n"
  "Less DLOM           = 48 × (1 − 0.25)  = <b>₹36 cr</b></div>"
  "<p class='trapline'>⚠ The discounts are applied <b>in sequence</b>, not added (a combined 45% "
  "haircut would give ₹33 cr). And a DCF built on management's forecasts is already a "
  "<b>control</b> value — that is why the minority discount is needed at all.</p>")

q("Private valuation",
  "A private company is about to list. Which two things should change in the valuation?",
  ["The DLOM disappears and K_e moves toward the plain CAPM figure",
   "The DLOM rises and K_e falls",
   "Only the capital structure changes",
   "Nothing changes — the cash flows are the same"], 0,
  "<div class='f'>shares become marketable        ⟹ illiquidity discount goes\n"
  "IPO investors are diversified   ⟹ K_e ⟶ plain CAPM\n"
  "both effects push value <b>up</b></div>"
  "<p>In the Kavita case that is the move from ₹259 cr to something approaching the undiscounted "
  "₹346 cr, and then higher again as K_e falls from 20% toward 11.84%. "
  "<span class='pen'>Watch the use of proceeds: taken out by the owners → ignore; used to repay debt "
  "→ the debt ratio and cost of capital change; held for planned reinvestment → add to the DCF.</span></p>")

# ======================================================= REAL OPTIONS (33–34)
q("Real options",
  "A patent gives exclusive rights for 8 years. Developing the drug costs ₹800 cr today and the PV "
  "of the cash flows if developed is ₹700 cr. Outcomes are highly uncertain. "
  "Is the patent worth nothing?",
  ["No — the right to develop later is a call option with positive value despite the negative NPV",
   "Yes — the NPV is −₹100 cr so the project should be abandoned",
   "It is worth exactly −₹100 cr",
   "It has value only once the NPV turns positive"], 0,
  "<div class='f'>Map onto a call:  S = 700   K = 800   T = 8 yrs   σ = high\n"
  "Out of the money today, but <b>time value &gt; 0</b> whenever σ &gt; 0</div>"
  "<p class='grn'>All three conditions hold: <b>flexibility</b> (a right, not an obligation), "
  "<b>uncertainty</b> (with no uncertainty an option is worth only its intrinsic value), and "
  "<b>exclusivity</b> (the patent). A generic 'option to expand the factory' usually fails the third.</p>")

q("Real options",
  "In Laura Martin's stealth-tier valuation, the market value per home passed is $3,000 and 120 "
  "channels are currently lit. What value does she assign to the underlying, S?",
  ["$25.00", "$23.15", "$17.65", "$250.00"], 0,
  "<div class='f'>S = value per home passed ÷ lit channels = 3,000 ÷ 120 = <b>$25.00</b>\n"
  "<span class='pen'>(in the case itself: 2,500 ÷ 108 = $23.15)</span></div>"
  "<p class='trapline'>⚠ Know what to criticise: she takes σ = 50% from a <b>one-month</b> option on "
  "Cox <b>equity</b> to price a <b>ten-year</b> option on a channel's cash flows — wrong horizon and "
  "levered rather than asset volatility. And if the DCF's terminal value already grows on digital "
  "services, adding the option double-counts.</p>")

# ======================================================= AI VALUATION (35)
q("AI valuation",
  "A private company is valued at $120bn. Its most recent month's revenue was $500m. "
  "What is its run-rate revenue multiple, and what is the caution?",
  ["20× — run-rate annualises the latest month and is not trailing revenue",
   "240× — the multiple on monthly revenue",
   "10× — half the annualised figure to be conservative",
   "24× — using the trailing twelve months"], 0,
  "<div class='f'>Run-rate revenue = 500m × 12 = <b>$6bn</b>\n"
  "Multiple = 120 ÷ 6 = <b>20×</b></div>"
  "<p class='trapline'>⚠ In his Anthropic example the same $965bn valuation gave <b>50×</b> on Q1 "
  "annualised, <b>31×</b> on H1 annualised and <b>20×</b> on run-rate. In a fast-growing company the "
  "choice of denominator matters more than any argument about the numerator — quoting a multiple "
  "without stating the basis is meaningless.</p>")


q("Quant",
  "EV/EBITDA is regressed on ROIC for 12 companies: EV/EBITDA = 4.2 + 0.35 × ROIC(%), with "
  "t-statistics of 2.9 and 2.6 and an R² of 41%. What is the best interpretation?",
  ["Both coefficients are significant, and ROIC explains 41% of the cross-sectional variation — "
   "the other 59% is everything else",
   "ROIC fully determines EV/EBITDA in this sector",
   "The slope is insignificant, so ROIC does not affect the multiple",
   "41% of the companies in the sample are correctly valued"], 0,
  "<div class='f'>n = 12, k = 2  ⟹  df = 10, 5% critical t ≈ <b>2.23</b>\n"
  "2.9 and 2.6 both exceed it  ⟹  both coefficients significant\n"
  "R² = 41%  ⟹  41% of the VARIATION explained, not 41% of the companies</div>"
  "<p class='grn'>Contrast with the P/E PYQ, where the slope's t of 0.8 killed it. Here the "
  "relationship is real — which is exactly the logic behind Laura Martin's ROIC target price, "
  "where the same regression on cable companies had R² = 70%.</p>"
  "<p class='trapline'>⚠ R² is about variance explained. It never says anything about how many "
  "companies are \"correctly valued\", and a significant slope never means a variable is the "
  "only thing that matters.</p>")

# ======================================================= GUEST LECTURE (36–40)
q("Guest lecture",
  "An Indian private company issues shares to a resident investor at a premium. Under which statute "
  "does the valuation requirement arise, and by what name is it known?",
  ["The Income-tax Act — angel tax", "The Companies Act — preferential allotment",
   "SEBI regulations — open offer", "FEMA — transfer to a non-resident"], 0,
  "<div class='f'>Income-tax Act: an amount above ₹50,000 received without consideration is taxable.\n"
  "Applied to a share premium, it taxes the <b>excess of issue price over fair value</b>.</div>"
  "<p><b>The rest of the map:</b> Companies Act — preferential allotment, buyback, merger/demerger. "
  "SEBI — open offer, preferential allotment. FEMA — overseas direct investment and "
  "resident↔non-resident transfers. IBC — liquidation. Ind AS — purchase price allocation, options, "
  "financial instruments. <span class='pen'>Also worth knowing: §9(1)(i), the retrospective provision "
  "behind the Vodafone dispute — 'tax anything, anytime'.</span></p>")

q("Guest lecture",
  "A registered valuer uses a risk-free rate of 7%, a beta of 0.93, a market risk premium of 7%, "
  "and adds a company-specific risk premium of 3.5%. What cost of equity does she report?",
  ["17.01%", "13.51%", "20.51%", "16.51%"], 0,
  "<div class='f'>CAPM part = 7% + 0.93 × 7%  = 7% + 6.51% = <b>13.51%</b>\n"
  "K_e       = 13.51% + 3.5% CSRP        = <b>17.01%</b></div>"
  "<p><b>CSRP</b> compensates for risks beta cannot see: size, client concentration, promoter "
  "dependency, single-location risk, key-person exposure. Indian practice caps it near <b>4%</b> and "
  "runs the market risk premium at <b>6–7%</b>. "
  "<span class='grn'>It is the practitioner's route to the same problem total beta solves "
  "academically.</span></p>")

q("Guest lecture",
  "A target's trade creditors are on 60-day terms but it is actually paying at 165 days. "
  "How should this be handled in the bridge from enterprise value to equity value?",
  ["The excess is a stretch creditor — a debt-like item to be subtracted",
   "Leave it entirely inside working capital",
   "Add it as a surplus asset",
   "Ignore it, since trade credit carries no interest"], 0,
  "<div class='f'>normal terms      =  60 days  ⟶ stays in operating working capital\n"
  "actual            = 165 days\n"
  "<b>excess 105 days   ⟶ disguised borrowing ⟶ debt-like item, SUBTRACT</b></div>"
  "<p><b>The full debt-like list:</b> borrowings · unfunded gratuity and leave encashment · "
  "stretch creditors · non-convertible preference shares · lease liabilities · contingent "
  "liabilities at <span class='pen'>estimated impact × probability</span> · minority interest.</p>")

q("Guest lecture",
  "A database records a transaction at 6× EV/EBITDA. The advisor knows the deal was actually "
  "negotiated on net asset value plus two years' PAT as goodwill. What is the lesson for comparable "
  "transaction multiples?",
  ["The multiple was back-solved from a price set on a different basis, so CTM data can be spurious",
   "The database is simply wrong and should be corrected",
   "NAV-based deals cannot be compared at all",
   "The multiple is fine because the price paid is the price paid"], 0,
  "<div class='f'>deal negotiated on NAV + goodwill  ⟶  database stores a <b>multiple</b>\n"
  "⟹ the 6× describes nothing about how the price was actually reached</div>"
  "<p><b>The other database traps:</b> a deal where 100% of equity was bought but only 60% of the "
  "consideration was disclosed; period adjustments to revenue and margins; management replacement "
  "cost; actuarial gratuity provisioning — all inside a real 'adjusted EBITDA' and none of them "
  "visible in the database. Different databases also compute the same company's multiple differently.</p>")

q("Guest lecture",
  "A business is midway through a heavy capital-expenditure programme and is growing at 22%, well "
  "above its long-run rate. Which terminal-value method is most appropriate?",
  ["The H-model, in which growth fades from the horizon rate to the perpetual rate",
   "Gordon growth with a higher terminal g to reflect the capex",
   "An exit multiple applied to current-year EBITDA",
   "A zero-growth perpetuity"], 0,
  "<div class='f'>Gordon assumes growth <b>snaps</b> from 22% to ~4% in a single year — not credible\n"
  "H-model: growth <b>fades linearly</b> to the perpetual rate, then continues forever</div>"
  "<p class='grn'>Three terminal-value methods are on the syllabus: <b>Gordon growth</b>, the "
  "<b>H-model</b>, and <b>exit multiples</b> (EV/EBITDA or EV/EBIT on terminal-year earnings). "
  "The alternative to the H-model is simply to lengthen the explicit forecast period until steady "
  "state is credible — which is the same idea by another route.</p>")


# --------------------------------------------------------------------- build
def qblock(i, d):
    opts = "".join(
        f'<div class="opt{" right" if j == d["ans"] else ""}">'
        f'<span class="k">{"ABCD"[j]}</span><span class="txt">{o}</span></div>'
        for j, o in enumerate(d["opts"]))
    badge = "\u2605 ACTUAL PYQ \u00b7 " if d["pyq"] else ""
    return (f'<div class="qb">'
            f'<div class="qhead"><span class="qno">Q{i}</span>'
            f'<span class="qtag">{badge}{d["topic"]}</span></div>'
            f'<div class="stem">{d["stem"]}</div>'
            f'<div class="opts">{opts}</div>'
            f'<div class="ans">Ans: {"ABCD"[d["ans"]]}</div>'
            f'<div class="work"><span class="wl">Working</span>{d["work"]}</div>'
            f'</div>')


def shuffle_options(seed=20260831):
    """Deterministic per-question permutation, so rebuilds are reproducible."""
    state = seed
    perms = [(0, 1, 2, 3), (1, 0, 2, 3), (1, 2, 0, 3), (1, 2, 3, 0),
             (2, 0, 1, 3), (3, 1, 2, 0), (2, 3, 0, 1), (3, 0, 1, 2)]
    for d in Q:
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        p = perms[state % len(perms)]          # p[new position] = old index
        d["opts"] = [d["opts"][old] for old in p]
        d["ans"] = p.index(d["ans"])


# two questions per sheet, except where a long one needs the room to itself
# questions whose working needs a sheet of its own (measured, not guessed)
# measured, not guessed: the three PYQs and these questions need a sheet each
SOLO = {1, 2, 3, 4, 12, 14, 26, 28, 30, 32, 36, 38, 40}


def pack():
    sheets, cur = [], []
    for i, d in enumerate(Q, start=1):
        if i in SOLO:
            if cur:
                sheets.append(cur)
                cur = []
            sheets.append([(i, d)])
        else:
            cur.append((i, d))
            if len(cur) == 2:
                sheets.append(cur)
                cur = []
    if cur:
        sheets.append(cur)
    return sheets


def build():
    shuffle_options()
    sheets = pack()
    total = len(sheets) + 1
    out = [HEAD]
    out.append(
        f'<div class="sheet cover" data-pg="1 / {total}">'
        '<h1>40 Solved<br>MCQs</h1>'
        '<div class="sub">Every answer worked out.<br>'
        'Business Analysis &amp; Valuation · Prof. Pitabas Mohanty<br>'
        'XLRI Jamshedpur · PGDM BMJ 2025–27 · Term IV</div>'
        '<div style="margin-top:12mm" class="sub">'
        'The circled option is the answer. The boxed working below it is how you would '
        'get there in the exam.<br><br>'
        '<span class="red">Q1–Q3 are actual questions</span> from sir\u2019s own End Term '
        'Pattern slides, with his marking: <span class="red">+4 for right, \u22121 for wrong</span>. '
        'Three more questions in this set are built on those same patterns, because he reuses them.<br><br>'
        '<span class="red">Five questions are from the guest-lecture session</span> \u2014 sir has said '
        'that block is worth 4\u20135 questions.</div>'
        '</div>\n')
    for n, group in enumerate(sheets, start=2):
        body = "".join(qblock(i, d) for i, d in group)
        out.append(f'<div class="sheet" data-pg="{n} / {total}">{body}</div>\n')
    out.append("</div>\n")
    return "".join(out), total


if __name__ == "__main__":
    html, total = build()
    with open("BAV_Solved_MCQs.html", "w") as f:
        f.write(html)
    guest = sum(1 for d in Q if d["topic"] == "Guest lecture")
    print(f"{len(Q)} questions on {total} sheets ({guest} from the guest lecture), "
          f"{len(html):,} bytes")
