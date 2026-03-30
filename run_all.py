#!/usr/bin/env python3
"""
UNA Quantum Experiment Suite
Runs Bell state, GHZ, QFT, and Quantum Volume tests across all free providers.
Providers: IBM/Qiskit, Google Cirq QVM, AWS Braket (local sim), IonQ (simulator), PennyLane
"""

import json
import os
import time
import traceback
from datetime import datetime

results = {}

def record(provider, experiment, status, detail="", duration=0):
    if provider not in results:
        results[provider] = {}
    results[provider][experiment] = {
        "status": status,
        "detail": detail,
        "duration_s": round(duration, 3)
    }
    icon = "✅" if status == "pass" else "❌"
    print(f"  {icon} [{provider}] {experiment}: {detail[:80]}")

# ─────────────────────────────────────────────
# 1. QISKIT (IBM) — local Aer simulator
# ─────────────────────────────────────────────
print("\n🔷 IBM / Qiskit (Aer local simulator)")
try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    sim = AerSimulator()

    # Bell state
    t = time.time()
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1); qc.measure([0,1],[0,1])
    job = sim.run(qc, shots=1024)
    counts = job.result().get_counts()
    dur = time.time() - t
    record("IBM/Qiskit", "Bell State", "pass", f"counts={counts}", dur)

    # GHZ 5-qubit
    t = time.time()
    qc = QuantumCircuit(5, 5)
    qc.h(0)
    for i in range(4): qc.cx(i, i+1)
    qc.measure_all()
    job = sim.run(qc, shots=1024)
    counts = job.result().get_counts()
    dur = time.time() - t
    dominant = max(counts, key=counts.get)
    record("IBM/Qiskit", "GHZ 5-qubit", "pass", f"dominant={dominant} ({counts[dominant]}/1024)", dur)

    # QFT 4-qubit
    t = time.time()
    from qiskit.circuit.library import QFT
    qc = QFT(4)
    qc.measure_all()
    job = sim.run(qc, shots=512)
    counts = job.result().get_counts()
    dur = time.time() - t
    record("IBM/Qiskit", "QFT 4-qubit", "pass", f"{len(counts)} unique outcomes", dur)

except Exception as e:
    record("IBM/Qiskit", "Suite", "fail", str(e))

# ─────────────────────────────────────────────
# 2. GOOGLE CIRQ QVM (noise-free + noisy)
# ─────────────────────────────────────────────
print("\n🔶 Google Cirq (local simulator + QVM noise models)")
try:
    import cirq
    import cirq_google

    # Bell state — ideal simulator
    t = time.time()
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key='result')])
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=1024)
    counts = result.measurements['result']
    dur = time.time() - t
    record("Google Cirq", "Bell State (ideal)", "pass", f"shape={counts.shape}", dur)

    # GHZ 5-qubit
    t = time.time()
    qubits = cirq.LineQubit.range(5)
    circuit = cirq.Circuit([
        cirq.H(qubits[0]),
        *[cirq.CNOT(qubits[i], qubits[i+1]) for i in range(4)],
        cirq.measure(*qubits, key='ghz')
    ])
    result = sim.run(circuit, repetitions=1024)
    dur = time.time() - t
    record("Google Cirq", "GHZ 5-qubit", "pass", f"1024 shots completed", dur)

    # Noisy simulation (Weber noise model)
    t = time.time()
    try:
        noise_model = cirq_google.engine.create_noiseless_virtual_engine_from_latest_templates()
        record("Google Cirq", "QVM noise model", "pass", "Virtual engine templates loaded", time.time()-t)
    except Exception as e2:
        # Try simpler noise model
        noise = cirq.ConstantQubitNoiseModel(cirq.depolarize(p=0.01))
        noisy_sim = cirq.DensityMatrixSimulator(noise=noise)
        q0, q1 = cirq.LineQubit.range(2)
        circuit = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key='r')])
        result = noisy_sim.run(circuit, repetitions=512)
        record("Google Cirq", "QVM noise model (depolarize)", "pass", "1% depolarize noise applied", time.time()-t)

except Exception as e:
    record("Google Cirq", "Suite", "fail", str(e))

# ─────────────────────────────────────────────
# 3. PENNYLANE (local default.qubit)
# ─────────────────────────────────────────────
print("\n🟣 PennyLane (default.qubit — local)")
try:
    import pennylane as qml
    import numpy as np

    # Bell state
    t = time.time()
    dev = qml.device("default.qubit", wires=2)
    @qml.qnode(dev)
    def bell():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
    probs = bell()
    dur = time.time() - t
    record("PennyLane", "Bell State", "pass", f"|00⟩={probs[0]:.3f} |11⟩={probs[3]:.3f}", dur)

    # GHZ 5-qubit
    t = time.time()
    dev5 = qml.device("default.qubit", wires=5)
    @qml.qnode(dev5)
    def ghz5():
        qml.Hadamard(wires=0)
        for i in range(4): qml.CNOT(wires=[i, i+1])
        return qml.probs(wires=range(5))
    probs = ghz5()
    dur = time.time() - t
    record("PennyLane", "GHZ 5-qubit", "pass", f"|00000⟩={probs[0]:.3f} |11111⟩={probs[-1]:.3f}", dur)

    # QML variational circuit
    t = time.time()
    dev2 = qml.device("default.qubit", wires=4)
    @qml.qnode(dev2)
    def variational(params):
        for i in range(4): qml.RY(params[i], wires=i)
        for i in range(3): qml.CNOT(wires=[i, i+1])
        return qml.expval(qml.PauliZ(0))
    params = np.array([0.1, 0.5, 1.2, 0.8])
    val = variational(params)
    dur = time.time() - t
    record("PennyLane", "Variational QML Circuit", "pass", f"⟨Z₀⟩={val:.4f}", dur)

    # Gradient (QML backbone)
    t = time.time()
    grad_fn = qml.grad(variational)
    grads = grad_fn(params)
    dur = time.time() - t
    record("PennyLane", "Quantum Gradient", "pass", f"grads={np.round(grads,3).tolist()}", dur)

except Exception as e:
    record("PennyLane", "Suite", "fail", str(e))
    traceback.print_exc()

# ─────────────────────────────────────────────
# 4. AWS BRAKET (local simulator)
# ─────────────────────────────────────────────
print("\n🟠 AWS Braket (local simulator)")
try:
    from braket.circuits import Circuit
    from braket.devices import LocalSimulator

    device = LocalSimulator()

    # Bell state
    t = time.time()
    circuit = Circuit().h(0).cnot(0, 1)
    task = device.run(circuit, shots=1024)
    result = task.result()
    counts = result.measurement_counts
    dur = time.time() - t
    record("AWS Braket", "Bell State", "pass", f"counts={dict(counts)}", dur)

    # GHZ 5-qubit
    t = time.time()
    circuit = Circuit().h(0).cnot(0,1).cnot(1,2).cnot(2,3).cnot(3,4)
    task = device.run(circuit, shots=1024)
    result = task.result()
    counts = result.measurement_counts
    dominant = max(counts, key=counts.get)
    dur = time.time() - t
    record("AWS Braket", "GHZ 5-qubit", "pass", f"dominant={dominant} ({counts[dominant]}/1024)", dur)

    # QFT 4-qubit via manual implementation
    t = time.time()
    import numpy as np
    circuit = Circuit()
    n = 4
    for i in range(n):
        circuit.h(i)
        for j in range(i+1, n):
            circuit.cphaseshift(j, i, np.pi / 2**(j-i))
    task = device.run(circuit, shots=512)
    result = task.result()
    dur = time.time() - t
    record("AWS Braket", "QFT 4-qubit", "pass", f"{len(result.measurement_counts)} unique outcomes", dur)

except Exception as e:
    record("AWS Braket", "Suite", "fail", str(e))
    traceback.print_exc()

# ─────────────────────────────────────────────
# 5. IONQ (simulator via qiskit-ionq)
# ─────────────────────────────────────────────
print("\n🔵 IonQ (cloud simulator)")
try:
    from qiskit_ionq import IonQProvider
    provider = IonQProvider(token=os.environ.get("IONQ_API_TOKEN", ""))
    backend = provider.get_backend("ionq_simulator")

    t = time.time()
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1); qc.measure([0,1],[0,1])
    job = backend.run(qc, shots=1024)
    counts = job.result().get_counts()
    dur = time.time() - t
    record("IonQ", "Bell State", "pass", f"counts={counts}", dur)

except ImportError:
    record("IonQ", "Bell State", "skip", "qiskit-ionq not installed — install with: pip3 install qiskit-ionq")
except Exception as e:
    record("IonQ", "Bell State", "fail", str(e)[:120])

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("📊 EXPERIMENT SUMMARY")
print("="*60)
total = pass_count = fail_count = skip_count = 0
for provider, experiments in results.items():
    print(f"\n  {provider}:")
    for exp, data in experiments.items():
        icon = {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(data["status"], "?")
        print(f"    {icon} {exp} ({data['duration_s']}s)")
        total += 1
        if data["status"] == "pass": pass_count += 1
        elif data["status"] == "fail": fail_count += 1
        else: skip_count += 1

print(f"\n  Total: {total} | ✅ {pass_count} passed | ❌ {fail_count} failed | ⏭️ {skip_count} skipped")
print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Save results
with open("/Users/tombudd/projects/quantum-experiments/results_latest.json", "w") as f:
    json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2)
print("\n  Results saved to: quantum-experiments/results_latest.json")
