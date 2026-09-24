from __future__ import annotations

import json
from pathlib import Path

from .analysis import summarize
from .config import AnalysisConfig
from .data import generate_orders
from .report import write_report
from .visualization import create_charts


def run_pipeline(config: AnalysisConfig | None = None) -> dict:
    """Run the full simulation, analysis, visualization, and reporting pipeline."""

    config = config or AnalysisConfig()
    output_dir = Path(config.output_dir)
    data_dir = output_dir / "data"
    chart_dir = output_dir / "charts"
    data_dir.mkdir(parents=True, exist_ok=True)

    data = generate_orders(config)
    summaries = summarize(data)
    data.to_csv(data_dir / "simulated_orders.csv", index=False)
    summaries["monthly"].to_csv(data_dir / "monthly_summary.csv", index=False)
    summaries["region"].to_csv(data_dir / "region_summary.csv", index=False)
    summaries["channel"].to_csv(data_dir / "channel_summary.csv", index=False)
    charts = create_charts(summaries, chart_dir)
    write_report(summaries, output_dir / "analysis_report.md")

    result = {
        "seed": config.seed,
        "rows": len(data),
        "revenue": round(summaries["total_revenue"], 2),
        "orders": summaries["total_orders"],
        "conversion_rate": round(summaries["conversion_rate"], 6),
        "roi": round(summaries["roi"], 6),
        "charts": [str(path) for path in charts],
    }
    (output_dir / "summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Generated {result['rows']:,} simulated observations.")
    print(f"Revenue: ${result['revenue']:,.0f} | Orders: {result['orders']:,} | ROI: {result['roi']:.2%}")
    print(f"Report: {output_dir / 'analysis_report.md'}")
    return result
