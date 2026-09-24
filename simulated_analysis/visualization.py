from __future__ import annotations

import os
from pathlib import Path

_MPL_CONFIG_DIR = Path("outputs/.matplotlib").resolve()
_MPL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CONFIG_DIR))

import matplotlib.pyplot as plt
import pandas as pd


COLORS = {"navy": "#17324D", "blue": "#3978A8", "gold": "#D39B38", "grid": "#D9E0E6"}


def _style(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def create_charts(summaries: dict, chart_dir: Path) -> list[Path]:
    chart_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titlesize": 13})
    created: list[Path] = []

    monthly = summaries["monthly"]
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(monthly["month"], monthly["revenue"], color=COLORS["navy"], linewidth=2.5)
    axes[0].fill_between(monthly["month"], monthly["revenue"], color=COLORS["blue"], alpha=0.13)
    axes[0].set_title("Monthly Revenue")
    axes[0].set_ylabel("Revenue")
    axes[1].plot(monthly["month"], monthly["orders"], color=COLORS["gold"], linewidth=2.5)
    axes[1].set_title("Monthly Orders")
    axes[1].set_ylabel("Orders")
    axes[1].set_xlabel("Month")
    for ax in axes:
        _style(ax)
    fig.suptitle("Business Trend Overview", x=0.08, ha="left", fontsize=16, fontweight="bold")
    fig.tight_layout()
    path = chart_dir / "monthly_trends.png"
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    created.append(path)

    region = summaries["region"].sort_values("revenue")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(region["region"], region["revenue"], color=COLORS["blue"])
    ax.set_title("Revenue by Region")
    ax.set_xlabel("Revenue")
    _style(ax)
    fig.tight_layout()
    path = chart_dir / "region_revenue.png"
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    created.append(path)

    channel = summaries["channel"].sort_values("roi")
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(channel["channel"], channel["roi"] * 100, color=COLORS["gold"])
    ax.bar_label(bars, fmt="%.0f%%", padding=4)
    ax.set_title("Marketing ROI by Channel")
    ax.set_xlabel("ROI ((Revenue - Spend) / Spend)")
    _style(ax)
    fig.tight_layout()
    path = chart_dir / "channel_roi.png"
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    created.append(path)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(channel["marketing_spend"], channel["revenue"], s=100, color=COLORS["navy"])
    for _, row in channel.iterrows():
        ax.annotate(row["channel"], (row["marketing_spend"], row["revenue"]), xytext=(7, 5), textcoords="offset points")
    ax.set_title("Channel Spend and Revenue")
    ax.set_xlabel("Marketing spend")
    ax.set_ylabel("Revenue")
    _style(ax)
    fig.tight_layout()
    path = chart_dir / "channel_spend_revenue.png"
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    created.append(path)

    return created
