# Public Release Standard

This repository should meet a high-trust public release bar before it is treated as portfolio-ready.

The internal goal is maximum credibility without exposing private systems. Publicly, that means every artifact should be reproducible, bounded, redacted, and evidence-first.

## Release Criteria

A public artifact should satisfy all of the following:

1. **Clear scope** — the artifact states what it does and what it does not prove.
2. **Reproducible path** — a reviewer can run or inspect the artifact without private access.
3. **Synthetic or public data only** — no private logs, receipts, prompts, schemas, or operational details.
4. **Evidence before claims** — claims are supported by code, examples, reports, or explicit methodology.
5. **Limitations included** — quantum, inference, and AI relevance limits are explicit.
6. **Redaction boundary preserved** — no proprietary architecture, internal labels, private codenames, or production traces.
7. **Security checked** — no secrets, credentials, tokens, provider account metadata, or personal data.
8. **Independent-review friendly** — a skeptical reviewer can reproduce or understand the experiment without private context.

## Minimum Artifact Checklist

Before an artifact is promoted as public portfolio material, it should include:

- `README.md` section describing purpose, scope, and limitations
- Reproducible simulator-first example or clearly marked roadmap status
- Synthetic input fixture, if data is needed
- Expected output or sample report, if evaluation is involved
- Backend/simulator details
- Shot count, seed, and optimizer settings where applicable
- Classical baseline where applicable
- Clear license
- Redaction review
- Security review

## Claim Discipline

Avoid claims such as:

- "quantum advantage" without strong independent evidence
- "verified speedup" without reproducible benchmarking
- "production-ready"
- "AGI-relevant"
- "proves active inference on hardware" without careful qualification

Prefer claims such as:

- "demonstrates a toy variational experiment"
- "provides a simulator-first research sketch"
- "shows a reproducible example under bounded assumptions"
- "compares a small quantum circuit to a classical toy baseline"

## Promotion Rule

Documentation-only artifacts are acceptable as public methodology, but they should not be described as implemented experiments until executable files, fixtures, and sample outputs exist.

Runnable artifacts should include tests where practical.

## Public Boundary

The public repository is not the private system. It is a safe demonstration layer.

When a private method is useful, publish only the clean-room abstraction, toy example, or synthetic experiment.