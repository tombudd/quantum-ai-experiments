#!/usr/bin/env python3
"""
Quantum AI experiment smoke runner.

Runs a small simulator-first set of quantum circuits across locally available
providers. Missing optional provider packages are reported as skips.
"""

from __future__ import annotations

import json
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_FILE = RESULTS_DIR / "results_latest.json"

results: dict[str, dict[str, dict[str, object]]] = {}


def record(provider: str, experiment: str, status: str, detail: str = "", duration: float = 0.0) -> None:
    if provider not in results:
        results[provider] = {}
    results[provider][experiment] = {
        "status": status,
        "detail": detail,
        "duration_s": round(duration, 3),
    }
    icon = {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(status, "?")
    print(f"  {icon} [{provider}] {experiment}: {detail[:100]}")


def run_qiskit_suite() -> None:
    print("\n🔷 IBM / Qiskit Aer local simulator")
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit.library import QFT
        from qiskit_aer import AerSimulator
    except ImportError as exc:
        record("IBM/Qiskit", "Suite", "skip", f"missing dependency: {exc}")
        return

    try:
        sim = AerSimulator()

        start = time.time()
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        counts = sim.run(qc, shots=1024).result().get_counts()
        record("IBM/Qiskit", "Bell State", "pass", f"counts={counts}", time.time() - start)

        start = time.time()
        qc = QuantumCircuit(5, 5)
        qc.h(0)
        for i in range(4):
            qc.cx(i, i + 1)
        qc.measure(range(5), range(5))
        counts = sim.run(qc, shots=1024).result().get_counts()
        dominant = max(counts, key=counts.get)
        record("IBM/Qiskit", "GHZ 5-qubit", "pass", f"dominant={dominant} ({counts[dominant]}/1024)", time.time() - start)

        start = time.time()
        qc = QuantumCircuit(4)
        qc.append(QFT(4), range(4))
        qc.measure_all()
        counts = sim.run(qc, shots=512).result().get_counts()
        record("IBM/Qiskit", "QFT 4-qubit", "pass", f"{len(counts)} unique outcomes", time.time() - start)
    except Exception as exc:  # pragma: no cover - provider/runtime specific
        record("IBM/Qiskit", "Suite", "fail", str(exc)[:160])
        traceback.print_exc()


def run_cirq_suite() -> None:
    print("\n🔶 Google Cirq local simulator")
    try:
        import cirq
    except ImportError as exc:
        record("Google Cirq", "Suite", "skip", f"missing dependency: {exc}")
        return

    try:
        start = time.time()
        q0, q1 = cirq.LineQubit.range(2)
        circuit = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="result")])
        sim = cirq.Simulator()
        result = sim.run(circuit, repetitions=1024)
        record("Google Cirq", "Bell State", "pass", f"shape={result.measurements['result'].shape}", time.time() - start)

        start = time.time()
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit([
            cirq.H(qubits[0]),
            *[cirq.CNOT(qubits[i], qubits[i + 1]) for i in range(4)],
            cirq.measure(*qubits, key="ghz"),
        ])
        sim.run(circuit, repetitions=1024)
        record("Google Cirq", "GHZ 5-qubit", "pass", "1024 shots completed", time.time() - start)
    except Exception as exc:  # pragma: no cover - provider/runtime specific
        record("Google Cirq", "Suite", "fail", str(exc)[:160])
        traceback.print_exc()


def run_pennylane_suite() -> None:
    print("\n🟣 PennyLane default.qubit local simulator")
    try:
        import numpy as np
        import pennylane as qml
    except ImportError as exc:
        record("PennyLane", "Suite", "skip", f"missing dependency: {exc}")
        return

    try:
        start = time.time()
        dev = qml.device("default.qubit", wires=2)

        @qml.qnode(dev)
        def bell():
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            return qml.probs(wires=[0, 1])

        probs = bell()
        record("PennyLane", "Bell State", "pass", f"|00⟩={probs[0]:.3f} |11⟩={probs[3]:.3f}", time.time() - start)

        start = time.time()
        dev4 = qml.device("default.qubit", wires=4)

        @qml.qnode(dev4)
        def variational(params):
            for i in range(4):
                qml.RY(params[i], wires=i)
            for i in range(3):
                qml.CNOT(wires=[i, i + 1])
            return qml.expval(qml.PauliZ(0))

        params = np.array([0.1, 0.5, 1.2, 0.8])
        value = variational(params)
        record("PennyLane", "Variational QML Circuit", "pass", f"⟨Z₀⟩={value:.4f}", time.time() - start)
    except Exception as exc:  # pragma: no cover - provider/runtime specific
        record("PennyLane", "Suite", "fail", str(exc)[:160])
        traceback.print_exc()


def main() -> None:
    print("\nQuantum AI Experiment Smoke Suite")
    print("=" * 60)
    run_qiskit_suite()
    run_cirq_suite()
    run_pennylane_suite()

    total = pass_count = fail_count = skip_count = 0
    print("\n" + "=" * 60)
    print("📊 EXPERIMENT SUMMARY")
    print("=" * 60)
    for provider, experiments in results.items():
        print(f"\n  {provider}:")
        for experiment, data in experiments.items():
            status = str(data["status"])
            icon = {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(status, "?")
            print(f"    {icon} {experiment} ({data['duration_s']}s)")
            total += 1
            pass_count += status == "pass"
            fail_count += status == "fail"
            skip_count += status == "skip"

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {"total": total, "pass": pass_count, "fail": fail_count, "skip": skip_count},
        "results": results,
    }
    RESULTS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nResults saved to: {RESULTS_FILE.relative_to(Path(__file__).resolve().parent)}")


if __name__ == "__main__":
    main()
