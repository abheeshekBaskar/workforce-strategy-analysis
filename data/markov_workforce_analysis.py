"""
Markov Analysis: Workforce Transition Forecasting Model
========================================================
Author: Abheeshek Baskar
Portfolio: https://abheeshekBaskar.github.io

This script demonstrates how Markov Analysis can be applied to HR workforce
planning. It models employee transitions between job levels over time and
forecasts future workforce composition — enabling proactive talent gap analysis.

Usage:
    python markov_workforce_analysis.py

Output:
    - Console: Year-by-year workforce forecast table
    - File: markov_forecast_results.csv
    - Plot: markov_workforce_forecast.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ─────────────────────────────────────────────
# 1. DEFINE JOB STATES
# ─────────────────────────────────────────────

STATES = [
    "Junior Analyst",
    "Senior Analyst",
    "Manager",
    "Director",
    "Exit"
]

# ─────────────────────────────────────────────
# 2. TRANSITION PROBABILITY MATRIX
#
# Each row = current state
# Each column = next-period state
# Row must sum to 1.0
#
# Read row 0 as: "A Junior Analyst has a 55% chance of staying Junior Analyst,
# 25% chance of being promoted to Senior Analyst, 0% to Manager directly,
# 0% to Director, and 20% chance of exiting the organization."
# ─────────────────────────────────────────────

TRANSITION_MATRIX = np.array([
    # Jr Analyst  Sr Analyst  Manager  Director   Exit
    [0.55,        0.25,       0.00,    0.00,      0.20],   # Junior Analyst
    [0.00,        0.50,       0.30,    0.00,      0.20],   # Senior Analyst
    [0.00,        0.00,       0.60,    0.25,      0.15],   # Manager
    [0.00,        0.00,       0.00,    0.75,      0.25],   # Director
    [0.00,        0.00,       0.00,    0.00,      1.00],   # Exit (absorbing)
])

# ─────────────────────────────────────────────
# 3. CURRENT WORKFORCE (headcount by state)
# ─────────────────────────────────────────────

INITIAL_WORKFORCE = np.array([
    50,   # Junior Analyst
    30,   # Senior Analyst
    15,   # Manager
    5,    # Director
    0,    # Exit (not part of active workforce)
])

FORECAST_YEARS = 5

# ─────────────────────────────────────────────
# 4. MARKOV FORECAST ENGINE
# ─────────────────────────────────────────────

def run_markov_forecast(initial: np.ndarray, matrix: np.ndarray, years: int) -> pd.DataFrame:
    """
    Apply transition matrix iteratively to forecast workforce year-by-year.

    Parameters
    ----------
    initial : np.ndarray
        Starting headcount distribution across states.
    matrix : np.ndarray
        Stochastic transition matrix (rows sum to 1).
    years : int
        Number of periods to forecast.

    Returns
    -------
    pd.DataFrame
        Year-by-year workforce distribution (active states only).
    """
    active_states = STATES[:-1]  # Exclude "Exit" from display
    records = []

    current = initial.astype(float)
    records.append({"Year": "Current", **dict(zip(STATES, current.astype(int)))})

    for year in range(1, years + 1):
        current = current @ matrix
        records.append({"Year": f"Year {year}", **dict(zip(STATES, np.round(current).astype(int)))})

    df = pd.DataFrame(records).set_index("Year")
    return df[active_states]  # Drop "Exit" column for readability


def compute_gap_analysis(forecast: pd.DataFrame) -> pd.DataFrame:
    """
    Compare final forecast year against current headcount to surface talent gaps.
    """
    baseline = forecast.iloc[0]
    final = forecast.iloc[-1]
    gap = final - baseline

    gap_df = pd.DataFrame({
        "Current": baseline,
        f"Year {FORECAST_YEARS} Forecast": final,
        "Net Change": gap,
        "% Change": ((gap / baseline.replace(0, np.nan)) * 100).round(1)
    })
    return gap_df


# ─────────────────────────────────────────────
# 5. VISUALIZATION
# ─────────────────────────────────────────────

def plot_forecast(forecast: pd.DataFrame, output_path: str = "markov_workforce_forecast.png"):
    """
    Generate a stacked area chart showing workforce composition over time.
    """
    active_states = list(forecast.columns)
    years = list(forecast.index)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor("#0F1117")

    palette = ["#4FC3F7", "#29B6F6", "#00ACC1", "#006064"]

    # ── Left: Stacked Area Chart ──────────────────────────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor("#0F1117")

    data = forecast.values.T  # shape: (states, years)
    x = np.arange(len(years))

    ax1.stackplot(x, data, labels=active_states, colors=palette, alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, color="#CCCCCC", fontsize=10)
    ax1.set_ylabel("Headcount", color="#CCCCCC", fontsize=11)
    ax1.set_title("Workforce Composition Over Time", color="#FFFFFF", fontsize=13, fontweight="bold", pad=15)
    ax1.tick_params(colors="#CCCCCC")
    ax1.spines[:].set_color("#333333")
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

    legend = ax1.legend(loc="upper left", framealpha=0.2, labelcolor="#FFFFFF",
                        facecolor="#1A1D27", edgecolor="#444444", fontsize=9)

    # ── Right: Line Chart Per Level ───────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor("#0F1117")

    for i, state in enumerate(active_states):
        ax2.plot(x, forecast[state].values, marker="o", linewidth=2.5,
                 color=palette[i], label=state, markersize=6)

    ax2.set_xticks(x)
    ax2.set_xticklabels(years, color="#CCCCCC", fontsize=10)
    ax2.set_ylabel("Headcount", color="#CCCCCC", fontsize=11)
    ax2.set_title("Headcount Trajectory by Job Level", color="#FFFFFF", fontsize=13, fontweight="bold", pad=15)
    ax2.tick_params(colors="#CCCCCC")
    ax2.spines[:].set_color("#333333")
    ax2.grid(axis="y", color="#1E2230", linewidth=1)
    ax2.legend(loc="upper right", framealpha=0.2, labelcolor="#FFFFFF",
               facecolor="#1A1D27", edgecolor="#444444", fontsize=9)

    plt.suptitle(
        "Markov Workforce Transition Analysis  ·  5-Year Forecast",
        color="#FFFFFF", fontsize=15, fontweight="bold", y=1.01
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"\n📊 Chart saved → {output_path}")
    plt.close()


# ─────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  MARKOV WORKFORCE TRANSITION ANALYSIS")
    print("  5-Year Forecast Model")
    print("=" * 60)

    # ── Validate matrix ───────────────────────────────────────────
    row_sums = TRANSITION_MATRIX.sum(axis=1)
    assert np.allclose(row_sums, 1.0), f"Transition matrix rows must sum to 1.0. Got: {row_sums}"

    # ── Print transition matrix ───────────────────────────────────
    print("\n📋 Transition Probability Matrix:")
    tm_df = pd.DataFrame(TRANSITION_MATRIX, index=STATES, columns=STATES)
    print(tm_df.to_string())

    # ── Run forecast ──────────────────────────────────────────────
    forecast = run_markov_forecast(INITIAL_WORKFORCE, TRANSITION_MATRIX, FORECAST_YEARS)

    print("\n📈 Workforce Forecast (Headcount by Job Level):")
    print(forecast.to_string())

    # ── Gap analysis ──────────────────────────────────────────────
    gap = compute_gap_analysis(forecast)
    print(f"\n🔍 Gap Analysis (Current vs Year {FORECAST_YEARS}):")
    print(gap.to_string())

    # ── Key insights ──────────────────────────────────────────────
    print("\n💡 Key Insights:")
    for state in forecast.columns:
        delta = forecast[state].iloc[-1] - forecast[state].iloc[0]
        direction = "▲" if delta > 0 else "▼" if delta < 0 else "→"
        print(f"   {direction} {state}: {forecast[state].iloc[0]} → {forecast[state].iloc[-1]} ({delta:+.0f})")

    print("\n   Interpretation: Headcount concentration shifts upward as")
    print("   junior employees are promoted or exit, requiring external")
    print("   hiring to maintain junior pipeline.")

    # ── Save CSV ──────────────────────────────────────────────────
    output_csv = Path(__file__).parent / "markov_forecast_results.csv"
    forecast.to_csv(output_csv)
    print(f"\n💾 Results saved → {output_csv}")

    # ── Plot ──────────────────────────────────────────────────────
    output_png = Path(__file__).parent / "markov_workforce_forecast.png"
    plot_forecast(forecast, str(output_png))

    print("\n✅ Analysis complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
