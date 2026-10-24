---
name: definitions-cartographer
description: >-
  Index, query, resolve, and audit canonical ecosystem terminology, inline concept definitions (Policy §5.1), acronyms, and semantic speech-to-text aliases using definitions_lookup.py and definitions_registry.104a.bejson. Use when resolving ambiguous terms, colloquialisms, speech-to-text mishears, or retrieving canonical definitions and policy contracts for concepts across BEHTML, BEJSON, and tooling. Do NOT use for indexing executable skill manifests and execution DAGs (use skill-ecosystem-cartographer), modeling database entity primary/foreign keys (use component-taxonomy-architect), designing variable identifier prefixes (use code-taxonomy-architect), or enforcing zero-filler templates (use template-literal-skeleton).
---

# Skill: `definitions-cartographer` (Layer 6 - Ecosystem Definitions & Semantic Cartography)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 6 (L5_Composition_Root)`
- **Era & Library Binding**: `Universal (Foundational & Integrity Eras, Policy §5.1, §12.4)`
- **Reference Specification**: `references/definitions_cartography_spec.md`
- **Data Registry**: `data/definitions_registry.104a.bejson`
- **CLI / Query Tool**: `scripts/definitions_lookup.py`
- **Date Created**: `2026-10-19`
- **RELATIONAL_ID**: `b3e8194a-5c2d-4e91-87a3-1f6d0b92e854`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Core Mandate & Purpose

`definitions-cartographer` serves as the authoritative semantic index and concept cartographer across the ecosystem. It acts as the conceptual counterpart to `skill-ecosystem-cartographer`:
- While `skill-ecosystem-cartographer` catalogs **code artifacts, skill manifests, and execution layers**,
- `definitions-cartographer` catalogs **vocabulary, definitions, acronyms, semantic aliases, and speech-to-text mishears**.

### Core Capabilities:
1. **Semantic Aliasing & Speech-to-Text Bridging**:
   Maps colloquialisms, typos, and voice-to-text mishears (e.g. `certographer` $\rightarrow$ `Cartographer`, `shelf doc` $\rightarrow$ `Template_Document_With_Shelf.html`, `pollock` $\rightarrow$ `Policy`) to canonical system identifiers.
2. **Policy §5.1 Inline Definition Compliance**:
   Provides instant $O(1)$ lookup for exact, one-sentence inline definitions of technical terms required on first use.
3. **Deliverable Taxonomy Normalization**:
   Guarantees strict distinction between `Template`, `Example`, `Demonstration`, and `Reference` per Policy §12.4.

---

## 2. Querying & CLI Usage

Query terms using [`scripts/definitions_lookup.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/definitions-cartographer/scripts/definitions_lookup.py):

### 2.1 Substring & Alias Lookup
```bash
# Query by keyword or speech-to-text alias:
python3 scripts/definitions_lookup.py --query "certographer"
```

### 2.2 Exact Canonical Term Lookup
```bash
# Query exact canonical concept:
python3 scripts/definitions_lookup.py --term "Ry"
```

### 2.3 Filter by Domain Category
```bash
# Filter by category (Deliverable_Types, BEHTML, BEJSON, Policy, Architecture, UI_Branding):
python3 scripts/definitions_lookup.py --category Deliverable_Types
```

### 2.4 Inline Format (for Direct Insertion)
```bash
# Emits concise 'Term: Definition' format for inline documentation:
python3 scripts/definitions_lookup.py --term "Field Map Cache" --format inline
```

---

## 3. Registered Domain Categories

1. **`Deliverable_Types`**: Canonical four-pillar taxonomy (`Template`, `Example`, `Demonstration`, `Reference`) per Policy §12.4.
2. **`BEHTML`**: Spatial mathematics ($R_y = 32\text{px}$, 8-lane / 16-wide grid geometry, Z-plane occlusion, viewport locking).
3. **`BEJSON`**: Data integrity invariants (`Field Map Cache`, `ResilientPIDLock`, `Format 104`, `Format 105`).
4. **`Policy`**: Absolute governance rules (`Zero-Filler Skeleton Law`, negative constraints, author crediting).
5. **`UI_Branding`**: Aesthetic visual contracts (`Tri-Color Palette` `#FFFFFF`/`#000000`/`#DE2626`, cubic imagery).
6. **`Architecture`**: System roles (`Owning Writer`, `Cartographer`, `Layered Architecture`).

---

## 4. Boundary Rules & Negative Guardrails

- **Do NOT** index skill manifests or execution DAGs $\rightarrow$ Use [`skill-ecosystem-cartographer`](file:///data/data/com.termux/files/home/.gemini/config/skills/skill-ecosystem-cartographer/SKILL.md).
- **Do NOT** model entity relational graphs, PKs, or foreign keys $\rightarrow$ Use [`component-taxonomy-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/component-taxonomy-architect/SKILL.md).
- **Do NOT** design field prefixes or module signatures $\rightarrow$ Use [`code-taxonomy-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/code-taxonomy-architect/SKILL.md).
- **Do NOT** enforce zero-filler template structures $\rightarrow$ Use [`template-literal-skeleton`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-literal-skeleton/SKILL.md).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
