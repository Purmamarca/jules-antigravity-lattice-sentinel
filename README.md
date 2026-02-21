# Jules Antigravity Lattice Sentinel

An AI-native repository designed with the **AI as an Amplifier** philosophy. This system manages atomic deployments of lattice nodes with high integrity, built through strict Test-Driven Development (TDD) and architectural observability.

---

## 🚀 Core Philosophy: AI as an Amplifier

This project is built on the belief that AI tools do not replace developer judgment but **amplify** it.

### 1. Criteria over Speed

When code is written at AI-speed, design quality and architectural integrity are often the first victims. We use **TDD** as the necessary framework to maintain control and ensure that speed does not lead to "architectural drift."

### 2. Tests as an Intentional Contract

Writing tests before implementation forces the developer to define the **"intent"**. This acts as a strict contract that the AI-generated implementation must follow, preventing the AI from using its "creative license" to deviate from guidelines.

### 3. Maintaining Domain Integrity

We reject generic patterns (like using dictionaries for business logic). This repository enforces **strict domain models** in `src/domain/models.py`. TDD forces the AI to respect these specific structures rather than defaulting to generic behaviors.

---

## 🏗️ Architectural Framework

The system follows a separation of **Intent** (Orchestrator) and **Effect** (Infrastructure).

### Components:

- **`AntigravityOrchestrator`**: Coordinates the deployment logic using the **Saga Pattern**. Every operation is a "transaction" that must have a corresponding "compensation" (rollback) to ensure atomicity.
- **`LatticeVault`**: The infrastructure layer. It is isolated and can only be touched once architectural criteria (authorization and audit) are met.
- **`JulesAudit`**: The observability service. Every state change attempt, success, or failure is logged with a **'Quantum-Signature'** for full auditability.

### Directory Structure:

```text
src/
├── domain/            # Pure Business Logic & Models (Data Integrity)
│   └── models.py
├── infrastructure/    # Side-Effects & External APIs (Isolation)
│   └── lattice_vault.py
├── services/          # Cross-Cutting Concerns (Observability)
│   └── jules_audit.py
└── orchestrator.py    # Coordination (Saga Pattern)
tests/
└── integration/       # Contract Verification
```

---

## 🛠️ Development Protocol (Red-Green-Refactor)

All development MUST follow the Red-Green-Refactor cycle to ensure long-term velocity and stability.

1.  **🔴 RED (Defining Intent)**:
    - Create a failing test in `tests/integration/` that captures the new requirement or failure scenario.
    - _Why?_ To establish the contract before writing a single line of production logic.
2.  **🟢 GREEN (Implementing Effect)**:
    - Implement the **minimum** amount of code in `src/` to make the test pass.
    - _Why?_ To prevent over-engineering and ensure the AI doesn't add unwanted logic.
3.  **🔵 REFACTOR (Optimizing Structure)**:
    - Clean up the code, improve documentation, and ensure adherence to `.cursorrules`.
    - _Why?_ To maintain architectural health without losing the "Green" state.

---

## 🚦 Getting Started

### Prerequisites

- Python 3.10+
- Dependencies: `pytest`, `pytest-asyncio`

### Installation

```bash
pip install pytest pytest-asyncio
```

### Verification

To verify the system's integrity and audit contracts:

```bash
python -m pytest -v tests/integration/
```

---

## 🛡️ Responsibility Alignment

- **Absolute Separation**: Infrastructure (`LatticeVault`) is never accessed directly without passing through the Audit/Verification layer.
- **Zero Residuals**: Failed deployments must leave the system at the 'Last Known Good Sync' point with no partial data.

---

_Institutionalized by Google Antigravity Sentinel Protocol_
