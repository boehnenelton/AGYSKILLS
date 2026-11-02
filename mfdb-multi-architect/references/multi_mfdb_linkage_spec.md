# Multi-MFDB Linkage Mechanisms & Federation Specification

> **Parent Skill:** `mfdb-multi-architect` (Layer 5)  
> **Release_Version:** 300 | **Format:** Markdown / BEJSON Specifications  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Bidirectional Handshake Protocol

Multi-MFDB guarantees relational integrity across decoupled physical files through bidirectional handshake verification.

### 1.1 Manifest Declaration (Top-Down)
The root manifest (`104a.mfdb.bejson`) declares all registered child entities in its `Values` matrix. Each row defines:
- `entity_name`: Logical entity name (e.g., `projects`, `users`, `tasks`).
- `file_path`: Canonical relative POSIX path from the manifest to the entity file (e.g., `data/projects.104.bejson`).
- `description`: Architectural summary of the entity.
- `record_count`: Current integer row count (synchronized upon mutation).
- `schema_version`: Semantic schema version string.
- `primary_key`: Primary key column name (e.g., `proj_uuid`).

### 1.2 Entity Header Declaration (Bottom-Up)
Every child entity table declares:
- `Parent_Hierarchy`: Relative POSIX path pointing back to the authoritative manifest (e.g., `../104a.mfdb.bejson`).
- `Network_Role`: Must be declared as `"Slave"`.
- `Records_Type`: Single-element array containing the capitalized entity type token (e.g., `["ProjectEntity"]`).

### 1.3 Handshake Verification Invariant
Let $\mathcal{M}$ be the manifest file at path $P_M$, and $\mathcal{E}$ be an entity table at path $P_E$:
$$\text{HandshakeValid}(\mathcal{M}, \mathcal{E}) \iff \left( \text{NormPath}(P_M \mathbin{/} \text{Lookup}(\mathcal{M}, \mathcal{E}.\text{name}).\text{path}) = P_E \right) \land \left( \text{NormPath}(\text{Dir}(P_E) \mathbin{/} \mathcal{E}.\text{Parent\_Hierarchy}) = P_M \right)$$

---

## 2. Linkage Error Code Registry (E30-E38)

All Multi-MFDB tools and validators must emit deterministic error codes upon detecting linkage violations:

| Error Code | Error Constant | Trigger Condition & Remediation |
| :--- | :--- | :--- |
| **`E30`** | `E_MFDB_MISSING_MANIFEST` | Manifest file `104a.mfdb.bejson` does not exist at the target path. Run scaffolding or restore manifest from backup. |
| **`E31`** | `E_MFDB_INVALID_FORMAT_VERSION` | Format version mismatch. Manifest or entity does not declare valid BEJSON `104`, `104a`, `104db`, `105`, `105a`, or `105db`. |
| **`E32`** | `E_MFDB_MISSING_RECORDS_TYPE` | Root JSON object is missing mandatory `Records_Type` array. |
| **`E33`** | `E_MFDB_MISSING_FIELDS` | Document header is missing the canonical `Fields` schema array. |
| **`E34`** | `E_MFDB_MISSING_VALUES` | Document payload is missing the `Values` tabular row array. |
| **`E35`** | `E_MFDB_UNRESOLVED_PARENT_HIERARCHY` | Entity declares `Parent_Hierarchy` pointing to a non-existent filesystem path, or points to a file that does not register the entity. |
| **`E36`** | `E_MFDB_CYCLIC_DEPENDENCY` | Circular reference detected during hierarchical graph traversal ($A \to B \to C \to A$). Traversal halts immediately. |
| **`E37`** | `E_MFDB_NETWORK_ROLE_MISMATCH` | Role contradiction. Entity declares `Network_Role: "Master"` while registered as a `Slave` child in a parent manifest. |
| **`E38`** | `E_MFDB_UNREGISTERED_ENTITY` | An entity file exists within the database partition directory on disk but is omitted from the parent manifest registry. |

---

## 3. Relative Coordinate Pointer Resolution Math

In Multi-MFDB, foreign key relationships resolve via coordinate tuples:
$$\text{Coordinate Pointer} = \langle \mathcal{P}_{\text{rel}}, \mathcal{E}_{\text{type}}, \mathcal{R}_{\text{id}} \rangle$$

### 3.1 Pointer Components
1. **$\mathcal{P}_{\text{rel}}$ (Relative Path)**: Relative POSIX path from the current file to the target entity table.
2. **$\mathcal{E}_{\text{type}}$ (Target Records_Type)**: Expected entity type token, ensuring the target file has not been replaced with an incompatible schema.
3. **$\mathcal{R}_{\text{id}}$ (Target Primary Key)**: RFC 4122 Version 4 UUID string.

### 3.2 Sandboxed Path Evaluation
To protect against directory traversal attacks, paths must resolve within the designated cluster root directory:
```python
def resolve_sandboxed_pointer(
    source_file_path: Path,
    relative_pointer_path: str,
    cluster_root_boundary: Path
) -> Path:
    resolved_target_path = (source_file_path.parent / relative_pointer_path).resolve()
    cluster_root_resolved = cluster_root_boundary.resolve()
    if not str(resolved_target_path).startswith(str(cluster_root_resolved)):
        raise ValueError(f"Security Violation: Pointer path escapes cluster boundary: {relative_pointer_path}")
    return resolved_target_path
```

---

## 4. Directed Acyclic Graph (DAG) Cycle Prevention

Multi-MFDB hierarchies must form a valid Directed Acyclic Graph. Cycles are detected via Depth-First Search (DFS) with a 3-color vertex marking algorithm:
- **White (0)**: Unvisited node.
- **Gray (1)**: Currently in active recursion stack. Re-encountering a Gray node indicates a cycle (`E36`).
- **Black (2)**: Completely evaluated node with all subtrees verified.

```python
def verify_dag_cycle_freedom(graph_adjacency_map: Dict[str, List[str]]) -> None:
    node_visitation_colors: Dict[str, int] = {node_key: 0 for node_key in graph_adjacency_map}

    def depth_first_visit(current_node: str):
        node_visitation_colors[current_node] = 1 # Gray: in stack
        for adjacent_child_node in graph_adjacency_map.get(current_node, []):
            child_color = node_visitation_colors.get(adjacent_child_node, 0)
            if child_color == 1:
                raise MFDBLinkageError("E36", f"Cyclic dependency detected involving: {adjacent_child_node}")
            if child_color == 0:
                depth_first_visit(adjacent_child_node)
        node_visitation_colors[current_node] = 2 # Black: verified

    for candidate_root_node in graph_adjacency_map:
        if node_visitation_colors[candidate_root_node] == 0:
            depth_first_visit(candidate_root_node)
```
