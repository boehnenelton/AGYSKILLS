# Reference: Redundancy Archetypes & Consolidation Patterns

- **Version**: 100
- **Policy Anchor**: Policy §1.3 (Code Cleanup), Policy §6.1 (Heritage Naming)
- **Author**: Elton Boehnen

---

## 1. Redundancy Archetypes

In growing codebases and agent ecosystems, redundant logic emerges across three main vectors:

### 1. Code Duplication Archetypes
- **Type 1 (Exact AST Duplication)**: Exact identical code blocks copied across separate script files.
- **Type 2 (Parametric Clones)**: Logic that differs only in variable names, hardcoded paths, or magic numbers.
- **Type 3 (Inlined Library Logic)**: Primitives (like field map caching or sanitization) re-implemented locally instead of importing canonical `$ADMIN_LIBRARIES`.

### 2. Skill Trigger Collisions
- When two skills share identical positive trigger tokens (e.g., "validate bejson") without mutual negative constraints, routing becomes non-deterministic.
- **Jaccard Threshold**: Overlap $\ge 0.55$ warrants consolidation or asymmetric negative constraint disambiguation.

### 3. Storage & Schema Duplication
- Storing identical denormalized relational data across multiple tables or files without foreign-key pointers.

---

## 2. Consolidation Strategy Matrix

| Redundancy Type | Primary Pattern | Target Location | Migration Risk |
| :--- | :--- | :--- | :--- |
| **Exact Function Clone** | Extract to Shared Module | `lib/` or `$ADMIN_LIBRARIES` | Low |
| **Parametric Clone** | Parameterized Function Extraction | `lib/common.py` | Medium |
| **Trigger Collision** | Asymmetric Negative Triggers | `SKILL.md` frontmatter | Zero |
| **Duplicate Schema** | Normalization with `_fk` UUIDs | `schema_registry.104a.bejson` | Medium |

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
