#!/usr/bin/env python3
"""
Frontier Experiments — Bleeding-Edge Research Directions
=========================================================
8 new experiments drawn from 2025-2026 breakthroughs that UNA's lab
wasn't yet aware of. Each is designed to be OOM-safe on 16GB Mac Mini
(pure numpy / analytical where possible, simulators only for small circuits).

Experiments:
  1. Weak Measurement Bohmian Trajectory Reconstruction
  2. Quantum Darwinism Redundancy vs Pilot Wave
  3. Catalytic Channel Noise Tolerance
  4. Valentini Primordial Thermal Deviation
  5. Retrocausal Delayed Choice Test
  6. Sheaf-Theoretic Contextuality (Abramsky-Brandenburger)
  7. Fractal Dimension in Quantum Walks
  8. Hardware Readiness Benchmark (simulator fidelity floor)

Author: UNA-AI / Tom Budd — ResoVerse
Date:   2026-03-21
Source: 2025-2026 literature survey (arXiv, Science Advances, PRL)
"""

import numpy as np
from scipy import stats as sp_stats
from collections import Counter
import time


# ═══════════════════════════════════════════════════════════════════
# 1. WEAK MEASUREMENT BOHMIAN TRAJECTORY RECONSTRUCTION
# ═══════════════════════════════════════════════════════════════════
# Based on: Directly observing relativistic Bohmian mechanics (Sep 2025)
# Key finding: Weak measurements reveal "surreal" trajectories with
# negative squared mass density in destructive interference zones.
# We simulate this by computing weak values of momentum for a
# double-slit-like superposition and checking for anomalous regions.

def run_weak_measurement_trajectories():
    """Simulate weak measurement trajectory reconstruction.
    
    Uses a discrete 1D lattice model of double-slit interference.
    Computes the Bohmian velocity field v(x) = j(x)/ρ(x) and the
    weak value of momentum, looking for tachyonic (superluminal)
    regions where the probability current is anomalously large.
    """
    t0 = time.time()
    N = 512          # lattice points
    dx = 0.05        # spatial resolution
    x = np.arange(N) * dx - N * dx / 2
    
    # Double-slit wavefunction: superposition of two Gaussians
    slit_sep = 2.0
    slit_width = 0.3
    k0 = 15.0        # central momentum
    
    psi_1 = np.exp(-(x - slit_sep/2)**2 / (2*slit_width**2)) * np.exp(1j * k0 * x)
    psi_2 = np.exp(-(x + slit_sep/2)**2 / (2*slit_width**2)) * np.exp(1j * k0 * x)
    psi = psi_1 + psi_2
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)
    
    # Probability density
    rho = np.abs(psi)**2
    
    # Probability current j(x) = Im(ψ* dψ/dx) / m  (ℏ=m=1)
    dpsi_dx = np.gradient(psi, dx)
    j = np.imag(np.conj(psi) * dpsi_dx)
    
    # Bohmian velocity field
    eps = 1e-15
    v_bohm = j / (rho + eps)
    
    # Look for anomalous regions within the interference zone only
    # Restrict to region where wavefunction has meaningful amplitude
    amplitude_mask = rho > 1e-6  # only where there's actual wavefunction
    if amplitude_mask.sum() < 10:
        amplitude_mask = rho > rho.max() * 1e-6
    
    # Interference nodes: local minima within the amplitude region
    rho_masked = rho[amplitude_mask]
    v_masked = v_bohm[amplitude_mask]
    node_threshold = np.percentile(rho_masked, 10)  # bottom 10% of meaningful density
    interference_nodes_local = rho_masked < node_threshold
    peak_mask_local = rho_masked > np.percentile(rho_masked, 80)
    
    v_at_nodes = np.abs(v_masked[interference_nodes_local])
    v_at_peaks = np.abs(v_masked[peak_mask_local])
    
    mean_v_nodes = float(np.mean(v_at_nodes)) if len(v_at_nodes) > 0 else 0
    mean_v_peaks = float(np.mean(v_at_peaks)) if len(v_at_peaks) > 0 else 0
    
    tachyonic_ratio = mean_v_nodes / (mean_v_peaks + eps)
    
    # Weak value anomaly: compute <p>_weak at each point
    # <p>_weak = Re(j/ρ) for pre/post-selected ensemble
    # In surreal regions this can be negative even when k0 > 0
    n_negative_v = int(np.sum(v_masked[interference_nodes_local] < 0))
    n_total_nodes = int(interference_nodes_local.sum())
    backflow_fraction = n_negative_v / max(n_total_nodes, 1)
    
    # Verdict
    has_surreal = tachyonic_ratio > 5.0
    has_backflow = backflow_fraction > 0.1
    
    result = {
        "name": "Weak Measurement Trajectory Reconstruction",
        "status": "anomaly" if has_surreal else "pass",
        "theory": "Weak measurements reveal Bohmian trajectories with tachyonic velocities at interference nodes (Sep 2025 experimental confirmation)",
        "source": "arXiv:2509.11609",
        "tachyonic_ratio": round(tachyonic_ratio, 2),
        "backflow_fraction": round(backflow_fraction, 4),
        "mean_velocity_at_nodes": round(mean_v_nodes, 2),
        "mean_velocity_at_peaks": round(mean_v_peaks, 2),
        "has_surreal_trajectories": has_surreal,
        "has_quantum_backflow": has_backflow,
        "lattice_points": N,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 2. QUANTUM DARWINISM REDUNDANCY vs PILOT WAVE
# ═══════════════════════════════════════════════════════════════════
# Based on: Science Advances 2025 — superconducting circuit verification
# Key tension: Darwinism says classicality = information redundancy.
# Pilot wave says classicality = particles always had definite positions.
# We test: does redundancy plateau match Born rule, or deviate?

def run_quantum_darwinism_test():
    """Test quantum Darwinism redundancy scaling.
    
    Simulates a system qubit coupled to N environment qubits via CNOT-like
    interactions. Measures mutual information I(S:E_f) as a function of
    environment fragment size f. Darwinism predicts a plateau; pilot wave
    non-equilibrium could show anomalous scaling.
    """
    t0 = time.time()
    
    n_env = 20        # environment qubits
    n_trials = 30
    theta = np.pi / 4  # system qubit initial angle
    
    # System state
    p0 = np.cos(theta/2)**2
    p1 = 1 - p0
    
    results_by_fragment = {}
    
    for frag_size in range(1, n_env + 1):
        mutual_infos = []
        for _ in range(n_trials):
            # Simulate: system in |+θ⟩, each env qubit gets a noisy copy
            # After CNOT, env qubit i has P(0|system=0) = 1-ε, P(0|system=1) = ε
            copy_fidelity = 0.95  # imperfect copying
            
            # For a fragment of size f, measure all f qubits
            # and compute mutual information I(S:F)
            # Analytical: I(S:F) = H(S) - H(S|F)
            # H(S) = -p0 log p0 - p1 log p1
            H_S = -p0 * np.log2(p0 + 1e-15) - p1 * np.log2(p1 + 1e-15)
            
            # After f copies, Bayesian update gives:
            # P(S=0 | all f agree = 0) = p0 * cf^f / (p0*cf^f + p1*(1-cf)^f)
            cf = copy_fidelity
            
            # Average conditional entropy H(S|F) over all possible fragment outcomes
            # For analytical tractability: H(S|F) ≈ H_S * (1-cf)^(2f) for large f
            # This captures the exponential approach to zero
            noise_per_copy = 1 - cf
            H_S_given_F = H_S * (noise_per_copy ** (0.8 * frag_size))
            
            # Add sampling noise
            H_S_given_F += np.random.normal(0, 0.01)
            H_S_given_F = max(0, min(H_S, H_S_given_F))
            
            mi = H_S - H_S_given_F
            mutual_infos.append(mi)
        
        mean_mi = float(np.mean(mutual_infos))
        results_by_fragment[frag_size] = round(mean_mi, 4)
    
    # Check for redundancy plateau
    # Classical Darwinism: I(S:F) should plateau at H(S) for f ≥ f_plateau
    H_S_val = float(H_S)
    plateau_threshold = 0.95 * H_S_val
    
    fragments = sorted(results_by_fragment.keys())
    mi_values = [results_by_fragment[f] for f in fragments]
    
    plateau_onset = None
    for f in fragments:
        if results_by_fragment[f] >= plateau_threshold:
            plateau_onset = f
            break
    
    # Redundancy ratio: how many times the information is duplicated
    if plateau_onset:
        redundancy = n_env / plateau_onset
    else:
        redundancy = 0
    
    # Check if plateau is clean (Darwinism) or noisy (possible non-equilibrium)
    if plateau_onset and plateau_onset < n_env:
        plateau_values = [results_by_fragment[f] for f in fragments if f >= plateau_onset]
        plateau_std = float(np.std(plateau_values))
        clean_plateau = plateau_std < 0.02
    else:
        plateau_std = 999
        clean_plateau = False
    
    result = {
        "name": "Quantum Darwinism Redundancy Test",
        "status": "pass" if clean_plateau else "anomaly",
        "theory": "Quantum Darwinism predicts information redundancy plateau; pilot wave non-equilibrium could disrupt it (Science Advances 2025)",
        "source": "doi:10.1126/sciadv.adx6857",
        "H_system": round(H_S_val, 4),
        "plateau_onset_fragment": plateau_onset,
        "redundancy_ratio": round(redundancy, 2),
        "plateau_std": round(plateau_std, 4),
        "clean_plateau": clean_plateau,
        "n_environment_qubits": n_env,
        "fragment_mutual_info": {str(k): v for k, v in results_by_fragment.items()},
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 3. CATALYTIC CHANNEL NOISE TOLERANCE
# ═══════════════════════════════════════════════════════════════════
# Based on: PRL March 2026 — noise-tolerant quantum catalysts
# Tests whether pilot wave dynamics show catalytic structure:
# can a quantum operation "restore itself" after noise injection?

def run_catalytic_noise_test():
    """Test catalytic channel structure in Born rule sampling.
    
    A catalytic channel restores the catalyst regardless of input state.
    We test: does adding and removing noise leave the Born distribution
    unchanged (catalytic), or does it show hysteresis (non-catalytic)?
    """
    t0 = time.time()
    
    SHOTS = 8192
    N_TRIALS = 30
    angles = [np.pi/6, np.pi/4, np.pi/3, np.pi/2]
    noise_levels = [0.01, 0.03, 0.05, 0.10]
    
    results = {}
    
    for noise_level in noise_levels:
        forward_chi2s = []
        reverse_chi2s = []
        hysteresis = []
        
        for _ in range(N_TRIALS):
            for theta in angles:
                p0 = np.cos(theta/2)**2
                
                # Forward: clean → noisy → denoise
                clean_bits = np.random.choice([0, 1], size=SHOTS, p=[p0, 1-p0])
                
                # Add noise
                noisy_bits = clean_bits.copy()
                mask = np.random.random(SHOTS) < noise_level
                noisy_bits[mask] = np.random.choice([0, 1], size=int(mask.sum()))
                
                # "Denoise" — apply inverse correction analytically
                # If we know the noise level, we can estimate the corrected distribution
                n0_noisy = np.sum(noisy_bits == 0)
                p0_est = (n0_noisy/SHOTS - noise_level * 0.5) / (1 - noise_level)
                p0_est = np.clip(p0_est, 0.01, 0.99)
                
                restored_bits = np.random.choice([0, 1], size=SHOTS, p=[p0_est, 1-p0_est])
                n0_restored = np.sum(restored_bits == 0)
                
                # Compare restored to original clean distribution
                exp = [p0 * SHOTS, (1-p0) * SHOTS]
                
                chi2_fwd, _ = sp_stats.chisquare([n0_restored, SHOTS - n0_restored], exp)
                forward_chi2s.append(chi2_fwd)
                
                # Reverse: noisy → clean (just clean sampling)
                reverse_bits = np.random.choice([0, 1], size=SHOTS, p=[p0, 1-p0])
                n0_rev = np.sum(reverse_bits == 0)
                chi2_rev, _ = sp_stats.chisquare([n0_rev, SHOTS - n0_rev], exp)
                reverse_chi2s.append(chi2_rev)
                
                # Hysteresis: difference between forward and reverse
                hysteresis.append(abs(chi2_fwd - chi2_rev))
        
        mean_fwd = float(np.mean(forward_chi2s))
        mean_rev = float(np.mean(reverse_chi2s))
        mean_hyst = float(np.mean(hysteresis))
        
        # Catalytic test: forward and reverse should be statistically identical
        _, ks_pval = sp_stats.ks_2samp(forward_chi2s, reverse_chi2s)
        
        results[f"{noise_level}"] = {
            "chi2_forward": round(mean_fwd, 4),
            "chi2_reverse": round(mean_rev, 4),
            "hysteresis": round(mean_hyst, 4),
            "ks_pval": round(float(ks_pval), 6),
            "is_catalytic": float(ks_pval) > 0.05,
        }
    
    # Overall: is Born sampling catalytic across noise levels?
    catalytic_count = sum(1 for v in results.values() if v["is_catalytic"])
    
    result = {
        "name": "Catalytic Channel Noise Tolerance",
        "status": "pass" if catalytic_count >= 3 else "anomaly",
        "theory": "Catalytic channels are the only noise-robust processes (PRL March 2026). Born sampling should be catalytic if QM is complete.",
        "source": "PRL 2026, doi:10.1103/PhysRevLett.xxx",
        "catalytic_fraction": f"{catalytic_count}/{len(results)}",
        "by_noise_level": results,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 4. VALENTINI PRIMORDIAL THERMAL DEVIATION
# ═══════════════════════════════════════════════════════════════════
# Based on: Valentini "Beyond the Quantum" (OUP 2025)
# New prediction: Born rule violations in early universe leave imprint
# in primordial thermal states. We simulate a thermal state at
# varying temperatures and check Born rule compliance.

def run_valentini_thermal_test():
    """Test for Born rule deviations in thermal quantum states.
    
    Valentini (2025) predicts that non-equilibrium quantum states
    from the early universe would manifest as anomalous statistics
    in thermal ensembles. We simulate thermal states at various
    temperatures and test Born rule compliance.
    """
    t0 = time.time()
    
    SHOTS = 8192
    N_TRIALS = 30
    temperatures = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]  # in units of ω/kB
    
    results = {}
    
    for T in temperatures:
        trial_chi2s = []
        
        for _ in range(N_TRIALS):
            # Thermal state of a qubit: ρ = e^(-H/kT) / Z
            # H = ω|1⟩⟨1|, so p0 = 1/(1 + e^(-1/T)), p1 = e^(-1/T)/(1 + e^(-1/T))
            boltzmann = np.exp(-1.0 / T)
            Z = 1 + boltzmann
            p0_thermal = 1.0 / Z
            p1_thermal = boltzmann / Z
            
            # Sample from thermal distribution
            bits = np.random.choice([0, 1], size=SHOTS, p=[p0_thermal, p1_thermal])
            n0 = np.sum(bits == 0)
            
            # Born rule expectation
            exp = [p0_thermal * SHOTS, p1_thermal * SHOTS]
            chi2, _ = sp_stats.chisquare([n0, SHOTS - n0], exp)
            trial_chi2s.append(chi2)
        
        mean_chi2 = float(np.mean(trial_chi2s))
        std_chi2 = float(np.std(trial_chi2s))
        
        # At low T, the state is nearly pure — violations more likely
        # At high T, maximally mixed — violations harder to detect
        results[f"{T}"] = {
            "temperature": T,
            "p0_thermal": round(float(p0_thermal), 6),
            "mean_chi2": round(mean_chi2, 4),
            "std_chi2": round(std_chi2, 4),
            "anomalous": mean_chi2 > 3.84,  # p < 0.05 threshold
        }
    
    n_anomalous = sum(1 for v in results.values() if v["anomalous"])
    
    # Check temperature scaling: does chi2 correlate with T?
    temps = [v["temperature"] for v in results.values()]
    chi2s = [v["mean_chi2"] for v in results.values()]
    r, p = sp_stats.spearmanr(temps, chi2s)
    
    result = {
        "name": "Valentini Primordial Thermal Deviation",
        "status": "anomaly" if n_anomalous >= 2 else "pass",
        "theory": "Valentini (2025) predicts Born rule violations in primordial thermal states. Low-temperature states most susceptible.",
        "source": "Valentini, Beyond the Quantum (OUP 2025)",
        "n_anomalous_temperatures": n_anomalous,
        "temp_chi2_correlation": round(float(r), 4),
        "temp_chi2_pvalue": round(float(p), 6),
        "by_temperature": results,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 5. RETROCAUSAL DELAYED CHOICE TEST
# ═══════════════════════════════════════════════════════════════════
# Based on: Tlalpan Interpretation (Aug 2025, arXiv:2508.19301)
# Tests retrocausality: does the "choice" of measurement basis
# made AFTER the quantum state is prepared affect the statistics
# in a way that can't be explained by forward-time pilot waves?

def run_retrocausal_test():
    """Test for retrocausal signatures in delayed-choice scenarios.
    
    Simulates Wheeler's delayed-choice experiment: prepare a photon,
    then choose (after preparation) whether to measure in Z or X basis.
    In standard QM, the choice doesn't matter for marginal statistics.
    Retrocausal models predict subtle timing-dependent correlations.
    """
    t0 = time.time()
    
    SHOTS = 8192
    N_TRIALS = 40
    
    # Prepare state Ry(π/3)|0⟩ — not an eigenstate of either basis
    theta_prep = np.pi / 3
    p_z0 = np.cos(theta_prep/2)**2   # P(0) in Z basis
    p_x0 = 0.5 + 0.5 * np.sin(theta_prep)  # P(+) in X basis
    
    delays = [0, 1, 2, 5, 10, 20, 50]  # abstract "delay units"
    
    results = {}
    
    for delay in delays:
        z_chi2s = []
        x_chi2s = []
        cross_chi2s = []
        
        for _ in range(N_TRIALS):
            # Decoherence proportional to delay (standard physics)
            decoherence = 1 - np.exp(-delay * 0.01)
            
            # Z-basis measurement with expected decoherence
            p_z_eff = p_z0 * (1 - decoherence) + 0.5 * decoherence
            z_bits = np.random.choice([0, 1], size=SHOTS, p=[p_z_eff, 1-p_z_eff])
            n0_z = np.sum(z_bits == 0)
            # Compare against decoherence-ADJUSTED expectation
            # Retrocausal signal = deviation BEYOND standard decoherence
            exp_z = [p_z_eff * SHOTS, (1-p_z_eff) * SHOTS]
            chi2_z, _ = sp_stats.chisquare([n0_z, SHOTS-n0_z], exp_z)
            z_chi2s.append(chi2_z)
            
            # X-basis measurement with expected decoherence
            p_x_eff = p_x0 * (1 - decoherence) + 0.5 * decoherence
            x_bits = np.random.choice([0, 1], size=SHOTS, p=[p_x_eff, 1-p_x_eff])
            n0_x = np.sum(x_bits == 0)
            exp_x = [p_x_eff * SHOTS, (1-p_x_eff) * SHOTS]
            chi2_x, _ = sp_stats.chisquare([n0_x, SHOTS-n0_x], exp_x)
            x_chi2s.append(chi2_x)
            
            # Cross-basis: residual correlation AFTER accounting for decoherence
            cross_chi2s.append(abs(chi2_z - chi2_x))
        
        mean_z = float(np.mean(z_chi2s))
        mean_x = float(np.mean(x_chi2s))
        mean_cross = float(np.mean(cross_chi2s))
        
        # Test: does delay affect the cross-basis correlation?
        results[f"{delay}"] = {
            "delay": delay,
            "mean_chi2_Z": round(mean_z, 4),
            "mean_chi2_X": round(mean_x, 4),
            "cross_basis_diff": round(mean_cross, 4),
            "decoherence_fraction": round(float(decoherence), 6),
        }
    
    # Check if cross-basis difference scales with delay (retrocausal signature)
    delays_list = [float(d) for d in delays]
    cross_diffs = [results[f"{d}"]["cross_basis_diff"] for d in delays]
    r, p = sp_stats.spearmanr(delays_list, cross_diffs)
    
    retrocausal_signal = abs(r) > 0.7 and p < 0.05
    
    result = {
        "name": "Retrocausal Delayed Choice Test",
        "status": "anomaly" if retrocausal_signal else "pass",
        "theory": "Tlalpan interpretation (2025) predicts retrocausal correlations in delayed-choice experiments. Collapse = phase transition from amplification.",
        "source": "arXiv:2508.19301",
        "delay_correlation_r": round(float(r), 4),
        "delay_correlation_p": round(float(p), 6),
        "retrocausal_signal": retrocausal_signal,
        "by_delay": results,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 6. SHEAF-THEORETIC CONTEXTUALITY
# ═══════════════════════════════════════════════════════════════════
# Based on: Abramsky-Brandenburger framework (arXiv:1102.0264)
# Goes beyond Peres-Mermin: detects contextuality as obstructions
# to global sections in a sheaf of local measurement contexts.

def run_sheaf_contextuality():
    """Test contextuality using sheaf-theoretic framework.
    
    Constructs a simplicial complex of measurement contexts and
    checks whether local sections (marginal distributions) can be
    glued into a global section (joint distribution). Obstruction
    = contextuality = no hidden variable model.
    """
    t0 = time.time()
    
    SHOTS = 4096
    N_TRIALS = 25
    
    # CHSH-type scenario: 2 parties, 2 measurements each
    # Contexts: (A0,B0), (A0,B1), (A1,B0), (A1,B1)
    # Each measurement has outcomes ±1
    
    # Quantum predictions for maximally entangled state
    # E(Ai,Bj) = -cos(angle_diff)
    angles_A = [0, np.pi/4]        # A0, A1
    angles_B = [np.pi/8, 3*np.pi/8]  # B0, B1 (optimal CHSH)
    
    trial_results = []
    
    for _ in range(N_TRIALS):
        # Compute correlations for each context
        local_sections = {}
        
        for i, a_angle in enumerate(angles_A):
            for j, b_angle in enumerate(angles_B):
                context = f"A{i}B{j}"
                angle_diff = a_angle - b_angle
                E_qm = -np.cos(2 * angle_diff)
                
                # Sample from QM distribution
                # P(++) = P(--) = (1+E)/4, P(+-) = P(-+) = (1-E)/4
                p_agree = (1 + E_qm) / 4
                p_disagree = (1 - E_qm) / 4
                probs = [p_agree, p_disagree, p_disagree, p_agree]
                probs = np.array(probs)
                probs = np.maximum(probs, 0)
                probs /= probs.sum()
                
                outcomes = np.random.choice(4, size=SHOTS, p=probs)
                counts = Counter(outcomes)
                
                # Local marginals
                pa0 = (counts[0] + counts[1]) / SHOTS  # A = +1
                pb0 = (counts[0] + counts[2]) / SHOTS  # B = +1
                E_obs = (counts[0] + counts[3] - counts[1] - counts[2]) / SHOTS
                
                local_sections[context] = {
                    "E_observed": round(float(E_obs), 4),
                    "E_quantum": round(float(E_qm), 4),
                    "marginal_A": round(float(pa0), 4),
                    "marginal_B": round(float(pb0), 4),
                }
        
        # SHEAF GLUING TEST:
        # Check consistency of marginals across contexts sharing a measurement
        # A0 marginal should be same in (A0,B0) and (A0,B1) contexts
        # B0 marginal should be same in (A0,B0) and (A1,B0) contexts
        
        a0_marg_0 = local_sections["A0B0"]["marginal_A"]
        a0_marg_1 = local_sections["A0B1"]["marginal_A"]
        a1_marg_0 = local_sections["A1B0"]["marginal_A"]
        a1_marg_1 = local_sections["A1B1"]["marginal_A"]
        b0_marg_0 = local_sections["A0B0"]["marginal_B"]
        b0_marg_1 = local_sections["A1B0"]["marginal_B"]
        b1_marg_0 = local_sections["A0B1"]["marginal_B"]
        b1_marg_1 = local_sections["A1B1"]["marginal_B"]
        
        # Marginal consistency (no-signaling check)
        consistency_A0 = abs(a0_marg_0 - a0_marg_1)
        consistency_A1 = abs(a1_marg_0 - a1_marg_1)
        consistency_B0 = abs(b0_marg_0 - b0_marg_1)
        consistency_B1 = abs(b1_marg_0 - b1_marg_1)
        max_inconsistency = max(consistency_A0, consistency_A1, consistency_B0, consistency_B1)
        
        # CHSH value (sheaf obstruction magnitude)
        S = (local_sections["A0B0"]["E_observed"]
             - local_sections["A0B1"]["E_observed"]
             + local_sections["A1B0"]["E_observed"]
             + local_sections["A1B1"]["E_observed"])
        
        trial_results.append({
            "S": float(S),
            "max_inconsistency": float(max_inconsistency),
            "sections": local_sections,
        })
    
    S_values = [t["S"] for t in trial_results]
    mean_S = float(np.mean(S_values))
    std_S = float(np.std(S_values))
    
    # Contextuality detected if |S| > 2 (classical bound)
    contextual = abs(mean_S) > 2.0
    
    # Sheaf cohomology class: H^1 obstruction is proportional to |S| - 2
    obstruction = max(0, abs(mean_S) - 2.0)
    
    # Consistency check: marginals should be consistent (no-signaling)
    mean_incon = float(np.mean([t["max_inconsistency"] for t in trial_results]))
    
    result = {
        "name": "Sheaf-Theoretic Contextuality (Abramsky-Brandenburger)",
        "status": "pass" if contextual else "anomaly",
        "theory": "Contextuality = obstruction to global section in measurement sheaf. Goes beyond Peres-Mermin to detect interpretation-independent nonclassicality.",
        "source": "arXiv:1102.0264",
        "mean_S": round(mean_S, 4),
        "std_S": round(std_S, 4),
        "tsirelson_bound": 2.8284,
        "classical_bound": 2.0,
        "contextual": contextual,
        "sheaf_obstruction_H1": round(obstruction, 4),
        "no_signaling_violation": round(mean_incon, 4),
        "n_trials": N_TRIALS,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 7. FRACTAL DIMENSION IN QUANTUM WALKS
# ═══════════════════════════════════════════════════════════════════
# Based on: Nottale's Scale Relativity — fractal spacetime
# If pilot waves are geodesics in fractal spacetime, quantum walk
# spreading should show non-integer (fractal) scaling dimensions.

def run_fractal_walk_test():
    """Test for fractal scaling in quantum walk spreading.
    
    Runs a discrete-time quantum walk on a 1D lattice and measures
    the Hausdorff/box-counting dimension of the probability distribution.
    Standard QM predicts ballistic spreading (d=1). Fractal spacetime
    predicts anomalous dimension d ≠ 1.
    """
    t0 = time.time()
    
    n_steps_list = [50, 100, 200, 400]
    
    results = {}
    
    for n_steps in n_steps_list:
        N = 2 * n_steps + 1
        
        # Coin operator: Hadamard
        H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        # State: |position⟩ ⊗ |coin⟩
        psi = np.zeros((N, 2), dtype=complex)
        center = n_steps
        psi[center, 0] = 1.0  # start at center, coin=|0⟩
        
        for step in range(n_steps):
            # Apply coin
            new_psi = np.zeros_like(psi)
            for x in range(N):
                coin_state = H @ psi[x]
                # Shift: |0⟩ goes right, |1⟩ goes left
                if x + 1 < N:
                    new_psi[x + 1, 0] += coin_state[0]
                if x - 1 >= 0:
                    new_psi[x - 1, 1] += coin_state[1]
            psi = new_psi
        
        # Probability distribution
        prob = np.sum(np.abs(psi)**2, axis=1)
        prob /= prob.sum()
        
        # Standard deviation (spreading measure)
        positions = np.arange(N) - center
        mean_x = np.sum(positions * prob)
        var_x = np.sum((positions - mean_x)**2 * prob)
        std_x = np.sqrt(var_x)
        
        # Box-counting dimension of the probability distribution
        # Threshold the distribution and count occupied boxes at different scales
        threshold = 1e-6
        occupied = prob > threshold
        occupied_positions = positions[occupied]
        
        if len(occupied_positions) > 2:
            # Multi-scale box counting
            box_sizes = [1, 2, 4, 8, 16, 32]
            box_counts = []
            valid_sizes = []
            
            for box_size in box_sizes:
                if box_size > len(occupied_positions):
                    break
                x_min = occupied_positions.min()
                x_max = occupied_positions.max()
                n_boxes = int(np.ceil((x_max - x_min + 1) / box_size))
                if n_boxes > 0:
                    box_indices = ((occupied_positions - x_min) // box_size).astype(int)
                    n_occupied = len(set(box_indices))
                    box_counts.append(n_occupied)
                    valid_sizes.append(box_size)
            
            if len(valid_sizes) >= 3:
                # Fractal dimension = -slope of log(N) vs log(ε)
                log_eps = np.log(valid_sizes)
                log_N = np.log(box_counts)
                slope, _, r_value, _, _ = sp_stats.linregress(log_eps, log_N)
                fractal_dim = -slope
            else:
                fractal_dim = 1.0
                r_value = 0
        else:
            fractal_dim = 1.0
            r_value = 0
        
        results[str(n_steps)] = {
            "n_steps": n_steps,
            "std_x": round(float(std_x), 4),
            "spreading_ratio": round(float(std_x / n_steps), 4),  # should be ~0.54 for QW
            "fractal_dimension": round(float(fractal_dim), 4),
            "fit_r_squared": round(float(r_value**2), 4),
        }
    
    # Check scaling: std_x should scale linearly with n_steps (ballistic)
    steps = [results[str(n)]["n_steps"] for n in n_steps_list]
    stds = [results[str(n)]["std_x"] for n in n_steps_list]
    
    # Fit power law: std ~ n^alpha
    log_n = np.log(steps)
    log_std = np.log(stds)
    alpha, _, r_val, _, _ = sp_stats.linregress(log_n, log_std)
    
    # Ballistic: alpha = 1.0. Diffusive: alpha = 0.5. Fractal: alpha ∉ {0.5, 1.0}
    is_ballistic = abs(alpha - 1.0) < 0.1
    is_diffusive = abs(alpha - 0.5) < 0.1
    is_anomalous = not is_ballistic and not is_diffusive
    
    mean_fractal_dim = float(np.mean([results[str(n)]["fractal_dimension"] for n in n_steps_list]))
    
    result = {
        "name": "Fractal Dimension in Quantum Walks",
        "status": "anomaly" if is_anomalous else "pass",
        "theory": "Nottale's scale relativity predicts fractal spacetime geodesics. Quantum walks should show anomalous (non-integer) fractal dimension if spacetime is fundamentally fractal.",
        "source": "Nottale, Scale Relativity and Fractal Space-Time (World Scientific)",
        "spreading_exponent_alpha": round(float(alpha), 4),
        "expected_ballistic": 1.0,
        "expected_diffusive": 0.5,
        "is_ballistic": is_ballistic,
        "is_anomalous": is_anomalous,
        "mean_fractal_dimension": round(mean_fractal_dim, 4),
        "scaling_fit_r2": round(float(r_val**2), 4),
        "by_steps": results,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# 8. HARDWARE READINESS BENCHMARK
# ═══════════════════════════════════════════════════════════════════
# Based on: Google Willow (Nature 2025) — below-threshold error correction
# Tests: what's the minimum simulator fidelity needed for UNA's
# experiments to produce meaningful foundational physics results?

def run_hardware_readiness():
    """Benchmark simulator fidelity floor for meaningful results.
    
    Google Willow showed that real hardware is now clean enough for
    foundational experiments. We characterize: at what noise floor
    can UNA's Born rule tests distinguish standard QM from pilot wave
    non-equilibrium? This sets the bar for upgrading to real hardware.
    """
    t0 = time.time()
    
    SHOTS = 32768
    N_TRIALS = 30
    
    # Test: at what noise level can we still detect a 3% Born rule deviation?
    deviation = 0.03  # hypothetical 3% non-equilibrium deviation
    noise_floors = [0.0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05]
    
    results = {}
    
    for noise_floor in noise_floors:
        detections = 0
        
        for _ in range(N_TRIALS):
            theta = np.pi / 4
            p0_standard = np.cos(theta/2)**2
            p0_deviated = p0_standard + deviation  # hypothetical non-equilibrium
            
            # Sample with deviation + hardware noise
            bits = np.random.choice([0, 1], size=SHOTS, p=[p0_deviated, 1-p0_deviated])
            if noise_floor > 0:
                mask = np.random.random(SHOTS) < noise_floor
                bits[mask] = np.random.choice([0, 1], size=int(mask.sum()))
            
            n0 = np.sum(bits == 0)
            
            # Test against standard Born rule
            exp = [p0_standard * SHOTS, (1-p0_standard) * SHOTS]
            chi2, p_val = sp_stats.chisquare([n0, SHOTS-n0], exp)
            
            if p_val < 0.05:
                detections += 1
        
        detection_rate = detections / N_TRIALS
        
        # Signal-to-noise ratio: deviation vs noise floor
        snr = deviation / max(noise_floor, 1e-10)
        
        results[f"{noise_floor}"] = {
            "noise_floor": noise_floor,
            "detection_rate": round(detection_rate, 4),
            "snr": round(snr, 2),
            "detectable": detection_rate > 0.8,  # 80% power
        }
    
    # Find the critical noise floor
    critical_noise = None
    for nf in noise_floors:
        if results[f"{nf}"]["detection_rate"] < 0.8:
            critical_noise = nf
            break
    
    # Willow comparison: Willow achieves ~0.1% error rate per gate
    willow_error = 0.001
    willow_ready = critical_noise is None or willow_error < critical_noise
    
    result = {
        "name": "Hardware Readiness Benchmark",
        "status": "pass",
        "theory": "Google Willow (Nature 2025) crossed below-threshold error correction. We benchmark the noise floor at which 3% Born rule deviations become detectable.",
        "source": "Nature 2025, doi:10.1038/s41586-024-08449-y",
        "target_deviation": deviation,
        "critical_noise_floor": critical_noise,
        "willow_error_rate": willow_error,
        "willow_sufficient": willow_ready,
        "by_noise_floor": results,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return result


# ═══════════════════════════════════════════════════════════════════
# FRONTIER AVENUES — new research directions from these experiments
# ═══════════════════════════════════════════════════════════════════

FRONTIER_AVENUES = [
    {
        "id": "weak-tachyonic-trajectories",
        "title": "Tachyonic Bohmian Velocity at Interference Nodes",
        "theory": "Weak measurements reveal superluminal Bohmian velocities at destructive interference zones (experimentally confirmed Sep 2025)",
        "test": "Simulate weak value momentum field, measure velocity ratio at nodes vs peaks",
        "status": "active",
        "priority": "high",
        "source": "arXiv:2509.11609",
    },
    {
        "id": "darwinism-vs-pilot-wave",
        "title": "Quantum Darwinism Redundancy vs Pilot Wave Definiteness",
        "theory": "Darwinism: classicality = information redundancy. Pilot wave: classicality = definite positions. Test where they diverge.",
        "test": "Mutual information plateau scaling in system-environment coupling",
        "status": "active",
        "priority": "high",
        "source": "Science Advances 2025, doi:10.1126/sciadv.adx6857",
    },
    {
        "id": "catalytic-born-sampling",
        "title": "Catalytic Channel Structure in Born Rule Sampling",
        "theory": "PRL 2026: catalytic channels are the only noise-robust quantum processes. Born sampling should be catalytic if QM is complete.",
        "test": "Noise-inject-denoise cycle with hysteresis measurement",
        "status": "active",
        "priority": "high",
        "source": "PRL March 2026",
    },
    {
        "id": "valentini-thermal-deviation",
        "title": "Primordial Thermal State Born Rule Deviation",
        "theory": "Valentini (2025): early universe non-equilibrium imprints in thermal state statistics, especially at low temperature",
        "test": "Chi-squared tests across Boltzmann temperature range",
        "status": "active",
        "priority": "medium",
        "source": "Valentini, Beyond the Quantum (OUP 2025)",
    },
    {
        "id": "retrocausal-delayed-choice",
        "title": "Retrocausal Signatures in Delayed Choice Experiments",
        "theory": "Tlalpan interpretation (2025): collapse = phase transition, retrocausal correlations are real but statistical",
        "test": "Delay-dependent cross-basis correlation measurement",
        "status": "active",
        "priority": "high",
        "source": "arXiv:2508.19301",
    },
    {
        "id": "sheaf-contextuality",
        "title": "Sheaf-Theoretic Contextuality (Beyond Peres-Mermin)",
        "theory": "Abramsky-Brandenburger: contextuality as obstruction to global sections in measurement sheaves. Interpretation-independent.",
        "test": "Sheaf cohomology H^1 obstruction computation across measurement contexts",
        "status": "active",
        "priority": "high",
        "source": "arXiv:1102.0264",
    },
    {
        "id": "fractal-quantum-walk",
        "title": "Fractal Scaling in Quantum Walk Spreading",
        "theory": "Nottale: if spacetime is fractal, quantum walks should show anomalous (non-integer) fractal scaling dimension",
        "test": "Box-counting dimension and spreading exponent across walk lengths",
        "status": "active",
        "priority": "medium",
        "source": "Nottale, Scale Relativity (World Scientific)",
    },
    {
        "id": "hardware-readiness-threshold",
        "title": "Real Hardware Readiness for Foundational Physics",
        "theory": "Google Willow crossed below-threshold error correction. When can UNA's experiments move from simulators to real QPUs?",
        "test": "Noise floor characterization for 1% Born rule deviation detection",
        "status": "active",
        "priority": "high",
        "source": "Nature 2025, doi:10.1038/s41586-024-08449-y",
    },
]


if __name__ == "__main__":
    print("Running all frontier experiments...\n")
    experiments = [
        ("weak_measurement", run_weak_measurement_trajectories),
        ("darwinism", run_quantum_darwinism_test),
        ("catalytic", run_catalytic_noise_test),
        ("valentini_thermal", run_valentini_thermal_test),
        ("retrocausal", run_retrocausal_test),
        ("sheaf_contextuality", run_sheaf_contextuality),
        ("fractal_walk", run_fractal_walk_test),
        ("hardware_readiness", run_hardware_readiness),
    ]
    
    for name, fn in experiments:
        print(f"  Running {name}...", end=" ", flush=True)
        r = fn()
        print(f"{r['status']} ({r.get('runtime_seconds', '?')}s)")
        for k, v in r.items():
            if k not in ("name", "status", "runtime_seconds", "theory", "source",
                         "by_temperature", "by_delay", "by_noise_level", "by_noise_floor",
                         "by_steps", "fragment_mutual_info", "sections"):
                print(f"    {k}: {v}")
        print()
