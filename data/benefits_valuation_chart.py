"""
Employee Benefits Valuation Chart
==================================
Author: Abheeshek Baskar

Visualizes Fractl survey data on which employee benefits are most and least
valued by job seekers. Supports Case Study 4: Employee Benefits Strategy.

Source: Fractl survey (cited in case study analysis)

Usage:
    python benefits_valuation_chart.py

Output:
    - benefits_valuation_chart.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# DATA: Fractl Survey — Benefit Consideration Rates
# % of job seekers who give each benefit "some" or "heavy" consideration
# ─────────────────────────────────────────────

BENEFITS = [
    "Health / Dental / Vision Insurance",
    "Flexible Hours",
    "More Vacation Time",
    "Work-From-Home Options",
    "Student Loan / Tuition Assistance",
    "Unlimited PTO",
    "401(k) / Retirement Matching",
    "Parental Leave",
    "Mental Health Support",
    "In-Office Perks (food, coffee)",
    "Company Events / Team Outings",
]

# Consideration rates (approximate % based on survey findings)
RATES = [88, 88, 80, 78, 48, 45, 72, 65, 58, 32, 28]

# Tier classification for color coding
TIERS = [
    "high",    # Health insurance
    "high",    # Flexible hours
    "high",    # Vacation
    "high",    # WFH
    "mid",     # Student loans
    "mid",     # Unlimited PTO
    "mid",     # 401k
    "mid",     # Parental leave
    "mid",     # Mental health
    "low",     # In-office perks
    "low",     # Company events
]

TIER_COLORS = {
    "high": "#00BCD4",
    "mid":  "#546E7A",
    "low":  "#BF360C",
}

TIER_LABELS = {
    "high": "High Value",
    "mid":  "Moderate Value",
    "low":  "Least Valued",
}

# ─────────────────────────────────────────────
# SORT: Descending by rate
# ─────────────────────────────────────────────

paired = sorted(zip(RATES, BENEFITS, TIERS), reverse=True)
rates_sorted, benefits_sorted, tiers_sorted = zip(*paired)

# ─────────────────────────────────────────────
# PLOT
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor("#0F1117")
ax.set_facecolor("#0F1117")

y_pos = np.arange(len(benefits_sorted))
bar_colors = [TIER_COLORS[t] for t in tiers_sorted]

bars = ax.barh(
    y_pos,
    rates_sorted,
    color=bar_colors,
    height=0.62,
    edgecolor="none",
    zorder=3
)

# Value labels on bars
for bar, rate in zip(bars, rates_sorted):
    ax.text(
        bar.get_width() + 1.2,
        bar.get_y() + bar.get_height() / 2,
        f"{rate}%",
        va="center", ha="left",
        color="#CCCCCC", fontsize=10, fontweight="bold"
    )

# Axes
ax.set_yticks(y_pos)
ax.set_yticklabels(benefits_sorted, color="#DDDDDD", fontsize=10.5)
ax.set_xlim(0, 102)
ax.set_xlabel("% of Job Seekers Who Give This Benefit Serious Consideration",
              color="#999999", fontsize=10, labelpad=10)
ax.tick_params(axis="x", colors="#666666", labelsize=9)
ax.tick_params(axis="y", length=0)
ax.spines[:].set_visible(False)
ax.xaxis.grid(True, color="#1A1E2A", linewidth=1, zorder=0)
ax.set_axisbelow(True)

# Invert y so highest value is on top
ax.invert_yaxis()

# Title
ax.set_title(
    "Which Employee Benefits Matter Most to Job Seekers?",
    color="#FFFFFF", fontsize=15, fontweight="bold",
    loc="left", pad=18
)
ax.text(
    0, len(benefits_sorted) + 0.9,
    "Source: Fractl Survey  ·  Case Study 4: Employee Benefits Strategy",
    color="#666666", fontsize=9, transform=ax.transData
)

# Legend
legend_patches = [
    mpatches.Patch(color=TIER_COLORS[t], label=TIER_LABELS[t])
    for t in ["high", "mid", "low"]
]
leg = ax.legend(
    handles=legend_patches,
    loc="lower right",
    framealpha=0.15,
    facecolor="#1A1D27",
    edgecolor="#333333",
    labelcolor="#CCCCCC",
    fontsize=9.5
)

# Annotation callout
ax.annotate(
    "Flexibility rivals health\ninsurance in perceived value —\nat near-zero cost to employers",
    xy=(88, 1),
    xytext=(60, 3.8),
    color="#00BCD4",
    fontsize=8.5,
    arrowprops=dict(arrowstyle="->", color="#00BCD4", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#0D1520", edgecolor="#00BCD4", alpha=0.9)
)

plt.tight_layout(pad=1.8)
plt.savefig("benefits_valuation_chart.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("✅ Chart saved → benefits_valuation_chart.png")
plt.close()
