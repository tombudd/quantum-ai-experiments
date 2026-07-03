# Status and Claim Boundaries

This repository is a public educational research sandbox.

## Current Status

```text
REPO_STATUS: PUBLIC_RESEARCH_SANDBOX
PRIVATE_RUNTIME_CONNECTION: NOT_PRESENT
PRODUCTION_RUNTIME_CONNECTION: NOT_PRESENT
AUTONOMOUS_AGENT_CONNECTION: NOT_PRESENT
QUANTUM_ADVANTAGE_CLAIM: NOT_MADE
NEW_PHYSICS_CLAIM: NOT_MADE
```

## Verified Boundaries

The safe public claim is:

```text
This repo contains small quantum/AI experiment examples and simulator-first probes for learning, portfolio review, and method demonstration.
```

The repo should not be described as:

- a production system
- a live autonomous runtime
- a private architecture release
- proof of quantum advantage
- proof of new physics
- a connected component of any private platform

## Activity State

This repo is live on GitHub, but it should be treated as a research sandbox rather than an actively maintained production package unless new commits, issues, tests, or releases establish otherwise.

## Public Hardening Notes

The public-hardening pass does four things:

1. Removes project-specific private wording from public-facing files.
2. Fixes the README/license mismatch by standardizing on Apache 2.0.
3. Makes the smoke runner write results to a repository-relative path.
4. Adds explicit claim boundaries so reviewers know what is and is not being asserted.

## Future Clean-Room Additions

Good next additions:

- `tests/` for the smoke runner
- GitHub Actions CI
- small notebook-free examples
- verified simulator result snapshots
- rewritten public-safe experiment modules
- a methods note explaining controls, p-values, and limitations
