#!/usr/bin/env python3
"""
scripts/coordinate_web_triad.py
Web Domain Coordinator: Orchestrates and audits Phase 1 -> Phase 2 -> Phase 3 handoffs.
"""

import sys
import subprocess
from pathlib import Path

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

def run_step(step_name: str, cmd_list: list) -> bool:
    print(f"\n[RUNNING STEP] {step_name}...")
    res = subprocess.run(cmd_list, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[PASSED] {step_name}")
        if res.stdout:
            print(res.stdout.strip())
        return True
    else:
        print(f"[FAILED] {step_name}", file=sys.stderr)
        if res.stderr:
            print(res.stderr.strip(), file=sys.stderr)
        return False

def verify_all():
    skills_root = get_script_path().parent.parent

    # Phase 1: Validate Taxonomy Planner
    tax_manifest = skills_root / "web-taxonomy-planner" / "assets" / "sample_taxonomy_blueprint.104a.bejson"
    tax_script = skills_root / "web-taxonomy-planner" / "scripts" / "plan_web_taxonomy.py"
    if not run_step("Phase 1: Taxonomy Planner Validation", [sys.executable, str(tax_script), "--validate", str(tax_manifest)]):
        return False

    # Phase 2: Validate Framework Manifest
    fw_manifest = skills_root / "web-framework-architect" / "assets" / "sample_web_framework.104a.bejson"
    fw_script = skills_root / "web-framework-architect" / "scripts" / "fw_compiler.py"
    if not run_step("Phase 3: Web Framework 12 Invariant Laws Audit", [sys.executable, str(fw_script), "--validate", str(fw_manifest)]):
        return False

    print("\n[ALL PHASES PASSED] The Three-Domain Architecture pipeline is healthy and synchronized.")
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--verify-all":
        ok = verify_all()
        sys.exit(0 if ok else 1)
    else:
        print("Usage: python3 coordinate_web_triad.py --verify-all")

if __name__ == "__main__":
    main()
