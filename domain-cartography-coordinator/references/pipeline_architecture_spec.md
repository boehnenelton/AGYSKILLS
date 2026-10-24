# Pipeline Architecture Specification: Multi-Domain Cartography & Typing

* System: Layer 6 Multi-Domain Architectural Decomposition Engine
* Component: `domain-cartography-coordinator`
* Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Architectural Role Contracts

```
[Project Vision & Objective]
  │
  ▼
planning_coordinator (Layer 6: Turn-delay scheduling & phase orchestration)
  │
  ├── 1. skill_cartographer (Audits capabilities, identifies missing skills & tool DAG)
  ├── 2. terms_cartographer (Extracts ubiquitous language, entity prefixes & semantic suffixes)
  └── 3. domain_type_cartographer (Partitions the system into architectural verticals)
        │
        ▼
     domain_router (Evaluates domain stack & dispatches to specialized domain engines)
        │
        ├── [Domain A: Python / Backend]
        │     ├── python_cartography_terms (Python idioms, stdlib primitives, typing protocols)
        │     └── python_domain_typer
        │           ├── Interfaces & Protocols (structural contracts)
        │           ├── BEJSON Schemas (104/104a tabular definitions & field maps)
        │           ├── Function Signatures (<family>_<component>_<verb>_<target>)
        │           └── Classes & Managers (<Domain><Family><Subsystem><Role>)
        │
        ├── [Domain B: BEHTML / Presentation]
        │     ├── behtml_cartography_terms (8-lane coordinates, Ry=32px quantization, BECSS Tri-Color)
        │     └── behtml_domain_typer (BEHTMLElement spatial schemas, container templates)
        │
        └── [Domain C: Bash / Scaffolding]
              ├── bash_cartography_terms (POSIX constraints, jq primitives, exit codes)
              └── bash_domain_typer (CLI flags, environment variables, self-locating paths)
```

### 1.1 `planning_coordinator`
- **Responsibility**: Top-level phase gatekeeper and multi-turn state coordinator.
- **Contract**: Accepts raw project vision prompts; enforces Turn 1 contract freezing; prohibits code scaffolding until all domain types pass validation.
- **State Emitted**: `planning_state.104a.bejson` tracking phase completion (`CARTOGRAPHY_AUDIT`, `ROUTING`, `TYPING`, `CONTRACT_FROZEN`).

### 1.2 `skill_cartographer`
- **Responsibility**: Scans ecosystem skill manifests across `~/.gemini/config/skills` and `$ADMIN_SKILLS`.
- **Contract**: Maps required tools to installed skills; flags any missing dependency or execution node prior to Turn 2.

### 1.3 `terms_cartographer`
- **Responsibility**: Harvests ubiquitous language and normalizes naming models.
- **Contract**: Enforces Policy §6.1 Hierarchy-Group-Purpose naming formula:
  $$\text{Variable} = \langle\text{hierarchy\_or\_scope}\rangle\_\langle\text{group\_or\_domain}\rangle\_\langle\text{purpose\_or\_role}\rangle$$
- **Semantic Suffixes**: Mandatory suffixes for data fields (`_metric`, `_count`, `_timestamp`, `_flag`, `_fk`, `_url`, `_secret`).

### 1.4 `domain_type_cartographer`
- **Responsibility**: System partitioning into architectural verticals.
- **Contract**: Maps raw functional requirements into distinct domains:
  - `Domain_Backend_Python`: Persistence, data modeling, APIs, daemons.
  - `Domain_Presentation_BEHTML`: UI components, tabular layouts, document views.
  - `Domain_Scaffolding_Bash`: CLI utilities, cron runners, process supervision.

### 1.5 `domain_router`
- **Responsibility**: Dynamic dispatcher routing domain packages to specialized typers.

---

## 2. Specialized Domain Typer Contracts

### 2.1 Domain A: Python / Backend (`python_domain_typer`)
- **Interfaces & Protocols**: Pure structural contracts declared via `typing.Protocol` with runtime checkability (`@runtime_checkable`).
- **BEJSON Schemas**: Standard 104/104a schemas containing `Format`, `Format_Version`, `Fields`, and `Values`, with mandatory O(1) `field_map` caching.
- **Function Signatures**: Strictly formatted as:
  ```python
  def <family>_<component>_<verb>_<target>(...) -> <ReturnType>:
  ```
- **Classes & Managers**: Strictly formatted as:
  ```python
  class <Domain><Family><Subsystem><Role>:
  ```

### 2.2 Domain B: BEHTML / Presentation (`behtml_domain_typer`)
- **Grid Geometry**: 8-lane ($12.5\%$) primary grid or 16-sublane ($6.25\%$) stage.
- **Vertical Quantization**: Row heights quantized to $R_y = 32\text{px}$ multiples ($32\text{px}, 64\text{px}, 96\text{px}, \dots$).
- **Color Palette**: Policy §8.1 Tri-Color tokens strictly enforced:
  - Background: `#000000` or `#FFFFFF`
  - Text: `#FFFFFF` or `#000000`
  - Accent / Active: `#DE2626`
- **Zero-Filler Skeleton Law**: All rendered markup skeletons must contain simple placeholder labels (`Title`, `Content Body`), never fabricated content or lorem ipsum.

### 2.3 Domain C: Bash / Scaffolding (`bash_domain_typer`)
- **Self-Locating Bootstrap**: Every shell script must include Policy §4.2 self-locating resolution:
  ```bash
  get_script_path() {
      local source="${BASH_SOURCE[0]}"
      while [ -h "$source" ]; do
          local dir="$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
          source="$(readlink "$source")"
          [[ $source != /* ]] && source="$dir/$source"
      done
      echo "$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
  }
  SCRIPT_PATH=$(get_script_path)
  ```
- **CLI Standard Arguments**: Mandatory CLI argument parser supporting `--version`, `--config`, `--reset`, and `--help`.
- **Atomic File Persistence**: Updates to persistent state files must execute via temporary files and atomic POSIX replacement (`mv -f`).
- **Deterministic Exit Codes**:
  - `0`: Clean execution
  - `10`: Path or file dialog failure
  - `20`: Environment or config missing
  - `30`: Schema validation error
