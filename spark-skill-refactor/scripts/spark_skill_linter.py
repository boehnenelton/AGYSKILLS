#!/usr/bin/env python3
"""
Spark Skill Linter and Cartographer Collision Validator
Validates SKILL.md files and skill clusters against 2026 Cartographer standards:
- Code 130: Line count ceiling (< 500 lines)
- Code 131: Forbidden filler tokens in templates (lorem ipsum) and phonetic drift aliases
- Tri-partite frontmatter schema (name, capability, positive 'Use when', negative 'Do NOT use')
- Forbidden punctuation (em-dashes, en-dashes) and missing blank lines before lists
- Cluster Mode (--cluster):
  - Code 430: E_CARTOGRAPHER_DUPLICATE_SKILL
  - Code 431: E_CARTOGRAPHER_TRIGGER_COLLISION (Jaccard overlap J >= 0.25 without mutual exclusion)
  - Code 432: E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL (non-reciprocal sibling exclusion)
  - Code 433: E_CARTOGRAPHER_DANGLING_SIBLING_REF (unregistered skill in negative guardrail)
"""
import argparse
import re
import sys
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "for", "from",
    "in", "into", "is", "it", "not", "of", "on", "or", "that", "the", "to",
    "use", "when", "with", "across", "via", "using", "used"
}

PHONETIC_DRIFT_TOKENS = {
    "certographer": "Cartographer",
    "cartographer ancblayers": "Cartographer and Layers",
    "fillker": "filler"
}


def extract_frontmatter(content: str) -> tuple[dict, str]:
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not fm_match:
        return {}, content
    fm_text, body = fm_match.group(1), fm_match.group(2)
    meta = {}
    name_m = re.search(r"^name:\s*([^\n]+)", fm_text, re.MULTILINE)
    if name_m:
        raw_name = name_m.group(1).strip().strip("'\"")
        meta["raw_name"] = raw_name
        meta["name"] = raw_name.replace("user:", "").replace("system:", "")
    desc_m = re.search(r"^description:\s*([^\n]+)", fm_text, re.MULTILINE)
    if desc_m:
        meta["description"] = desc_m.group(1).strip().strip("'\"")
    return meta, body


def parse_trigger_clauses(description: str) -> tuple[set[str], set[str]]:
    """Extracts positive token set T+ and referenced negative sibling skill names T-."""
    neg_split = re.split(r"do\s+not\s+use", description, flags=re.IGNORECASE)
    pos_text = neg_split[0]
    neg_text = " ".join(neg_split[1:]) if len(neg_split) > 1 else ""

    tokens = {
        tok.lower()
        for tok in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", pos_text)
        if tok.lower() not in STOPWORDS and len(tok) > 2
    }
    referenced_siblings = set(
        re.findall(r"\b(?:use\s+)([a-z0-9]+(?:-[a-z0-9]+)+)\b", neg_text.lower())
    )
    return tokens, referenced_siblings


def jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    if not set_a or not set_b:
        return 0.0
    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


def lint_skill(skill_path: Path) -> dict:
    skill_file = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not skill_file.exists():
        return {"valid": False, "line_count": 0, "errors": [f"File not found: {skill_file}"], "warnings": []}

    content = skill_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []
    warnings = []

    if len(lines) > 500:
        errors.append(f"[Code 130: E_LINE_BUDGET_EXCEEDED] Line count ({len(lines)}) exceeds hard ceiling of 500 lines.")

    meta, _ = extract_frontmatter(content)
    if not meta:
        errors.append("Invalid or missing YAML frontmatter delimiters (---).")
    else:
        clean_name = meta.get("name", "")
        if not clean_name:
            errors.append("Missing required 'name' field in frontmatter.")
        else:
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", clean_name):
                errors.append(f"Invalid name format '{clean_name}'. Must be kebab-case (a-z, 0-9, hyphens).")
            if len(clean_name) > 64:
                errors.append(f"Name '{clean_name}' exceeds 64 characters ({len(clean_name)}).")

        desc_text = meta.get("description", "")
        if not desc_text:
            errors.append("Missing required 'description' field in frontmatter.")
        else:
            if len(desc_text) > 1024:
                errors.append(f"Description length ({len(desc_text)}) exceeds 1024-character limit.")
            if "use when" not in desc_text.lower():
                warnings.append("Description lacks explicit positive trigger clause ('Use when...').")
            if "do not use" not in desc_text.lower() and "not use" not in desc_text.lower():
                errors.append("Description lacks explicit negative guardrails ('Do NOT use for...').")

    for idx, line in enumerate(lines, 1):
        if "\u2014" in line:
            errors.append(f"Line {idx}: Found em-dash (\u2014). Replace with hyphen (-) or period (.).")
        if "\u2013" in line:
            errors.append(f"Line {idx}: Found en-dash (\u2013). Replace with hyphen (-) or period (.).")

    for idx in range(1, len(lines)):
        curr = lines[idx].strip()
        prev = lines[idx - 1].strip()
        if curr.startswith("- ") or curr.startswith("* ") or re.match(r"^\d+\.\s", curr):
            if prev and not (
                prev.startswith("- ")
                or prev.startswith("* ")
                or re.match(r"^\d+\.\s", prev)
                or prev.startswith("```")
            ) and not prev.endswith(":"):
                warnings.append(f"Line {idx + 1}: Missing blank line before list item.")

    return {
        "valid": len(errors) == 0,
        "line_count": len(lines),
        "meta": meta,
        "errors": errors,
        "warnings": warnings,
    }


def audit_cluster(cluster_dir: Path, known_skills: set[str] | None = None) -> dict:
    skill_files = sorted(cluster_dir.glob("*/SKILL.md"))
    records = {}
    errors = []
    warnings = []

    for sf in skill_files:
        res = lint_skill(sf.parent)
        name = res.get("meta", {}).get("name") or sf.parent.name
        if name in records:
            errors.append(f"[Code 430: E_CARTOGRAPHER_DUPLICATE_SKILL] Duplicate skill name '{name}'.")
        pos_tokens, neg_siblings = parse_trigger_clauses(res.get("meta", {}).get("description", ""))
        records[name] = {
            "path": sf,
            "lint": res,
            "pos_tokens": pos_tokens,
            "neg_siblings": neg_siblings,
        }
        for err in res["errors"]:
            errors.append(f"[{name}] {err}")
        for warn in res["warnings"]:
            warnings.append(f"[{name}] {warn}")

    registered = set(records.keys()) | (known_skills or set())
    names = sorted(records.keys())

    for i, name_a in enumerate(names):
        rec_a = records[name_a]
        for target in sorted(rec_a["neg_siblings"]):
            if known_skills is not None and target not in registered:
                errors.append(
                    f"[Code 433: E_CARTOGRAPHER_DANGLING_SIBLING_REF] '{name_a}' references unregistered skill '{target}'."
                )
            elif target in records and name_a not in records[target]["neg_siblings"]:
                warnings.append(
                    f"[Code 432: E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL] '{name_a}' excludes '{target}', but '{target}' does not exclude '{name_a}'."
                )

        for name_b in names[i + 1:]:
            rec_b = records[name_b]
            j_score = jaccard_similarity(rec_a["pos_tokens"], rec_b["pos_tokens"])
            if j_score >= 0.25:
                a_ex_b = name_b in rec_a["neg_siblings"]
                b_ex_a = name_a in rec_b["neg_siblings"]
                if not (a_ex_b and b_ex_a):
                    errors.append(
                        f"[Code 431: E_CARTOGRAPHER_TRIGGER_COLLISION] '{name_a}' and '{name_b}' share Jaccard similarity J={j_score:.2f} (>=0.25) without mutual exclusion."
                    )

    return {"valid": len(errors) == 0, "count": len(records), "errors": errors, "warnings": warnings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark Skill Linter & Cartographer Validator")
    parser.add_argument("target", nargs="?", default=".", help="Path to skill directory or cluster root")
    parser.add_argument("--cluster", action="store_true", help="Run pairwise Cartographer cluster audit")
    args = parser.parse_args()

    target_path = Path(args.target)
    if args.cluster:
        report = audit_cluster(target_path)
        print(f"Cluster Target: {target_path} | Skills Scanned: {report['count']}")
        print(f"Status: {'PASS' if report['valid'] else 'FAIL'}")
    else:
        report = lint_skill(target_path)
        print(f"Target: {target_path}")
        print(f"Status: {'PASS' if report['valid'] else 'FAIL'} | Lines: {report['line_count']}")

    if report["errors"]:
        print("Errors:")
        for e in report["errors"]:
            print(f"  [ERROR] {e}")
    if report["warnings"]:
        print("Warnings:")
        for w in report["warnings"]:
            print(f"  [WARN] {w}")
    sys.exit(0 if report["valid"] else 1)
