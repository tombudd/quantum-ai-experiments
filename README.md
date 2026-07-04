# Quantum AI Experiments

> Public educational research sandbox exploring quantum information, simulator-based hypothesis testing, variational circuits, and quantum-inspired AI ideas.

[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?logo=qiskit)](https://qiskit.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status: Research Sandbox](https://img.shields.io/badge/Status-Research%20Sandbox-lightgrey)]()

---

## Scope

This repository contains small, reproducible experiments at the intersection of quantum information, simulator testing, optimization, and AI-adjacent inference questions.

The goal is not to claim production readiness, verified quantum advantage, AGI relevance, hardware breakthrough, or deployment utility. The goal is to make experimental thinking visible through clear, runnable, public-safe examples.

Current areas:

1. **Simulator smoke tests** — Bell, GHZ, QFT, and small variational-circuit checks across available local simulators.
2. **Quantum-inspired inference sketches** — toy active-inference and belief-update ideas where code is present.
3. **Quantum random-walk / search sketches** — exploratory state-space examples where code is present.
4. **Noise and fidelity checks** — simulator-first comparisons where reproducible assumptions are documented.

Where hardware or provider-backed results are discussed, they should be treated as experimental observations that require independent reproduction.

See [`STATUS.md`](STATUS.md) for the current verification and claim boundaries.

---

## Why Quantum × Inference?

Active inference and related probabilistic methods involve optimization over probability distributions. Quantum circuits may offer useful ways to explore representations, sampling behavior, and variational objectives.

Possible research directions include:

- superposition-inspired representations for candidate states
- amplitude-style encodings for probability-like structures
- variational quantum circuits for optimization objectives
- quantum walks for exploratory search patterns
- simulator and noise characterization for realistic limits

These are theoretical and experimental motivations, not claims of practical advantage.

---

## Current Public Structure

```text
quantum-ai-experiments/
├── run_all.py                 # Simulator-oriented smoke runner
├── requirements.txt           # Minimal local dependencies
├── STATUS.md                  # Verification and claim boundaries
├── README.md
└── results/                   # Generated locally when the runner is executed
```

Future experiments may add `circuits/`, `experiments/`, `analysis/`, or `docs/` directories. Until a file exists in this repository, it should be read as roadmap only, not implemented functionality.

---

## What This Repo Is

This is a public portfolio and learning repo for:

- quantum computing fundamentals
- quantum simulator experiments
- AI-adjacent inference and belief-update ideas
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

## Running the Smoke Runner

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the public smoke suite:

```bash
python run_all.py
```

Generated outputs are written locally to:

```text
results/results_latest.json
```

Some provider-specific sections require optional simulator packages. If an optional provider package or token is missing, that section should skip or fail without implying failure of unrelated sections.

---

## Reporting Standards

Any claimed result should include:

- backend or simulator used
- date of run
- circuit size
- shot count
- optimizer settings where applicable
- random seed where applicable
- classical baseline where applicable
- noise model or hardware notes where applicable
- clear limitations

Claims of speedup, production utility, AI-system relevance, hardware breakthrough, or new physics require extraordinary evidence and should not be made casually.

---

## Public Boundary

This is a public exploratory repository. It may include toy circuits, synthetic data, simulator outputs, and redacted methodology.

It must not include private production architecture, proprietary system internals, private receipts, unreleased research logs, secrets, API tokens, private provider job context, or internal codenames from private systems.

The preferred pattern for every experiment is:

1. define the hypothesis clearly
2. run an ideal simulator baseline
3. run noisy or alternate simulator variants where available
4. compare distributions using explicit statistical metrics where applicable
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

## References

- Friston, K. (2019). A free energy principle for a particular physics.
- Cerezo, M. et al. (2021). Variational quantum algorithms. *Nature Reviews Physics*.
- Aharonov, Y. et al. (1993). Quantum random walks. *Physical Review A*.
- IBM Quantum documentation and public backend notes.

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

© 2025–2026 Tom Budd / ResoVerse Technologies
