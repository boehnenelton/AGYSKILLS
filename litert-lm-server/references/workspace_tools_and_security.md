# Workspace Tools & Security Sandbox Specification

When `workspace_tools: true` is included in a chat request, the LiteRT-LM server exposes local filesystem inspection and editing capabilities directly to the model.

---

## 1. Registered Tool Inventory

| Tool Name | Parameters | Allowed Modes | Functional Description |
| :--- | :--- | :--- | :--- |
| `find` | `pattern: str`, `path: str = "."`, `exclude_dirs: list[str] = [".git", ".venv", "__pycache__"]` | Read-only & Read-write | Searches file paths matching a glob or substring pattern. |
| `grep` | `pattern: str`, `path: str = "."`, `exclude_dirs: list[str] = [".git", ".venv"]` | Read-only & Read-write | Searches file contents using regular expressions. |
| `read` | `path: str`, `start_line: int = 1`, `end_line: int = 200` | Read-only & Read-write | Reads a bounded line range from a text file. |
| `line_count`| `path: str` | Read-only & Read-write | Counts lines in a file without loading entire content into memory. |
| `write` | `path: str`, `content: str`, `overwrite: bool = false` | Read-write Only | Writes new text or overwrites an existing file. |
| `edit` | `path: str`, `target_string: str`, `replacement_string: str` | Read-write Only | Replaces a single exact target string within a file. |
| `shell` | `command: str`, `approval_id: str` | Read-write Only | Executes an approved shell command with current working dir locked. |

---

## 2. Path Sandboxing & Confinement Rules

1. **Root Confinement:** All file paths received from the model must resolve strictly inside `workspace_path`.
2. **Directory Traversal Defense:** Paths containing `..` or leading slashes are canonicalized via `pathlib.Path.resolve()`. If `not resolved_path.is_relative_to(workspace_root)`, the call is aborted immediately with `PermissionError`.
3. **Symbolic Link Verification:** Symlinks pointing outside the workspace boundary are rejected.
4. **Binary File Protection:** Files detected as binary (containing null bytes in initial header) cannot be opened by `read` or `edit` to prevent context pollution.

---

## 3. Human-in-the-Loop Shell Approval Protocol

For arbitrary commands (`shell`), automated execution without supervision is prohibited:
1. The client must supply `workspace_shell_approval_id`.
2. When the model invokes `shell`, the server halts and registers a pending approval request.
3. The client receives notice and polls `GET /v1/workspace/shell-approvals/{approval_id}`.
4. The client confirms or denies via `POST /v1/workspace/shell-approvals/{approval_id}/{call_id}` with `{"approved": true}`.
5. If denied or unanswered within 5 minutes, the command is terminated with an error returned to the model.
