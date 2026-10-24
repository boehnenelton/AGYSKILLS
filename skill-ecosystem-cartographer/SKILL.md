---
name: skill-ecosystem-cartographer
description: >-
  Catalog installed Antigravity CLI (agy) skills across workspace, global, and
  plugin directories, map layer routing topologies, register input/output
  functional boundaries into skill_registry_catalog.104a.bejson, and prevent
  semantic trigger collisions via pairwise negative guardrail auditing. Use when
  indexing installed skills, generating ecosystem routing maps, verifying mutual
  negative constraint symmetry, or detecting trigger overlaps across L1-L6 skills.
  Do NOT use for scaffolding or authoring new skill files (use skill-architect),
  executing runtime multi-skill DAG workflows (use skill-chain-coordinator),
  composing pipeline recipe markdowns (use skill-chain-recipe-composer),
  indexing ecosystem terminology and concept definitions (use definitions-cartographer), or
  auditing general non-skill policy documents (use policy-conflict-auditor).
---

# skill-ecosystem-cartographer (Layer 6 Ecosystem Topology & Collision Auditor)

## Summary

`skill-ecosystem-cartographer` is the authoritative Layer 6 registry manager and topological auditor for the Antigravity skill ecosystem. It serves as the exclusive Write-Owner of `data/skill_registry_catalog.104a.bejson`, ensuring every installed skill occupies a well-defined tier (`L1-L6`), obeys downward dependency laws, and maintains pairwise disjoint activation boundaries ($A(S_i) \cap A(S_j) = \emptyset$).

## When to Use

- Scanning workspace (`.agents/skills/`), global (`~/.gemini/antigravity-cli/skills/`), and plugin directories to build or refresh `data/skill_registry_catalog.104a.bejson`.
- Auditing a newly scaffolded or updated skill for semantic trigger collisions (`Code 431`), asymmetric negative guardrails (`Code 432`), or dangling sibling pointers (`Code 433`).
- Generating visual Mermaid routing topologies and layer dependency matrices across all installed skills.
- Resolving shadowed skills across Antigravity's 5-level loading precedence hierarchy.

## When NOT to Use

- Do NOT use for designing, scaffolding, or linting an individual `SKILL.md` file (use `skill-architect`).
- Do NOT use for executing multi-skill DAG pipelines, spawning stage subagents, or enforcing runtime stage gates (use `skill-chain-coordinator`).
- Do NOT use for scheduling $N = K + 1$ multi-turn conversational pre-planning delays (use `planning-schema-planner`).
- Do NOT use for extracting atomic rules from general prose policy documents outside skill registries (use `policy-conflict-auditor`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer 6 (`L6: Root Orchestration & Meta-Governance`)
- **Codebase Layer Mapping**: `L5_Composition_Root`
- **Exclusive Write-Owner Of**: `data/skill_registry_catalog.104a.bejson` (`SkillCatalogEntry` entity) and `reports/audits/topology_collision_matrix.md`
- **Allowed Downward Dependencies**: `bejson-104-core` (L1), `bejson-104-validator` (L2), `policy-conflict-auditor` (L2)
- **Sandbox Policy**: All `agy` CLI invocations MUST include `--sandbox`.
- **BEJSON Access Policy**: All `.bejson` reads and mutations MUST resolve column indices dynamically via `field_map`.

---

## 2. Step-by-Step Cartography & Collision Prevention Workflow

### Step 1: Multi-Surface Skill Discovery & Indexing
Execute the black-box cartographer script to scan installed skill directories, sanitize frontmatter strings at the boundary layer, compute SHA-256 digests, and persist `data/skill_registry_catalog.104a.bejson`:

```bash
python3 scripts/cartographer_index.py \
  --scan-root "/storage/emulated/0/Documents/AGY/skills" \
  --catalog "/storage/emulated/0/Documents/AGY/data/skill_registry_catalog.104a.bejson" \
  --report "/storage/emulated/0/Documents/AGY/reports/audits/topology_collision_matrix.md"
```

### Step 2: Pairwise Trigger Collision & Guardrail Verification
The indexer automatically evaluates Codes `430-433`:
- **`Code 430 (E_CARTOGRAPHER_DUPLICATE_SKILL)`**: Rejects duplicate canonical names within the same discovery scope.
- **`Code 431 (E_CARTOGRAPHER_TRIGGER_COLLISION)`**: Detects overlapping positive triggers ($J(T^+(S_i), T^+(S_j)) \ge 0.25$) lacking mutual negative redirections.
- **`Code 432 (E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL)`**: Flags non-reciprocal sibling exclusions within the same domain cluster.
- **`Code 433 (E_CARTOGRAPHER_DANGLING_SIBLING_REF)`**: Identifies `(use <sibling>)` pointers referencing unregistered skills.

### Step 3: Gate Verification
- Verify `Exit Code 0` and inspect `reports/audits/topology_collision_matrix.md` before authorizing `skill-chain-coordinator` to execute any multi-skill DAG.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
