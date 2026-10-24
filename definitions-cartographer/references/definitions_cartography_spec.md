# Specification: Definitions Cartography Architecture

> **Parent Skill:** `definitions-cartographer` (Layer 6)  
> **Schema Binding:** BEJSON 104a `Ecosystem_Definitions_Cartography`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026  
> **RELATIONAL_ID:** `1c4d9a20-8e7b-4395-bf3a-9e120f83dc47`

---

## 1. Purpose & Mandate

`definitions-cartographer` maintains the canonical vocabulary, acronym, semantic alias, and inline definition registry across the ecosystem. It fulfills two core mandates:
1. **Semantic Normalization**: Resolves natural language colloquialisms, voice-to-text / speech mishears (e.g. `certographer` $\rightarrow$ `Cartographer`, `shelf doc` $\rightarrow$ `Template_Document_With_Shelf.html`), and technical acronyms.
2. **Policy §5.1 Inline Definitions**: Provides authoritative, one-sentence definitions of technical terms to satisfy the mandate to *"Define technical terms inline on first use"*.

---

## 2. Schema Specification

The underlying database resides at `data/definitions_registry.104a.bejson` using the `Ecosystem_Definitions_Cartography` schema:

| Field Name | Type | Description | Invariant Constraint |
| :--- | :--- | :--- | :--- |
| `term_uuid` | `string` | Unique deterministic identifier | Immutable UUID/slug |
| `canonical_term` | `string` | Formal system name of the concept | PascalCase or UpperCase |
| `domain_category` | `string` | Domain classification | `Deliverable_Types`, `BEHTML`, `BEJSON`, `Policy`, `Architecture`, `UI_Branding`, `Tooling` |
| `inline_definition` | `string` | Single-sentence definition for Policy §5.1 inline use | Max 160 characters |
| `technical_contract_summary` | `string` | Core technical invariant or contract | Specific rule or bound |
| `synonyms_aliases_csv` | `string` | Comma-separated colloquialisms, mishears, and aliases | Lowercase CSV |
| `canonical_reference_pointer` | `string` | Relative path to authoritative specification | Valid file path |
| `policy_binding` | `string` | Applicable policy section | e.g. `Policy §12.4`, `Policy §8.1` |

---

## 3. Boundary Rules & Non-Overlaps

- **Skill Manifests**: Delegated to `skill-ecosystem-cartographer`.
- **Database Schema Modeling**: Delegated to `component-taxonomy-architect`.
- **Code Identifiers & Naming**: Delegated to `code-taxonomy-architect`.
- **Zero-Filler Template Enforcement**: Delegated to `template-literal-skeleton`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
