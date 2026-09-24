from __future__ import annotations

import numpy as np
import pandas as pd

from .config import AnalysisConfig


def generate_orders(config: AnalysisConfig) -> pd.DataFrame:
    """Generate daily region-channel observations with a fixed random seed.

    The data is synthetic and intended for methodological demonstration only.
    Each row represents one day, region, and acquisition channel.
    """

    rng = np.random.default_rng(config.seed)
    dates = pd.date_range(config.start_date, periods=config.periods, freq="D")
    regions = {
        "East": 1.12,
        "South": 1.00,
        "North": 0.92,
        "West": 0.84,
    }
    channels = {
        "Search": {"traffic": 1.10, "conversion": 0.058, "spend": 420},
        "Social": {"traffic": 1.25, "conversion": 0.039, "spend": 360},
        "Email": {"traffic": 0.62, "conversion": 0.091, "spend": 115},
        "Affiliate": {"traffic": 0.78, "conversion": 0.067, "spend": 220},
    }

    rows: list[dict[str, object]] = []
    for date in dates:
        day_of_year = date.dayofyear
        seasonality = 1 + 0.14 * np.sin(2 * np.pi * day_of_year / 365)
        campaign_lift = 1.0 + (0.18 if date.day in (1, 15) else 0.0)
        for region, region_factor in regions.items():
            for channel, channel_info in channels.items():
                expected_customers = (
                    520 * region_factor * channel_info["traffic"] * seasonality * campaign_lift
                )
                customers = int(rng.poisson(expected_customers))
                conversion_rate = channel_info["conversion"] * (0.96 + 0.08 * rng.random())
                orders = int(rng.binomial(customers, min(conversion_rate, 0.95)))
                average_order_value = max(35, rng.normal(86 + 5 * region_factor, 8))
                revenue = orders * average_order_value
                spend = channel_info["spend"] * (0.94 + 0.12 * rng.random()) * seasonality
                rows.append(
                    {
                        "date": date,
                        "region": region,
                        "channel": channel,
                        "customers": customers,
                        "orders": orders,
                        "revenue": round(float(revenue), 2),
                        "marketing_spend": round(float(spend), 2),
                    }
                )

    return pd.DataFrame(rows)
