"""Company-profile exhibits: header wordmarks, ownership structure, products."""
import numpy as np
import matplotlib.patches as mpatches
from style import *

# ------------------------------------------------------------------ wordmarks
def wordmark(name, sub, fname, accent):
    """A typeset wordmark for the running header.

    This is NOT the company's trademark logo. It is a plain typographic mark in
    the report's own design language. Drop a real logo PNG in at fig/<fname>.png
    and recompile to swap it in; the header geometry is unchanged.
    """
    fig, ax = plt.subplots(figsize=(2.6, 0.30))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 12)
    ax.add_patch(mpatches.Rectangle((0, 0.4), 2.9, 11.2, color=accent, lw=0))
    ax.text(6.0, 6.0, name, fontsize=13.0, fontweight="bold", color=NAVY,
            va="center", ha="left")
    fig.savefig(os.path.join(FIGDIR, fname + ".png"), dpi=460,
                bbox_inches="tight", pad_inches=0.008, transparent=True)
    plt.close(fig)

# ------------------------------------------------------- ownership structure
def structure(title, parent, parent_pct, company, subs, fname, accent, note):
    fig, ax = newfig(3.35, 2.25)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    def box(x, y, w, h, label, fc, tc="white", fs=7.0, bold=True):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.4", fc=fc, ec="none", zorder=3))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", color=tc,
                fontsize=fs, fontweight=("bold" if bold else "normal"), zorder=4)

    box(14, 82, 72, 13, parent, MUTED, fs=6.6)
    ax.annotate("", xy=(50, 69), xytext=(50, 82),
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.1))
    ax.text(52.5, 75.5, parent_pct, fontsize=6.8, color=INK, fontweight="bold", va="center")

    box(12, 55, 76, 14, company, accent, fs=8.2)

    n = len(subs)
    slot = 96.0 / n
    for i, (nm, pct) in enumerate(subs):
        cx = 2 + slot * i + slot / 2
        ax.plot([50, 50], [55, 44], color=INK2, lw=1.0)
        ax.plot([cx, cx], [44, 36], color=INK2, lw=1.0)
        ax.plot([min(cx, 50), max(cx, 50)], [44, 44], color=INK2, lw=1.0)
        ax.add_patch(mpatches.FancyArrowPatch((cx, 38), (cx, 34.5),
            arrowstyle="-|>", color=INK2, lw=1.0, mutation_scale=8))
        box(cx - slot / 2 + 2.2, 20, slot - 4.4, 14, nm, "#D7E3F5", tc=INK, fs=6.2)
        ax.text(cx, 16.4, pct, ha="center", fontsize=6.5, color=INK, fontweight="bold")
    ax.text(50, 6.5, note, ha="center", va="center", fontsize=6.0, color=MUTED,
            wrap=True)
    ax.set_title(title, pad=6)
    save(fig, fname)

# ------------------------------------------------------------------- products
def products(title, rows, fname, note):
    """rows: (segment, share_of_revenue_pct, colour)"""
    fig, ax = newfig(3.35, 1.85)
    labs = [r[0] for r in rows]; vals = [r[1] for r in rows]; cols = [r[2] for r in rows]
    y = np.arange(len(rows))
    ax.barh(y, vals, color=cols, height=.52, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 1.4, yi, f"{v:.0f}%", va="center", fontsize=7.0, color=INK,
                fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=6.7); ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.22); ax.set_xlabel("Share of cement revenue (%)")
    ax.set_title(title)
    tidy(ax, ygrid=False, xgrid=True)
    fig.text(0.02, -0.02, note, fontsize=5.9, color=MUTED, ha="left")
    save(fig, fname)

# ------------------------------------------------------------- shareholding
def shareholding(title, promoter, fname, accent, footnote):
    fig, ax = newfig(3.35, 1.15)
    ax.barh([0], [promoter], color=accent, height=.44, zorder=3)
    ax.barh([0], [100 - promoter], left=[promoter], color="#C9CDD4", height=.44, zorder=3)
    ax.text(promoter / 2, 0, f"Promoter {promoter:.2f}%", ha="center", va="center",
            color="white", fontsize=7.4, fontweight="bold")
    ax.text(promoter + (100 - promoter) / 2, 0, f"Public float {100-promoter:.2f}%",
            ha="center", va="center", color=INK, fontsize=7.0, fontweight="bold")
    ax.set_yticks([]); ax.set_xlim(0, 100); ax.set_ylim(-.45, .45)
    ax.set_xlabel("Percent of equity share capital")
    ax.set_title(title)
    tidy(ax, ygrid=False, xgrid=True)
    fig.text(0.02, -0.06, footnote, fontsize=5.9, color=MUTED, ha="left")
    save(fig, fname)

if __name__ == "__main__":
    wordmark("Ambuja Cements", "NSE: AMBUJACEM  |  Adani Group", "logo_amb", ORANGE)
    wordmark("UltraTech Cement", "NSE: ULTRACEMCO  |  Aditya Birla Group", "logo_utcl", BLUE)

    structure("Exhibit A17  Ownership and control at the valuation date",
              "Adani promoter group", "67.64%",
              "AMBUJA CEMENTS LTD",
              [("ACC Ltd\n(listed)", "50.05%"), ("Orient\nCement", "majority"),
               ("Sanghi\nIndustries", "merged"), ("Penna\nCement", "merged")],
              "amb_ownership", ORANGE,
              "All four are being merged into Ambuja; the share count rises c.13.7%.")

    structure("Exhibit U15  Ownership and control at the valuation date",
              "Aditya Birla group / Grasim Industries", "promoter control",
              "ULTRATECH CEMENT LTD",
              [("The India\nCements (listed)", "74.99%"),
               ("Kesoram\ncement assets", "acquired"),
               ("Other subsidiaries\n& associates", "various")],
              "utcl_ownership", BLUE,
              "Standalone is 92.8% of group revenue and 90.7% of group EBITDA.")

    products("Exhibit A18  What Ambuja sells",
             [("Grey cement — OPC, PPC, PSC\n(Ambuja, ACC, Orient brands)", 86, ORANGE),
              ("Blended & premium products\n(Ambuja Plus, Kawach, Compocem)", 9, "#F0A07C"),
              ("Ready-mix concrete & other\n(ACC Concrete, aggregates)", 5, "#F7CDBA")],
             "amb_products",
             "Split is indicative of the product mix disclosed in the FY2025-26 report; "
             "the company does not publish a full revenue split by product.")

    products("Exhibit U16  What UltraTech sells",
             [("Grey cement — OPC, PPC, PSC\n(UltraTech brand)", 85, BLUE),
              ("White cement, putty & wall care\n(Birla White)", 7, "#7FA9E0"),
              ("Ready-mix concrete & building\nproducts (UltraTech Building Solutions)", 8, "#C3D7F1")],
             "utcl_products",
             "Split is indicative of the segment mix disclosed in the FY2025-26 report; "
             "grey cement is the reported primary segment.")

    shareholding("Exhibit A19  Promoter holding and free float",
                 67.64, "amb_shareholding", ORANGE,
                 "Promoter 67.64% (67.68% on a voting-rights basis) at 31 March 2026; revised to "
                 "67.29% from 10 April 2026 on the Sanghi share issue. Company disclosure.")
    print("profile exhibits written")
