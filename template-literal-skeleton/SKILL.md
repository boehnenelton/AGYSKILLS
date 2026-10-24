---
name: template-literal-skeleton
description: >-
  Enforce the global Zero-Filler Skeleton Law across templates of all formats (HTML, CLI menus, UI layouts, scripts, BEJSON): output strict, bare-bones structural skeletons with zero filler, zero 'lorem ipsum', and zero fabricated examples using simple, literal placeholder text labels ('Title', 'Content Body', 'Menu Header', 'Menu Item 1'). Use whenever generating or scaffolding bare-bones templates of any format. Do NOT use for scaffolding Release 300 Foundational Era BEJSON 104 data stores (use template-104-template), Integrity Era Format 105 UUID data stores (use template-105-template), populating real production content, or executing runtime logic.
---

# Skill: `template-literal-skeleton` (Layer 4 - Global Zero-Filler Skeleton Law)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4 (L4_Presentation_Transport)`
- **Era & Library Binding**: `Universal (Foundational & Integrity Eras, Policy §12)`
- **Reference Specification**: `references/literal_placeholder_rule_spec.md`
- **Verification Tool**: `scripts/verify_zero_filler.py`
- **Date Created**: `2026-10-19`
- **RELATIONAL_ID**: `2f7a91b4-4e2c-4f80-9a3d-1e5b8d0c4f62`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Core Directive & Policy Absolutism

> [!IMPORTANT]
> **Core Directive (Policy §12.1)**:
> Whenever generating a template of any format (HTML, CLI menus, UI layouts, scripts, data), you must output a **strict, bare-bones structural skeleton**. Absolutely no filler content, no "lorem ipsum", and no fabricated examples.

This directive is an unwavering global absolute across all templates generated in any language or environment.

---

## 2. The Literal Placeholder Rule

Use simple, literal, and descriptive text labels as placeholders for all structural elements:

1. **HTML & Web Templates**:
   - Title section must contain only the text: `Title`
   - Section headings: `Section Heading 1`, `Section Heading 2`
   - Main body containers: `Content Body`
   - Data tables: `Column 1`, `Column 2`, `Cell 1-1`, `Cell 1-2`
   - Cards & modules: `Card Title 1`, `Card Content Body 1`
   - Buttons: `Action 1`, `Action 2`

2. **Terminal / CLI Templates**:
   - Menu headers: `Menu Header`
   - Menu choices: `1. Menu Item 1`, `2. Menu Item 2`, `3. Menu Item 3`
   - Prompts: `Select an option [1-3]: `

3. **Application & Script Skeletons (Python / Bash / JS / TS)**:
   - Module docstrings: `Module Description`
   - Function bodies: `# Function Logic` or `pass`
   - Main entry point: `# Main Execution`

4. **UI Layouts & Components**:
   - Containers: `Header`, `Sidebar`, `Main Content`, `Footer`

---

## 3. Strict Prohibitions

- ❌ **NO conversational fluff** or explanatory conversational filler within template output.
- ❌ **NO fake articles**, hypothetical scenarios, simulated tutorials, or assumed content.
- ❌ **NO "lorem ipsum"** or pseudo-Latin dummy text under any circumstances.
- ❌ **Render only the exact architecture requested**, populated exclusively with literal placeholder labels.

---

## 4. Deliverable Taxonomy: Template vs. Example vs. Demonstration vs. Reference

To ensure strict architectural clarity across templating systems, engineering workflows, and BEHTML/BEJSON tooling, these four deliverables are formalized with mutually exclusive boundaries:

| Deliverable | Definition & Purpose | Content Policy | Consumption Lifecycle |
| :--- | :--- | :--- | :--- |
| **Template** | Uninstantiated structural skeleton or blueprint defining geometry, DOM/CLI hierarchy, and CSS hooks. | **Zero filler, zero domain copy**. Populated exclusively with literal placeholders (`Title`, `Content Body`, `Menu Item 1`) or `{{VAR:-default}}` slots. | Cloned directly to start new projects; populated with real data without cleanup. |
| **Example** | Focused pedagogical snippet illustrating how a specific pattern, syntax, or component works in isolation. | Minimal contextual sample snippet strictly necessary to teach the pattern. | Read, studied, and adapted; borrowed into application logic. |
| **Demonstration** | Fully operational end-to-end showcase or test harness displaying multiple integrated features under live conditions. | Coherent simulated test fixtures, active telemetry charts, live dev-grid toggles, and dynamic layer sliders. | Executed and viewed in browser/terminal to verify look-and-feel and operational fidelity. |
| **Reference** | Normative technical specification, invariant sheet, API contract, or lookup dictionary documenting constants and rules. | Authoritative and fact-dense; exact formulas ($R_y = 32\text{px}$), token colors (`#DE2626`), schemas, and error codes. Non-executable. | Consulted by developers, agents, and linters to verify compliance and audit system rules. |

Reference Specification: [`references/template_example_demonstration_taxonomy.md`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-literal-skeleton/references/template_example_demonstration_taxonomy.md)

---

## 5. Canonical Skeleton Exemplars

### 4.1 HTML Document Skeleton
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Title</title>
</head>
<body>
    <header>
        <h1>Title</h1>
    </header>
    <main>
        <h2>Section Heading 1</h2>
        <p>Content Body</p>
    </main>
    <footer>
        <div>Footer Text</div>
    </footer>
</body>
</html>
```

### 4.2 Terminal CLI Menu Skeleton (Bash)
```bash
#!/usr/bin/env bash

show_menu() {
    clear
    echo "=================================="
    echo "           Menu Header            "
    echo "=================================="
    echo "1. Menu Item 1"
    echo "2. Menu Item 2"
    echo "3. Exit"
    echo "=================================="
    read -rp "Select an option [1-3]: " choice
    case "$choice" in
        1) # Action 1 Logic
           ;;
        2) # Action 2 Logic
           ;;
        3) exit 0 ;;
        *) echo "Invalid selection." ;;
    esac
}
```

### 4.3 Python Script Skeleton
```python
#!/usr/bin/env python3
"""
Module Name:        script_skeleton
Description:        Module Description
"""

def function_one() -> None:
    # Function Logic
    pass

def main() -> int:
    # Main Execution
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

---

## 5. Automated Verification

Templates are automatically audited using [`scripts/verify_zero_filler.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-literal-skeleton/scripts/verify_zero_filler.py):

```bash
python3 verify_zero_filler.py <template_file>
```
The script asserts zero occurrences of:
- `lorem ipsum`, `dolor sit amet`, `consectetur`
- Fabricated story text, mock personas, or hypothetical blog posts
- Enforces presence of literal labels (`Title`, `Content Body`, `Menu Header`, etc.)

---

## When NOT to Use

- **Populating real production data or finalized content**: When the user requests generating finished application content or articles, populate real copy instead of placeholders.
- **Data binding with live database rows**: Use `bejson-104-core` or `bejson-105-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
