---
name: agy-plugins
description: >-
  Scaffold, package, configure, and audit Antigravity CLI plugins (plugin.json, mcp_config.json, hooks.json, rules/AGENTS.md, skills/). Enforces standard directory topology, manifest declaration syntax, lifecycle hook registration, tool namespacing, and enable/disable configuration management in config.json. Use when packaging multi-skill ecosystems, building team developer bundles, configuring plugin-scoped MCP servers, or preparing plugins for marketplace distribution.
---

# Skill: `agy-plugins`

- **Purpose**: Authoring, bundling, and managing Antigravity CLI plugins.
- **Target Platform**: Antigravity CLI (`agy`) & Antigravity 2.0 Harness
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Plugin Directory Topology

A valid Antigravity plugin must reside within a subdirectory of `plugins/` (e.g. `.agents/plugins/<name>/` or `~/.gemini/config/plugins/<name>/`):

```text
plugins/<plugin_name>/
├── plugin.json         # REQUIRED: Manifest declaration
├── mcp_config.json     # OPTIONAL: Model Context Protocol servers
├── hooks.json          # OPTIONAL: Lifecycle event hooks
├── rules/              # OPTIONAL: Bundled rule files
│   └── AGENTS.md       # Recommended consolidated rule file
└── skills/             # OPTIONAL: Bundled skills
    └── <skill_name>/
        └── SKILL.md
```

---

## 2. The `plugin.json` Manifest

The `plugin.json` file marks the directory as an Antigravity plugin:

```json
{
  "name": "bejson-developer-toolkit",
  "version": "1.0.0",
  "description": "Standardized skills, rules, and validators for the BEJSON ecosystem.",
  "author": "Elton Boehnen",
  "disabled": false
}
```

* **`name`** (string, optional): Display identifier. Defaults to the directory name if omitted.
* **`disabled`** (bool, optional): If `true`, the plugin ships disabled until toggled on.

---

## 3. Configuration & Lifecycle State

Plugins are enabled by default once discovered. User overrides are recorded in `~/.gemini/config/config.json`:

```json
{
  "plugins": {
    "bejson-developer-toolkit": {
      "enabled": true
    }
  }
}
```

CLI commands to toggle plugins:
```bash
agy plugin list
agy plugin enable bejson-developer-toolkit
agy plugin disable bejson-developer-toolkit
```

---

## 4. Packaging Guidelines

1. **Rule Consolidation**: Always place rules under `rules/AGENTS.md` rather than scattering multiple `.md` files.
2. **Tool Namespacing**: Ensure bundled tool scripts and MCP servers avoid colliding with built-in commands.
3. **Relative Execution**: All commands declared in `hooks.json` or `mcp_config.json` inside a plugin should use paths relative to the plugin root or environment variables.
