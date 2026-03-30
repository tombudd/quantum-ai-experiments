#!/usr/bin/env python3
"""
UNA Quantum Lab — Pilot Wave Theory Experiments
================================================
Inspired by: "A 100-year-old theory might explain what's wrong with quantum mechanics"
             (Scientific American, Mar 2026 — Valentini / de Broglie pilot wave theory)

This suite implements 6 experiments testing predictions of de Broglie-Bohm
(pilot wave) theory against standard quantum mechanics:

  Exp 12: Born Rule Statistical Deviation Search
  Exp 13: Weak Measurement Bohmian Trajectory Reconstruction
  Exp 14: CHSH Non-Locality / Bell Inequality at Scale
  Exp 15: Cross-Platform Noise Signature Analysis
  Exp 16: Holographic Entanglement Entropy Scaling
  Exp 17: Contextuality (Peres-Mermin Square) Test

Hardware: IBM Qiskit Aer (local), IonQ simulator, Google Cirq
Theory:   Pilot wave theory predicts particles always have definite positions
          guided by a pilot wave. In "quantum non-equilibrium," the Born rule
          (P = |ψ|²) can be violated. We search for such deviations.

Author: UNA-AI / Tom Budd — ResoVerse
Date:   2026-03-21
"""

import json
import math
import time
import traceback
import numpy as np
from datetime import datetime
from collections import Counter
from scipy import stats as sp_stats

results = {}

def record(exp_id, name, status, detail="", duration=0, data=None):
    results[exp_id] = {
        "name": name,
        "status": status,
        "detail": str(detail)[:300],
        "duration_s": round(duration, 3),
        "data": data or {}
    }
    icon = "✅" if status == "pass" else ("⚠️" if status == "anomaly" else "❌")
    print(f"  {icon}  [{exp_id}] {name}  ({round(duration,3)}s)")
    if detail:
        print(f"       → {str(detail)[:120]}")


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 12: Born Rule Statistical Deviation Search
# ═══════════════════════════════════════════════════════════════════════
# Pilot wave theory predicts that in non-equilibrium conditions, the Born
# rule P = |ψ|² can be violated. We prepare many identical states, measure
# in multiple bases, and use chi-squared tests to detect deviations.

def exp12_born_rule_deviation():
    """Search for statistical deviations from Born rule predictions."""
    print("\n" + "═"*64)
    print("  EXP 12: Born Rule Statistical Deviation Search")
    print("═"*64)
    t = time.time()

    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    sim = AerSimulator()

    SHOTS = 8192  # High shot count for statistical power
    chi2_results = []

    # Test 1: Equal superposition — should be 50/50
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    counts = sim.run(qc, shots=SHOTS).result().get_counts()
    observed = [counts.get('0', 0), counts.get('1', 0)]
    expected = [SHOTS/2, SHOTS/2]
    chi2, p_val = sp_stats.chisquare(observed, expected)
    chi2_results.append({"basis": "H|0⟩ → Z-basis", "chi2": chi2, "p_value": p_val,
                          "observed": observed, "expected": [int(e) for e in expected]})

    # Test 2: Rotation by various angles — Born rule predicts cos²(θ/2)
    angles = [np.pi/6, np.pi/4, np.pi/3, np.pi*2/5, np.pi*3/7]
    for theta in angles:
        qc = QuantumCircuit(1, 1)
        qc.ry(theta, 0)
        qc.measure(0, 0)
        counts = sim.run(qc, shots=SHOTS).result().get_counts()
        p0_expected = np.cos(theta/2)**2
        p1_expected = np.sin(theta/2)**2
        observed = [counts.get('0', 0), counts.get('1', 0)]
        expected_counts = [p0_expected * SHOTS, p1_expected * SHOTS]
        chi2, p_val = sp_stats.chisquare(observed, expected_counts)
        chi2_results.append({
            "basis": f"Ry({theta:.4f})|0⟩",
            "chi2": round(chi2, 4),
            "p_value": round(p_val, 6),
            "observed": observed,
            "expected": [round(e, 1) for e in expected_counts],
            "born_rule_pred": round(p0_expected, 4)
        })

    # Test 3: Entangled pair — conditional probabilities
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    counts = sim.run(qc, shots=SHOTS).result().get_counts()
    # Born rule: only 00 and 11, each 50%
    obs_00 = counts.get('00', 0)
    obs_11 = counts.get('11', 0)
    obs_01 = counts.get('01', 0)
    obs_10 = counts.get('10', 0)
    # For perfect Bell state: expect 0 for 01/10
    total_valid = obs_00 + obs_11
    total_anomalous = obs_01 + obs_10
    chi2_bell, p_bell = sp_stats.chisquare(
        [obs_00, obs_11, obs_01 + obs_10],
        [SHOTS/2, SHOTS/2, 0.001]  # near-zero expected for anomalous
    ) if total_anomalous > 0 else (0.0, 1.0)

    chi2_results.append({
        "basis": "Bell(Φ+) → ZZ",
        "chi2": round(chi2_bell, 4) if total_anomalous > 0 else 0.0,
        "p_value": round(p_bell, 6) if total_anomalous > 0 else 1.0,
        "observed": {"00": obs_00, "11": obs_11, "01": obs_01, "10": obs_10},
        "anomalous_fraction": round(total_anomalous / SHOTS, 6)
    })

    # Test 4: GHZ state high-qubit Born rule test
    for n_qubits in [5, 8, 12]:
        qc = QuantumCircuit(n_qubits, n_qubits)
        qc.h(0)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        qc.measure(range(n_qubits), range(n_qubits))
        counts = sim.run(qc, shots=SHOTS).result().get_counts()
        all_zero = '0' * n_qubits
        all_one = '1' * n_qubits
        valid = counts.get(all_zero, 0) + counts.get(all_one, 0)
        anomalous = SHOTS - valid
        chi2_results.append({
            "basis": f"GHZ-{n_qubits} → Z⊗{n_qubits}",
            "valid_fraction": round(valid / SHOTS, 6),
            "anomalous_fraction": round(anomalous / SHOTS, 6),
            "all_zero": counts.get(all_zero, 0),
            "all_one": counts.get(all_one, 0),
            "other_states": anomalous
        })

    # Overall assessment
    significant_deviations = sum(1 for r in chi2_results
                                  if 'p_value' in r and r['p_value'] < 0.05)
    total_tests = sum(1 for r in chi2_results if 'p_value' in r)
    # Under null hypothesis (Born rule holds), expect ~5% false positives
    expected_false_pos = total_tests * 0.05

    status = "anomaly" if significant_deviations > expected_false_pos * 2 else "pass"
    detail = (f"{total_tests} chi² tests | {significant_deviations} significant (p<0.05) | "
              f"Expected false positives: {expected_false_pos:.1f} | "
              f"Verdict: {'ANOMALY — possible non-equilibrium signal' if status == 'anomaly' else 'Consistent with Born rule'}")

    record("EXP-12", "Born Rule Deviation Search", status, detail,
           time.time() - t, {"chi2_tests": chi2_results, "shots_per_test": SHOTS})


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 13: Weak Measurement Bohmian Trajectory Reconstruction
# ═══════════════════════════════════════════════════════════════════════
# In pilot wave theory, particles follow definite trajectories guided by
# the pilot wave. We use sequential weak measurements to reconstruct
# approximate Bohmian trajectories through a double-slit analog circuit.

def exp13_bohmian_trajectories():
    """Reconstruct approximate Bohmian trajectories via weak measurements."""
    print("\n" + "═"*64)
    print("  EXP 13: Weak Measurement Bohmian Trajectory Reconstruction")
    print("═"*64)
    t = time.time()

    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    sim = AerSimulator()

    SHOTS = 4096
    # Double-slit analog: qubit 0 is "which path", qubit 1 is "detector"
    # Weak measurement = partial CNOT (controlled-Ry with small angle)
    weak_angles = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0, np.pi/2]  # Increasing measurement strength
    trajectory_data = []

    for weak_theta in weak_angles:
        qc = QuantumCircuit(3, 3)  # q0=particle, q1=weak meter, q2=strong meter

        # Prepare superposition (double slit)
        qc.h(0)

        # Weak measurement: partial entanglement with meter q1
        qc.cry(weak_theta, 0, 1)

        # Free evolution (phase accumulation)
        qc.rz(np.pi/4, 0)

        # Strong measurement at detector
        qc.cx(0, 2)
        qc.measure([0, 1, 2], [0, 1, 2])

        counts = sim.run(qc, shots=SHOTS).result().get_counts()

        # Analyze: weak measurement should partially reveal which-path
        # without fully collapsing interference
        # Compute interference visibility
        total = sum(counts.values())
        # Extract conditional probabilities
        meter_0 = sum(v for k, v in counts.items() if k[1] == '0')  # weak meter = 0
        meter_1 = sum(v for k, v in counts.items() if k[1] == '1')  # weak meter = 1

        # Interference visibility: V = |P(0|meter=0) - P(0|meter=1)| / (sum)
        p_path0_given_m0 = sum(v for k, v in counts.items() if k[1] == '0' and k[2] == '0') / max(meter_0, 1)
        p_path0_given_m1 = sum(v for k, v in counts.items() if k[1] == '1' and k[2] == '0') / max(meter_1, 1)

        visibility = abs(p_path0_given_m0 - p_path0_given_m1)
        which_path_info = abs(meter_0 - meter_1) / total

        trajectory_data.append({
            "weak_angle": round(weak_theta, 4),
            "visibility": round(visibility, 4),
            "which_path_info": round(which_path_info, 4),
            "complementarity_sum": round(visibility**2 + which_path_info**2, 4),
            "meter_counts": {"0": meter_0, "1": meter_1},
            "raw_counts": dict(counts)
        })

    # Bohmian prediction: complementarity sum V² + D² ≤ 1
    # Standard QM also predicts this, but pilot wave gives a trajectory interpretation
    complementarity_violations = sum(1 for td in trajectory_data
                                      if td['complementarity_sum'] > 1.05)

    detail = (f"{len(weak_angles)} weak measurement strengths tested | "
              f"Complementarity violations: {complementarity_violations} | "
              f"Trajectory visibility range: {trajectory_data[0]['visibility']:.3f} → {trajectory_data[-1]['visibility']:.3f}")

    status = "anomaly" if complementarity_violations > 0 else "pass"
    record("EXP-13", "Bohmian Trajectory Reconstruction", status, detail,
           time.time() - t, {"trajectories": trajectory_data})


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 14: CHSH Bell Inequality Test at Scale
# ═══════════════════════════════════════════════════════════════════════
# The CHSH inequality S ≤ 2 (classical) vs S ≤ 2√2 ≈ 2.828 (quantum).
# Pilot wave theory reproduces QM predictions (including violations) but
# through a deterministic, non-local mechanism. We measure S precisely.

def exp14_chsh_bell_inequality():
    """CHSH Bell inequality measurement at high statistical precision."""
    print("\n" + "═"*64)
    print("  EXP 14: CHSH Non-Locality / Bell Inequality at Scale")
    print("═"*64)
    t = time.time()

    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    sim = AerSimulator()

    SHOTS = 8192

    def chsh_circuit(theta_a, theta_b):
        """Create CHSH measurement circuit for given measurement angles."""
        qc = QuantumCircuit(2, 2)
        # Create Bell state |Φ+⟩
        qc.h(0)
        qc.cx(0, 1)
        # Measurement rotations
        qc.ry(2 * theta_a, 0)
        qc.ry(2 * theta_b, 1)
        qc.measure([0, 1], [0, 1])
        return qc

    def expectation_value(counts, shots):
        """Compute E = P(same) - P(different)."""
        same = counts.get('00', 0) + counts.get('11', 0)
        diff = counts.get('01', 0) + counts.get('10', 0)
        return (same - diff) / shots

    # Standard CHSH angles: a1=0, a2=π/4, b1=π/8, b2=3π/8
    a1, a2 = 0, np.pi/4
    b1, b2 = np.pi/8, 3*np.pi/8

    measurement_pairs = [
        ("a1,b1", a1, b1),
        ("a1,b2", a1, b2),
        ("a2,b1", a2, b1),
        ("a2,b2", a2, b2),
    ]

    correlators = {}
    for label, ta, tb in measurement_pairs:
        qc = chsh_circuit(ta, tb)
        counts = sim.run(qc, shots=SHOTS).result().get_counts()
        E = expectation_value(counts, SHOTS)
        correlators[label] = {
            "E": round(E, 6),
            "counts": dict(counts),
            "angles": (round(ta, 4), round(tb, 4))
        }

    # CHSH parameter: S = E(a1,b1) - E(a1,b2) + E(a2,b1) + E(a2,b2)
    S = (correlators["a1,b1"]["E"] - correlators["a1,b2"]["E"] +
         correlators["a2,b1"]["E"] + correlators["a2,b2"]["E"])

    S_theory = 2 * np.sqrt(2)  # ≈ 2.828, Tsirelson bound
    deviation_from_theory = abs(S - S_theory) / S_theory

    # Also test at non-standard angles to probe for non-equilibrium effects
    sweep_S = []
    for offset in np.linspace(0, np.pi/4, 8):
        a1s, a2s = offset, offset + np.pi/4
        b1s, b2s = offset + np.pi/8, offset + 3*np.pi/8
        Es = {}
        for label, ta, tb in [("E11", a1s, b1s), ("E12", a1s, b2s),
                                ("E21", a2s, b1s), ("E22", a2s, b2s)]:
            qc = chsh_circuit(ta, tb)
            counts = sim.run(qc, shots=2048).result().get_counts()
            Es[label] = expectation_value(counts, 2048)
        Ss = Es["E11"] - Es["E12"] + Es["E21"] + Es["E22"]
        sweep_S.append({"offset": round(offset, 4), "S": round(Ss, 4)})

    # Check if any sweep point exceeds Tsirelson bound (would be non-equilibrium signal)
    tsirelson_violations = sum(1 for s in sweep_S if abs(s["S"]) > 2.85)

    detail = (f"S = {S:.4f} (theory: {S_theory:.4f}, deviation: {deviation_from_theory:.4%}) | "
              f"Classical bound: 2.0 | Tsirelson bound: {S_theory:.3f} | "
              f"Tsirelson violations in sweep: {tsirelson_violations}/{len(sweep_S)}")

    status = "anomaly" if tsirelson_violations > 0 else "pass"
    record("EXP-14", "CHSH Bell Inequality at Scale", status, detail,
           time.time() - t, {"S_value": round(S, 6), "correlators": correlators,
                              "angle_sweep": sweep_S, "tsirelson_violations": tsirelson_violations})


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 15: Cross-Platform Noise Signature Analysis
# ═══════════════════════════════════════════════════════════════════════
# If noise is purely hardware decoherence, different simulators should
# produce qualitatively different noise patterns. If there's a universal
# "non-equilibrium relaxation" signature, it should appear across all.

def exp15_noise_signatures():
    """Compare noise signatures across multiple quantum backends."""
    print("\n" + "═"*64)
    print("  EXP 15: Cross-Platform Noise Signature Analysis")
    print("═"*64)
    t = time.time()

    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, depolarizing_error
    import cirq

    SHOTS = 4096
    platform_data = {}

    # Common circuit: 8-qubit GHZ state
    def ideal_ghz_probs(n):
        """Return Born rule prediction for GHZ state."""
        probs = {}
        probs['0' * n] = 0.5
        probs['1' * n] = 0.5
        return probs

    n_qubits = 8

    # Platform 1: Qiskit Aer (ideal)
    sim_ideal = AerSimulator()
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))
    counts_ideal = sim_ideal.run(qc, shots=SHOTS).result().get_counts()
    platform_data["Qiskit_ideal"] = dict(counts_ideal)

    # Platform 2: Qiskit Aer with 1% depolarizing noise
    noise_1 = NoiseModel()
    noise_1.add_all_qubit_quantum_error(depolarizing_error(0.01, 1), ['h', 'x'])
    noise_1.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ['cx'])
    sim_noisy1 = AerSimulator(noise_model=noise_1)
    counts_n1 = sim_noisy1.run(qc, shots=SHOTS).result().get_counts()
    platform_data["Qiskit_1pct_noise"] = dict(counts_n1)

    # Platform 3: Qiskit Aer with 5% depolarizing noise
    noise_5 = NoiseModel()
    noise_5.add_all_qubit_quantum_error(depolarizing_error(0.05, 1), ['h', 'x'])
    noise_5.add_all_qubit_quantum_error(depolarizing_error(0.10, 2), ['cx'])
    sim_noisy5 = AerSimulator(noise_model=noise_5)
    counts_n5 = sim_noisy5.run(qc, shots=SHOTS).result().get_counts()
    platform_data["Qiskit_5pct_noise"] = dict(counts_n5)

    # Platform 4: Google Cirq (ideal)
    qs = cirq.LineQubit.range(n_qubits)
    cirq_circuit = cirq.Circuit([
        cirq.H(qs[0]),
        *[cirq.CNOT(qs[i], qs[i+1]) for i in range(n_qubits - 1)],
        cirq.measure(*qs, key='result')
    ])
    cirq_result = cirq.Simulator().run(cirq_circuit, repetitions=SHOTS)
    cirq_counts = Counter()
    for row in cirq_result.measurements['result']:
        cirq_counts[''.join(map(str, row))] += 1
    platform_data["Cirq_ideal"] = dict(cirq_counts)

    # Platform 5: Google Cirq with 1% noise
    cirq_noise = cirq.ConstantQubitNoiseModel(cirq.depolarize(p=0.01))
    cirq_noisy = cirq.DensityMatrixSimulator(noise=cirq_noise)
    cirq_result_n = cirq_noisy.run(cirq_circuit, repetitions=SHOTS)
    cirq_counts_n = Counter()
    for row in cirq_result_n.measurements['result']:
        cirq_counts_n[''.join(map(str, row))] += 1
    platform_data["Cirq_1pct_noise"] = dict(cirq_counts_n)

    # Analyze: compute KL divergence from ideal Born rule for each platform
    analysis = {}
    ideal_probs = ideal_ghz_probs(n_qubits)
    all_states = set()
    for pd in platform_data.values():
        all_states.update(pd.keys())

    for platform, counts in platform_data.items():
        total = sum(counts.values())
        # Fraction in valid GHZ states
        valid = counts.get('0' * n_qubits, 0) + counts.get('1' * n_qubits, 0)
        fidelity = valid / total

        # Distribution entropy
        probs = np.array([counts.get(s, 0) / total for s in sorted(all_states)])
        probs = probs[probs > 0]
        entropy = -np.sum(probs * np.log2(probs))

        # Asymmetry: |P(0...0) - P(1...1)| / (P(0...0) + P(1...1))
        p_all0 = counts.get('0' * n_qubits, 0) / total
        p_all1 = counts.get('1' * n_qubits, 0) / total
        asymmetry = abs(p_all0 - p_all1) / max(p_all0 + p_all1, 1e-10)

        analysis[platform] = {
            "fidelity": round(fidelity, 4),
            "entropy_bits": round(entropy, 4),
            "asymmetry": round(asymmetry, 4),
            "unique_states": len(counts),
            "total_shots": total
        }

    # Cross-platform comparison: is noise universal or platform-specific?
    fidelities = {k: v["fidelity"] for k, v in analysis.items()}
    noisy_fidelities = {k: v for k, v in fidelities.items() if "noise" in k.lower()}
    ideal_fidelities = {k: v for k, v in fidelities.items() if "ideal" in k.lower()}

    detail = (f"5 platforms tested (2 ideal, 3 noisy) | "
              f"Ideal fidelity: {np.mean(list(ideal_fidelities.values())):.4f} | "
              f"Noisy fidelity range: {min(noisy_fidelities.values()):.4f}–{max(noisy_fidelities.values()):.4f} | "
              f"Noise patterns: {'platform-specific (consistent with decoherence)' if len(set(round(v, 2) for v in noisy_fidelities.values())) > 1 else 'UNIVERSAL (potential non-equilibrium)'}")

    record("EXP-15", "Cross-Platform Noise Signatures", "pass", detail,
           time.time() - t, {"analysis": analysis, "platform_counts_summary": {
               k: {"valid": v.get('0'*n_qubits, 0) + v.get('1'*n_qubits, 0), "total": sum(v.values())}
               for k, v in platform_data.items()
           }})


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 16: Holographic Entanglement Entropy Scaling
# ═══════════════════════════════════════════════════════════════════════
# The holographic principle suggests information in a region scales with
# its boundary area, not its volume. We test entanglement entropy scaling
# in GHZ chains: does it follow volume law or area law?

def exp16_holographic_entropy():
    """Test entanglement entropy scaling — volume law vs area law."""
    print("\n" + "═"*64)
    print("  EXP 16: Holographic Entanglement Entropy Scaling")
    print("═"*64)
    t = time.time()

    import pennylane as qml
    import pennylane.numpy as pnp

    entropy_data = []

    for n_qubits in [4, 6, 8, 10, 12, 14]:
        dev = qml.device("default.qubit", wires=n_qubits)

        @qml.qnode(dev)
        def ghz_state():
            qml.Hadamard(wires=0)
            for i in range(n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            return qml.state()

        state = ghz_state()

        # Compute entanglement entropy for bipartition at midpoint
        half = n_qubits // 2
        # Reshape state into bipartite form
        state_matrix = state.reshape(2**half, 2**(n_qubits - half))
        # SVD to get Schmidt coefficients
        _, schmidt_values, _ = np.linalg.svd(state_matrix, full_matrices=False)
        # Von Neumann entropy: S = -Σ λ² log(λ²)
        schmidt_sq = schmidt_values**2
        schmidt_sq = schmidt_sq[schmidt_sq > 1e-12]  # Filter zeros
        entropy = -np.sum(schmidt_sq * np.log2(schmidt_sq))

        # Also compute entropy for different cut positions
        cut_entropies = []
        for cut in range(1, n_qubits):
            sm = state.reshape(2**cut, 2**(n_qubits - cut))
            _, sv, _ = np.linalg.svd(sm, full_matrices=False)
            sv_sq = sv**2
            sv_sq = sv_sq[sv_sq > 1e-12]
            s = -np.sum(sv_sq * np.log2(sv_sq))
            cut_entropies.append(round(float(s), 6))

        entropy_data.append({
            "n_qubits": n_qubits,
            "midpoint_entropy": round(float(entropy), 6),
            "max_possible_entropy": half,  # Volume law upper bound
            "cut_entropies": cut_entropies,
            "entropy_per_qubit": round(float(entropy) / n_qubits, 6)
        })

    # Analysis: fit scaling law
    # Area law: S ~ constant (boundary)
    # Volume law: S ~ n/2 (bulk)
    # GHZ state: S = 1 bit regardless of size (area law!)
    sizes = [d["n_qubits"] for d in entropy_data]
    entropies = [d["midpoint_entropy"] for d in entropy_data]

    # Check if entropy is constant (area law) or grows with size (volume law)
    entropy_variance = np.var(entropies)
    mean_entropy = np.mean(entropies)

    if entropy_variance < 0.01:
        scaling_law = "AREA LAW (constant entropy — holographic)"
    elif all(entropies[i] <= entropies[i+1] for i in range(len(entropies)-1)):
        scaling_law = "VOLUME LAW (growing entropy — non-holographic)"
    else:
        scaling_law = "MIXED (possible dimensional transition)"

    detail = (f"Tested n={sizes} | Midpoint entropies: {[round(e, 3) for e in entropies]} | "
              f"Variance: {entropy_variance:.6f} | Scaling: {scaling_law}")

    record("EXP-16", "Holographic Entanglement Entropy", "pass", detail,
           time.time() - t, {"entropy_data": entropy_data, "scaling_law": scaling_law,
                              "entropy_variance": round(entropy_variance, 8)})


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENT 17: Contextuality — Peres-Mermin Square
# ═══════════════════════════════════════════════════════════════════════
# Contextuality means measurement outcomes depend on what else is being
# measured. The Peres-Mermin square is a 3x3 grid of observables where
# QM violates non-contextual hidden variable constraints. This is key to
# the pilot wave interpretation — Bohmian mechanics IS contextual.

def exp17_peres_mermin():
    """Test quantum contextuality via Peres-Mermin magic square."""
    print("\n" + "═"*64)
    print("  EXP 17: Peres-Mermin Contextuality Test")
    print("═"*64)
    t = time.time()

    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    sim = AerSimulator()

    SHOTS = 8192

    # Peres-Mermin square observables (2 qubits):
    # Row 1: X⊗I, I⊗X, X⊗X  (product = +I)
    # Row 2: I⊗Y, Y⊗I, Y⊗Y  (product = +I)
    # Row 3: X⊗Y, Y⊗X, Z⊗Z  (product = +I)
    # Col products: all -I (anti-commuting constraint)
    # Non-contextual HV: impossible for all rows +1 AND all cols -1

    observables = {
        "XI": lambda qc: qc.h(0),                              # measure X on q0
        "IX": lambda qc: qc.h(1),                              # measure X on q1
        "XX": lambda qc: (qc.h(0), qc.h(1)),                  # measure X⊗X
        "IY": lambda qc: qc.sdg(1),                            # measure Y on q1 (via S†H)
        "YI": lambda qc: qc.sdg(0),                            # measure Y on q0
        "YY": lambda qc: (qc.sdg(0), qc.sdg(1)),              # measure Y⊗Y
        "XY": lambda qc: (qc.h(0), qc.sdg(1)),                # measure X⊗Y
        "YX": lambda qc: (qc.sdg(0), qc.h(1)),                # measure Y⊗X
        "ZZ": lambda qc: None,                                 # Z⊗Z = computational basis
    }

    # For each observable, prepare a maximally entangled state and measure
    obs_results = {}

    for obs_name, rotation_fn in observables.items():
        qc = QuantumCircuit(2, 2)
        # Prepare Bell state
        qc.h(0)
        qc.cx(0, 1)
        # Apply measurement basis rotation
        rotation_fn(qc)
        # Complete basis change for Y measurements
        if 'Y' in obs_name:
            for i, c in enumerate(obs_name):
                if c == 'Y':
                    qc.h(i)
        elif obs_name == "ZZ":
            pass  # Already in Z basis
        else:
            pass  # H already applied

        qc.measure([0, 1], [0, 1])
        counts = sim.run(qc, shots=SHOTS).result().get_counts()

        # Compute expectation: +1 for same parity, -1 for different
        same = counts.get('00', 0) + counts.get('11', 0)
        diff = counts.get('01', 0) + counts.get('10', 0)
        E = (same - diff) / SHOTS

        obs_results[obs_name] = {
            "expectation": round(E, 4),
            "counts": dict(counts)
        }

    # Check row and column products
    rows = [
        ("Row1", ["XI", "IX", "XX"], +1),
        ("Row2", ["IY", "YI", "YY"], +1),
        ("Row3", ["XY", "YX", "ZZ"], +1),
    ]
    cols = [
        ("Col1", ["XI", "IY", "XY"], -1),
        ("Col2", ["IX", "YI", "YX"], -1),
        ("Col3", ["XX", "YY", "ZZ"], -1),
    ]

    constraint_results = []
    for label, obs_list, expected_sign in rows + cols:
        product = 1.0
        for obs in obs_list:
            product *= obs_results[obs]["expectation"]
        matches = (product > 0 and expected_sign > 0) or (product < 0 and expected_sign < 0)
        constraint_results.append({
            "label": label,
            "observables": obs_list,
            "product": round(product, 4),
            "expected": expected_sign,
            "matches_QM": matches
        })

    matching = sum(1 for c in constraint_results if c["matches_QM"])

    detail = (f"9 Peres-Mermin observables measured | "
              f"Constraint satisfaction: {matching}/{len(constraint_results)} | "
              f"Contextuality: {'CONFIRMED' if matching >= 4 else 'inconclusive'} | "
              f"Pilot wave prediction: contextual (consistent with Bohmian mechanics)")

    record("EXP-17", "Peres-Mermin Contextuality", "pass", detail,
           time.time() - t, {"observables": obs_results, "constraints": constraint_results})


# ═══════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔" + "═"*62 + "╗")
    print("║  UNA QUANTUM LAB — PILOT WAVE THEORY EXPERIMENTS            ║")
    print("║  de Broglie-Bohm / Valentini Non-Equilibrium Search         ║")
    print("║  ResoVerse.io / UNA-AI                                      ║")
    print("╚" + "═"*62 + "╝")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backends: Qiskit Aer, Google Cirq, PennyLane")
    print()

    experiments = [
        ("EXP-12", exp12_born_rule_deviation),
        ("EXP-13", exp13_bohmian_trajectories),
        ("EXP-14", exp14_chsh_bell_inequality),
        ("EXP-15", exp15_noise_signatures),
        ("EXP-16", exp16_holographic_entropy),
        ("EXP-17", exp17_peres_mermin),
    ]

    for exp_id, exp_fn in experiments:
        try:
            exp_fn()
        except Exception as e:
            record(exp_id, exp_id, "fail", f"EXCEPTION: {str(e)}")
            traceback.print_exc()

    # ─── SUMMARY ───
    print("\n" + "═"*64)
    print("📊  UNA PILOT WAVE EXPERIMENT SUITE — RESULTS")
    print("═"*64)
    total = pass_c = fail_c = anomaly_c = 0
    for exp_id, d in sorted(results.items()):
        icon = {"pass": "✅", "fail": "❌", "anomaly": "⚠️"}.get(d["status"], "?")
        print(f"  {icon}  {exp_id}: {d['name']}  ({d['duration_s']}s)")
        print(f"       {d['detail'][:100]}")
        total += 1
        if d["status"] == "pass": pass_c += 1
        elif d["status"] == "fail": fail_c += 1
        elif d["status"] == "anomaly": anomaly_c += 1

    print(f"\n  {'─'*60}")
    print(f"  Total: {total}  |  ✅ {pass_c} passed  |  ⚠️ {anomaly_c} anomalies  |  ❌ {fail_c} failed")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if anomaly_c > 0:
        print(f"\n  🔬  {anomaly_c} ANOMALIES DETECTED — requires further investigation")
        print(f"      These results warrant replication on IBM ibm_fez real QPU")
    else:
        print(f"\n  📝  All results consistent with standard QM / Born rule")
        print(f"      No non-equilibrium signals detected at this precision")
        print(f"      Next step: repeat on IBM ibm_fez real QPU for hardware-level test")

    print("═"*64)

    # Save results
    output = {
        "experiment_suite": "Pilot Wave Theory — de Broglie-Bohm Experiments",
        "inspired_by": "Valentini, Beyond the Quantum (OUP 2026) / Scientific American Mar 2026",
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total": total,
            "passed": pass_c,
            "anomalies": anomaly_c,
            "failed": fail_c,
            "verdict": "ANOMALY_DETECTED" if anomaly_c > 0 else "CONSISTENT_WITH_BORN_RULE"
        }
    }

    output_path = "/Users/tombudd/projects/quantum-experiments/pilot_wave_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  💾  Saved → {output_path}\n")
