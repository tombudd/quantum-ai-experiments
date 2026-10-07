#!/usr/bin/env python3
"""
Cross-domain quantum/AI experiment stubs.

Public sandbox version. This file intentionally avoids private architecture
references and keeps only small reproducible examples suitable for review.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats as sp_stats

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def run_temporal_autocorrelation(
    sequence_length: int = 40, repeats: int = 15
) -> dict[str, object]:
    """Estimate lag-one autocorrelation for repeated independent fair-bit sequences."""
    if sequence_length < 2:
        raise ValueError("sequence_length must be at least 2")
    if repeats < 1:
        raise ValueError("repeats must be at least 1")

    rng = np.random.default_rng(42)
    values = []
    for _ in range(repeats):
        x = rng.binomial(1, 0.5, size=sequence_length).astype(float)
        mean = x.mean()
        denominator = np.sum((x - mean) ** 2)
        if denominator:
            numerator = np.sum((x[:-1] - mean) * (x[1:] - mean))
            values.append(float(numerator / denominator))
    mean_r1 = float(np.mean(values)) if values else 0.0

    # For independent bits, the approximate SE of one lag-one autocorrelation
    # is 1/sqrt(sequence_length). Averaging independent repetitions reduces it
    # by sqrt(number of valid sequences).
    effective_repeats = max(len(values), 1)
    se = 1 / np.sqrt(sequence_length * effective_repeats)
    z_score = abs(mean_r1) / se
    p_value = 2 * (1 - float(sp_stats.norm.cdf(abs(z_score))))
    return {
        "name": "Temporal Autocorrelation Probe",
        "status": "review" if p_value < 0.05 else "pass",
        "mean_autocorrelation": round(mean_r1, 6),
        "standard_error": round(float(se), 6),
        "z_score": round(z_score, 4),
        "p_value": round(p_value, 6),
        "repeats": repeats,
    }


def run_noise_sweep(shots: int = 4096) -> dict[str, object]:
    """Run a synthetic one-sided readout-bias stress sweep.

    Each bias event forces an otherwise fair binary outcome to zero. This
    produces p(0) = 0.5 + noise_level/2. It is an illustrative asymmetric
    readout-bias model, not calibrated hardware noise or symmetric depolarizing
    noise.
    """
    if shots < 1:
        raise ValueError("shots must be at least 1")

    rng = np.random.default_rng(7)
    rows = []
    for noise_level in [0.0, 0.01, 0.03, 0.05, 0.10]:
        p0 = 0.5 + noise_level * 0.5
        observed_zeros = int(rng.binomial(shots, p0))
        chi2, p_value = sp_stats.chisquare(
            [observed_zeros, shots - observed_zeros],
            [shots / 2, shots / 2],
        )
        rows.append(
            {
                "noise_level": noise_level,
                "expected_zero_probability": p0,
                "observed_zeros": observed_zeros,
                "chi2": round(float(chi2), 4),
                "p_value": round(float(p_value), 6),
            }
        )
    return {"name": "Noise Sweep Probe", "status": "pass", "rows": rows}


def run_all() -> dict[str, object]:
    return {
        "temporal_autocorrelation": run_temporal_autocorrelation(),
        "noise_sweep": run_noise_sweep(),
    }


if __name__ == "__main__":
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = run_all()
    output_path = RESULTS_DIR / "cross_domain_latest.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    print(f"Saved: {output_path}")
