# Reference: Audit Domain Orchestration Topology & Dispatch Matrix

- **Version**: 100
- **Policy Anchor**: Policy §2.3, Policy §7.1, Policy §10.6
- **Author**: Elton Boehnen

---

## 1. Domain Auditing Matrix

The table below defines the dispatch sequence and execution conditions for every auditor tool in the ecosystem:

| Phase | Auditor Tool | Architectural Layer | Primary Input Target | Exit Code Trigger |
| :---: | :--- | :---: | :--- | :---: |
| **Phase 1** | `audit_readiness_tool.py` | Layer 2 | Project root, config/, perms | Exit 30 (Unready) |
| **Phase 1** | `secrets_leak_auditor.py` | Layer 2 | Repos, configs, transcripts | Exit 1 (Leak) |
| **Phase 2** | `audit_constraint_tool.py` | Layer 2 | Git diffs, AGENTS.md, $ADMIN_LIBRARIES | Exit 30 (Breach) |
| **Phase 2** | `policy_bejson_auditor.py`| Layer 2 | AST source, field map caches | Exit 1 (Violations) |
| **Phase 3** | `audit_deviation_tool.py`  | Layer 2 | Goal contracts, git logs, tests | Exit 30 (Deviation) |
| **Phase 4** | `audit_gap_tool.py`        | Layer 5 | Codebase, multi-language matrices | Exit 30 (Gaps) |
| **Phase 4** | `audit_redundancy_tool.py` | Layer 5 | Source AST, skill manifests | Exit 30 (Duplicates) |

---

## 2. DAG Execution Policies

1. **Fail-Fast vs. Comprehensive Sweep**:
   - In `--fail-fast` mode, a Phase 1 blocker (`NO_GO` or leaked secret) halts pipeline execution immediately.
   - In default comprehensive mode, all phases execute and aggregate into the Executive Audit Dossier.
2. **Standard Log Commits**:
   - The coordinator commits an authoritative structured log entry via `$LOGGING_TOOL write` per Policy §2.3.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
