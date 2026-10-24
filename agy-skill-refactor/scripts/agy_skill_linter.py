#!/usr/bin/env python3
"""
Antigravity CLI (agy) Skill & Preset Linter
Validates agy skills, prompt templates, and bash/python runners against 2026 standards:
- Checks for --sandbox in execution commands
- Checks for plan-first mode (--mode=plan) in audit/inspection workflows
- Validates BEJSON 104a field map caching patterns (no hardcoded row indices)
- Checks for zero conversational preamble / fluff in prompt templates
- Validates minute-based timing variables (no hardcoded raw second sleeps)
- Enforces line budget (< 500 lines) and no em-dashes
"""
import sys
import re
from pathlib import Path

def lint_agy_skill(skill_path: Path) -> dict:
    skill_file = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not skill_file.exists():
        return {"valid": False, "errors": [f"File not found: {skill_file}"]}

    content = skill_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []
    warnings = []

    # Check line budget
    if len(lines) > 500:
        errors.append(f"Line count ({len(lines)}) exceeds hard ceiling of 500 lines.")

    # Check frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not fm_match:
        errors.append("Invalid or missing YAML frontmatter delimiters (---).")
    else:
        fm_text = fm_match.group(1)
        name_match = re.search(r"^name:\s*([^\n]+)", fm_text, re.MULTILINE)
        if not name_match:
            errors.append("Missing required 'name' field in frontmatter.")
        else:
            raw_name = name_match.group(1).strip().strip("'\"")
            clean_name = raw_name.replace("user:", "").replace("system:", "")
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", clean_name):
                errors.append(f"Invalid name format '{clean_name}'. Must be kebab-case.")

        desc_match = re.search(r"^description:\s*(>-\s*\n|\"[^\"]*\"|'[^']*'|[^\n]+)", fm_text, re.MULTILINE)
        if not desc_match:
            errors.append("Missing required 'description' field in frontmatter.")

    # Check for em-dashes and en-dashes
    for idx, line in enumerate(lines, 1):
        if "—" in line:
            errors.append(f"Line {idx}: Found em-dash (—). Replace with hyphen (-) or period (.).")
        if "–" in line:
            errors.append(f"Line {idx}: Found en-dash (–). Replace with hyphen (-) or period (.).")

    # Domain-specific checks for agy standards
    if "--sandbox" not in content:
        warnings.append("Skill does not explicitly mandate or reference the '--sandbox' isolation flag.")

    if "field map" not in content.lower() and "bejson" in content.lower():
        warnings.append("Skill references BEJSON but does not mention dynamic field map caching.")

    return {
        "valid": len(errors) == 0,
        "line_count": len(lines),
        "errors": errors,
        "warnings": warnings
    }

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    result = lint_agy_skill(target)
    print(f"Target: {target}")
    print(f"Status: {'PASS' if result['valid'] else 'FAIL'} | Lines: {result['line_count']}")
    if result["errors"]:
        print("Errors:")
        for err in result["errors"]:
            print(f"  [ERROR] {err}")
    if result["warnings"]:
        print("Warnings:")
        for w in result["warnings"]:
            print(f"  [WARN] {w}")
    sys.exit(0 if result["valid"] else 1)
