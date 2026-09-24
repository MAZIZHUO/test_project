from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AnalysisConfig:
    """Central configuration for a reproducible analysis run."""

    seed: int = 20260925
    start_date: str = "2025-10-01"
    periods: int = 365
    output_dir: Path = Path("outputs")
