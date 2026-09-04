#!/usr/bin/env python3
"""
Altitude versus downrange for the controlled re-entry of Melpomene (Scenario 2).

Everything plotted here is read from the DRAMA-SARA output file
"..._Altitude_vs__Downrange.html". No trajectory is recomputed.

Outputs footprint_controlled.pdf (vector, for LaTeX) and .png (for quick viewing).
"""

import json
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# 0. Input file
# ----------------------------------------------------------------------------
SARA_HTML = "2026-08-29_16_55_45_default_Altitude_vs__Downrange.html"
MAIN_LABEL = r"Main body (bus and antenna)"

# ----------------------------------------------------------------------------
# 1. Fonts. Internal Matplotlib emulation using Times and STIX (math)
# ----------------------------------------------------------------------------
plt.rcParams.update({
    "text.usetex": False,                  # Disable external LaTeX dependency
    "font.family": "serif",                
    "font.serif": ["Times New Roman", "Times", "serif"], # Use Times font
    "mathtext.fontset": "stix",            # Math elements in STIX (matches Times)
    "axes.formatter.use_mathtext": True,   # Axis numbers use math font
    "axes.unicode_minus": False,           # Prevent minus sign errors
    "font.size": 14,                       # Larger base text size
    "axes.linewidth": 0.8
})

# ----------------------------------------------------------------------------
# 2. Which surviving object belongs to which material.
# ----------------------------------------------------------------------------
MATERIAL_OF = {
    "SP":      "Aluminium",
    "Antenna": "Aluminium",
    "PL3":     "Aluminium",
    "TCU":     "Copper",
    "RWL":     "Steel",
    "Batt":    "Copper",
    "Tank":    "Titanium",
}
STYLE = {
    "Titanium":  ("#1f6fe0", r"Titanium (TiAl6V4)"),
    "Copper":    ("#e8622a", r"Copper"),
    "Steel":     ("#00a878", r"Steel (A316)"),
    "Aluminium": ("#4b2fa8", r"Aluminium (AA7075)"),
}
GROUND = 0.5     # km, below this an object is taken as having reached the ground

def group_of(name):
    """Map an object name to the entry of MATERIAL_OF it belongs to."""
    for key in ("SP", "Antenna", "PL3", "TCU", "RWL", "Batt", "Tank"):
        if name.startswith(key):
            return key
    return None

# ----------------------------------------------------------------------------
# 3. Read the traces out of the DRAMA html
# ----------------------------------------------------------------------------
try:
    raw = open(SARA_HTML, encoding="utf8", errors="replace").read()
    data = json.loads(re.search(r"var plotly_data = (\{.*?\})\s*\n", raw, re.S).group(1))
except FileNotFoundError:
    print(f"Error: File '{SARA_HTML}' not found.")
    exit(1)

compound, survivors, demised = None, {}, []
for trace in data.get("data", []):
    name = trace.get("name", "")
    if trace.get("mode") != "lines" or len(trace.get("x", [])) < 2:
        continue
    x = [float(v) for v in trace["x"]]
    y = [float(v) for v in trace["y"]]
    if name.startswith("Compound_of"):
        if compound is None or len(x) > len(compound[0]):
            compound = (x, y)
        continue
    if y[-1] <= GROUND:
        survivors.setdefault(group_of(name), (x, y))
    else:
        demised.append((x, y))

x_bu, h_bu = compound[0][-1], compound[1][-1]
x_land = {k: v[0][-1] for k, v in survivors.items()}
x_first, x_last = min(x_land.values()), max(x_land.values())
footprint = x_last - x_first
h_dem = [y[-1] for _, y in demised]
n_dem, dem_lo, dem_hi = len(demised), min(h_dem), max(h_dem)

print(f"break-up at {x_bu:.0f} km, {h_bu:.1f} km altitude")
print(f"{len(survivors)} surviving groups, {n_dem} items demised "
      f"between {dem_lo:.0f} and {dem_hi:.0f} km")
print(f"footprint {footprint:.0f} km, from {x_first:.0f} to {x_last:.0f} km")

# ----------------------------------------------------------------------------
# 4. Figure
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.2, 5.3))

for x, y in demised:
    ax.plot(x, y, color="0.72", lw=0.7, zorder=2)
ax.plot([], [], color="0.72", lw=0.9, label=r"Demised before impact")

ax.axhline(h_bu, color="0.55", ls="--", lw=0.9, zorder=1)
ax.plot(*compound, color="black", lw=2.6, zorder=6, label=MAIN_LABEL)

drawn = set()
for key, (x, y) in survivors.items():
    if key is None:
        continue
    material = MATERIAL_OF[key]
    color, label = STYLE[material]
    ax.plot(x, y, color=color, lw=1.9, zorder=5,
            label=label if material not in drawn else None)
    drawn.add(material)

# --- annotations, all placed in empty regions of the plot --------------------
ax.text(60, h_bu + 3.5, rf"break-up of the main body, ${h_bu:.0f}$ km",
        fontsize=13, color="0.3", va="bottom")

n_high = sum(1 for h in h_dem if h >= 66)
ax.annotate(rf"${n_dem}$ items demise before impact," "\n"
            rf"${n_high}$ of them between ${min(h for h in h_dem if h >= 66):.0f}$ "
            rf"and ${dem_hi:.0f}$ km",
            xy=(3250, 73.5), xytext=(2950, 104), fontsize=13, color="0.3",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.8,
                            shrinkA=6, shrinkB=2))

ax.annotate(r"solar panels separate at the entry" "\n" r"interface and land first",
            xy=(x_first - 12, 26), xytext=(430, 46), fontsize=13, color="0.3",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.8,
                            shrinkA=6, shrinkB=2))

# --- Footprint annotation ---
ax.annotate("", xy=(x_first, 9), xytext=(x_last, 9),
            arrowprops=dict(arrowstyle="<->", color="0.3", lw=1.1))

_fp = f"{footprint:,.0f}".replace(",", r"\,")
ax.text(x_first - 80, 9, rf"footprint, ${_fp}$ km",
        ha="right", va="center", fontsize=13, color="0.3")

# -----------------------------------------------------------------------

ax.set_xlabel(r"Downrange from the entry interface [km]")
ax.set_ylabel(r"Altitude [km]")
ax.set_xlim(0, x_last * 1.04)
ax.set_ylim(0, 134)
ax.grid(alpha=0.22, lw=0.6)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

handles, labels = ax.get_legend_handles_labels()
order = [labels.index(MAIN_LABEL)] + \
        [i for i, l in enumerate(labels)
         if l not in (MAIN_LABEL, r"Demised before impact")] + \
        [labels.index(r"Demised before impact")]
        
ax.legend([handles[i] for i in order], [labels[i] for i in order],
          loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3,
          frameon=False, fontsize=13, columnspacing=2.2)

fig.tight_layout()
fig.savefig("footprint_controlled.pdf", bbox_inches="tight")
fig.savefig("footprint_controlled.png", dpi=200, bbox_inches="tight")
print("Graphs generated.")