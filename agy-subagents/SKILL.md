---
name: agy-subagents
description: >-
  Architect, define, spawn, monitor, and coordinate concurrent Antigravity CLI subagents (define_subagent, invoke_subagent, manage_subagents, send_message). Enforces workspace isolation strategies (inherit, branch, share), model tier selection (flash, flash_lite, pro, inherit), clean-slate context boundaries, reactive wakeup protocols (zero status polling), and structured delegation payloads. Use when designing parallel research workers, background debugging agents, worktree refactoring tasks, or multi-agent pipelines.
---

# Skill: `agy-subagents`

- **Purpose**: Defining, dispatching, and managing concurrent background subagents in the Antigravity CLI.
- **Target Platform**: Antigravity CLI (`agy`) & Antigravity 2.0 Harness
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Subagent Lifecycle & Core Tools

Antigravity equips agents with four fundamental subagent primitives:

1. **`define_subagent`**: Dynamically creates a new specialized agent type with custom system prompts and permission sets.
2. **`invoke_subagent`**: Launches one or more subagent sessions running concurrently in the background.
3. **`send_message`**: Sends instructions or feedback to a running subagent by its `conversationID`.
4. **`manage_subagents`**: Lists active subagents (`list`), checks live states, or terminates sessions (`kill`, `kill_all`).

---

## 2. Workspace Isolation Strategies

When launching a subagent via `invoke_subagent`, choose the proper `Workspace` parameter:

| Workspace Mode | Environment | Use Case |
| :--- | :--- | :--- |
| **`inherit`** *(Default)* | Exact same working directory as parent | Quick shared tasks, fast edits, or read-only codebase research. |
| **`branch`** | Isolated **Git worktree** branched from current HEAD | Experimental refactoring, breaking changes, or code where diffs must be reviewed before merging. |
| **`share`** | Shared repository storage with isolated runtime state | Multi-branch testing without disk duplication. |

---

## 3. Model Tiers & Context Economics

Subagents start with a **clean-slate context window** (zero inherited parent chat history). Match the model to the task:

- **`flash`**: Ideal for codebase research, grep searches, reading large files, and quick sanity checks.
- **`flash_lite`**: Minimal token footprint for high-volume batch data transformations.
- **`pro`**: High-reasoning model for complex algorithmic refactoring, multi-file architectural planning, and adversarial security audits.
- **`inherit`**: Matches the parent agent's current model.

---

## 4. The Reactive Wakeup Protocol (Zero Polling)

### Cardinal Rule: NEVER Poll Subagent Status
The Antigravity engine features built-in **Reactive Wakeup**:
- When a subagent completes its task or sends a message, the system resumes the parent agent automatically.
- **Do NOT** loop or sleep waiting for subagents.
- After calling `invoke_subagent`, either continue other tasks or stop calling tools to yield execution.

---

## 5. Standard Invocation Pattern

```python
# Example: Spawning a background research subagent
invoke_subagent(
    Subagents=[
        {
            "TypeName": "research",
            "Role": "Codebase Investigator",
            "Model": "flash",
            "Workspace": "inherit",
            "Prompt": "Search for all references to MFDB Network_Role across libraries_104 and return a summary of occurrences."
        }
    ]
)
# Stop calling tools here; the system wakes you when the subagent responds.
```
