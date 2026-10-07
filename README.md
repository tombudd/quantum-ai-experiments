# Quantum AI Experiments

> Public educational research sandbox exploring quantum information, simulator-based hypothesis testing, variational circuits, and quantum-inspired AI ideas.

[![Qiskit](https://img.shields.io/badge/Qiskit-2.5.x-6929C4?logo=qiskit)](https://qiskit.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status: Research Sandbox](https://img.shields.io/badge/Status-Research%20Sandbox-lightgrey)](STATUS.md)

## Scope

This repository contains small, reproducible examples at the intersection of quantum information, simulator testing, optimization, and AI-adjacent inference questions. It is a learning and portfolio sandbox. It does not claim production readiness, quantum advantage, hardware breakthroughs, AGI relevance, or deployment utility.

Current executable examples:

- `run_all.py`: small Bell, GHZ, QFT, and variational-circuit simulator smoke checks.
- `experiments/cross_domain_experiments.py`: a repeated fair-bit autocorrelation probe and a synthetic one-sided readout-bias stress sweep.
- `experiments/frontier_experiments.py`: a review placeholder; it does not implement the experiments removed during public hardening.

The repository does not currently include runnable pilot-wave trajectory, contextuality, or new-physics experiments. Ideas not represented by executable files are roadmap only.

See [`STATUS.md`](STATUS.md) for verification boundaries and [`PUBLIC_RELEASE_STANDARD.md`](PUBLIC_RELEASE_STANDARD.md) for the public release criteria.

## Repository Structure

```text
quantum-ai-experiments/
├── circuits/                  # QASM examples, if present
├── experiments/               # Public experiment scripts and placeholders
├── tests/                     # Bounded regression tests
├── results/                   # Generated outputs
├── run_all.py                 # Simulator smoke runner
├── requirements.txt           # Full local dependency set
├── STATUS.md
└── README.md
```

## Setup and Run

Create a virtual environment and install the listed dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the bounded regression tests and smoke runner:

```bash
python -m unittest discover -s tests -v
python run_all.py
python experiments/cross_domain_experiments.py
```

The runner records unavailable providers as skipped when their packages are absent. The requirements file lists the full local stack used by the examples.

Generated JSON outputs are written under `results/`.

## Method and Limits

The noise sweep is a synthetic, asymmetric readout-bias stress model: a fraction of otherwise fair outcomes is forced to zero. It is not a calibrated hardware noise model, and it does not represent symmetric depolarizing noise. The autocorrelation probe uses seeded independent fair-bit sequences and an approximate standard error that accounts for the number of valid repetitions.

Hardware or provider-backed results require separate documentation of the backend, inputs, shot count, seed, and limitations. Simulator results alone do not establish practical advantage.

## What This Repo Is Not

This repository is not:

- a production quantum AI system
- a private AI integration or runtime
- a live autonomous agent
- evidence of quantum speedup or deployment utility
- proof of new physics
- a release of private architecture, operational logs, credentials, or proprietary schemas

Any unusual result is a reason to add controls and independent reproduction, not a claim of discovery.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

© 2025–2026 Tom Budd / ResoVerse Technologies
