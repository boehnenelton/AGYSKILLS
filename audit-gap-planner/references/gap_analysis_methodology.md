# Reference: Structural Gap Analysis Methodology & Capability Matrices

- **Version**: 100
- **Policy Anchor**: Policy §7.1 (Surgical Execution), Policy §3.6 (Tracker Validation)
- **Author**: Elton Boehnen

---

## 1. Capability Matrix Analysis Framework

Structural gap audits evaluate software systems against four rigorous coverage matrices:

### 1. Multi-Language Parity Matrix
When building core platform primitives, all four canonical languages must offer behavioral equivalence:

| Primitive Component | Python (PY) | JavaScript (JS) | TypeScript (TS) | Bash (SH) | Gap Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Core Parser & Deserializer | [x] | [x] | [x] | [x] | Full Parity |
| O(1) Field Map Caching | [x] | [x] | [x] | [x] | Full Parity |
| Format Upgrader (104 -> 105) | [x] | [x] | [ ] | [ ] | Port Gap (TS/SH) |
| Atomic POSIX Replacement | [x] | [x] | [x] | [x] | Full Parity |

### 2. Error Code & Invariant Coverage
Verify that all canonical failure states (E10-E95) are explicitly defined and handled:
- Invariant E30-E38 (MFDB Manifest / Parent hierarchy link)
- Invariant E39 (Referential integrity foreign keys)
- Invariant E90-E95 (105 UUID structure and transition)

### 3. CLI Ergonomics & Operability Matrix
Every production utility script must implement:
- `--help`: Comprehensive usage, flags, and examples.
- `--version`: Solid integer version and release tag.
- `--json`: Structured machine-readable stdout output.
- Deterministic exit codes: 0 (Success), 10 (Path Error), 20 (Env Error), 30 (Domain finding).

---

## 2. Gap Scoring & Prioritization Formula

Gap Severity Score ($S_{gap}$) is calculated as:
$$S_{gap} = W_{impact} \times (1.0 - C_{redundancy})$$

Where:
- $W_{impact}$: Blocker (10.0), High (7.0), Medium (4.0), Low (1.0)
- $C_{redundancy}$: Existing alternative coverage (0.0 if no fallback exists, 0.5 if partial workaround exists)

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
