import numpy as np
from style import *
from model import Ambuja, grid
a = Ambuja(); R = a.run()
Y = a.years

# 1 ---- Football field: valuation ranges vs traded price
def f_football():
    fig, ax = newfig(3.35, 2.05)
    _g = grid(a, R, [.10, .12], [a.g]); _lo, _hi = sorted([_g[0][0], _g[1][0]])
    rows = [("DCF, five methods\n(FCFF/CCF/APV/FCFE/EVA)", R["vps"], R["vps"], BLUE),
            ("DCF range, WACC 10-12%\nat g 6.99%", _lo, _hi, BLUE),
            ("Peer median EV/EBITDA\n(19.4x, consolidated)", 454.9, 493.3, ORANGE),
            ("Peer median P/E (47.5x)", 361.5, 434.0, ORANGE),
            ("Peer median P/B (3.97x)\n- see ROE caveat", 826.1, 1102.1, MUTED)]
    for i, (lab, lo, hi, c) in enumerate(rows):
        y = len(rows) - 1 - i
        if hi - lo < 1:
            ax.plot([lo], [y], "D", color=c, ms=6, zorder=4)
            ax.text(lo + 34, y, f"{lo:,.0f}", va="center", fontsize=6.8, color=INK, fontweight="bold")
        else:
            ax.barh(y, hi - lo, left=lo, height=.42, color=c, alpha=.85, zorder=3)
            ax.text(hi + 30, y, f"{lo:,.0f}-{hi:,.0f}", va="center", fontsize=6.5, color=INK)
    ax.axvline(a.price, color=BAD, lw=1.5, zorder=5)
    ax.text(a.price + 16, 1.62, f"Traded\nRs {a.price:,.2f}", color=BAD,
            fontsize=6.8, fontweight="bold", va="center")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=6.5)
    ax.set_xlim(0, 1400); ax.set_xlabel("Value per share (Rs)")
    ax.set_title("Exhibit A1  Football field: every method against the price")
    tidy(ax, ygrid=False, xgrid=True); save(fig, "amb_football")

# 2 ---- EV to equity bridge
def f_bridge():
    fig, ax = newfig(3.35, 2.25)
    waterfall(ax, ["EV of\noperations", "+ Cash", "- Debt &\nleases",
                   "+ Tax under\nprotest", "- Deferred\ntax", "- Minority\ninterest"],
              [a.cash, -a.debt, a.protest, -a.dtl, -a.nci],
              start=R["ev"], total_label="Equity value\n(owners)")
    ax.set_ylabel("Rs crore"); ax.set_ylim(0, R["ev"] * 1.20)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_title("Exhibit A2  From enterprise value to the owners' claim")
    save(fig, "amb_bridge")

# 3 ---- FCFF profile
def f_fcff():
    fig, ax = newfig(3.35, 1.95)
    cols = [BAD if v < 0 else BLUE for v in R["fcff"]]
    ax.bar(Y, R["fcff"], color=cols, width=.66, zorder=3)
    bar_labels(ax, Y, R["fcff"], "{:,.0f}", dy=.03)
    ax.set_ylabel("FCFF (Rs cr)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_title("Exhibit A3  Free cash flow turns positive only in FY29")
    tidy(ax, zero=True); ax.tick_params(axis="x", rotation=45)
    save(fig, "amb_fcff")

# 4 ---- ROIC vs WACC
def f_roic():
    fig, ax = newfig(3.35, 2.05)
    x = np.arange(len(Y))
    ax.plot(x, np.array(R["roic_o"]) * 100, "-o", color=BLUE, lw=1.8, ms=3.4,
            label="ROIC, operating capital")
    ax.plot(x, np.array(R["roic_g"]) * 100, "-s", color=ORANGE, lw=1.8, ms=3.4,
            label="ROIC, including goodwill")
    ax.axhline(a.wacc * 100, color=BAD, lw=1.4, ls="--")
    ax.text(0.05, a.wacc * 100 + .30, f"WACC {a.wacc*100:.2f}%", color=BAD,
            fontsize=6.6, ha="left", fontweight="bold")
    ax.annotate(f"{R['roic_g'][-1]*100:.1f}%", (x[-1], R["roic_g"][-1] * 100),
                textcoords="offset points", xytext=(-3, -10), fontsize=6.6,
                color=ORANGE, ha="right", fontweight="bold")
    ax.annotate(f"{R['roic_o'][-1]*100:.1f}%", (x[-1], R["roic_o"][-1] * 100),
                textcoords="offset points", xytext=(-3, 5), fontsize=6.6,
                color=BLUE, ha="right", fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(Y, rotation=45)
    ax.set_ylabel("Return (%)"); ax.set_ylim(2, 13.6); ax.set_xlim(-.5, len(Y)-.3)
    ax.legend(loc="lower right", fontsize=6.4)
    ax.set_title("Exhibit A4  Return on capital never reaches its cost")
    tidy(ax); save(fig, "amb_roic")

# 5 ---- EVA
def f_eva():
    fig, ax = newfig(3.35, 1.95)
    cols = [BAD if v < 0 else GOOD for v in R["eva"]]
    ax.bar(Y, R["eva"], color=cols, width=.66, zorder=3)
    bar_labels(ax, Y, R["eva"], "{:,.0f}", dy=.05)
    ax.set_ylabel("EVA (Rs cr)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_title("Exhibit A5  Economic value added is negative for nine of ten years")
    tidy(ax, zero=True); ax.tick_params(axis="x", rotation=45)
    save(fig, "amb_eva")

# 6 ---- capacity, volume, utilisation (same unit MTPA -> one panel; util separate)
def f_capacity():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.35, 2.55), sharex=True,
                                   gridspec_kw={"height_ratios": [1.35, 1]})
    x = np.arange(len(Y))
    ax1.bar(x, a.capacity, color="#d7e3f5", width=.62, zorder=2, label="Capacity")
    ax1.bar(x, R["vol"], color=BLUE, width=.40, zorder=3, label="Volume sold")
    ax1.set_ylabel("Mn tonnes"); ax1.legend(fontsize=6.3, ncol=2, loc="upper left")
    ax1.set_title("Exhibit A6  The plants exist; the question is whether they fill")
    tidy(ax1)
    ax2.plot(x, np.array(a.util) * 100, "-o", color=ORANGE, lw=1.8, ms=3.2)
    ax2.axhline(67.89, color=MUTED, lw=1, ls=":")
    ax2.text(0.15, 65.9, "FY26 actual 67.9%", fontsize=6.2, color=MUTED)
    ax2.set_ylabel("Utilisation (%)"); ax2.set_ylim(65, 89)
    ax2.annotate("85%", (x[-1], 85), textcoords="offset points", xytext=(4, -2),
                 fontsize=6.6, color=ORANGE)
    ax2.set_xticks(x); ax2.set_xticklabels(Y, rotation=45); tidy(ax2)
    save(fig, "amb_capacity")

# 7 ---- EBITDA per tonne path
def f_ebitdat():
    fig, ax = newfig(3.35, 1.95)
    x = np.arange(len(Y))
    ax.plot(x, R["ebitda"] and [e * 10 / v for e, v in zip(R["ebitda"], R["vol"])],
            "-o", color=BLUE, lw=1.9, ms=3.4)
    ax.axhline(886.35, color=MUTED, ls=":", lw=1)
    ax.text(0, 900, "FY26 actual Rs 886", fontsize=6.3, color=MUTED)
    ax.axhline(966, color=ORANGE, ls="--", lw=1.2)
    ax.text(len(Y) - .15, 930, "UltraTech core assets Rs 966", fontsize=6.3,
            color=ORANGE, ha="right")
    e_t = [e * 10 / v for e, v in zip(R["ebitda"], R["vol"])]
    ax.annotate(f"Rs {e_t[-1]:,.0f}", (x[-1], e_t[-1]), textcoords="offset points",
                xytext=(-2, 6), fontsize=6.8, color=BLUE, ha="right", fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(Y, rotation=45)
    ax.set_ylabel("EBITDA per tonne (Rs)")
    ax.set_title("Exhibit A7  A 70% rise in unit EBITDA is already assumed")
    tidy(ax); save(fig, "amb_ebitdat")

# 8 ---- margin build: standalone vs subsidiary
def f_margins():
    fig, ax = newfig(3.35, 1.95)
    x = np.arange(len(Y))
    ax.plot(x, np.array(a.sa_marg) * 100, "-o", color=BLUE, lw=1.8, ms=3.2,
            label="Standalone (Sanghi, Penna inside)")
    ax.plot(x, np.array(a.sub_marg) * 100, "-s", color=AQUA, lw=1.8, ms=3.2,
            label="Subsidiaries (ACC, Orient)")
    ax.plot(x, [e / r * 100 for e, r in zip(R["ebitda"], R["rev"])], "--",
            color=MUTED, lw=1.5, label="Consolidated")
    ax.scatter([-0.6], [11.69], color=BLUE, s=16, zorder=5)
    ax.scatter([-0.6], [23.27], color=AQUA, s=16, zorder=5)
    ax.text(-0.55, 11.0, "FY26", fontsize=6.0, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels(Y, rotation=45); ax.set_xlim(-1.1, len(Y) - .4)
    ax.set_ylabel("EBITDA margin (%)"); ax.legend(fontsize=6.2, loc="lower right")
    ax.set_title("Exhibit A8  The parent carries the weak assets")
    tidy(ax); save(fig, "amb_margins")

# 9 ---- invested capital composition
def f_ic():
    fig, ax = newfig(3.35, 1.95)
    x = np.arange(len(Y))
    op = np.array(R["ic_o"]); gw = np.full(len(Y), a.gw)
    ax.bar(x, op, color=BLUE, width=.66, zorder=3, label="Operating invested capital")
    ax.bar(x, gw, bottom=op + 900, color=ORANGE, width=.66, zorder=3,
           label="Goodwill & intangibles")
    ax.set_xticks(x); ax.set_xticklabels(Y, rotation=45)
    ax.set_ylabel("Rs crore"); ax.legend(fontsize=6.3, loc="upper left")
    ax.set_ylim(0, 108000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.text(4.5, op[4] + gw[4] * 0.42, f"Goodwill Rs {a.gw:,.0f} cr, held flat",
            fontsize=6.2, color="white", ha="center", fontweight="bold")
    ax.set_title("Exhibit A9  A third of capital employed is acquisition goodwill")
    tidy(ax); save(fig, "amb_ic")

# 10 ---- sensitivity heatmap
def f_sens():
    fig, ax = newfig(3.35, 1.95)
    ws = [.09, .10, .11, .12, .13]; gs = [.02, .03, .04, .05, .06]
    M = grid(a, R, ws, gs)
    heat(ax, M, [f"{w*100:.0f}%" for w in ws], [f"{g*100:.0f}%" for g in gs],
         fmt="{:,.0f}", title_x="Terminal growth", title_y="WACC")
    ax.set_title("Exhibit A10  Value per share: no cell reaches Rs 401")
    save(fig, "amb_sens")

# 11 ---- peer EV/EBITDA
def f_peers():
    fig, ax = newfig(3.35, 1.85)
    names = ["Ambuja\n(consol.)", "Ramco", "Shree", "JK Cement", "UltraTech"]
    vals = [17.00, 18.98, 19.05, 19.69, 21.06]
    cols = [BLUE] + [MUTED] * 4
    ax.bar(names, vals, color=cols, width=.6, zorder=3)
    bar_labels(ax, names, vals, "{:.1f}x", dy=.02)
    ax.axhline(19.37, color=ORANGE, ls="--", lw=1.2)
    ax.text(2.0, 21.9, "Peer median 19.4x", fontsize=6.3, color=ORANGE, ha="center")
    ax.set_ylabel("EV / EBITDA (x)"); ax.set_ylim(0, 23.5)
    ax.set_title("Exhibit A11  Ambuja is the cheapest name in the set")
    tidy(ax); save(fig, "amb_peers")

# 12 ---- P/B vs ROE
def f_pbroe():
    fig, ax = newfig(3.35, 2.05)
    nm = ["Ambuja", "UltraTech", "Shree", "JK Cement", "Ramco"]
    roe = [3.81, 10.40, 6.81, 15.75, 2.19]; pb = [1.67, 4.24, 3.69, 5.64, 2.69]
    cols = [BLUE, MUTED, MUTED, MUTED, MUTED]
    ax.scatter(roe, pb, s=[70, 46, 46, 46, 46], color=cols, zorder=4,
               edgecolor=SURF, linewidth=1.2)
    m, b = np.polyfit(roe, pb, 1)
    xs = np.linspace(1, 17, 20)
    ax.plot(xs, m * xs + b, color=ORANGE, lw=1.3, ls="--", zorder=2)
    ax.text(12.2, m * 12.2 + b + .34, "P/B tracks ROE", fontsize=6.4, color=ORANGE)
    for n, r, p in zip(nm, roe, pb):
        ax.annotate(n, (r, p), textcoords="offset points", xytext=(5, -1),
                    fontsize=6.5, color=(INK if n == "Ambuja" else INK2),
                    fontweight=("bold" if n == "Ambuja" else "normal"))
    ax.set_xlabel("Return on equity (%)"); ax.set_ylabel("Price / book (x)")
    ax.set_xlim(0, 19); ax.set_ylim(0.8, 6.6)
    ax.set_title("Exhibit A12  Cheap on book because the return is poor")
    tidy(ax, xgrid=True); save(fig, "amb_pbroe")

# 13 ---- the tax credit decomposed
def f_tax():
    fig, ax = newfig(3.35, 2.15)
    labs = ["1. Litigation\nprovisions\nreleased", "1a. Tax paid\nunder protest\n(recoverable)",
            "2. Deferred tax\nliability", "3. s.72A loss\nshelter\n(memo only)",
            "Net effect\non value"]
    vals = [0.0, 2.48, -14.02, 0.0, -11.54]
    cols = [MUTED, GOOD, BAD, MUTED, NAVY]
    x = np.arange(len(vals))
    ax.bar(x, vals, color=cols, width=.6, zorder=3)
    for xi, v in zip(x, vals):
        ax.text(xi, v + (0.55 if v >= 0 else -0.55), f"{v:+.2f}" if v else "0.00",
                ha="center", va="bottom" if v >= 0 else "top",
                fontsize=6.6, color=INK, fontweight="bold" if xi == 4 else "normal")
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.2)
    ax.set_ylabel("Rs per share"); ax.set_ylim(-17, 5.5)
    ax.set_title("Exhibit A13  The Rs 2,338 cr tax credit is worth minus Rs 11.54")
    tidy(ax, zero=True); save(fig, "amb_tax")

# 14 ---- value composition: explicit vs terminal
def f_tv():
    fig, ax = newfig(3.35, 1.7)
    pv_exp = R["pv"]; pv_tv = R["pvtv"]
    ax.barh([0], [pv_exp], color=BLUE, height=.42, zorder=3, label="PV of explicit FCFF")
    ax.barh([0], [pv_tv], left=[pv_exp], color=ORANGE, height=.42, zorder=3,
            label="PV of terminal value")
    ax.text(pv_exp / 2, 0, f"{pv_exp/R['ev']*100:.0f}%", ha="center", va="center",
            color="white", fontsize=7.2, fontweight="bold")
    ax.text(pv_exp + pv_tv / 2, 0, f"{pv_tv/R['ev']*100:.0f}%", ha="center", va="center",
            color="white", fontsize=7.2, fontweight="bold")
    ax.set_yticks([]); ax.set_xlabel("Rs crore"); ax.set_ylim(-.5, .8)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.legend(fontsize=6.4, ncol=2, loc="upper left")
    ax.set_title("Exhibit A14  A ten-year horizon holds terminal value to 72%")
    tidy(ax, ygrid=False, xgrid=True); save(fig, "amb_tv")

# 15 ---- entity build
def f_entity():
    fig, ax = newfig(3.35, 1.8)
    cats = ["Share of\ngroup revenue", "Share of\ngroup EBITDA"]
    sa = [61.6, 44.7]; sub = [38.4, 55.3]
    x = np.arange(2)
    ax.bar(x, sa, color=BLUE, width=.5, zorder=3, label="Standalone parent")
    ax.bar(x, sub, bottom=np.array(sa) + 1.2, color=AQUA, width=.5, zorder=3,
           label="Subsidiaries (ACC, Orient)")
    for i in range(2):
        ax.text(i, sa[i] / 2, f"{sa[i]:.1f}%", ha="center", va="center",
                color="white", fontsize=7, fontweight="bold")
        ax.text(i, sa[i] + 1.2 + sub[i] / 2, f"{sub[i]:.1f}%", ha="center", va="center",
                color="white", fontsize=7, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=6.8)
    ax.set_ylabel("Percent"); ax.set_ylim(0, 108); ax.legend(fontsize=6.3, loc="upper center", ncol=2)
    ax.set_title("Exhibit A15  61.6% of revenue, 44.7% of profit")
    tidy(ax); save(fig, "amb_entity")

# 16 ---- what the price requires
def f_reverse():
    fig, ax = newfig(3.35, 1.85)
    labs = ["Terminal ROIC\n(operating)", "EBITDA per tonne\nFY36", "Utilisation\nFY36"]
    base = [R["t_roic"]*100, R["ebitda"][-1]*10/R["vol"][-1], 85]; req = [15.0, 2000, 90]
    x = np.arange(3); w = .34
    norm_b = [1, 1, 1]; norm_r = [r / b for r, b in zip(req, base)]
    ax.bar(x - w / 2, norm_b, w, color=BLUE, zorder=3, label="Model base case")
    ax.bar(x + w / 2, norm_r, w, color=BAD, zorder=3, label="Required for Rs 401")
    for i, (b, r) in enumerate(zip(base, req)):
        u = ["%", "", "%"][i]
        ax.text(i - w / 2, 1.02, f"{b:,.0f}{u}" if i != 0 else f"{b:.1f}%",
                ha="center", fontsize=6.4, color=INK)
        ax.text(i + w / 2, norm_r[i] + .02, f">{r:,.0f}{u}", ha="center",
                fontsize=6.4, color=BAD, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.6)
    ax.set_yticks([]); ax.set_ylim(0, 1.55); ax.legend(fontsize=6.3, ncol=2, loc="upper left")
    ax.set_title("Exhibit A16  Indexed to the base case = 1.0")
    tidy(ax, ygrid=False); save(fig, "amb_reverse")

for f in [f_football, f_bridge, f_fcff, f_roic, f_eva, f_capacity, f_ebitdat,
          f_margins, f_ic, f_sens, f_peers, f_pbroe, f_tax, f_tv, f_entity, f_reverse]:
    f(); print("ok", f.__name__)
