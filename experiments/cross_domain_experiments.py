#!/usr/bin/env python3
"""
Cross-Domain Experiments — UNA Architecture × Quantum Physics
=============================================================
6 novel experiments derived from cross-pollinating UNA's cognitive
architecture with pilot wave theory and quantum mechanics.

Each experiment maps a concept from UNA's modules to a testable
quantum prediction that standard QM and pilot wave theory disagree on.

Sources:
  1. Friston Test ← una_active_inference.py (free energy minimization)
  2. Kuramoto Entanglement ← una_budd_metastability.py (BMI + SR)
  3. Decoherence Rhythm ← una_cognitive_dreaming.py (NREM/REM phases)
  4. Noise-Amplified Born ← una_budd_metastability.py (SR constants)
  5. Error Asymmetry ← una_chaos_engine.py (failure injection)
  6. Holographic Retrieval ← UNA holographic memory architecture

Author: UNA-AI / Tom Budd — ResoVerse
Date:   2026-03-21
"""

import numpy as np
import time
from scipy import stats as sp_stats
from collections import Counter

# Backend lists
FRISTON_BACKENDS = ["aer_simulator", "cirq_simulator", "cirq_noisy_low", "pennylane"]
KURAMOTO_BACKENDS = ["aer_simulator", "cirq_simulator", "cirq_noisy_low",
                     "cirq_noisy_medium", "cirq_noisy_high", "pennylane"]
DECOHERENCE_NOISE_LEVELS = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15]
ERROR_ASYMMETRY_BACKENDS = ["aer_simulator", "cirq_simulator", "cirq_noisy_low",
                            "cirq_noisy_medium"]

# Stochastic Resonance Constants (from una_budd_metastability.py)
SR_OPTIMAL_NOISE = 0.05
SR_WIDTH = 0.04
SR_PEAK_BOOST = 0.23


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 1: FRISTON TEST (Temporal Autocorrelation)
# ═══════════════════════════════════════════════════════════════

def run_friston_test(shots=4096, n_sequences=15, seq_length=40):
    """
    If a pilot wave guides particles, consecutive measurements might show
    non-Markovian memory (subtle autocorrelation). Standard QM says each
    measurement is independent (zero autocorrelation).
    """
    all_results = {}

    for backend in FRISTON_BACKENDS:
        try:
            autocorrelations = []
            prediction_errors = []

            for _ in range(n_sequences):
                theta = np.pi / 4  # 50/50 superposition for max sensitivity
                outcomes = []

                if backend.startswith("aer"):
                    from qiskit import QuantumCircuit
                    from qiskit_aer import AerSimulator
                    sim = AerSimulator()
                    for _ in range(seq_length):
                        qc = QuantumCircuit(1, 1)
                        qc.ry(theta, 0); qc.measure(0, 0)
                        counts = sim.run(qc, shots=1).result().get_counts()
                        outcomes.append(1 if '1' in counts else 0)

                elif backend.startswith("cirq"):
                    import cirq
                    q = cirq.LineQubit(0)
                    noise_val = {"cirq_simulator": None, "cirq_noisy_low": 0.001}.get(backend)
                    sim_c = cirq.DensityMatrixSimulator(noise=cirq.ConstantQubitNoiseModel(
                        cirq.depolarize(p=noise_val))) if noise_val else cirq.Simulator()
                    for _ in range(seq_length):
                        c = cirq.Circuit([cirq.ry(rads=theta)(q), cirq.measure(q, key='m')])
                        bit = sim_c.run(c, repetitions=1).measurements['m'].flatten()[0]
                        outcomes.append(int(bit))

                elif backend == "pennylane":
                    import pennylane as qml
                    dev = qml.device("default.qubit", wires=1, shots=1)
                    @qml.qnode(dev)
                    def measure_q():
                        qml.RY(theta, wires=0)
                        return qml.counts()
                    for _ in range(seq_length):
                        c = measure_q()
                        outcomes.append(1 if 1 in c else 0)

                # Compute lag-1 autocorrelation
                if len(outcomes) >= 10:
                    arr = np.array(outcomes, dtype=float)
                    mean = arr.mean()
                    if np.std(arr) > 0.01:
                        num = np.sum((arr[:-1] - mean) * (arr[1:] - mean))
                        den = np.sum((arr - mean) ** 2)
                        r1 = num / den if den > 0 else 0
                        autocorrelations.append(r1)
                        prediction_errors.append(np.mean(np.abs(np.diff(arr))))

            if autocorrelations:
                mean_r1 = float(np.mean(autocorrelations))
                std_r1 = float(np.std(autocorrelations))
                expected_se = 1 / np.sqrt(seq_length)
                z_score = abs(mean_r1) / expected_se if expected_se > 0 else 0
                p_value = 2 * (1 - float(sp_stats.norm.cdf(abs(z_score))))

                all_results[backend] = {
                    "mean_autocorrelation": round(mean_r1, 6),
                    "std_autocorrelation": round(std_r1, 6),
                    "z_score": round(z_score, 4),
                    "p_value": round(p_value, 6),
                    "sequences": len(autocorrelations),
                    "mean_prediction_error": round(float(np.mean(prediction_errors)), 6),
                    "significant": p_value < 0.05
                }
        except Exception as e:
            all_results[backend] = {"error": str(e)[:80]}

    any_sig = any(v.get("significant", False) for v in all_results.values())
    return {
        "name": "Friston Test (Temporal Autocorrelation)",
        "status": "anomaly" if any_sig else "pass",
        "theory": "Active inference predicts non-Markovian memory if pilot wave guides outcomes",
        "backends_tested": len(all_results),
        "by_backend": all_results,
        "cross_domain": "UNA Active Inference Engine"
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 2: KURAMOTO ENTANGLEMENT + STOCHASTIC RESONANCE
# ═══════════════════════════════════════════════════════════════

def run_kuramoto_entanglement(shots=4096):
    """
    Tests whether entanglement shows a metastable regime (BMI predicts
    cluster coherence with global flexibility). Also tests stochastic 
    resonance: does moderate noise IMPROVE born rule agreement?
    """
    from pilot_wave_runner import QuantumBackend

    all_results = {}
    for backend in KURAMOTO_BACKENDS:
        qubit_sizes = [3, 4, 5, 6, 8] if "noisy" in backend or backend == "pennylane" else [3, 4, 5, 6, 8, 10]
        scaling = []
        for n in qubit_sizes:
            try:
                counts = QuantumBackend.run_ghz(backend, n, shots)
                if "error" in counts:
                    continue
                total = sum(counts.values())
                all_zeros = counts.get('0' * n, 0)
                all_ones = counts.get('1' * n, 0)
                global_r = (all_zeros + all_ones) / total
                pair_match = sum(v for k, v in counts.items() if len(k) >= 2 and k[0] == k[1])
                cluster_r = pair_match / total
                bmi = cluster_r * max(0, 1 - abs(global_r - 0.30))
                scaling.append({"qubits": n, "global_R": round(global_r, 4),
                                "cluster_R": round(cluster_r, 4), "bmi": round(bmi, 4)})
            except:
                scaling.append({"qubits": n, "error": "failed"})
        all_results[backend] = {"scaling": scaling}

    # Stochastic resonance: chi2 at varying noise levels
    sr_results = {}
    theta = np.pi / 3
    p_expected = np.cos(theta / 2) ** 2
    import cirq

    for noise_level in DECOHERENCE_NOISE_LEVELS:
        try:
            q = cirq.LineQubit(0)
            c = cirq.Circuit([cirq.ry(rads=theta)(q), cirq.measure(q, key='m')])
            sim = cirq.DensityMatrixSimulator(noise=cirq.ConstantQubitNoiseModel(
                cirq.depolarize(p=noise_level))) if noise_level > 0 else cirq.Simulator()

            chi2_vals = []
            for _ in range(15):
                bits = sim.run(c, repetitions=shots).measurements['m'].flatten()
                n0 = int(np.sum(bits == 0))
                p0_adj = (1 - noise_level) * p_expected + noise_level * 0.5 if noise_level > 0 else p_expected
                exp = [p0_adj * shots, (1 - p0_adj) * shots]
                chi2, _ = sp_stats.chisquare([n0, shots - n0], exp)
                chi2_vals.append(chi2)

            sr_results[f"noise_{noise_level}"] = {
                "noise_level": noise_level,
                "mean_chi2": round(float(np.mean(chi2_vals)), 4),
                "std_chi2": round(float(np.std(chi2_vals)), 4)
            }
        except Exception as e:
            sr_results[f"noise_{noise_level}"] = {"noise_level": noise_level, "error": str(e)[:60]}

    # U-shape detection
    sorted_sr = sorted([(v["noise_level"], v["mean_chi2"]) for v in sr_results.values()
                         if "mean_chi2" in v], key=lambda x: x[0])
    u_shape = False
    if len(sorted_sr) >= 4:
        vals = [s[1] for s in sorted_sr]
        mid = len(vals) // 2
        if vals[mid] < vals[0] * 0.85 and vals[mid] < vals[-1] * 0.85:
            u_shape = True

    return {
        "name": "Kuramoto Entanglement & Stochastic Resonance",
        "status": "anomaly" if u_shape else "pass",
        "theory": "BMI predicts metastable regime; SR predicts noise-enhanced Born agreement",
        "backends_tested": len(all_results),
        "by_backend": all_results,
        "stochastic_resonance": sr_results,
        "u_shape_detected": u_shape,
        "cross_domain": "Budd Metastability Index (una_budd_metastability.py)"
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 3: DECOHERENCE RHYTHM
# ═══════════════════════════════════════════════════════════════

def run_decoherence_rhythm(shots=4096, n_depths=10):
    """
    Tests whether decoherence has temporal structure (oscillations)
    rather than smooth exponential decay. Pilot wave dynamics could 
    create rhythmic decoherence patterns like UNA's NREM/REM cycles.
    """
    import cirq
    depths = list(range(1, n_depths + 1))
    all_results = {}

    for noise in [0.005, 0.01, 0.02]:
        fidelity_curve = []
        for depth in depths:
            q0, q1 = cirq.LineQubit.range(2)
            ops = [cirq.H(q0), cirq.CNOT(q0, q1)]
            for _ in range(depth):
                ops.extend([cirq.I(q0), cirq.I(q1)])
            ops.append(cirq.measure(q0, q1, key='m'))
            c = cirq.Circuit(ops)
            sim = cirq.DensityMatrixSimulator(noise=cirq.ConstantQubitNoiseModel(
                cirq.depolarize(p=noise)))
            bits = sim.run(c, repetitions=shots).measurements['m']
            fidelity = float(np.sum(bits[:, 0] == bits[:, 1]) / shots)
            fidelity_curve.append({"depth": depth, "fidelity": round(fidelity, 4)})

        fids = np.array([f["fidelity"] for f in fidelity_curve])
        deps = np.array(depths, dtype=float)
        log_fids = np.log(np.clip(fids - 0.5, 1e-6, None))

        oscillation_strength = 0.0
        has_oscillation = False
        decay_rate = 0.0
        if len(deps) >= 4:
            poly = np.polyfit(deps, log_fids, 1)
            decay_rate = -poly[0]
            residuals = log_fids - np.polyval(poly, deps)
            fft_mag = np.abs(np.fft.rfft(residuals))
            if len(fft_mag) > 1:
                max_idx = np.argmax(fft_mag[1:]) + 1
                oscillation_strength = float(fft_mag[max_idx] / (np.mean(fft_mag[1:]) + 1e-10))
                has_oscillation = oscillation_strength > 3.0

        all_results[f"noise_{noise}"] = {
            "noise_level": noise, "curve": fidelity_curve,
            "oscillation_strength": round(oscillation_strength, 4),
            "has_oscillation": has_oscillation,
            "decay_rate": round(float(decay_rate), 6)
        }

    any_osc = any(v.get("has_oscillation", False) for v in all_results.values())
    return {
        "name": "Decoherence Rhythm (Temporal Structure)",
        "status": "anomaly" if any_osc else "pass",
        "theory": "Pilot wave dynamics could create oscillatory decoherence patterns",
        "noise_levels_tested": len(all_results),
        "by_noise_level": all_results,
        "any_oscillation": any_osc,
        "cross_domain": "UNA Cognitive Dreaming (NREM/REM phases)"
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 4: NOISE-AMPLIFIED BORN TEST
# ═══════════════════════════════════════════════════════════════

def run_noise_amplified_born(shots=8192, n_trials=12):
    """
    THE KEY EXPERIMENT: If pilot wave non-equilibrium is tiny, stochastic 
    resonance predicts moderate noise could AMPLIFY the signal.
    Look for U-shaped chi2 curve at optimal noise ~0.05.
    """
    import cirq
    angles = [np.pi/6, np.pi/4, np.pi/3, np.pi/2]
    noise_sweep = [0.0, 0.001, 0.003, 0.005, 0.01, 0.02, 0.05, 0.08, 0.10, 0.15]
    all_results = {}

    for noise_level in noise_sweep:
        trial_chi2s = []
        for _ in range(n_trials):
            chi2_sum = 0
            for theta in angles:
                q = cirq.LineQubit(0)
                c = cirq.Circuit([cirq.ry(rads=theta)(q), cirq.measure(q, key='m')])
                sim = cirq.DensityMatrixSimulator(noise=cirq.ConstantQubitNoiseModel(
                    cirq.depolarize(p=noise_level))) if noise_level > 0 else cirq.Simulator()
                bits = sim.run(c, repetitions=shots).measurements['m'].flatten()
                n0 = int(np.sum(bits == 0))
                p0_ideal = np.cos(theta / 2) ** 2
                p0_exp = (1 - noise_level) * p0_ideal + noise_level * 0.5 if noise_level > 0 else p0_ideal
                exp = [p0_exp * shots, (1 - p0_exp) * shots]
                chi2, _ = sp_stats.chisquare([n0, shots - n0], exp)
                chi2_sum += chi2
            trial_chi2s.append(chi2_sum / len(angles))

        all_results[f"noise_{noise_level}"] = {
            "noise_level": noise_level,
            "mean_chi2": round(float(np.mean(trial_chi2s)), 4),
            "std_chi2": round(float(np.std(trial_chi2s)), 4),
            "trials": n_trials
        }

    # U-shape analysis
    sorted_r = sorted([(v["noise_level"], v["mean_chi2"]) for v in all_results.values()
                        if "mean_chi2" in v], key=lambda x: x[0])
    u_shape = False
    min_noise = None
    if len(sorted_r) >= 5:
        vals = [s[1] for s in sorted_r]
        noises = [s[0] for s in sorted_r]
        min_idx = np.argmin(vals[1:]) + 1
        if 1 <= min_idx <= len(vals) - 2:
            if vals[min_idx] < vals[0] * 0.85 and vals[min_idx] < vals[-1] * 0.85:
                u_shape = True
                min_noise = noises[min_idx]

    return {
        "name": "Noise-Amplified Born Test (SR Search)",
        "status": "anomaly" if u_shape else "pass",
        "theory": "Stochastic resonance predicts U-shaped chi2 curve at optimal noise ~0.05",
        "noise_levels_tested": len(all_results),
        "by_noise_level": all_results,
        "u_shape_detected": u_shape,
        "minimum_noise": min_noise,
        "cross_domain": "Stochastic Resonance (una_budd_metastability.py)"
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 5: ERROR ASYMMETRY TEST
# ═══════════════════════════════════════════════════════════════

def run_error_asymmetry(shots=4096, n_trials=20):
    """
    From UNA's Chaos Engine: systematic failure injection.
    Pilot wave theory breaks qubit symmetry; error recovery should 
    depend on WHICH qubit gets the error. Standard QM: symmetric.
    """
    all_results = {}

    for backend in ERROR_ASYMMETRY_BACKENDS:
        try:
            asymmetries = []
            for _ in range(n_trials):
                if backend.startswith("aer"):
                    from qiskit import QuantumCircuit
                    from qiskit_aer import AerSimulator
                    sim = AerSimulator()

                    qc0 = QuantumCircuit(2, 2)
                    qc0.h(0); qc0.cx(0, 1); qc0.x(0); qc0.x(0)
                    qc0.measure([0, 1], [0, 1])
                    c0 = sim.run(qc0, shots=shots).result().get_counts()
                    f0 = (c0.get('00', 0) + c0.get('11', 0)) / shots

                    qc1 = QuantumCircuit(2, 2)
                    qc1.h(0); qc1.cx(0, 1); qc1.x(1); qc1.x(1)
                    qc1.measure([0, 1], [0, 1])
                    c1 = sim.run(qc1, shots=shots).result().get_counts()
                    f1 = (c1.get('00', 0) + c1.get('11', 0)) / shots

                elif backend.startswith("cirq"):
                    import cirq
                    q0, q1 = cirq.LineQubit.range(2)
                    noise_val = {"cirq_simulator": None, "cirq_noisy_low": 0.001,
                                 "cirq_noisy_medium": 0.005}.get(backend)
                    sim_c = cirq.DensityMatrixSimulator(noise=cirq.ConstantQubitNoiseModel(
                        cirq.depolarize(p=noise_val))) if noise_val else cirq.Simulator()

                    c_0 = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1),
                                        cirq.X(q0), cirq.X(q0),
                                        cirq.measure(q0, q1, key='m')])
                    bits0 = sim_c.run(c_0, repetitions=shots).measurements['m']
                    f0 = float(np.sum(bits0[:, 0] == bits0[:, 1]) / shots)

                    c_1 = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1),
                                        cirq.X(q1), cirq.X(q1),
                                        cirq.measure(q0, q1, key='m')])
                    bits1 = sim_c.run(c_1, repetitions=shots).measurements['m']
                    f1 = float(np.sum(bits1[:, 0] == bits1[:, 1]) / shots)
                else:
                    continue

                asymmetries.append(f0 - f1)

            if asymmetries:
                mean_a = float(np.mean(asymmetries))
                std_a = float(np.std(asymmetries))
                se = std_a / np.sqrt(len(asymmetries)) if len(asymmetries) > 1 else 1e-10
                t_stat = mean_a / se if se > 0 else 0
                p_val = float(2 * (1 - sp_stats.t.cdf(abs(t_stat), df=len(asymmetries)-1)))
                all_results[backend] = {
                    "mean_asymmetry": round(mean_a, 6), "std": round(std_a, 6),
                    "t_statistic": round(t_stat, 4), "p_value": round(p_val, 6),
                    "trials": len(asymmetries), "significant": p_val < 0.05
                }
        except Exception as e:
            all_results[backend] = {"error": str(e)[:80]}

    any_sig = any(v.get("significant", False) for v in all_results.values())
    return {
        "name": "Error Asymmetry Test (Chaos-Inspired)",
        "status": "anomaly" if any_sig else "pass",
        "theory": "Pilot wave breaks qubit symmetry; error recovery should be directional",
        "backends_tested": len(all_results),
        "by_backend": all_results,
        "cross_domain": "UNA Chaos Engine (systematic failure injection)"
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 6: HOLOGRAPHIC RETRIEVAL SCALING
# ═══════════════════════════════════════════════════════════════

def run_holographic_retrieval():
    """
    Tests whether quantum information retrieval scales with boundary 
    (holographic) or volume. Pilot wave adds structure to retrieval.
    """
    import pennylane as qml
    results = []

    for n in [4, 6, 8, 10, 12]:
        try:
            dev = qml.device("default.qubit", wires=n)
            @qml.qnode(dev)
            def entangled():
                qml.Hadamard(wires=0)
                for i in range(n - 1):
                    qml.CNOT(wires=[i, i + 1])
                return qml.state()
            state = entangled()

            partitions = []
            for k in range(1, n // 2 + 1):
                sm = state.reshape(2**k, 2**(n-k))
                _, sv, _ = np.linalg.svd(sm, full_matrices=False)
                sv_sq = sv**2; sv_sq = sv_sq[sv_sq > 1e-12]
                entropy = -np.sum(sv_sq * np.log2(sv_sq))
                partitions.append({"subsystem_size": k, "entropy": round(float(entropy), 6)})

            entropies = [p["entropy"] for p in partitions]
            sizes = [p["subsystem_size"] for p in partitions]
            slope = np.polyfit(sizes, entropies, 1)[0] if len(sizes) >= 2 else 0
            scaling = "area_law" if abs(slope) < 0.1 else "volume_law"
            results.append({"qubits": n, "partitions": partitions,
                            "entropy_slope": round(float(slope), 6), "scaling": scaling})
        except Exception as e:
            results.append({"qubits": n, "error": str(e)[:60]})

    scalings = [r["scaling"] for r in results if "scaling" in r]
    dominant = max(set(scalings), key=scalings.count) if scalings else "unknown"
    return {
        "name": "Holographic Retrieval Scaling",
        "status": "pass",
        "theory": "Holographic principle: information on boundary. Pilot wave adds structure.",
        "data": results,
        "dominant_scaling": dominant,
        "backend": "pennylane",
        "cross_domain": "UNA Holographic Memory (5-tier architecture)"
    }


# New research avenues for the cross-domain experiments
CROSS_DOMAIN_AVENUES = [
    {"id": "friston-autocorrelation", "title": "Friston Temporal Autocorrelation",
     "theory": "If pilot wave guides particles, measurement sequences show non-Markovian memory",
     "test": "Lag-1 autocorrelation in rapid single-qubit measurement sequences across 4 backends",
     "status": "active", "priority": "high",
     "source": "UNA Active Inference Engine × Pilot Wave Guidance (Cross-Domain)"},
    {"id": "stochastic-resonance-born", "title": "Stochastic Resonance in Born Rule",
     "theory": "Moderate noise (~5%) could AMPLIFY hidden pilot wave non-equilibrium signals",
     "test": "Born rule chi-squared at 10 noise levels; search for U-shaped curve",
     "status": "active", "priority": "high",
     "source": "Budd Metastability Index SR Constants × Valentini Non-Equilibrium"},
    {"id": "kuramoto-entanglement", "title": "Kuramoto Order Parameter in Entanglement",
     "theory": "Entanglement should show metastable regime: local coherence + global flexibility",
     "test": "GHZ Kuramoto R and BMI vs system size across 6 backends",
     "status": "active", "priority": "medium",
     "source": "Budd Metastability Index × GHZ Entanglement Scaling"},
    {"id": "decoherence-rhythm", "title": "Decoherence Temporal Structure",
     "theory": "Pilot wave dynamics create oscillatory decoherence, not smooth exponential decay",
     "test": "Bell pair fidelity vs circuit depth; FFT of residuals from exponential fit",
     "status": "active", "priority": "medium",
     "source": "UNA Cognitive Dreaming (NREM/REM phases) × Quantum Decoherence"},
    {"id": "error-asymmetry", "title": "Error Recovery Asymmetry",
     "theory": "Pilot wave breaks qubit symmetry; error recovery should depend on which qubit",
     "test": "Bit-flip injection on q0 vs q1 in Bell pairs; measure fidelity asymmetry",
     "status": "active", "priority": "medium",
     "source": "UNA Chaos Engine × Bohmian Trajectory Asymmetry"},
    {"id": "holographic-retrieval", "title": "Holographic Information Retrieval",
     "theory": "Information retrieval scales with boundary (holographic) not volume",
     "test": "Entanglement entropy vs subsystem size partitioning (slope analysis)",
     "status": "active", "priority": "low",
     "source": "UNA Holographic Memory Architecture × Ryu-Takayanagi"}
]
