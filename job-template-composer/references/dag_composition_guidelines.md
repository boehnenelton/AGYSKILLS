# Reference: JobMaker Task DAG Composition Guidelines

- **Version**: 100
- **Policy Anchor**: Policy §7.2 (Goal-Driven Execution)
- **Author**: Elton Boehnen

---

## 1. The 1-Action-per-Task Law

When decomposing complex projects into JobMaker task rows:
- Every task row must represent a single, verifiable operational action.
- Combine no more than one primary mutating step and its immediate verification test per task.
- Unverifiable goals like "Investigate options" must be formulated as "Scan codebase and output recommendations to dev/options.md".

---

## 2. Context Pipelining Mechanics

1. **`Contextualize_Plan`**: Set to `true` when downstream tasks need visibility of the high-level roadmap to prevent isolated decisions.
2. **`Contextualize_Last`**: Set to `true` when a task strictly consumes the output, file path, or schema of the preceding task.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
