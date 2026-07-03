# Quantum AI Experiments

> Exploratory toy experiments at the intersection of quantum circuits, optimization, inference, and AI-adjacent research questions.

[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?logo=qiskit)](https://qiskit.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status: Exploratory](https://img.shields.io/badge/Status-Exploratory%20Research-yellow)]()

---

## Scope

This repository contains exploratory quantum computing experiments relevant to AI-adjacent optimization and inference questions, including:

1. Toy active-inference-inspired optimization using variational circuits
2. Quantum belief-propagation sketches
3. Quantum random-walk experiments for state-space exploration
4. Noise fingerprinting and simulator-vs-hardware comparison patterns

These experiments are educational and exploratory. They do **not** claim production advantage, AGI relevance, verified quantum speedup, or deployment readiness.

Where hardware results are discussed, they should be treated as experimental observations that require independent reproduction.

---

## Why Quantum × Inference?

Active inference and related probabilistic methods involve optimization over probability distributions. Quantum circuits may offer useful ways to explore representations, sampling behavior, and variational objectives.

Possible research directions include:

- Superposition as a representation for candidate states
- Amplitude encoding for probability-like structures
- Variational quantum circuits for optimization objectives
- Quantum walks for exploratory search patterns
- Noise characterization for realistic hardware limits

These are theoretical and experimental motivations, not claims of practical advantage.

---

## Planned Public Structure

The repository is being built as a safe public research surface. Planned structure:

```text
quantum-ai-experiments/
├── circuits/
│   ├── active_inference_vqc.qasm
│   ├── belief_propagation.qasm
│   ├── quantum_walk.qasm
│   └── noise_benchmark.qasm
├── experiments/
│   ├── 01_free_energy_vqc.py
│   ├── 02_belief_propagation.py
│   ├── 03_quantum_walk.py
│   ├── 04_hardware_noise.py
│   └── 05_classical_comparison.py
├── results/
│   └── sample_simulator_baseline.json
├── analysis/
│   └── example_analysis.ipynb
└── docs/
    ├── experimental_methodology.md
    ├── hardware_notes.md
    └── limitations.md
```

Until a file exists in the repository, the structure above should be read as a roadmap, not as a claim of implemented functionality.

---

## Example Experiment: Toy Variational Objective

A central toy question:

**Can a small parameterized quantum circuit minimize a free-energy-inspired objective in a reproducible simulator setting?**

The intended workflow is:

1. Define a small synthetic probability distribution.
2. Encode a toy belief state into a circuit representation.
3. Optimize parameters using a classical optimizer around the quantum circuit.
4. Compare against a classical baseline.
5. Report limitations, noise sensitivity, and reproduction steps.

This should be treated as a research sketch unless the accompanying code, data, and reproduction instructions are present.

---

## Running Experiments

Simulator-only examples should be runnable without a quantum hardware account.

```bash
pip install "qiskit>=1.0" "qiskit-aer" numpy scipy matplotlib
python experiments/01_free_energy_vqc.py --backend aer_simulator
```

Hardware-backed experiments may require an IBM Quantum account and should clearly distinguish simulator results from real-device results.

```bash
export IBM_QUANTUM_TOKEN=your_token_here
python experiments/01_free_energy_vqc.py --backend <backend_name>
```

Do not commit tokens, credentials, provider job IDs containing private account context, or unreproducible private results.

---

## Reporting Standards

Any claimed result should include:

- Backend or simulator used
- Date of run
- Circuit size
- Shot count
- Optimizer settings
- Random seed where applicable
- Classical baseline
- Noise model or hardware notes
- Clear limitations

Claims of speedup, production utility, or AI-system relevance require extraordinary evidence and should not be made casually.

---

## Public Boundary

This is a public exploratory repository. It may include toy circuits, synthetic data, simulator outputs, and redacted methodology.

It must not include private production architecture, proprietary system internals, private receipts, unreleased research logs, secrets, API tokens, or internal codenames from private systems.

---

## References

- Friston, K. (2019). A free energy principle for a particular physics.
- Cerezo, M. et al. (2021). Variational quantum algorithms. *Nature Reviews Physics*.
- Aharonov, Y. et al. (1993). Quantum random walks. *Physical Review A*.
- IBM Quantum documentation and public backend notes.

---

© 2025–2026 Tom Budd / ResoVerse Technologies · Apache 2.0 License