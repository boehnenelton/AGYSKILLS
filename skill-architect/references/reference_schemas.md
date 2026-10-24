# Canonical BEJSON 104a Reference Schemas for the Layered Skill Ecosystem

> **Parent Skill:** `skill-architect` (Layer 6)  
> **Version:** 100 | **Release_Version:** 300 | **RELATIONAL_ID:** `c4f82e19-7d3a-4c9b-8e12-5a0b6f3d9e27`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Skill Ecosystem Registry Schema (`skill_registry_catalog.104a.bejson`)

Maintained exclusively by `skill-ecosystem-cartographer` (Write-Owner) to catalog every installed workspace, global, and plugin skill, its layer assignment (`1-6`), positive/negative trigger clauses, sibling redirection pointers, input/output artifact contracts, and manifest SHA-256 fingerprint.

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Registry_Domain": "Antigravity_Skill_Ecosystem_Cartography",
  "Schema_Version": "1.0.0",
  "Records_Type": ["SkillCatalogEntry"],
  "Fields": [
    {"name": "skill_entry_uuid", "type": "string"},
    {"name": "skill_canonical_name", "type": "string"},
    {"name": "skill_layer_tier_number", "type": "integer"},
    {"name": "skill_codebase_layer_mapping", "type": "string"},
    {"name": "skill_domain_prefix_token", "type": "string"},
    {"name": "skill_functional_suffix_token", "type": "string"},
    {"name": "skill_scope_origin_kind", "type": "string"},
    {"name": "skill_manifest_relative_path", "type": "string"},
    {"name": "skill_positive_triggers_csv", "type": "string"},
    {"name": "skill_negative_triggers_csv", "type": "string"},
    {"name": "skill_blocked_siblings_csv", "type": "string"},
    {"name": "skill_allowed_downward_deps_csv", "type": "string"},
    {"name": "skill_input_contract_spec", "type": "string"},
    {"name": "skill_output_artifact_spec", "type": "string"},
    {"name": "skill_body_line_count_metric", "type": "integer"},
    {"name": "skill_desc_char_count_metric", "type": "integer"},
    {"name": "skill_manifest_sha256_hash", "type": "string"},
    {"name": "skill_linter_verified_flag", "type": "boolean"},
    {"name": "skill_created_at", "type": "string"}
  ],
  "Values": [
    [
      "a1000000-0000-4000-8000-000000000001",
      "skill-architect",
      6,
      "L5_Composition_Root",
      "skill",
      "-architect",
      "global",
      "skills/skill-architect/SKILL.md",
      "authoring new SKILL.md bundles,defining skill directory topologies,scaffolding layer-specific reference shards,auditing skill manifests",
      "executing multi-skill DAG workflows,mapping installed ecosystem routing topologies,composing multi-skill recipe blueprints,decomposing monolithic application source code",
      "skill-chain-coordinator,skill-ecosystem-cartographer,skill-chain-recipe-composer,arch-layered-refactor",
      "bejson-format-core,bejson-schema-validator",
      "Skill specification parameters (name, layer 1-6, positive triggers, negative sibling mappings)",
      "Verified SKILL.md bundle (SKILL.md, references/, scripts/, assets/) passing codes 401-415",
      195,
      612,
      "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      true,
      "2026-10-17T08:30:00Z"
    ],
    [
      "a1000000-0000-4000-8000-000000000002",
      "skill-ecosystem-cartographer",
      6,
      "L5_Composition_Root",
      "skill",
      "-cartographer",
      "global",
      "skills/skill-ecosystem-cartographer/SKILL.md",
      "cataloging installed skills,mapping routing topologies,registering functional boundaries,detecting trigger collisions,auditing reciprocal negative guardrails",
      "scaffolding new skill files,executing runtime DAG pipelines,scheduling conversational turn delays",
      "skill-architect,skill-chain-coordinator,planning-schema-planner",
      "bejson-format-core,bejson-schema-validator,policy-conflict-auditor",
      "Installed skill directories (.agents/skills/, ~/.gemini/antigravity-cli/skills/, plugins)",
      "data/skill_registry_catalog.104a.bejson and reports/audits/topology_collision_matrix.md",
      210,
      580,
      "f4a1d55309ad2d250bcaf5d9007fc03538bf52f5750c045db506002c8963c966",
      true,
      "2026-10-17T08:30:00Z"
    ],
    [
      "a1000000-0000-4000-8000-000000000003",
      "skill-chain-coordinator",
      6,
      "L5_Composition_Root",
      "skill",
      "-coordinator",
      "global",
      "skills/skill-chain-coordinator/SKILL.md",
      "orchestrating multi-skill DAG execution flow,managing stage gate transitions,delegating subagent handoffs,enforcing contract freezing between layers",
      "scaffolding raw skill manifests,cataloging static skill registries without execution,scheduling N=K+1 conversational turn delays,executing JobMaker task lists",
      "skill-architect,skill-ecosystem-cartographer,planning-schema-planner,job-workflow-manager",
      "bejson-format-core,bejson-schema-validator,skill-ecosystem-cartographer",
      "Approved Recipe Blueprint or multi-skill DAG goal + verified skill_registry_catalog.104a.bejson",
      "data/dag_pipeline_ledger.104a.bejson and verified stage deliverables",
      230,
      604,
      "05b2e66410be3e361cdbg6e0118gd14649cg63g6861d156ec617113d9074d077",
      true,
      "2026-10-17T08:30:00Z"
    ]
  ]
}
```

---

## 2. Multi-Skill DAG Execution Ledger Schema (`dag_pipeline_ledger.104a.bejson`)

Maintained exclusively by `skill-chain-coordinator` (Write-Owner) to track topological stage execution, input/output artifact handoffs, subagent isolation modes (`inherit`, `branch`, `share`), and deterministic Stage Gate verification statuses.

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Registry_Domain": "Antigravity_DAG_Pipeline_Coordination",
  "Schema_Version": "1.0.0",
  "Records_Type": ["DagStageExecution"],
  "Fields": [
    {"name": "dag_stage_uuid", "type": "string"},
    {"name": "dag_pipeline_run_id", "type": "string"},
    {"name": "dag_stage_sequence_number", "type": "integer"},
    {"name": "dag_skill_entry_fk", "type": "string"},
    {"name": "dag_skill_canonical_name", "type": "string"},
    {"name": "dag_skill_layer_tier_number", "type": "integer"},
    {"name": "dag_upstream_stage_uuid_fk", "type": "string"},
    {"name": "dag_execution_mode_kind", "type": "string"},
    {"name": "dag_workspace_isolation_mode", "type": "string"},
    {"name": "dag_subagent_conversation_id", "type": "string"},
    {"name": "dag_input_artifact_path", "type": "string"},
    {"name": "dag_handoff_artifact_path", "type": "string"},
    {"name": "dag_handoff_sha256_hash", "type": "string"},
    {"name": "dag_gate_validator_command", "type": "string"},
    {"name": "dag_gate_exit_code_metric", "type": "integer"},
    {"name": "dag_stage_lifecycle_state", "type": "string"},
    {"name": "dag_contract_frozen_flag", "type": "boolean"},
    {"name": "dag_stage_created_at", "type": "string"}
  ],
  "Values": [
    [
      "b2000000-0000-4000-8000-000000000001",
      "run_20261017_083000",
      1,
      "a1000000-0000-4000-8000-000000000001",
      "code-taxonomy-architect",
      5,
      null,
      "plan",
      "inherit",
      "conv-subagent-01",
      "src/",
      "target/schemas/preset_taxonomy.md",
      "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
      "python3 scripts/taxonomy_naming_linter.py target/schemas/preset_taxonomy.md",
      0,
      "VERIFIED",
      true,
      "2026-10-17T08:30:10Z"
    ]
  ]
}
```

---

## 3. Layer 1 Boundary Sanitization & O(1) Field Map Accessor Template

All Python scripts interacting with the schemas above MUST embed this exact boundary-layer sanitization and O(1) lookup implementation:

```python
import os
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List

MANDATORY_BEJSON_KEYS = (
    "Format",
    "Format_Version",
    "Format_Creator",
    "Records_Type",
    "Fields",
    "Values",
)

def bejson_core_sanitize_doc(raw_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Boundary-layer sanitization: strips leading/trailing whitespace from keys, field names, and string values."""
    clean_doc: Dict[str, Any] = {
        (k.strip() if isinstance(k, str) else k): v for k, v in raw_doc.items()
    }
    fields = clean_doc.get("Fields")
    if isinstance(fields, list):
        for fdef in fields:
            if isinstance(fdef, dict):
                for fkey in ("name", "type"):
                    if isinstance(fdef.get(fkey), str):
                        fdef[fkey] = fdef[fkey].strip()
    values = clean_doc.get("Values")
    if isinstance(values, list):
        for row in values:
            if isinstance(row, list):
                for idx, cell in enumerate(row):
                    if isinstance(cell, str) and cell and (cell[0].isspace() or cell[-1].isspace()):
                        row[idx] = cell.strip()
    return clean_doc

def bejson_core_get_field_map(bejson_doc: Dict[str, Any]) -> Dict[str, int]:
    """Compiles an O(1) lookup dictionary mapping field_name -> 0-based column index."""
    fields_list = bejson_doc.get("Fields", [])
    return {field_obj["name"]: col_idx for col_idx, field_obj in enumerate(fields_list)}

def bejson_core_atomic_write(target_file_path: Path, bejson_doc: Dict[str, Any]) -> None:
    """Writes a BEJSON document atomically via .tmp -> flush -> os.fsync -> os.replace."""
    target_file_path = target_file_path.resolve()
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".bejson_{os.getpid()}_",
        suffix=".tmp",
        dir=str(target_file_path.parent),
    )
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
            json.dump(bejson_doc, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(str(tmp_path), str(target_file_path))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise
```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
