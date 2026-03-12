"""Simple AI-like textual analysis for investment metrics."""

from __future__ import annotations


def analyze_investment(roi: float) -> str:
    """Return a text assessment based on ROI bands."""

    if roi > 10:
        return "High yield investment: ROI is above 10%, indicating strong profitability potential."
    if 6 <= roi <= 10:
        return "Stable investment: ROI is between 6% and 10%, suggesting balanced risk and return."
    return "Low yield investment: ROI is below 6%, consider improving terms or exploring alternatives."
