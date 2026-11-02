# Reference: JobMaker BEJSON 104a Specification & Field Invariants

- **Version**: 100
- **Policy Anchor**: Policy §6.2 (BEJSON Core Mandate)
- **Author**: Elton Boehnen

---

## 1. Top-Level Envelope Fields

Every JobMaker BEJSON 104a document requires the following top-level metadata:

| Field Name | Type | Allowed / Required Values |
| :--- | :--- | :--- |
| `Format` | string | `"BEJSON"` |
| `Format_Version` | string | `"104a"` |
| `Format_Creator` | string | `"Elton Boehnen"` |
| `Schema_Name` | string | `"Job Schema"` |
| `Schema_Version` | string | `"1.0"` |
| `Records_Type` | array | `["JobTask"]` |
| `Job_Goal` | string | Freeform descriptive goal statement |
| `Job_Type` | string | Primary classification (`coding`, `writing`, `audit`, etc.) |
| `Contextualize_Plan` | boolean | `true` or `false` |
| `Contextualize_Last` | boolean | `true` or `false` |
| `Job_Complete` | boolean | Evaluates true only when all mandatory tasks are complete |

---

## 2. The 11 Canonical Task Fields (`_JOB_FIELDS`)

In the `Fields` array, the schema defines:

1. `task_id` (string): Synthetic UUID string.
2. `task_order` (integer): Sequential 1-indexed order (`1..N`).
3. `task_title` (string): Short descriptive title.
4. `task_description` (string): Actionable instructions.
5. `task_context` (string): Embedded prior context or inputs.
6. `task_reference` (string): File path references or pointers.
7. `task_mandatory` (boolean): Whether task is required to complete job.
8. `is_completed` (boolean): Task execution state.
9. `audit_enabled` (boolean): Whether audit verification is required.
10. `audit_passed` (boolean/null): Audit result.
11. `audit_fail_reason` (string): Reason if audit fails.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
