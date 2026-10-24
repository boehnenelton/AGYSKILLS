---
name: concept-idea-pattern-extraction
description: >-
  Extract, distill, cluster, and normalize raw concepts, seed ideas, heuristic proxy signals, recurring design archetypes, and reusable system patterns from unstructured notes, transcripts, documents, or existing codebases into structured markdown catalogs and BEJSON 104a pattern registries. Use when harvesting ideas, extracting concept patterns, identifying reusable architectural motifs, or turning raw brainstorming into structured pattern cards. Do NOT use for deep forensic inspection of subtle nuances and mechanical couplings inside a single locked specification (use concept-nuance-pattern-analysis), Turn 1 BEJSON 104 vs 105 schema allocation planning (use planning-schema-planner), designing snake_case identifier prefixes (use code-taxonomy-architect), or parameterizing {{VAR:-default}} slots (use prompt-placeholder-composer).
---

# Skill: `concept-idea-pattern-extraction` (Layer 5 - Concept & Idea Pattern Extraction)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (L3_Use_Cases_Cross_Layer_Blueprinting)`
- **Domain**: `concepts / concept (Conceptual Intelligence & Pattern Extraction)`
- **Write-Owned Entity**: `ConceptIdeaPattern` (`data/concept_idea_patterns.104a.bejson`)
- **Primary Output Subdirectory**: `target/ideas/concept_idea_patterns_<slug>.md`
- **Date Created**: `2026-10-18`
- **RELATIONAL_ID**: `4f8e1c92-7a3b-4d50-9b14-6e2c8a0d5f31`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`concept-idea-pattern-extraction` operates at **Layer 5** within the `concepts` (`concept-*`) domain. It takes unstructured, noisy, or multi-source inputs (voice/speech-to-text transcripts, brainstorm notes, project archives, or multi-file repositories) and extracts every distinct **Concept Archetype**, **Seed Idea**, **Cheap-Signal Heuristic Proxy**, and **Reusable System Pattern** into a normalized, implementation-ready catalog.

---

## 2. The 5-Stage Concept & Idea Pattern Extraction Pipeline

| Stage | Pipeline Phase | Core Extraction Operation | Output Artifact / Structure |
| :--- | :--- | :--- | :--- |
| **Stage 1** | **Signal Harvesting & Context Decoding** | Decode speech-to-text mishears (Policy 5.1), strip conversational noise, and isolate every atomic idea or conceptual primitive. | Sanitized list of atomic concept candidates. |
| **Stage 2** | **Archetype & Family Clustering** | Group related ideas into canonical pattern families (*Spatial Grid Patterns*, *Persistence & Indexing Patterns*, *Heuristic Signal Proxies*, *Governance & Guardrail Patterns*, *Workflow Automation Patterns*). | Clustered concept taxonomy tree. |
| **Stage 3** | **Canonical Pattern Card Compilation** | For each extracted idea/pattern, define its problem statement, mechanical signature, trigger condition, anti-patterns blocked, and target architectural layer (`L1` through `L6`). | Standardized Pattern Cards (see [`references/concept_idea_extraction_guide.md`](./references/concept_idea_extraction_guide.md)). |
| **Stage 4** | **Cross-Domain Transferability Mapping** | Identify how each extracted pattern generalizes from its origin context to greenfield projects or sibling domains. | Isomorphic transfer matrix. |
| **Stage 5** | **Dual Deliverable Persistence** | Emit the Markdown catalog (`target/ideas/concept_idea_patterns_<slug>.md`) and atomic BEJSON 104a registry (`data/concept_idea_patterns.104a.bejson`). | Verified `.md` + `.104a.bejson` (`Exit Code 0`). |

---

## 3. Canonical BEJSON 104a Schema (`ConceptIdeaPattern`)

All extracted concept and idea pattern records persisted to `data/concept_idea_patterns.104a.bejson` use the `idea_` field prefix (Policy 10.2) and resolve column offsets exclusively via `field_map = bejson_core_get_field_map(doc)` (Policy 6.2) with boundary whitespace sanitization (Policy 10.9):

- **0**: `idea_pattern_uuid` (`string` - Immutable UUIDv4 primary key)
- **1**: `idea_pattern_code` (`string` - Deterministic identifier, e.g., `CIP-001`)
- **2**: `idea_pattern_name` (`string` - Concise canonical name of the concept/idea pattern)
- **3**: `idea_archetype_family` (`string` - Pattern cluster: `spatial_ui`, `data_substrate`, `heuristic_proxy`, `governance_guardrail`, `workflow_pipeline`)
- **4**: `idea_problem_solved` (`string` - Core friction, bottleneck, or failure mode solved)
- **5**: `idea_mechanism_signature` (`string` - How the idea/pattern operates mechanically)
- **6**: `idea_trigger_when` (`string` - Explicit condition when this pattern should be applied)
- **7**: `idea_anti_pattern_blocked` (`string` - Anti-pattern or mistake prevented by this idea)
- **8**: `idea_target_layer_tier` (`integer` - Target 6-tier layer `1` through `6` for downstream execution)
- **9**: `idea_created_at` (`string` - UTC ISO-8601 timestamp)

```python
def bejson_read_idea_field(doc: dict, field_map: dict[str, int], row: list, col_name: str):
    clean_col = col_name.strip()
    col_idx = field_map[clean_col]
    val = row[col_idx]
    return val.strip() if isinstance(val, str) else val
```

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

Validate extracted BEJSON 104a pattern registries and enforce `--sandbox` on all headless `agy` runs:

```bash
python3 scripts/extract_concept_idea_patterns.py "assets/template_concept_idea_patterns.104a.bejson"
agy --sandbox -p "Execute concept-idea-pattern-extraction verification gate and return deterministic JSON status."
```

---

## When NOT to Use

- **Performing a deep 6-axis forensic inspection of subtle nuances, latent borders, or coupled parameters inside a single locked specification**: Redirect immediately to `concept-nuance-pattern-analysis`.
- **Executing Turn 1 BEJSON Era (104 vs. 105) schema allocation planning**: Redirect immediately to `planning-schema-planner`.
- **Designing snake_case entity field prefixes and library family function names**: Redirect immediately to `code-taxonomy-architect`.
- **Composing `{{VAR:-default}}` placeholder slot schemas**: Redirect immediately to `prompt-placeholder-composer`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
