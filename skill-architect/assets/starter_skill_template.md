---
name: {{SKILL_NAME}}
description: >-
  {{CAPABILITY_SUMMARY}}. Use when {{POSITIVE_TRIGGERS}}. Do NOT use for
  {{NEGATIVE_TRIGGERS_WITH_SIBLINGS}}.
---

# {{SKILL_NAME}} (Layer {{LAYER_NUMBER}} - {{LAYER_TITLE}})

## Summary

{{SUMMARY_PARAGRAPH}}

## When to Use

- {{USE_CASE_1}}
- {{USE_CASE_2}}

## When NOT to Use

- {{EXCLUSION_1}} (use `{{SIBLING_SKILL_1}}`).
- {{EXCLUSION_2}} (use `{{SIBLING_SKILL_2}}`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Tier**: Layer {{LAYER_NUMBER}} (`L{{LAYER_NUMBER}}`)
- **Codebase Layer Alignment**: `{{CODEBASE_LAYER}}`
- **Allowed Downward Dependencies**: {{ALLOWED_DEPENDENCIES}}
- **Input Contract**: `{{INPUT_CONTRACT}}`
- **Output Artifact Contract**: `{{OUTPUT_CONTRACT}}`

## 2. Step-by-Step Execution Workflow

1. **Pre-Flight Gate Check**: Verify upstream input contracts and schema invariants via `field_map`.
2. **Core Execution**: Execute the layer-specific pipeline or black-box script in `scripts/`.
3. **Post-Execution Verification**: Run the deterministic validator and verify exit code `0`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
