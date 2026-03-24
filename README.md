# Quantum AI Experiments

> Quantum computing experiments relevant to AI — active inference on quantum hardware, variational algorithms, and fidelity validation results. All circuits runnable on IBM Quantum and other public backends.

[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?logo=qiskit)](https://qiskit.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IBM Quantum](https://img.shields.io/badge/Runs%20on-IBM%20Quantum-blue)]()
[![Status: Active](https://img.shields.io/badge/Status-Active%20Research-brightgreen)]()

---

## Overview

This repository contains quantum computing experiments at the intersection of quantum information theory and AI — specifically:

1. **Active inference on quantum hardware** — implementing the free energy principle as a quantum variational circuit
2. **Quantum belief propagation** — Bayesian inference using quantum superposition
3. **Quantum random walk** — exploring state spaces more efficiently than classical search
4. **Noise fingerprinting** — characterising real hardware noise for calibration

All experiments are designed to run on real quantum hardware (IBM Quantum) as well as local simulators. Results from actual hardware runs are included in [`results/`](results/).

---

## Why Quantum × Active Inference?

Active inference involves minimising variational free energy — an optimisation problem over probability distributions. Quantum computing offers potential advantages for:

- **Superposition**: exploring multiple belief states simultaneously
- **Amplitude encoding**: representing continuous probability distributions efficiently  
- **Variational quantum circuits**: natural fit for the variational free energy objective
- **Quantum walks**: efficient state-space exploration for policy selection

These are theoretical advantages. This repo is about testing whether they manifest on real, noisy hardware.

---

## Repository Structure

```
quantum-ai-experiments/
├── circuits/
│   ├── active_inference_vqc.qasm   # Variational circuit for free energy minimisation
│   ├── belief_propagation.qasm     # Quantum belief update circuit
│   ├── quantum_walk.qasm           # Discrete quantum walk
│   └── noise_benchmark.qasm        # Hardware noise characterisation
├── experiments/
│   ├── 01_free_energy_vqc.py       # VQC implementation of active inference
│   ├── 02_belief_propagation.py    # Quantum Bayesian inference
│   ├── 03_quantum_walk.py          # Quantum walk experiments
│   ├── 04_hardware_noise.py        # Noise fingerprinting across backends
│   └── 05_classical_comparison.py  # Benchmark against classical implementations
├── results/
│   ├── ibm_sherbrooke_2025_q3.json
│   ├── ibm_kyiv_2025_q4.json
│   └── simulator_baseline.json
├── analysis/
│   ├── fidelity_analysis.ipynb
│   ├── noise_characterisation.ipynb
│   └── classical_vs_quantum.ipynb
└── docs/
    ├── experimental_methodology.md
    └── hardware_notes.md
```

---

## Key Experiments

### Experiment 1: Active Inference as VQC

The central experiment: can variational free energy be minimised on a quantum circuit?

We encode the belief distribution `q(x)` as amplitude coefficients and the generative model `p(o,x)` as a parameterised unitary. Free energy minimisation becomes VQE (Variational Quantum Eigensolver) over the free energy operator.

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

def free_energy_ansatz(n_states: int, depth: int = 2) -> QuantumCircuit:
    """
    Parameterised ansatz for free energy minimisation.
    
    Encodes belief distribution q(x) as amplitude vector.
    Parameters theta are optimised to minimise F = KL[q||p] - E_q[log p(o|x)]
    """
    n_qubits = int(np.ceil(np.log2(n_states)))
    theta = ParameterVector('θ', length=n_qubits * depth * 2)
    
    qc = QuantumCircuit(n_qubits)
    
    # Initial Hadamard layer — uniform superposition
    qc.h(range(n_qubits))
    
    # Alternating Ry rotations and CNOT entanglement
    param_idx = 0
    for d in range(depth):
        for q in range(n_qubits):
            qc.ry(theta[param_idx], q)
            param_idx += 1
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        for q in range(n_qubits):
            qc.rz(theta[param_idx], q)
            param_idx += 1
    
    return qc
```

**Results (IBM Sherbrooke, Q3 2025):**
- 4-qubit circuit, 2-layer ansatz
- Classical optimum: F = 0.143
- Quantum result: F = 0.151 ± 0.008
- Fidelity vs. ideal simulator: 94.2%

### Experiment 3: Quantum Walk for Policy Selection

Active inference policy selection requires computing expected free energy G(π) for each candidate policy. For large policy spaces, this is expensive classically. We test whether a quantum walk over the policy graph provides a speedup.

Results are mixed: small policy spaces show no quantum advantage (overhead dominates). For policy graphs with >32 nodes, quantum walk begins to show a ~1.4× speedup on simulator — not yet confirmed on hardware due to decoherence.

---

## Hardware Fidelity Results

| Backend | Date | Circuit | Fidelity vs. Ideal | Notes |
|---------|------|---------|-------------------|-------|
| IBM Sherbrooke | Q3 2025 | active_inference_vqc (4q, d=2) | 94.2% | ELBO within 5.6% of classical |
| IBM Kyiv | Q4 2025 | belief_propagation (3q) | 97.1% | Low noise backend |
| IBM Kyiv | Q4 2025 | quantum_walk (4q, 8 steps) | 89.3% | Walk decoherence at step 6+ |
| Simulator (AerSimulator) | — | All circuits | 99.8% | Baseline reference |

---

## Running the Experiments

### Prerequisites

```bash
pip install qiskit>=1.0 qiskit-ibm-runtime>=0.20 numpy scipy matplotlib
```

### Simulator (no account needed)

```bash
python experiments/01_free_energy_vqc.py --backend aer_simulator
```

### Real Hardware (IBM Quantum account required)

```bash
export IBM_QUANTUM_TOKEN=your_token_here
python experiments/01_free_energy_vqc.py --backend ibm_sherbrooke
```

---

## Methodology

All experiments follow the same protocol:
1. Run on `AerSimulator` to establish ideal baseline
2. Run on real hardware with 1000+ shots per circuit
3. Compare distributions using fidelity metric: `F = |⟨ψ_ideal|ψ_real⟩|²`
4. Report mean ± standard deviation across 5 hardware runs

Hardware results are included in `results/` as JSON with full shot data.

---

## References

- Friston, K. (2019). A free energy principle for a particular physics.
- Cerezo, M. et al. (2021). Variational quantum algorithms. *Nature Reviews Physics*.
- Aharonov, Y. et al. (1993). Quantum random walks. *Physical Review A*.
- IBM Quantum (2024). Eagle r3 processor specifications.

---

© 2025–2026 Tom Budd / ResoVerse Technologies · MIT License
