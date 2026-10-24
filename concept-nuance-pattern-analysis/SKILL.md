---
name: concept-nuance-pattern-analysis
description: >-
  Analyze and dissect subtle conceptual nuances, latent structural invariants, micro-patterns, mechanical couplings, edge-case failure modes, and architectural tradeoffs within specifications, templates, codebases, or system designs into structured markdown reports and BEJSON 104a nuance registries. Use when inspecting the deep nuances, hidden constraints, why-it-works mechanics, or micro-pattern interactions of a concept or design specification. Do NOT use for extracting raw seed ideas or harvesting broad concept archetypes across unstructured notes (use concept-idea-pattern-extraction), designing snake_case identifier prefixes (use code-taxonomy-architect), modeling entity primary/foreign keys (use component-taxonomy-architect), or enforcing BE HTML CSS tokens (use behtml-design-preferences).
---

# Skill: `concept-nuance-pattern-analysis` (Layer 5 - Concept Nuance & Pattern Analysis)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (L3_Use_Cases_Cross_Layer_Blueprinting)`
- **Domain**: `concepts / concept (Conceptual Intelligence & Pattern Decomposition)`
- **Write-Owned Entity**: `ConceptNuancePattern` (`data/concept_nuance_patterns.104a.bejson`)
- **Primary Output Subdirectory**: `target/ideas/concept_nuance_analysis_<slug>.md`
- **Date Created**: `2026-10-18`
- **RELATIONAL_ID**: `9d4a2e18-6c3b-4f71-8a20-5b9e1d4c7f02`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`concept-nuance-pattern-analysis` operates at **Layer 5** within the `concepts` (`concept-*`) domain. Whereas surface summaries only restate what an artifact does, this skill performs a forensic 6-axis dissection of **why** every micro-decision, boundary constraint, implicit coupling, and structural nuance exists, what breaks if it is altered, and how its underlying micro-patterns can be formalized as deterministic invariants.

---

## 2. The 6-Axis Concept Nuance & Pattern Inspection Matrix

Every analysis executed by `concept-nuance-pattern-analysis` evaluates the target concept, specification, or artifact across six mandatory axes:

| Axis | Inspection Dimension | Core Analytical Question | Required Deliverable Elements |
| :--- | :--- | :--- | :--- |
| **Axis 1** | **Surface vs. Latent Invariants** | What hidden constraint is silently enforced by an seemingly minor detail? | Explicit rule vs. latent structural role (e.g., why a `3px solid transparent` border exists solely to optically align text with an adjacent `3px solid #DE2626` heading). |
| **Axis 2** | **Causal & Mechanical Coupling** | Which parameters are mathematically or mechanically locked together? | Dependency pairs/triads ($A \iff B$) showing how mutating parameter $A$ breaks invariant $B$ (e.g., `body { overflow: hidden }` coupled with `calc(17 * var(--ry-unit))` inner canvas scrolling). |
| **Axis 3** | **Quantization & Boundary Precision** | What exact unit, offset, or boundary condition governs the structure? | Exact numeric/ratio locks, tolerance ceilings (`0px` / `0%` drift), and boundary-layer sanitization rules. |
| **Axis 4** | **Failure Modes & Edge Degradation** | Where does the concept or heuristic break down under stress or mutation? | Honest enumeration of false-positive/false-negative triggers, overflow states, or positional drift hazards (`row[i]` vs. `field_map`). |
| **Axis 5** | **Tradeoff & Tension Resolution** | What competing engineering forces does this nuance reconcile? | Explicit statement of Force A vs. Force B and the exact mechanism that resolves both without compromise. |
| **Axis 6** | **Formalizable Micro-Pattern Rule** | How can this nuance be encoded as a deterministic Layer 2 / Layer 4 check? | Normalized `IF [Condition] AND [DomainBoundary] THEN [Requirement] UNLESS [Exception]` rule tuple. |

---

## 3. Canonical BEJSON 104a Schema (`ConceptNuancePattern`)

All nuance pattern records persisted to `data/concept_nuance_patterns.104a.bejson` use the `nuance_` field prefix (Policy 10.2) and resolve column offsets exclusively via `field_map = bejson_core_get_field_map(doc)` (Policy 6.2) after boundary whitespace sanitization (Policy 10.9):

- **0**: `nuance_pattern_uuid` (`string` - Immutable UUIDv4 primary key)
- **1**: `nuance_pattern_code` (`string` - Deterministic code, e.g., `CNP-001`)
- **2**: `nuance_concept_domain` (`string` - Target domain or subsystem)
- **3**: `nuance_surface_element` (`string` - Observable property, token, or construct)
- **4**: `nuance_latent_mechanism` (`string` - Underlying mechanical/causal reason it works)
- **5**: `nuance_coupled_dependencies` (`string` - Coupled parameters or invariants)
- **6**: `nuance_failure_mode` (`string` - Exact failure mode if omitted or altered)
- **7**: `nuance_confidence_tier` (`string` - `locked_invariant` | `strong_heuristic` | `contextual_prior`)
- **8**: `nuance_created_at` (`string` - UTC ISO-8601 timestamp)

```python
def bejson_read_nuance_field(doc: dict, field_map: dict[str, int], row: list, col_name: str):
    clean_col = col_name.strip()
    col_idx = field_map[clean_col]
    val = row[col_idx]
    return val.strip() if isinstance(val, str) else val
```

---

## 4. Step-by-Step Nuance Analysis Workflow

1. **Stage 1 - Artifact & Concept Intake**: Read the target concept, specification, template, or code module and strip conversational fluff to isolate every explicit and implicit parameter.
2. **Stage 2 - 6-Axis Micro-Pattern Dissection**: Map every structural detail across Axes 1-6 (Surface vs. Latent Invariant, Mechanical Coupling, Boundary Precision, Failure Mode, Tradeoff Resolution, Formal Rule). See [`references/concept_nuance_taxonomy.md`](./references/concept_nuance_taxonomy.md).
3. **Stage 3 - Deliverable Compilation & Verification**:
   - Write the structured Markdown report to `target/ideas/concept_nuance_analysis_<slug>.md`.
   - Validate or append structured records to `data/concept_nuance_patterns.104a.bejson` using `scripts/analyze_concept_nuances.py`:
     ```bash
     python3 scripts/analyze_concept_nuances.py "assets/template_concept_nuance_patterns.104a.bejson"
     agy --sandbox -p "Execute concept-nuance-pattern-analysis verification gate and return deterministic JSON status."
     ```

---

## When NOT to Use

- **Extracting raw seed ideas, brainstorming feature archetypes, or harvesting broad concept patterns across unstructured sources**: Redirect immediately to `concept-idea-pattern-extraction`.
- **Designing snake_case entity field prefixes and library family function names**: Redirect immediately to `code-taxonomy-architect`.
- **Modeling UUID primary keys, `_fk` foreign keys, and Write-Owner modules**: Redirect immediately to `component-taxonomy-architect`.
- **Enforcing or auditing BE HTML 16-sublane / Ry=32px CSS design preferences**: Redirect immediately to `behtml-design-preferences`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
