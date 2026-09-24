from __future__ import annotations

import pandas as pd


def _add_rates(summary: pd.DataFrame) -> pd.DataFrame:
    result = summary.copy()
    result["conversion_rate"] = result["orders"] / result["customers"]
    result["roi"] = (result["revenue"] - result["marketing_spend"]) / result["marketing_spend"]
    return result


def summarize(data: pd.DataFrame) -> dict[str, pd.DataFrame | float | int | str]:
    """Create analysis-ready aggregates using weighted rate calculations."""

    clean = data.copy()
    clean["date"] = pd.to_datetime(clean["date"])
    clean["month"] = clean["date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        clean.groupby("month", as_index=False)[["customers", "orders", "revenue", "marketing_spend"]]
        .sum()
        .pipe(_add_rates)
    )
    region = (
        clean.groupby("region", as_index=False)[["customers", "orders", "revenue", "marketing_spend"]]
        .sum()
        .pipe(_add_rates)
        .sort_values("revenue", ascending=False)
    )
    channel = (
        clean.groupby("channel", as_index=False)[["customers", "orders", "revenue", "marketing_spend"]]
        .sum()
        .pipe(_add_rates)
        .sort_values("roi", ascending=False)
    )

    total_revenue = float(clean["revenue"].sum())
    total_spend = float(clean["marketing_spend"].sum())
    total_orders = int(clean["orders"].sum())
    total_customers = int(clean["customers"].sum())
    return {
        "monthly": monthly,
        "region": region,
        "channel": channel,
        "total_revenue": total_revenue,
        "total_spend": total_spend,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "conversion_rate": total_orders / total_customers,
        "roi": (total_revenue - total_spend) / total_spend,
        "top_region": str(region.iloc[0]["region"]),
        "top_channel": str(channel.iloc[0]["channel"]),
    }
