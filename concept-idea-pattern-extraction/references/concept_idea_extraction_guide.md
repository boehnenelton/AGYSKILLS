# Concept & Idea Pattern Extraction: Archetype Catalog & Reference Guide

> **Parent Skill:** `concept-idea-pattern-extraction` (Layer 5 - `concepts` Domain)  
> **Version:** 100 | **Release_Version:** 300 | **RELATIONAL_ID:** `6e2a9d15-4c8b-4f03-9a72-1d5c3b8e0f49`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. The Five Canonical Concept & Idea Pattern Families

When harvesting concepts and ideas from raw user prompts, transcripts, or existing codebases, classify each extracted pattern into one of five archetype families:

| Family Token | Pattern Family | Core Extraction Focus | Downstream Target Skill Tier |
| :--- | :--- | :--- | :--- |
| **`data_substrate`** | **Substrate & Schema Patterns** | Tabular indexing (`field_map`), atomic file writes (`.tmp` -> `fsync` -> `replace`), UUIDv4 primary/foreign keys, boundary sanitization. | Layer 1 (`bejson-104-core`, `bejson-105-core`) & Layer 5 (`component-taxonomy-architect`) |
| **`heuristic_proxy`** | **Cheap-Signal Heuristic Proxies** | Fast, low-cost observable signals (headers, digests, byte offsets, structural markers) that approximate expensive ground-truth checks, paired with honest failure modes. | Layer 2 (`-validator`, `-auditor`) |
| **`workflow_pipeline`** | **Automation & Pipeline Patterns** | Sandboxed CLI dispatch (`agy --sandbox`), advisory locking (`fcntl.flock`), turn-gated planning (`N = K + 1`), sequential task runners. | Layer 3 (`-automator`, `-manager`) & Layer 6 (`skill-chain-coordinator`) |
| **`spatial_ui`** | **Spatial Grid & Visual Motifs** | 16-sublane (`6.25%`) / 8-lane (`12.5%`) grids, `Ry = 32px` vertical quantization, seamless transparent borders, Policy 8.1 Tri-Color (`#FFFFFF`, `#000000`, `#DE2626`). | Layer 4 (`behtml-design-preferences`, `behtml-templates`, `behtml-104-builder`) |
| **`governance_guardrail`** | **Set-Theoretic Routing & Governance** | 3-level mutual negative constraint triggers ($A(S_i) \cap A(S_j) = \emptyset$), progressive disclosure ceilings, layer downward dependency laws. | Layer 6 (`skill-architect`, `skill-ecosystem-cartographer`) |

---

## 2. Standard Pattern Card Markdown Template (`target/ideas/concept_idea_patterns_<slug>.md`)

```markdown
# Extracted Concept & Idea Pattern Catalog: [Source / Domain Title]

> **Extraction ID:** `CIP-CATALOG-YYYYMMDD`  
> **Skill:** `concept-idea-pattern-extraction` (Layer 5)  
> **Total Extracted Patterns:** N

## Pattern Card `CIP-001`: [Pattern Name]
- **Archetype Family:** `[data_substrate | heuristic_proxy | workflow_pipeline | spatial_ui | governance_guardrail]`
- **Core Problem Solved:** [What friction or failure mode this idea eliminates]
- **Mechanical Signature:** [How the pattern works step-by-step]
- **When to Apply (Positive Trigger):** [Explicit conditions where this pattern excels]
- **Anti-Patterns Blocked:** [What common mistakes or regressions it prevents]
- **Downstream Layer Hand-Off:** `Layer [1-6]` -> `[Target Skill Name]`
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
