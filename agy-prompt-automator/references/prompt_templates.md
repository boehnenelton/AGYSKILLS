# Massive List Generation Prompt Templates & Minute-Based Automation
**Author:** Elton Boehnen  
**Target Environment:** Linux, Termux (Android), macOS | Python 3.10+ | Bash 4+  
**Format Specifications:** BEJSON 104/104a, BECSS Tri-Color Law (#000000, #FFFFFF, #DE2626)  

This reference catalog provides production-grade prompt templates specifically engineered for **generating massive, structured, sequentially numbered lists** (feature menus, function catalogs, edge cases, schemas, and taxonomies), accompanied by minute-based automation loop recipes.

---

## 1. Minute-Based Automation Timing Variables & Loop Recipes

### 1.1 Standard Minute-Based Timing Variables
In shell scripts and daemons, timing parameters should be explicitly declared in minutes and dynamically converted:

```bash
# ==============================================================================
# Timing Parameters (Configured in Minutes)
# ==============================================================================
INTERVAL_MINUTES=5       # Fixed base cycle in minutes
MIN_MINUTES=2            # Minimum jitter bound in minutes
MAX_MINUTES=10           # Maximum jitter bound in minutes
HEARTBEAT_MINUTES=15     # Background health-check pulse in minutes
```

### 1.2 Pure Bash Minute Looper with Jitter
Executes automated tasks at randomized intervals specified in minutes:

```bash
#!/usr/bin/env bash
MIN_MINUTES=3
MAX_MINUTES=8
OUTPUT_DIR="./generated_lists"
mkdir -p "$OUTPUT_DIR"

while true; do
  # Calculate randomized delay in minutes and convert to seconds
  DELAY_MINS=$(( MIN_MINUTES + RANDOM % (MAX_MINUTES - MIN_MINUTES + 1) ))
  DELAY_SECS=$(( DELAY_MINS * 60 ))
  TIMESTAMP=$(date +'%Y%m%d_%H%M%S')

  echo "[$(date +'%T')] Dispatching task. Next cycle in ${DELAY_MINS}m (${DELAY_SECS}s)..."

  # Run Antigravity CLI in headless mode
  agy --sandbox -p \
    "Act as a system architect. Review the domain 'BEJSON 104 Data Architecture'. Generate an exhaustive 30-point numbered list of schema validation edge cases, positional integrity hazards, and migration hazards. Save to ${OUTPUT_DIR}/bejson_edge_cases_${TIMESTAMP}.md."

  echo "[$(date +'%T')] Execution complete. Sleeping ${DELAY_MINS} minutes..."
  sleep "${DELAY_MINS}m"
done
```

---

## 2. Exhaustive Feature & Idea Menus (1–50 Numbered Items)

### Template 2.1: 50-Point Exhaustive Tool Feature Menu
Forces the model to produce a massive, numbered menu of features so users or systems can select features by number:

```text
Act as a software ideation-feature-composer and systems architect. Analyze the tool concept: '{TOOL_CONCEPT_OR_NAME}'.
Generate an exhaustive, sequentially numbered feature menu containing exactly 50 distinct feature options, UI configurations, and automation workflows.

Structural Mandates:
1. Divide the 50 items into 5 clear, logical categories (10 items per category):
   - Category A: Core Execution & Data Manipulation
   - Category B: Terminal & CLI Automation
   - Category C: UI, Spatial Layout & Visualization (conforming to BECSS Tri-Color Law: #000000, #FFFFFF, #DE2626)
   - Category D: Persistence, BEJSON Schemas & Storage
   - Category E: Error Handling, Auditing & Recovery
2. Every item must be formatted as:
   [Number]. **[Concise Action Title]**: [Exact 2-sentence operational description detailing functionality and edge-case behavior].
3. Zero fluff, introductory banter, or closing summaries. Output only the structured menu.
4. Save the output directly to: target/ideas/feature_menu_{TIMESTAMP}.md
```

### Template 2.2: 30-Point CLI Automation Flag & Parameter Universe
Generates every possible CLI flag and command-line switch for a specific application:

```text
Act as a CLI tool architect. Focus on the tool: '{TOOL_NAME_OR_SUBJECT}'.
Generate an exhaustive, sequentially numbered list of 30 specialized CLI flags and parameter switches designed for advanced headless automation and terminal scripting.

Formatting Requirements:
1. Sequential numbering from 1 to 30.
2. Group into 3 categories:
   - Part 1: Execution Control & Non-Interactive Automation (e.g., --watch, --json, --diff-only, --timeout)
   - Part 2: File System & Workspace Boundary Routing (e.g., --dir, --output, --backup-dir, --sandbox)
   - Part 3: Diagnostics, Debugging & Audit Flags (e.g., --dry-run, --verbose, --audit, --export-schema)
3. Format each item as:
   `--[flag_name] [optional_arg]`: **[Short Name]** — [2-sentence technical rationale and operational behavior].
4. Output with zero conversational filler directly to: target/ideas/cli_flags_{TIMESTAMP}.md
```

---

## 3. Subject-Specific Function & Library Inventories

### Template 3.1: 25-Point Family Library Function Inventory
Inventories every function required to build a complete library family:

```text
Act as a senior software engineer specializing in BEJSON modular libraries.
Domain: '{LIBRARY_SUBJECT}' (Library Family: '{FAMILY_NAME}').
Generate an exhaustive, numbered inventory of 25 core functions required to construct a production-ready, zero-dependency library family.

Requirements:
1. Every function name must strictly adhere to the family naming convention: `{FAMILY_NAME}_[function_name]`.
2. Format:
   [Number]. `{FAMILY_NAME}_[function_name](args) -> ReturnType`
   - **Purpose**: [Precise operational purpose].
   - **Algorithmic Complexity**: [e.g. O(1), O(N)].
   - **Failure Modes**: [Deterministic exception or exit behavior].
3. Group into 4 architectural blocks:
   - Ingestion & Parsing
   - Transformation & In-Memory Operations
   - Atomic Persistence & I/O
   - Validation & Integrity Assurance
4. Save directly to: target/schemas/{FAMILY_NAME}_function_inventory_{TIMESTAMP}.md
```

### Template 3.2: 20-Point Shell & Subprocess Automation Function Catalog
```text
Act as a Linux and Termux automation engineer. Focus on: '{SUBPROCESS_SUBJECT}'.
Generate an exhaustive, sequentially numbered list of 20 modular Bash helper functions designed for background daemons, heartbeat services, and asynchronous process orchestration.

Requirements:
1. Numbered 1 to 20.
2. Each item must define:
   - Function signature: `fn_[name]()`
   - Operational description: Exactly what process or file descriptor it handles.
   - Deterministic exit code mapping (e.g. Exit 0: Success, Exit 10: Timeout, Exit 20: Missing env).
3. Zero-fluff output saved directly to: target/schemas/shell_functions_{TIMESTAMP}.md
```

---

## 4. Hostile Audits, Security & Edge Case Checklists

### Template 4.1: 40-Point Hostile Security & Vulnerability Checklist
Generates an extensive penetration testing and static audit checklist for codebases:

```text
[HOSTILE-AUDIT] Act as a paranoid security auditor and reverse engineer.
Target Subject: '{TARGET_SUBJECT_OR_MODULE}'.
Generate an exhaustive, sequentially numbered checklist of 40 critical vulnerability checks, secret leakage vectors, and dangerous execution patterns.

Categorization (10 items each):
1. **Credentials & Secret Exposure**: Scanning for hardcoded tokens, unsanitized environment reads, and git history leaks.
2. **Subprocess & Shell Execution Vulnerabilities**: Command injections, path traversal in arguments, and lack of sandboxing.
3. **File System & Storage Tampering**: Race conditions in tempfiles (TOCTOU), non-atomic overwrites, and permission escalations.
4. **Data Deserialization & Memory Bounds**: Unbounded payload ingestion, JSON injection, and cyclic recursion risks.

Format:
- [ ] [Number]. **[Risk Name]** (`[SEVERITY: CRITICAL/HIGH/MEDIUM]`): [Detailed explanation of the attack vector and exact remediation].
Save directly to: reports/audits/hostile_security_checklist_{TIMESTAMP}.md
```

### Template 4.2: 25-Point Tabular Data & Positional Integrity Hazards
```text
Act as a database architect. Focus on: 'BEJSON 104/104a Tabular Storage'.
Generate an exhaustive, numbered list of 25 structural edge cases, corruption vectors, and positional drift hazards in tabular data systems.

Mandates:
1. Numbered 1 to 25.
2. Must address: column schema mismatch, un-padded nulls, mid-array field insertion, non-atomic writes during crash, and field map cache cache invalidation.
3. Each item must provide: (a) The Hazard, (b) The Structural Impact, (c) The Deterministic Guardrail.
4. Save to: reports/audits/bejson_hazards_{TIMESTAMP}.md
```

---

## 5. Taxonomies, Ontologies & BEJSON Schemas

### Template 5.1: 30-Point Domain Entity & Field Taxonomy
Extracts all entities, fields, and relational mappings for a complex domain:

```text
Act as an enterprise ontologist and data architect. Domain: '{DOMAIN_SUBJECT}'.
Generate an exhaustive, sequentially numbered taxonomy of 30 distinct data entities and configuration tables required to fully represent this system.

Requirements:
1. Numbered 1 to 30.
2. For each entity, specify:
   - **Entity Name**: (e.g. `UserSession`, `AuditLog`, `StorageNode`)
   - **Fields Definition**: Exact list of field names in `snake_case`, prefixed by entity identity.
   - **Primitive Types**: (`string`, `integer`, `number`, `boolean`).
   - **Primary Key**: (UUID format).
   - **Foreign Keys**: (`<parent>_fk` mapping).
3. Save directly to: target/schemas/domain_taxonomy_{TIMESTAMP}.md
```

### Template 5.2: Complete BEJSON 104a Config Registry Builder
```text
[BEJSON-104A] Act as Elton Boehnen's systems architect. Target: '{SYSTEM_NAME_OR_TOOL}'.
Generate an authoritative BEJSON 104a ScriptConfig schema containing exactly 20 essential configuration settings, runtime defaults, and environment paths.

Mandatory Constraints:
1. Exact six top-level keys:
   - "Format": "BEJSON"
   - "Format_Version": "104a"
   - "Format_Creator": "Elton Boehnen"
   - "Records_Type": ["ScriptConfig"]
   - "Fields": [{"name": "setting_name", "type": "string"}, {"name": "setting_value", "type": "string"}, {"name": "description", "type": "string"}]
   - "Values": 20 rows matching Fields exactly.
2. Values must cover: local lib directory, master lib source, log level, timeouts, retry counts, buffer sizes, and debug switches.
3. Save directly to: target/schemas/system_config_{TIMESTAMP}.104a.bejson
```

---

## 6. Architectural Ideation & Subagent Decomposition

### Template 6.1: 20-Point Autonomous Subagent Workstream Breakdown
Decomposes a massive project into independent subagent task assignments:

```text
Act as an AI harness architect. Project Objective: '{PROJECT_OBJECTIVE}'.
Generate an exhaustive, sequentially numbered workstream breakdown defining 20 independent subagent tasks designed for parallel execution without shared memory collisions.

Formatting:
1. Numbered 1 to 20.
2. Each task must specify:
   - **Task Title**: [Action verb + specific target].
   - **Subagent Role**: [e.g. Code Reviewer, Test Author, Parser Implementer].
   - **Input Artifacts**: [Exact files or endpoints required].
   - **Deliverable**: [Concrete output file created].
   - **Independence Factor**: [Why this task can run concurrently without race conditions].
3. Save directly to: target/ideas/subagent_decomposition_{TIMESTAMP}.md
```

---

## 7. Python Automation Driver for Massive List Generation

This Python 3.10+ driver continuously iterates through subjects, renders the prompt templates, and executes them via `agy` on a configurable minute-based cadence.

```python
#!/usr/bin/env python3
"""
Autonomous Minute-Based List Generator Driver
"""
import os
import sys
import time
import random
import logging
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("list_generator_driver")

INTERVAL_MINUTES = 5.0  # Configure interval in minutes

TEMPLATES = [
    "Generate an exhaustive 30-point numbered list of advanced CLI automation workflows for local-first systems.",
    "Generate a 25-point inventory of modular Python utility functions for atomic BEJSON file persistence.",
    "Generate a 40-point hostile security checklist probing edge cases in shell automation daemons.",
    "Generate a 30-point feature expansion menu for an offline mobile text editor using Termux."
]

def run_minute_automation():
    logger.info("Starting list generation driver on a %.1f-minute interval.", INTERVAL_MINUTES)
    while True:
        prompt = random.choice(TEMPLATES)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        target_file = f"output_list_{timestamp}.md"
        
        full_prompt = f"{prompt} Output directly to {target_file}."
        logger.info("Executing prompt: %s", full_prompt)
        
        subprocess.run(["agy", "--sandbox", "-p", full_prompt])
        
        sleep_seconds = INTERVAL_MINUTES * 60.0
        logger.info("Sleeping for %.1f minutes...", INTERVAL_MINUTES)
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    run_minute_automation()
```
