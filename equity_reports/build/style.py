import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np, os

# --- validated categorical slots (dataviz reference palette, light mode) ---
BLUE   = "#2a78d6"   # slot 1  - subject company / primary series
ORANGE = "#eb6834"   # slot 2  - comparator / second series
AQUA   = "#1baf7a"   # slot 3  - third series
# --- status (reserved, never used as "series 4") ---
GOOD   = "#1e8e5a"
BAD    = "#c0392b"
WARN   = "#eda100"
# --- ink & surface ---
NAVY   = "#1F3864"
INK    = "#14161a"
INK2   = "#52514e"
MUTED  = "#8a8a86"
GRID   = "#e4e6ea"
SURF   = "#ffffff"

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "fig")
os.makedirs(FIGDIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.6,
    "axes.edgecolor": GRID, "axes.linewidth": 0.7,
    "axes.labelcolor": INK2, "axes.titlesize": 8.4,
    "axes.titleweight": "bold", "axes.titlecolor": NAVY,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 7.0, "ytick.labelsize": 7.0,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "legend.frameon": False,
    "legend.fontsize": 7.0, "xtick.major.size": 0, "ytick.major.size": 0,
})

def newfig(w=3.35, h=2.25):
    fig, ax = plt.subplots(figsize=(w, h)); return fig, ax

def tidy(ax, ygrid=True, xgrid=False, zero=False):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    if ygrid: ax.set_axisbelow(True); ax.yaxis.grid(True, color=GRID, lw=0.6)
    if xgrid: ax.set_axisbelow(True); ax.xaxis.grid(True, color=GRID, lw=0.6)
    if zero: ax.axhline(0, color=MUTED, lw=0.8)

def save(fig, name, pad=0.02):
    fig.tight_layout(pad=0.35)
    p = os.path.join(FIGDIR, name + ".png")
    fig.savefig(p, dpi=260, bbox_inches="tight", pad_inches=pad)
    plt.close(fig); return p

def pct(x, d=0): return f"{x*100:.{d}f}%"

def bar_labels(ax, xs, ys, fmt="{:,.0f}", dy=0.012, color=INK, size=6.6, rot=0):
    rng = max(ys) - min(min(ys), 0)
    for x, y in zip(xs, ys):
        va = "bottom" if y >= 0 else "top"
        off = rng * dy * (1 if y >= 0 else -1)
        ax.text(x, y + off, fmt.format(y), ha="center", va=va,
                fontsize=size, color=color, rotation=rot)

def waterfall(ax, labels, deltas, start=0.0, total_label=None,
              pos=GOOD, neg=BAD, base=BLUE, fmt="{:,.0f}"):
    """Bridge chart. labels[0] names the opening bar; labels[1:] name each delta."""
    assert len(labels) == len(deltas) + 1, "labels must be 1 + len(deltas)"
    nbar = len(labels) + (1 if total_label else 0)
    xs = np.arange(nbar)
    bottoms = [0.0]; heights = [start]; colors = [base]; tops = [start]
    cum = start
    for d in deltas:
        if d >= 0: bottoms.append(cum); heights.append(d); colors.append(pos)
        else:      bottoms.append(cum + d); heights.append(-d); colors.append(neg)
        cum += d; tops.append(cum)
    if total_label:
        bottoms.append(0.0); heights.append(cum); colors.append(base); tops.append(cum)
    ax.bar(xs, heights, bottom=bottoms, color=colors, width=0.62, zorder=3,
           edgecolor=SURF, linewidth=1.4)
    ax.set_xticks(xs)
    ax.set_xticklabels(list(labels) + ([total_label] if total_label else []),
                       rotation=32, ha="right", fontsize=6.4)
    run = start
    for i in range(len(deltas)):
        ax.plot([xs[i] + 0.31, xs[i + 1] - 0.31], [run, run], color=MUTED, lw=0.6, zorder=2)
        run += deltas[i]
    if total_label:
        ax.plot([xs[len(deltas)] + 0.31, xs[-1] - 0.31], [run, run], color=MUTED, lw=0.6, zorder=2)
    span = max(tops + [0]) - min(tops + [0]) or 1.0
    for x, b, h in zip(xs, bottoms, heights):
        ax.text(x, b + h + span * 0.025, fmt.format(h if h == heights[0] or True else h),
                ha="center", va="bottom", fontsize=6.3, color=INK)
    tidy(ax, zero=True)
    return ax

def heat(ax, M, rowlab, collab, fmt="{:,.0f}", ref=None, cmap_lo="#f2f7fd",
         cmap_hi="#2a78d6", title_x="", title_y=""):
    """Sequential single-hue heatmap (magnitude). None cells render blank."""
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    cm = LinearSegmentedColormap.from_list("seq", [cmap_lo, cmap_hi])
    A = np.array([[np.nan if v is None else v for v in r] for r in M], dtype=float)
    fin = A[np.isfinite(A)]
    norm = Normalize(vmin=np.nanmin(fin), vmax=np.nanmax(fin))
    ax.imshow(A, cmap=cm, norm=norm, aspect="auto")
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if not np.isfinite(A[i, j]):
                ax.text(j, i, "—", ha="center", va="center", fontsize=6.4, color=MUTED); continue
            shade = norm(A[i, j])
            ax.text(j, i, fmt.format(A[i, j]), ha="center", va="center",
                    fontsize=6.4, color=("white" if shade > 0.58 else INK),
                    fontweight=("bold" if ref == (i, j) else "normal"))
            if ref == (i, j):
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False,
                                           edgecolor=INK, lw=1.6, zorder=5))
    ax.set_xticks(range(len(collab))); ax.set_xticklabels(collab, fontsize=6.8)
    ax.set_yticks(range(len(rowlab))); ax.set_yticklabels(rowlab, fontsize=6.8)
    ax.set_xlabel(title_x, fontsize=7.0); ax.set_ylabel(title_y, fontsize=7.0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
