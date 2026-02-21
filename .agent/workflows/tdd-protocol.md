---
description: Red-Green-Refactor Mandate for Antigravity Sentinel
---

# TDD PROTOCOL: RED-GREEN-REFACTOR

Follow these steps to maintain architectural integrity and long-term velocity.

## 1. PHASES

### RED: The Intent

1. Identify the new behavior or failure scenario.
2. Create a file in `tests/integration/` (e.g., `test_new_feature.py`).
3. Define the `quantum_signature` and `node_ids` required.
4. Run `python -m pytest tests/integration/test_new_feature.py`.
5. **CRITICAL**: The test must fail. If it passes, your test is either redundant or incorrect.

### GREEN: The Minimum Effect

1. Open the relevant file in `src/`.
2. Implement the **MINIMUM** code required to satisfy the failing assertion.
3. Avoid generic patterns. Use `src/domain/models.py`.
4. Ensure every state change is reported to `JulesAudit`.
5. Run tests. Verify they pass.

### REFACTOR: The Cleanup

1. Review the logic for "Creative License" drift.
2. Ensure the Saga Pattern (rollbacks) handles the new logic.
3. Remove code duplication or improve variable names.
4. Verify tests stay Green.

## 2. WHEN NOT TO USE TDD

- Do NOT use TDD for simple `README.md` updates.
- Do NOT use TDD for "one-off" exploration scripts (spikes) that will not be merged into `src/`.

## 3. RESPONSIBILITY ALIGNMENT

- Never bypass the `JulesAudit` verification.
- Vault effects should only happen _after_ successful audit/auth verification.
