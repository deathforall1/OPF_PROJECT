"""Ownership, margin-stack, working-capital and D&A exhibits."""
import numpy as np
from style import *

# ---------------------------------------------------------------- donuts
def donut(title, labels, vals, cols, fname, note, centre):
    fig = plt.figure(figsize=(3.35, 1.95))
    axp = fig.add_axes([0.00, 0.06, 0.46, 0.80])
    axl = fig.add_axes([0.47, 0.06, 0.53, 0.80]); axl.axis("off")
    wedges, _ = axp.pie(vals, colors=cols, startangle=90, counterclock=False,
                        wedgeprops=dict(width=0.40, edgecolor=SURF, linewidth=1.5))
    axp.text(0, 0.10, centre[0], ha="center", va="center", fontsize=14,
             fontweight="bold", color=NAVY)
    axp.text(0, -0.22, centre[1], ha="center", va="center", fontsize=6.4, color=INK2)
    axp.axis("equal")
    n = len(labels)
    for i, (l, v, c) in enumerate(zip(labels, vals, cols)):
        y = 0.90 - i * (0.80 / max(n, 1))
        axl.add_patch(plt.Rectangle((0.02, y - 0.030), 0.055, 0.060,
                                    color=c, transform=axl.transAxes, clip_on=False))
        axl.text(0.10, y, l, fontsize=6.5, color=INK, va="center",
                 transform=axl.transAxes)
        axl.text(1.00, y, f"{v:.2f}%", fontsize=6.7, color=INK, va="center",
                 ha="right", fontweight="bold", transform=axl.transAxes)
    fig.text(0.02, 0.94, title, fontsize=8.4, fontweight="bold", color=NAVY, ha="left")
    fig.text(0.02, -0.045, note, fontsize=5.7, color=MUTED, ha="left")
    p = os.path.join(FIGDIR, fname + ".png")
    fig.savefig(p, dpi=260, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

# ------------------------------------------------------------ margin stack
def marginstack(title, rows, fname, note):
    """rows: (label, FY25, FY26)"""
    fig, ax = newfig(3.35, 2.0)
    labs = [r[0] for r in rows]
    a = [r[1] for r in rows]; b = [r[2] for r in rows]
    x = np.arange(len(rows)); w = .36
    ax.bar(x - w/2, a, w, color=MUTED, zorder=3, label="FY2024-25")
    ax.bar(x + w/2, b, w, color=BLUE, zorder=3, label="FY2025-26")
    for xi, v in zip(x - w/2, a):
        ax.text(xi, v + 1.0, f"{v:.1f}", ha="center", fontsize=6.3, color=INK)
    for xi, v, prev in zip(x + w/2, b, a):
        c = GOOD if v >= prev else BAD
        ax.text(xi, v + 1.0, f"{v:.1f}", ha="center", fontsize=6.3, color=c,
                fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.4)
    ax.set_ylabel("Percent of revenue"); ax.set_ylim(0, max(a + b) * 1.22)
    ax.legend(fontsize=6.3, ncol=2, loc="upper right")
    ax.set_title(title)
    tidy(ax)
    fig.text(0.02, -0.02, note, fontsize=5.8, color=MUTED, ha="left")
    save(fig, fname)

# --------------------------------------------------------------- CCC
def ccc(title, dio, dso, dpo, cc, fname, note):
    """each arg: (FY25, FY26)"""
    fig, ax = newfig(3.35, 2.0)
    labs = ["Inventory\ndays (DIO)", "Receivable\ndays (DSO)",
            "Payable\ndays (DPO)", "Cash conversion\ncycle"]
    a = [dio[0], dso[0], dpo[0], cc[0]]; b = [dio[1], dso[1], dpo[1], cc[1]]
    x = np.arange(4); w = .36
    cols_b = [BLUE, BLUE, BLUE, NAVY]
    ax.bar(x - w/2, a, w, color=MUTED, zorder=3, label="FY2024-25")
    ax.bar(x + w/2, b, w, color=cols_b, zorder=3, label="FY2025-26")
    for xi, v in zip(x - w/2, a):
        ax.text(xi, v + .7, f"{v:.1f}", ha="center", fontsize=6.3, color=INK)
    for xi, v in zip(x + w/2, b):
        ax.text(xi, v + .7, f"{v:.1f}", ha="center", fontsize=6.3, color=INK,
                fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.3)
    ax.set_ylabel("Days"); ax.set_ylim(0, max(a + b) * 1.22)
    ax.legend(fontsize=6.3, ncol=2, loc="upper right")
    ax.set_title(title)
    tidy(ax)
    fig.text(0.02, -0.02, note, fontsize=5.8, color=MUTED, ha="left")
    save(fig, fname)

# --------------------------------------------------------------- D&A
def da_split(fname):
    fig, ax = newfig(3.35, 2.0)
    labs = ["PPE depreciation,\nnet", "Right-of-use\ndepreciation",
            "Intangible\namortisation"]
    a = [1830, 210, 257]; b = [2677, 287, 607]
    x = np.arange(3); w = .36
    ax.bar(x - w/2, a, w, color=MUTED, zorder=3, label="FY2024-25")
    ax.bar(x + w/2, b, w, color=[BLUE, BLUE, BAD], zorder=3, label="FY2025-26")
    for xi, v in zip(x - w/2, a):
        ax.text(xi, v + 55, f"{v:,}", ha="center", fontsize=6.3, color=INK)
    for xi, v in zip(x + w/2, b):
        ax.text(xi, v + 55, f"{v:,}", ha="center", fontsize=6.3, color=INK,
                fontweight="bold")
    ax.annotate("+136%", (2 + w/2, 607), textcoords="offset points", xytext=(20, -4),
                fontsize=6.6, color=BAD, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.4)
    ax.set_ylabel("Rs crore"); ax.set_ylim(0, 3200)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.legend(fontsize=6.3, ncol=2, loc="upper left")
    ax.set_title("Exhibit A22  The charge that broke the EBIT margin")
    tidy(ax)
    fig.text(0.02, -0.02, "Total D&A rose 55.4% to Rs 3,570 cr against revenue growth of "
             "15.1%. Source: FY2025-26 consolidated statements, Note 49.",
             fontsize=5.8, color=MUTED, ha="left")
    save(fig, "amb_da")

if __name__ == "__main__":
    donut("Exhibit A20  Shareholding pattern, June 2026",
          ["Promoter group", "Mutual funds", "Other domestic institutions",
           "Foreign institutions", "Retail and others"],
          [67.33, 9.12, 8.42, 5.63, 9.50],
          [ORANGE, BLUE, "#7FA9E0", AQUA, "#C9CDD4"],
          "amb_ownership_donut",
          "Promoter shares are reported unpledged. Percentages sum to 100%. Source: "
          "FY2025-26 Integrated Annual Report, Shareholder Information; shareholding-pattern filings.",
          ("67.3%", "promoter"))

    donut("Exhibit U17  Shareholding pattern, June 2026",
          ["Promoter group", "Public institutions", "Public non-institutions",
           "Non-promoter non-public"],
          [59.33, 32.55, 7.95, 0.17],
          [BLUE, ORANGE, "#F0A07C", "#C9CDD4"],
          "utcl_ownership_donut",
          "Promoter control stable and unpledged. Foreign ownership fell while domestic "
          "mutual-fund and insurance ownership rose. Source: UltraTech shareholding-pattern filing.",
          ("59.3%", "promoter"))

    marginstack("Exhibit A21  Direct economics improved; the operating line did not",
                [("Manufacturing\ngross margin", 57.9, 58.8),
                 ("Delivered\ngross margin", 34.4, 35.4),
                 ("EBITDA\nmargin", 16.9, 16.1),
                 ("EBIT\nmargin", 10.4, 7.4)],
                "amb_marginstack",
                "Manufacturing gross margin deducts materials, stock-in-trade, inventory "
                "movement and power and fuel; delivered gross margin also deducts freight. "
                "Neither is a reported Ind AS subtotal. Source: FY2025-26 consolidated statements, Notes 44-51.")

    marginstack("Exhibit U18  At UltraTech the gain reached the operating line",
                [("Manufacturing\ngross margin", 57.7, 58.4),
                 ("Delivered\ngross margin", 34.7, 36.8),
                 ("EBITDA\nmargin", 16.5, 19.2),
                 ("EBIT\nmargin", 11.2, 14.0)],
                "utcl_marginstack",
                "Consolidated basis, so the EBITDA margin differs from the 18.8% standalone "
                "figure used in the valuation. Same definitions as Exhibit A21. "
                "Source: FY2025-26 consolidated results.")

    ccc("Exhibit A23  The cycle improved, but on supplier credit",
        (33.9, 29.8), (17.2, 17.0), (18.4, 26.0), (32.7, 20.8),
        "amb_ccc",
        "DIO and DPO use cash operating cost; DSO uses revenue from operations. Closing-balance "
        "proxies. Payables rose 39.7%, which is the main reason the cycle fell. "
        "Source: FY2025-26 consolidated statements, Notes 15, 17 and 35.")

    ccc("Exhibit U19  A cleaner working-capital improvement",
        (55.1, 49.5), (28.3, 24.9), (53.7, 52.3), (29.7, 22.1),
        "utcl_ccc",
        "Inventory days fell 5.6 and receivable days 3.4, more than offsetting a 1.4-day "
        "reduction in payable days. Core trade-cycle working capital released about Rs 639 crore. "
        "Source: FY2025-26 consolidated results and balance sheet.")

    da_split("amb_da")
    print("extra exhibits written")

def industry():
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(3.35,1.75),gridspec_kw={"width_ratios":[1.15,1]})
    yrs=["FY24","FY25","FY26","FY27E"]; prod=[416,452.5,491.4,527]
    cols=[MUTED,MUTED,BLUE,"#A8C4EA"]
    ax1.bar(yrs,prod,color=cols,width=.62,zorder=3)
    for x,v in zip(yrs,prod):
        ax1.text(x,v+9,f"{v:,.0f}",ha="center",fontsize=6.2,color=INK)
    ax1.set_ylabel("Mn tonnes",fontsize=6.6); ax1.set_ylim(0,600)
    ax1.tick_params(axis="x",labelsize=6.2)
    ax1.set_title("India cement production",fontsize=7.4)
    ax1.text(0.02,0.94,"+8.6% in FY26;\n7-8% outlook FY27",transform=ax1.transAxes,
             fontsize=5.9,color=INK2,va="top")
    tidy(ax1)
    nm=["UltraTech","Ambuja","Rest of\nindustry"]; sh=[28.6,15.1,56.3]
    c=[BLUE,ORANGE,"#D5D8DD"]
    w,_=ax2.pie(sh,colors=c,startangle=90,counterclock=False,
                wedgeprops=dict(width=.42,edgecolor=SURF,linewidth=1.4))
    ax2.text(0,0.06,"491",ha="center",va="center",fontsize=11,fontweight="bold",color=NAVY)
    ax2.text(0,-0.20,"Mn.T FY26",ha="center",va="center",fontsize=5.6,color=INK2)
    ax2.axis("equal"); ax2.set_title("Share of output",fontsize=7.4)
    for i,(n,v) in enumerate(zip(nm,sh)):
        ax2.text(1.12,0.55-i*0.30,f"{n}  {v:.1f}%",fontsize=5.9,color=INK,
                 transform=ax2.transAxes,va="center")
    fig.text(0.02,-0.05,"FY27E is the mid-point of ICRA's 7-8% volume outlook applied to "
             "FY26 production. Share is company sales divided by industry production - "
             "directional, not a reported market share. Sources: IBEF, Indian Cement "
             "Industry, May 2026; ICRA; company reports.",fontsize=5.3,color=MUTED,ha="left")
    save(fig,"ind_india")

if __name__ == "__main__":
    industry(); print("industry exhibit written")
