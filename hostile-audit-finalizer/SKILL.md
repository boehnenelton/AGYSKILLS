---
name: hostile-audit-finalizer
description: Conducts adversarial quality audits prior to task completion, verifies strict surgical scope (§5.1), synchronizes dev/change-log.md with bejson_project.json, logs UI directives to dev/UIPref.md, and emits the standby verbalization (§3.1, §3.6). Use when finalizing coding tasks, conducting pre-delivery reviews, or wrapping up development sessions. Do NOT use for AST field-map cache verification (use policy-bejson-auditor) or web browser testing (use playwright-debugger-auditor).
---
# Hostile Audit Finalizer

Adopts the adversarial posture of a hostile code auditor before concluding execution. Verifies surgical task scope, inspects modified files for regressions or syntax flaws, synchronizes changelogs, records user design directives in `dev/UIPref.md`, and verbalizes the standby state.

## When to Use

* Concluding any code editing, refactoring, or feature implementation task.
* Auditing git diffs or file modifications prior to ending an interaction turn.
* Synchronizing release notes between `dev/change-log.md` and `bejson_project.json`.
* Capturing user styling, theme, button, or menu preferences into `dev/UIPref.md`.

## Core Audit Rules

1. Hostile Auditing Mindset: Assume the role of a hostile auditor. Scrutinize every line changed. If any improvement or refinement is identified within scope, execute it immediately before declaring completion.
2. Surgical Scope Confinement (§5.1): Modify only what was requested. Never refactor adjacent code, external modules, or unrelated files. Confine audits and refactors strictly to modifications made within the active task.
3. Changelog Synchronization (§3.6, §9.3): Update `dev/change-log.md` with a timestamped entry and synchronize the summary string within `bejson_project.json` under `Change_Log`.
4. User Design Preferences (§10.7): Document any specific user design, styling, color, layout, or toolbar preferences explicitly requested during the task in `dev/UIPref.md`.
5. Standby Announcement (§3.1, §3.6): Conclude task execution by verbalizing the mandatory standby phrase: "Standing by waiting for instructions."

## Execution Steps

1. Review the list of modified files. Confirm zero unintended file modifications exist.
2. Check code against Negative Constraints:
   - Python runtime >= 3.10 syntax.
   - Zero `print()` calls for logging (standard `logging` only).
   - Zero hardcoded absolute paths outside `paths.json` and `secureenv_file.json`.
   - Untouched `Project_GUID` (`GUID_PLACEHOLDER` intact).
3. Append release notes to `dev/change-log.md`.
4. Update `Change_Log` attribute in `bejson_project.json`.
5. Check if user expressed UI or design preferences; if so, append to `dev/UIPref.md`.
6. Output final task wrap-up and verbalize: "Standing by waiting for instructions."

## Embedded Verification Checklist Template

```markdown
# Pre-Finalization Hostile Audit Checklist

- [ ] Surgical Scope Verified: Only requested files were modified. Adjacent files untouched.
- [ ] Negative Constraints Checked: Python 3.10+, no print() logging, relative paths, untouched external libs.
- [ ] Changelog Synchronized: dev/change-log.md updated and mirrored in bejson_project.json.
- [ ] UI Preferences Recorded: Any design preferences appended to dev/UIPref.md.
- [ ] Standby Announcement Ready: "Standing by waiting for instructions."
```

## Gotchas

* Do not expand scope to fix unrelated bugs found in adjacent files; log them in `dev/dead_code.md` or `dev/variable_naming_issues.md` instead.
* Never conclude a mutating task without synchronizing both changelog locations.
