# Quantum AI Experiments

> Public educational research sandbox exploring quantum information, active inference, variational circuits, simulator-based hypothesis testing, and quantum-inspired AI ideas.

[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?logo=qiskit)](https://qiskit.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status: Research Sandbox](https://img.shields.io/badge/Status-Research%20Sandbox-lightgrey)]()

---

## Overview

This repository contains small, reproducible experiments at the intersection of quantum information theory and AI. The goal is not to claim production readiness or proven quantum advantage. The goal is to make experimental thinking visible through clear, runnable examples.

Current areas:

1. **Active inference as a variational circuit** — mapping free-energy-style objectives onto parameterized quantum circuits.
2. **Quantum belief propagation** — using superposition-inspired encodings for Bayesian update experiments.
3. **Quantum random walks** — exploring policy/search spaces with quantum walk models.
4. **Noise and fidelity validation** — comparing simulator baselines with noisy backend assumptions.
5. **Pilot-wave-inspired probes** — educational simulations around Born-rule statistics, complementarity, contextuality, and trajectory reconstruction.

See [`STATUS.md`](STATUS.md) for the current verification boundaries.

---

## Repository Structure

```text
quantum-ai-experiments/
├── circuits/                  # QASM circuit examples
├── experiments/               # Python experiment scripts
├── results/                   # Example and generated result files
├── STATUS.md                  # Verification and claim boundaries
├── requirements.txt           # Python dependencies
├── run_all.py                 # Local simulator-oriented smoke runner
└── README.md
```

---

## What This Repo Is

This is a public portfolio and learning repo for:

- quantum computing fundamentals
- quantum simulator experiments
- AI-adjacent active inference and belief-update ideas
- statistical testing discipline
- public, non-proprietary research communication

---

## What This Repo Is Not

This repo is **not**:

- a production AI runtime
- a private-system integration surface
- a live autonomous agent
- proof of quantum advantage
- proof of new physics
- a release of private architecture, internal logs, proprietary schemas, or operational systems

Any anomaly-like result in this repo should be treated as a prompt for further controls, not as a claim of discovery.

---

## Running the Experiments

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the smoke suite:

```bash
python run_all.py
```

Generated outputs are written to:

```text
results/results_latest.json
```

Some deeper experiments require optional simulator packages. If a provider package is missing, the runner should skip or fail that section without affecting unrelated sections.

---

## Methodology

The preferred pattern for every experiment is:

1. define the hypothesis clearly
2. run an ideal simulator baseline
3. run noisy or alternate simulator variants where available
4. compare distributions using explicit statistical metrics
5. label speculative results as speculative
6. avoid claims that exceed the evidence

---

## Public Claim Boundary

Strongest safe claim:

```text
This is a public educational quantum/AI experiment sandbox with simulator-first examples and explicit verification boundaries.
```

Avoid claiming:

```text
validated quantum advantage
confirmed hardware breakthrough
production AI integration
private runtime connection
new physics discovery
```

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

© 2025–2026 Tom Budd / ResoVerse Technologies